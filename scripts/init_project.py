#!/usr/bin/env python3
"""Create a draft project office at a new, explicitly chosen path."""

import argparse
import json
from pathlib import Path


DOCUMENTS = {
    "charter.md": "CHARTER.md",
    "management-plan.md": "MANAGEMENT-PLAN.md",
    "project-profile.md": "PROJECT-PROFILE.md",
    "rulebook.md": "RULEBOOK.md",
    "team.md": "TEAM.md",
    "model-evaluation.md": "MODEL-EVALUATION.md",
    "milestones.md": "MILESTONES.md",
    "handover.md": "STATUS.md",
}


def initialize(destination, name):
    destination = Path(destination)
    if not name.strip():
        raise ValueError("Project name must be non-empty")
    if destination.exists() or destination.is_symlink():
        raise ValueError("Destination already exists. Choose a new project-office path")
    templates = Path(__file__).resolve().parents[1] / "assets" / "templates"
    documents = {
        output: (templates / source).read_text(encoding="utf-8").replace(
            "{{PROJECT_NAME}}", name
        )
        for source, output in DOCUMENTS.items()
    }
    registry = json.loads((templates / "artifacts.json").read_text(encoding="utf-8"))
    registry["project"] = name
    documents["DECISIONS.md"] = (
        "# Decisions\n\nAppend decisions with actor, authority, reason, impact, and evidence.\n"
    )
    documents["records/artifacts.json"] = (
        json.dumps(registry, ensure_ascii=False, indent=2) + "\n"
    )
    destination.mkdir(parents=True, exist_ok=False)
    created = [destination]
    try:
        for directory in ("roles", "tasks", "artifacts", "reviews", "evidence", "records"):
            path = destination / directory
            path.mkdir()
            created.append(path)
        for output, content in documents.items():
            path = destination / output
            with path.open("x", encoding="utf-8", newline="\n") as stream:
                created.append(path)
                stream.write(content)
    except OSError as error:
        for path in reversed(created):
            try:
                if path.is_dir():
                    path.rmdir()
                else:
                    path.unlink()
            except OSError:
                continue
        if destination.exists():
            raise OSError(f"Initialization interrupted. Inspect partial office at {destination}") from error
        raise
    return destination


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("destination", type=Path)
    parser.add_argument("--name", required=True)
    args = parser.parse_args()
    try:
        destination = initialize(args.destination, args.name)
    except (OSError, ValueError) as exc:
        parser.exit(1, f"Initialization failed: {exc}\n")
    print(f"Draft project office created at {destination.resolve()}")


if __name__ == "__main__":
    main()
