from __future__ import annotations

from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
WORKFLOW_PATH = REPO_ROOT / ".github" / "workflows" / "fork-sync.yml"


def _steps() -> list[dict]:
    workflow = yaml.safe_load(WORKFLOW_PATH.read_text(encoding="utf-8"))
    return workflow["jobs"]["sync"]["steps"]


def test_fork_sync_checks_for_existing_pr_before_sync() -> None:
    steps = _steps()
    check_step = next(step for step in steps if step.get("id") == "existing-pr")
    assert check_step["uses"] == "actions/github-script@v7"


def test_fork_sync_step_skips_when_existing_pr_present() -> None:
    steps = _steps()
    sync_step = next(step for step in steps if step.get("name") == "Sync upstream changes")
    assert sync_step["if"] == "steps.existing-pr.outputs.exists != 'true'"
