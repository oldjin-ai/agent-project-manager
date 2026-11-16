"""Synthetic fixtures exercise the structural gate's failure conditions."""

import copy
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch


SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
spec = importlib.util.spec_from_file_location("artifact_control", SCRIPTS / "artifact_control.py")
control = importlib.util.module_from_spec(spec)
spec.loader.exec_module(control)
init_spec = importlib.util.spec_from_file_location("init_project", SCRIPTS / "init_project.py")
initializer = importlib.util.module_from_spec(init_spec)
init_spec.loader.exec_module(initializer)


class DeliveryTests(unittest.TestCase):
    def setUp(self):
        temporary_root = os.environ.get("APM_TEST_TMPDIR")
        self.temporary = tempfile.TemporaryDirectory(dir=temporary_root)
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name) / "office"
        initializer.initialize(self.root, "Synthetic 测试")
        self.registry_path = self.root / "records" / "artifacts.json"
        self.artifact = self.make_artifact("A01")
        self.registry = {
            "schema_version": 1,
            "project": "Synthetic test",
            "milestones": [{"id": "M1", "required_artifacts": ["A01@v1"]}],
            "artifacts": [self.artifact],
        }
        self.save()

    def record(self, path, content):
        output = self.root / path
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(content, encoding="utf-8")
        return {"record": path, "sha256": control.digest(output)}

    def make_artifact(self, identity):
        payload_relative = f"artifacts/{identity}/v1/payload"
        payload = self.root / payload_relative
        payload.mkdir(parents=True)
        (payload / "成果.md").write_text("Synthetic candidate\n", encoding="utf-8")
        manifest = control.seal(payload)
        manifest_hash = control.digest(manifest)
        return {
            "id": identity, "version": "v1", "state": "accepted",
            "producer": {"actor": "builder", "session": "build-session"},
            "payload": payload_relative,
            "manifest": manifest.relative_to(self.root).as_posix(),
            "manifest_sha256": manifest_hash,
            "dependencies": [],
            "required_reviewers": ["qa"],
            "reviews": [{
                "actor": "qa", "session": "review-session", "verdict": "pass",
                "manifest_sha256": manifest_hash,
                **self.record(f"reviews/{identity}.md", "Synthetic review fixture"),
            }],
            "required_verification": ["behavioral"],
            "verification": [{
                "actor": "qa", "kind": "behavioral", "status": "pass",
                "method": "Synthetic command", "environment": "Isolated test fixture",
                "exit_code": 0, "manifest_sha256": manifest_hash,
                **self.record(f"evidence/{identity}.txt", "Synthetic result fixture"),
            }],
            "allowed_approvers": ["sponsor"],
            "approval": {
                "actor": "sponsor", "authority_ref": "Synthetic charter",
                "manifest_sha256": manifest_hash,
                **self.record(f"records/{identity}-signoff.md", "Synthetic approval fixture"),
            },
            "defects": [],
        }

    def save(self):
        self.registry_path.write_text(json.dumps(self.registry), encoding="utf-8")

    def assert_rejected(self, message):
        self.save()
        with self.assertRaisesRegex(control.InvalidRecord, message):
            control.check_registry(self.registry_path)

    def test_complete_fixture_passes(self):
        result = control.check_registry(self.registry_path)
        self.assertEqual(result["checked_artifacts"], ["A01@v1"])

    def test_empty_milestones_fail(self):
        self.registry["milestones"] = []
        self.assert_rejected("milestones must contain")

    def test_empty_required_set_fails(self):
        self.registry["milestones"][0]["required_artifacts"] = []
        self.assert_rejected("must contain")

    def test_missing_required_artifact_fails(self):
        self.registry["artifacts"] = []
        self.assert_rejected("Missing required artifact")

    def test_future_draft_is_scoped_to_milestone(self):
        draft = {"id": "A02", "version": "v1", "state": "draft"}
        self.registry["artifacts"].append(draft)
        self.registry["milestones"].append({"id": "M2", "required_artifacts": ["A02@v1"]})
        self.save()
        self.assertEqual(control.check_registry(self.registry_path, "M1")["structural_check"], "pass")
        with self.assertRaisesRegex(control.InvalidRecord, "state must be accepted"):
            control.check_registry(self.registry_path)

    def test_unknown_milestone_fails(self):
        with self.assertRaisesRegex(control.InvalidRecord, "Unknown milestone"):
            control.check_registry(self.registry_path, "M9")

    def test_payload_drift_fails(self):
        (self.root / self.artifact["payload"] / "成果.md").write_text("Changed", encoding="utf-8")
        self.assert_rejected("Payload differs")

    def test_unlisted_payload_file_fails(self):
        (self.root / self.artifact["payload"] / "extra.txt").write_text("Extra", encoding="utf-8")
        self.assert_rejected("Payload differs")

    def test_manifest_drift_fails(self):
        with (self.root / self.artifact["manifest"]).open("a", encoding="utf-8") as stream:
            stream.write(" ")
        self.assert_rejected("Manifest digest differs")

    def test_self_review_actor_fails(self):
        self.artifact["reviews"][0]["actor"] = "builder"
        self.assert_rejected("distinct producer/reviewer")

    def test_self_review_session_fails(self):
        self.artifact["reviews"][0]["session"] = "build-session"
        self.assert_rejected("distinct producer/reviewer")

    def test_missing_required_reviewer_fails(self):
        self.artifact["required_reviewers"].append("domain")
        self.assert_rejected("Required reviewer is missing")

    def test_conditional_review_fails(self):
        self.artifact["reviews"][0]["verdict"] = "conditional"
        self.assert_rejected("review must pass")

    def test_review_binding_fails(self):
        self.artifact["reviews"][0]["manifest_sha256"] = "0" * 64
        self.assert_rejected("Review binds another")

    def test_report_tamper_fails(self):
        (self.root / self.artifact["reviews"][0]["record"]).write_text("Changed", encoding="utf-8")
        self.assert_rejected("Review file digest differs")

    def test_verification_binding_fails(self):
        self.artifact["verification"][0]["manifest_sha256"] = "0" * 64
        self.assert_rejected("Verification binds another")

    def test_failed_or_skipped_verification_fails(self):
        self.artifact["verification"][0]["status"] = "skipped"
        self.assert_rejected("Verification must pass")

    def test_boolean_exit_code_fails(self):
        self.artifact["verification"][0]["exit_code"] = False
        self.assert_rejected("exit_code 0")

    def test_missing_verification_kind_fails(self):
        self.artifact["required_verification"].append("inspection")
        self.assert_rejected("Required verification kind")

    def test_unauthorized_approver_fails(self):
        self.artifact["approval"]["actor"] = "builder"
        self.assert_rejected("lacks declared authority")

    def test_open_major_finding_fails(self):
        self.artifact["defects"] = [{"id": "D01", "severity": "major", "status": "open"}]
        self.assert_rejected("Unresolved acceptance finding")

    def test_self_verified_defect_fails(self):
        self.artifact["defects"] = [{
            "id": "D01", "severity": "blocking", "status": "closed",
            "fixer": "builder", "verifier": "builder",
        }]
        self.assert_rejected("independent verification")

    def test_minor_risk_acceptance_passes(self):
        self.artifact["defects"] = [{
            "id": "D01", "severity": "minor", "status": "accepted_risk",
            "actor": "sponsor", "manifest_sha256": self.artifact["manifest_sha256"],
            **self.record("records/risk.md", "Synthetic risk decision"),
        }]
        self.save()
        control.check_registry(self.registry_path)

    def test_dependency_closure_passes(self):
        dependency = self.make_artifact("A00")
        self.registry["artifacts"].append(dependency)
        self.artifact["dependencies"] = [{
            "artifact": "A00@v1", "manifest_sha256": dependency["manifest_sha256"],
        }]
        self.save()
        self.assertEqual(len(control.check_registry(self.registry_path)["checked_artifacts"]), 2)

    def test_dependency_binding_fails(self):
        dependency = self.make_artifact("A00")
        self.registry["artifacts"].append(dependency)
        self.artifact["dependencies"] = [{"artifact": "A00@v1", "manifest_sha256": "0" * 64}]
        self.assert_rejected("Dependency binding differs")

    def test_dependency_cycle_fails(self):
        self.artifact["dependencies"] = [{
            "artifact": "A01@v1", "manifest_sha256": self.artifact["manifest_sha256"],
        }]
        self.assert_rejected("dependency cycle")

    def test_duplicate_artifact_fails(self):
        self.registry["artifacts"].append(copy.deepcopy(self.artifact))
        self.assert_rejected("Duplicate artifact")

    def test_duplicate_json_keys_fail(self):
        self.registry_path.write_text('{"schema_version":1,"schema_version":1}', encoding="utf-8")
        with self.assertRaisesRegex(control.InvalidRecord, "Duplicate JSON key"):
            control.check_registry(self.registry_path)

    def test_path_escape_fails(self):
        self.artifact["reviews"][0]["record"] = "../outside.md"
        self.assert_rejected("Unsafe relative path")

    def test_absolute_path_fails(self):
        self.artifact["reviews"][0]["record"] = "C:/outside.md"
        self.assert_rejected("Unsafe relative path")

    def test_missing_array_fails(self):
        del self.artifact["defects"]
        self.assert_rejected("defects must be an array")

    def test_seal_refuses_overwrite(self):
        payload = self.root / self.artifact["payload"]
        with self.assertRaisesRegex(control.InvalidRecord, "Manifest already exists"):
            control.seal(payload)

    def test_empty_payload_fails(self):
        payload = self.root / "artifacts" / "empty" / "payload"
        payload.mkdir(parents=True)
        with self.assertRaisesRegex(control.InvalidRecord, "must contain a file"):
            control.seal(payload)

    def test_missing_approval_fails(self):
        del self.artifact["approval"]
        self.assert_rejected("approval must be an object")

    def test_missing_reviews_fail(self):
        self.artifact["reviews"] = []
        self.assert_rejected("reviews must contain")

    def test_cli_initialize_and_seal(self):
        destination = self.root.parent / "cli-office"
        result = subprocess.run(
            [sys.executable, str(SCRIPTS / "init_project.py"), str(destination), "--name", "CLI test"],
            capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertTrue((destination / "CHARTER.md").is_file())
        payload = destination / "artifacts" / "A01" / "v1" / "payload"
        payload.mkdir(parents=True)
        (payload / "document.md").write_text("CLI candidate", encoding="utf-8")
        result = subprocess.run(
            [sys.executable, str(SCRIPTS / "artifact_control.py"), "seal", str(payload)],
            capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(json.loads(result.stdout)["sha256"], control.digest(payload.parent / "manifest.json"))

    def test_initializer_preserves_existing_directory(self):
        before = self.registry_path.read_bytes()
        with self.assertRaisesRegex(ValueError, "already exists"):
            initializer.initialize(self.root, "Other")
        self.assertEqual(self.registry_path.read_bytes(), before)

    def test_initializer_recovers_from_partial_write_failure(self):
        destination = self.root.parent / "retry-office"
        original_open = Path.open

        def fail_one_write(path, *args, **kwargs):
            if path == destination / "TEAM.md":
                raise OSError("Simulated disk error")
            return original_open(path, *args, **kwargs)

        with patch.object(Path, "open", fail_one_write):
            with self.assertRaisesRegex(OSError, "Simulated disk error"):
                initializer.initialize(destination, "Retry test")
        self.assertFalse(destination.exists())
        initializer.initialize(destination, "Retry test")
        self.assertTrue((destination / "records" / "artifacts.json").is_file())

    def test_cli_pass_and_fail(self):
        command = [sys.executable, str(SCRIPTS / "artifact_control.py"), "check", str(self.registry_path)]
        result = subprocess.run(command, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(json.loads(result.stdout)["structural_check"], "pass")
        self.artifact["state"] = "draft"
        self.save()
        result = subprocess.run(command, capture_output=True, text=True)
        self.assertEqual(result.returncode, 1)
        self.assertEqual(json.loads(result.stdout)["structural_check"], "fail")


if __name__ == "__main__":
    unittest.main()
