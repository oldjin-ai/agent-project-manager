#!/usr/bin/env python3
"""Seal candidate payloads and check version-bound delivery records."""

import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import stat
import sys


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
    attributes = getattr(path.lstat(), "st_file_attributes", 0)
    require(
        not path.is_symlink()
        and not attributes & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0),
        f"Linked/reparse path requires a separate immutable copy: {path}",
    )


def local_path(root, relative):
    nonempty(relative, "Relative path")
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
    path = root
    for part in parts.parts:
        path = path / part
        reject_link(path)
    require(path.resolve().is_relative_to(root.resolve()), f"Path escapes root: {relative}")
    return path


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


def seal(payload):
    payload = Path(payload).absolute()
    manifest = payload.parent / "manifest.json"
    require(not manifest.exists() and not manifest.is_symlink(), "Manifest already exists")
    content = {"schema_version": 1, "files": payload_entries(payload)}
    with manifest.open("x", encoding="utf-8", newline="\n") as stream:
        stream.write(json.dumps(content, ensure_ascii=False, indent=2) + "\n")
    return manifest


def bound_file(root, record, label):
    object_value(record, label)
    path = local_path(root, record.get("record"))
    require(path.is_file(), f"{label} file is missing")
    require(digest(path) == record.get("sha256"), f"{label} file digest differs")


def check_artifact(root, artifact):
    require(artifact.get("state") == "accepted", "Artifact state must be accepted")
    producer = object_value(artifact.get("producer"), "producer")
    nonempty(producer.get("actor"), "producer.actor")
    nonempty(producer.get("session"), "producer.session")
    payload = local_path(root, artifact.get("payload"))
    manifest_path = local_path(root, artifact.get("manifest"))
    require(manifest_path.is_file(), "Manifest is missing")
    manifest_hash = digest(manifest_path)
    require(manifest_hash == artifact.get("manifest_sha256"), "Manifest digest differs")
    manifest = object_value(load_json(manifest_path), "manifest")
    require(type(manifest.get("schema_version")) is int and manifest["schema_version"] == 1,
            "Unsupported manifest schema")
    require(manifest.get("files") == payload_entries(payload), "Payload differs from manifest")

    expected_reviewers = unique_texts(artifact.get("required_reviewers"), "required_reviewers")
    seen_reviewers = set()
    for review in list_value(artifact.get("reviews"), "reviews", required=True):
        object_value(review, "review")
        reviewer = nonempty(review.get("actor"), "review.actor")
        session = nonempty(review.get("session"), "review.session")
        require(reviewer != producer["actor"] and session != producer["session"],
                "Review must have a distinct producer/reviewer actor and session")
        require(reviewer not in seen_reviewers, "Duplicate reviewer in current acceptance")
        require(review.get("verdict") == "pass", "Current review must pass")
        require(review.get("manifest_sha256") == manifest_hash, "Review binds another candidate")
        bound_file(root, review, "Review")
        seen_reviewers.add(reviewer)
    require(set(expected_reviewers).issubset(seen_reviewers), "Required reviewer is missing")

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


def check_registry(registry_path, milestone=None):
    registry_path = Path(registry_path).absolute()
    root = registry_path.parent.parent
    local_path(root, registry_path.relative_to(root).as_posix())
    registry = object_value(load_json(registry_path), "registry")
    require(type(registry.get("schema_version")) is int and registry["schema_version"] == 1,
            "Unsupported register schema")
    nonempty(registry.get("project"), "project")
    artifacts = {}
    for artifact in list_value(registry.get("artifacts"), "artifacts"):
        key = artifact_key(artifact)
        require(key not in artifacts, f"Duplicate artifact {key}")
        artifacts[key] = artifact
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
            check_artifact(root, artifact)
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

    for key in required:
        visit(key)
    return {"structural_check": "pass", "project": registry["project"],
            "milestone": milestone, "checked_artifacts": sorted(checked)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="action", required=True)
    seal_parser = subparsers.add_parser("seal", help="Create a new sibling manifest.json")
    seal_parser.add_argument("payload", type=Path)
    check_parser = subparsers.add_parser("check", help="Read-only structural delivery check")
    check_parser.add_argument("registry", type=Path)
    check_parser.add_argument("--milestone")
    args = parser.parse_args()
    try:
        if args.action == "seal":
            manifest = seal(args.payload)
            result = {"manifest": str(manifest), "sha256": digest(manifest)}
        else:
            result = check_registry(args.registry, args.milestone)
    except (OSError, ValueError, RecursionError) as exc:
        print(json.dumps({"structural_check": "fail", "error": str(exc)}, ensure_ascii=False))
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
