#!/usr/bin/env python3
"""Seal candidate payloads or live scopes and check version-bound delivery records."""

import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import stat
import sys


DEFAULT_EXCLUDED_DIR_NAMES = frozenset({
    ".git",
    "__pycache__",
    "node_modules",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
})
DEFAULT_EXCLUDED_SUFFIXES = frozenset({".pyc", ".pyo", ".tmp"})


class InvalidRecord(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise InvalidRecord(message)


def nonempty(value, label):
    require(isinstance(value, str) and bool(value.strip()), f"{label} must be text")
    return value


def object_value(value, label):
    require(isinstance(value, dict), f"{label} must be an object")
    return value


def list_value(value, label, required=False):
    require(isinstance(value, list), f"{label} must be an array")
    require(not required or bool(value), f"{label} must contain an entry")
    return value


def unique_texts(value, label):
    values = list_value(value, label, required=True)
    for item in values:
        nonempty(item, label)
    require(len(values) == len(set(values)), f"{label} contains duplicates")
    return values


def digest(path):
    hasher = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            hasher.update(block)
    return hasher.hexdigest()


def reject_duplicate_keys(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, f"Duplicate JSON key {key}")
        result[key] = value
    return result


def load_json(path):
    return json.loads(
        Path(path).read_text(encoding="utf-8-sig"), object_pairs_hook=reject_duplicate_keys
    )


def reject_link(path):
    try:
        st = path.lstat()
    except FileNotFoundError:
        require(not path.is_symlink(), f"Linked/reparse path requires a separate immutable copy: {path}")
        return
    attributes = getattr(st, "st_file_attributes", 0)
    require(
        not path.is_symlink()
        and not stat.S_ISLNK(st.st_mode)
        and not attributes & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0),
        f"Linked/reparse path requires a separate immutable copy: {path}",
    )


def _validate_relative_posix(relative, label="Relative path"):
    nonempty(relative, label)
    parts = PurePosixPath(relative)
    require(
        not parts.is_absolute()
        and ".." not in parts.parts
        and "\\" not in relative
        and ":" not in relative
        and str(parts) == relative
        and relative != ".",
        f"Unsafe relative path {relative}",
    )
    return parts.parts


def local_path(root, relative):
    parts = _validate_relative_posix(relative)
    path = root
    for part in parts:
        path = path / part
        reject_link(path)
    require(path.resolve().is_relative_to(root.resolve()), f"Path escapes root: {relative}")
    return path


def _parts_under_any(parts, prefix_tuples):
    return any(
        len(parts) >= len(prefix) and parts[: len(prefix)] == prefix
        for prefix in prefix_tuples
    )


def _normalize_prefixes(prefixes, label="exclude_prefixes"):
    items = list_value(list(prefixes or ()), label)
    normalized = []
    for raw in items:
        text = nonempty(raw, label)
        if len(text) > 1 and text.endswith("/"):
            text = text.rstrip("/")
        _validate_relative_posix(text, label)
        if text not in normalized:
            normalized.append(text)
    normalized.sort()
    tuples = tuple(PurePosixPath(item).parts for item in normalized)
    return normalized, tuples


def payload_entries(payload):
    reject_link(payload)
    require(payload.is_dir(), "Payload must be a directory")
    entries = {}
    for path in sorted(payload.rglob("*")):
        reject_link(path)
        if path.is_dir():
            continue
        require(path.is_file(), f"Unsupported payload entry {path}")
        relative = path.relative_to(payload).as_posix()
        local_path(payload, relative)
        entries[relative] = {"sha256": digest(path), "bytes": path.stat().st_size}
    require(bool(entries), "Payload must contain a file")
    return entries


def _walk_scope_dir(project_root, directory, exc_tuples, entries):
    reject_link(directory)
    rel_dir = directory.relative_to(project_root).as_posix()
    dir_parts = PurePosixPath(rel_dir).parts
    if directory.name in DEFAULT_EXCLUDED_DIR_NAMES or _parts_under_any(dir_parts, exc_tuples):
        return
    for child in sorted(directory.iterdir(), key=lambda p: p.name):
        reject_link(child)
        rel = child.relative_to(project_root).as_posix()
        parts = _validate_relative_posix(rel)
        if _parts_under_any(parts, exc_tuples):
            continue
        if child.is_dir():
            if child.name in DEFAULT_EXCLUDED_DIR_NAMES:
                continue
            _walk_scope_dir(project_root, child, exc_tuples, entries)
        else:
            require(child.is_file(), f"Unsupported scope entry {child}")
            if child.name == ".git" or child.suffix.lower() in DEFAULT_EXCLUDED_SUFFIXES:
                continue
            entries[rel] = {"sha256": digest(child), "bytes": child.stat().st_size}


def scope_entries(project_root, scope_paths, exclude_prefixes=()):
    project_root = Path(project_root)
    reject_link(project_root)
    require(project_root.is_dir(), "Project root must be a directory")
    scopes = unique_texts(scope_paths, "scope_paths")
    _, exc_tuples = _normalize_prefixes(exclude_prefixes)
    entries = {}
    for scope in scopes:
        scope_parts = _validate_relative_posix(scope, "scope_paths")
        require(
            not _parts_under_any(scope_parts, exc_tuples),
            f"Scope path {scope} overlaps excluded prefix",
        )
        target = local_path(project_root, scope)
        require(target.exists(), f"Scope path is missing: {scope}")
        if target.is_file():
            if (
                target.name != ".git"
                and not any(part in DEFAULT_EXCLUDED_DIR_NAMES for part in scope_parts)
                and target.suffix.lower() not in DEFAULT_EXCLUDED_SUFFIXES
            ):
                entries[scope] = {"sha256": digest(target), "bytes": target.stat().st_size}
        else:
            require(target.is_dir(), f"Unsupported scope entry {target}")
            _walk_scope_dir(project_root, target, exc_tuples, entries)
    require(bool(entries), "Scoped deliverables must contain a file")
    return {key: entries[key] for key in sorted(entries)}


def seal(payload):
    payload = Path(payload).absolute()
    manifest = payload.parent / "manifest.json"
    require(not manifest.exists() and not manifest.is_symlink(), "Manifest already exists")
    content = {"schema_version": 1, "files": payload_entries(payload)}
    with manifest.open("x", encoding="utf-8", newline="\n") as stream:
        stream.write(json.dumps(content, ensure_ascii=False, indent=2) + "\n")
    return manifest


def seal_scope(manifest_out, project_root, scope_paths, exclude_prefixes=()):
    manifest_out = Path(manifest_out).absolute()
    project_root_abs = Path(project_root).absolute()
    reject_link(project_root_abs)
    project_root_res = project_root_abs.resolve()
    require(not manifest_out.exists() and not manifest_out.is_symlink(), "Manifest already exists")
    scopes = sorted(unique_texts(scope_paths, "scope_paths"))
    exc_list, exc_tuples = _normalize_prefixes(exclude_prefixes)

    if manifest_out.is_relative_to(project_root_res):
        m_rel = manifest_out.relative_to(project_root_res).as_posix()
        m_parts = PurePosixPath(m_rel).parts
        if not _parts_under_any(m_parts, exc_tuples):
            for scope in scopes:
                sc_parts = PurePosixPath(scope).parts
                require(
                    not (len(m_parts) >= len(sc_parts) and m_parts[: len(sc_parts)] == sc_parts),
                    f"Self-referential scope: manifest {m_rel} lies inside scope {scope}",
                )

    entries = scope_entries(project_root_abs, scopes, exc_list)
    if manifest_out.parent.exists():
        reject_link(manifest_out.parent)
    manifest_out.parent.mkdir(parents=True, exist_ok=True)
    reject_link(manifest_out.parent)
    resolved_manifest = manifest_out.parent.resolve() / manifest_out.name
    if resolved_manifest.is_relative_to(project_root_res):
        m_rel = resolved_manifest.relative_to(project_root_res).as_posix()
        require(m_rel not in entries, f"Self-referential scope: manifest {m_rel} was hashed")

    content = {
        "schema_version": 1,
        "mode": "scope",
        "scope_paths": scopes,
        "exclude_prefixes": exc_list,
        "files": entries,
    }
    with manifest_out.open("x", encoding="utf-8", newline="\n") as stream:
        stream.write(json.dumps(content, ensure_ascii=False, indent=2) + "\n")
    return manifest_out


def bound_file(root, record, label):
    object_value(record, label)
    path = local_path(root, record.get("record"))
    require(path.is_file(), f"{label} file is missing")
    require(digest(path) == record.get("sha256"), f"{label} file digest differs")


def _check_manifest_content(root, artifact, manifest_path, manifest, project_root):
    mode = manifest.get("mode", "payload")
    if mode == "payload":
        payload = local_path(root, artifact.get("payload"))
        require(manifest.get("files") == payload_entries(payload), "Payload differs from manifest")
        return
    if mode == "scope":
        effective_root_abs = Path(project_root).absolute() if project_root is not None else root.parent.absolute()
        reject_link(effective_root_abs)
        effective_root = effective_root_abs.resolve()
        scope_paths = sorted(unique_texts(artifact.get("scope_paths"), "scope_paths"))
        manifest_scopes = sorted(unique_texts(manifest.get("scope_paths"), "manifest.scope_paths"))
        require(scope_paths == manifest_scopes, "Artifact scope_paths differs from manifest")
        exc_list, _ = _normalize_prefixes(manifest.get("exclude_prefixes", []), "manifest.exclude_prefixes")
        manifest_files = object_value(manifest.get("files"), "manifest.files")
        if root.resolve().is_relative_to(effective_root):
            office_rel = root.resolve().relative_to(effective_root).as_posix()
            for rel_key in manifest_files:
                require(
                    rel_key != office_rel and not rel_key.startswith(f"{office_rel}/"),
                    f"Self-referential scope entry inside project office: {rel_key}",
                )
        if manifest_path.resolve().is_relative_to(effective_root):
            m_rel = manifest_path.resolve().relative_to(effective_root).as_posix()
            require(m_rel not in manifest_files, f"Self-referential manifest entry: {m_rel}")
        require(
            manifest_files == scope_entries(effective_root_abs, scope_paths, exc_list),
            "Scoped deliverables differ from manifest",
        )
        return
    raise InvalidRecord(f"Unsupported manifest mode {mode}")


def check_artifact(root, artifact, project_root=None, coordinator_actor=None):
    require(artifact.get("state") == "accepted", "Artifact state must be accepted")
    producer = object_value(artifact.get("producer"), "producer")
    nonempty(producer.get("actor"), "producer.actor")
    nonempty(producer.get("session"), "producer.session")

    effective_coordinator = artifact.get("coordinator_actor")
    if effective_coordinator is None:
        effective_coordinator = coordinator_actor
    if effective_coordinator is not None:
        nonempty(effective_coordinator, "coordinator_actor")

    manifest_path = local_path(root, artifact.get("manifest"))
    require(manifest_path.is_file(), "Manifest is missing")
    manifest_hash = digest(manifest_path)
    require(manifest_hash == artifact.get("manifest_sha256"), "Manifest digest differs")
    manifest = object_value(load_json(manifest_path), "manifest")
    require(type(manifest.get("schema_version")) is int and manifest["schema_version"] == 1,
            "Unsupported manifest schema")
    _check_manifest_content(root, artifact, manifest_path, manifest, project_root)

    expected_reviewers = unique_texts(artifact.get("required_reviewers"), "required_reviewers")
    seen_reviewers = set()
    for review in list_value(artifact.get("reviews"), "reviews", required=True):
        object_value(review, "review")
        reviewer = nonempty(review.get("actor"), "review.actor")
        session = nonempty(review.get("session"), "review.session")
        require(reviewer != producer["actor"] and session != producer["session"],
                "Review must have a distinct producer/reviewer actor and session")
        if effective_coordinator is not None:
            require(reviewer != effective_coordinator,
                    "Coordinator cannot act as independent reviewer")
        require(reviewer not in seen_reviewers, "Duplicate reviewer in current acceptance")
        require(review.get("verdict") == "pass", "Current review must pass")
        require(review.get("manifest_sha256") == manifest_hash, "Review binds another candidate")
        bound_file(root, review, "Review")
        seen_reviewers.add(reviewer)
    require(set(expected_reviewers).issubset(seen_reviewers), "Required reviewer is missing")

    if "review_history" in artifact:
        seen_history_ids = set()
        for entry in list_value(artifact.get("review_history"), "review_history"):
            object_value(entry, "review_history entry")
            hid = nonempty(entry.get("id"), "review_history.id")
            require(hid not in seen_history_ids, f"Duplicate review_history id {hid}")
            seen_history_ids.add(hid)
            nonempty(entry.get("actor"), "review_history.actor")
            verdict = nonempty(entry.get("verdict"), "review_history.verdict")
            require(
                verdict in ("pass", "conditional", "reject", "superseded"),
                f"Unsupported review_history verdict {verdict}",
            )
            if "manifest_sha256" in entry and entry["manifest_sha256"] is not None:
                nonempty(entry["manifest_sha256"], "review_history.manifest_sha256")
            bound_file(root, entry, "Review history")

    expected_kinds = unique_texts(artifact.get("required_verification"), "required_verification")
    seen_kinds = set()
    for evidence in list_value(artifact.get("verification"), "verification", required=True):
        object_value(evidence, "verification entry")
        kind = evidence.get("kind")
        require(kind in ("static", "behavioral", "inspection"), "Unknown verification kind")
        require(evidence.get("status") == "pass", "Verification must pass")
        require(evidence.get("manifest_sha256") == manifest_hash, "Verification binds another candidate")
        nonempty(evidence.get("method"), "verification.method")
        nonempty(evidence.get("environment"), "verification.environment")
        nonempty(evidence.get("actor"), "verification.actor")
        exit_code = evidence.get("exit_code")
        if kind != "inspection":
            require(type(exit_code) is int and exit_code == 0, "Command verification requires exit_code 0")
        else:
            require(exit_code is None or type(exit_code) is int and exit_code == 0,
                    "Inspection exit_code must be null or 0")
        bound_file(root, evidence, "Verification")
        seen_kinds.add(kind)
    require(set(expected_kinds).issubset(seen_kinds), "Required verification kind is missing")

    approvers = unique_texts(artifact.get("allowed_approvers"), "allowed_approvers")
    approval = object_value(artifact.get("approval"), "approval")
    require(approval.get("actor") in approvers, "Approval actor lacks declared authority")
    nonempty(approval.get("authority_ref"), "approval.authority_ref")
    require(approval.get("manifest_sha256") == manifest_hash, "Approval binds another candidate")
    bound_file(root, approval, "Approval")

    defect_ids = set()
    for defect in list_value(artifact.get("defects"), "defects"):
        object_value(defect, "defect")
        defect_id = nonempty(defect.get("id"), "defect.id")
        require(defect_id not in defect_ids, "Duplicate defect ID")
        defect_ids.add(defect_id)
        require(defect.get("severity") in ("blocking", "major", "minor"), "Unknown defect severity")
        if defect.get("status") == "closed":
            fixer = nonempty(defect.get("fixer"), "defect.fixer")
            verifier = nonempty(defect.get("verifier"), "defect.verifier")
            require(fixer != verifier, "Defect closure needs independent verification")
            if effective_coordinator is not None:
                require(verifier != effective_coordinator,
                        "Coordinator cannot verify defect closure")
            require(defect.get("manifest_sha256") == manifest_hash, "Defect retest binds another candidate")
            bound_file(root, defect, "Defect retest")
        else:
            require(defect.get("status") == "accepted_risk" and defect["severity"] == "minor",
                    f"Unresolved acceptance finding {defect_id}")
            require(defect.get("actor") in approvers, "Risk acceptance lacks declared authority")
            require(defect.get("manifest_sha256") == manifest_hash, "Risk acceptance binds another candidate")
            bound_file(root, defect, "Risk acceptance")


def artifact_key(artifact):
    object_value(artifact, "artifact")
    name = nonempty(artifact.get("id"), "artifact.id")
    version = nonempty(artifact.get("version"), "artifact.version")
    require("@" not in name and "@" not in version, "IDs and versions must exclude @")
    return f"{name}@{version}"


def check_registry(registry_path, milestone=None, project_root=None):
    registry_path = Path(registry_path).absolute()
    root = registry_path.parent.parent
    local_path(root, registry_path.relative_to(root).as_posix())
    registry = object_value(load_json(registry_path), "registry")
    require(type(registry.get("schema_version")) is int and registry["schema_version"] == 1,
            "Unsupported register schema")
    nonempty(registry.get("project"), "project")

    coordinator_actor = registry.get("coordinator_actor")
    if coordinator_actor is not None:
        nonempty(coordinator_actor, "coordinator_actor")

    artifacts = {}
    for artifact in list_value(registry.get("artifacts"), "artifacts"):
        key = artifact_key(artifact)
        require(key not in artifacts, f"Duplicate artifact {key}")
        artifacts[key] = artifact

    artifact_to_batch = {}
    if "batches" in registry:
        batch_ids = set()
        for batch in list_value(registry.get("batches"), "batches"):
            object_value(batch, "batch")
            bid = nonempty(batch.get("id"), "batch.id")
            require(bid not in batch_ids, f"Duplicate batch ID {bid}")
            batch_ids.add(bid)
            members = unique_texts(batch.get("artifacts"), f"batch[{bid}].artifacts")
            for member in members:
                require(member not in artifact_to_batch, f"Artifact {member} belongs to multiple batches")
                artifact_to_batch[member] = members

    milestones = list_value(registry.get("milestones"), "milestones", required=True)
    milestone_ids = set()
    required = []
    for entry in milestones:
        object_value(entry, "milestone")
        identity = nonempty(entry.get("id"), "milestone.id")
        require(identity not in milestone_ids, "Duplicate milestone ID")
        milestone_ids.add(identity)
        keys = unique_texts(entry.get("required_artifacts"), "milestone.required_artifacts")
        if milestone is None or identity == milestone:
            required.extend(keys)
    require(milestone is None or milestone in milestone_ids, "Unknown milestone")
    checked = set()
    active = set()

    def visit(key):
        nonempty(key, "dependency.artifact")
        require(key not in active, f"Acceptance dependency cycle at {key}")
        if key in checked:
            return
        require(key in artifacts, f"Missing required artifact {key}")
        active.add(key)
        artifact = artifacts[key]
        try:
            check_artifact(
                root,
                artifact,
                project_root=project_root,
                coordinator_actor=coordinator_actor,
            )
            dependency_keys = set()
            for dependency in list_value(artifact.get("dependencies"), "dependencies"):
                object_value(dependency, "dependency")
                dep_key = nonempty(dependency.get("artifact"), "dependency.artifact")
                require(dep_key not in dependency_keys, "Duplicate dependency")
                dependency_keys.add(dep_key)
                visit(dep_key)
                require(dependency.get("manifest_sha256") == artifacts[dep_key]["manifest_sha256"],
                        f"Dependency binding differs for {dep_key}")
        except InvalidRecord as exc:
            raise InvalidRecord(f"{key}: {exc}") from exc
        active.remove(key)
        checked.add(key)

    pending = list(required)
    while pending:
        key = pending.pop(0)
        if key in checked:
            continue
        visit(key)
        for checked_key in list(checked):
            for peer in artifact_to_batch.get(checked_key, ()):
                if peer not in checked and peer not in pending:
                    pending.append(peer)

    return {"structural_check": "pass", "project": registry["project"],
            "milestone": milestone, "checked_artifacts": sorted(checked)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="action", required=True)

    seal_parser = subparsers.add_parser("seal", help="Create a new sibling manifest.json for a payload directory")
    seal_parser.add_argument("payload", type=Path)

    scope_parser = subparsers.add_parser("seal-scope", help="Seal declared live deliverable paths into a manifest")
    scope_parser.add_argument("manifest", type=Path)
    scope_parser.add_argument("--root", type=Path, required=True, help="Project root directory")
    scope_parser.add_argument("--scope", nargs="+", required=True, help="Relative POSIX deliverable paths")
    scope_parser.add_argument("--exclude-prefix", nargs="*", default=[], help="Relative prefixes to exclude")

    check_parser = subparsers.add_parser("check", help="Read-only structural delivery check")
    check_parser.add_argument("registry", type=Path)
    check_parser.add_argument("--milestone")
    check_parser.add_argument("--project-root", type=Path, default=None,
                              help="Project root for scope-mode manifests (defaults to parent of office root)")

    args = parser.parse_args()
    try:
        if args.action == "seal":
            manifest = seal(args.payload)
            result = {"manifest": str(manifest), "sha256": digest(manifest)}
        elif args.action == "seal-scope":
            manifest = seal_scope(args.manifest, args.root, args.scope, args.exclude_prefix)
            result = {"manifest": str(manifest), "sha256": digest(manifest)}
        else:
            result = check_registry(args.registry, args.milestone, project_root=args.project_root)
    except (OSError, ValueError, RecursionError) as exc:
        print(json.dumps({"structural_check": "fail", "error": str(exc)}, ensure_ascii=False))
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
