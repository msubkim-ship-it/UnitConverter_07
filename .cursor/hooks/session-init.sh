#!/usr/bin/env bash
# session-init.sh — sessionStart: inject UnitConverter_07 session context.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export UC07_HOOK_INPUT="$(cat)"

"${SCRIPT_DIR}/_python.sh" <<'PY'
import json
import os
import sys


def build_additional_context() -> str:
    return "\n".join(
        [
            "## UnitConverter_07 — Session Context",
            "",
            "**Project:** UnitConverter_07 (Length Unit Conversion)",
            "**Method:** Dual-Track TDD + ECB",
            "**SSOT (헌법):** `.cursorrules` — Rule·계약·Phase 제약은 `.cursorrules`가 정본",
            "",
            "### ECB",
            "- 의존 방향: boundary → control → entity (단방향)",
            "- entity: stdlib만 | control: entity | boundary: control + entity",
            "- MagicConstant·ErrorCode: entity SSOT (`constants.py`, `exceptions.py` Enum)",
            "- `config/units.json`: boundary 로드·주입용 (수치 리터럴 복사 금지)",
            "",
            "### Dual-Track TDD",
            "- Logic Track (entity/control): Domain Mock 금지 — D-* / `test_d_*`",
            "- UI Track (boundary): stdin·stdout·파일 I/O Mock 허용 — U-* / `test_u_*`",
            "- 브랜치: spec → red → green → refactoring → staging → main",
            "",
            "### Test/Review Loop",
            "- RED: `tests/`만 수정, `pytest` exit ≠ 0",
            "- GREEN/REFACTOR: `pytest -v` exit = 0",
            "- Golden Master: 사용자 승인 없이 갱신 금지",
            "",
            "### Slash Commands",
            "- `/red-test-plan` → `/red-skeleton` → `/green-minimal` (TDD 워크플로)",
            "- `/review-ecb` — ECB 계약 리뷰 (ErrorCode Enum·SSOT, 수정 없음)",
            "",
            "### 참고",
            "- Skill: `.cursor/skills/unit-converter-tdd/SKILL.md`",
            "- D-* TC ID: `.cursor/skills/unit-converter-tdd/reference.md`",
        ]
    )


def main() -> None:
    raw = os.environ.get("UC07_HOOK_INPUT", "")
    try:
        hook_input = json.loads(raw) if raw.strip() else {}
    except json.JSONDecodeError:
        hook_input = {}

    session_id = hook_input.get("session_id", "")
    composer_mode = hook_input.get("composer_mode", "")

    output = {
        "env": {
            "UC07_PROJECT": "UnitConverter_07",
            "UC07_SSOT_RULES": ".cursorrules",
            "UC07_SESSION_ID": session_id,
            "UC07_COMPOSER_MODE": composer_mode,
        },
        "additional_context": build_additional_context(),
    }
    json.dump(output, sys.stdout, ensure_ascii=False)


if __name__ == "__main__":
    main()
PY
