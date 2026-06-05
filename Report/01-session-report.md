# 01 — UnitConverter_07 Cursor 설계·문서화 세션 보고서

| 항목 | 내용 |
|------|------|
| 프로젝트 | UnitConverter_07 |
| 저장소 | https://github.com/msubkim-ship-it/UnitConverter_07 |
| 세션 일자 | 2026-06-05 |
| 대응 Transcript | [Prompting/01-session-transcript.md](../Prompting/01-session-transcript.md) |
| 작성 | AI Agent 세션 산출물 정리 |

---

## 1. 세션 목적

레거시 `UnitConverter.py`를 **ECB + Dual-Track TDD** 방식으로 재구축하기 위한 **설계·Agent 인프라·문서**를 마련한다. (앱 구현·TC 본문은 본 세션 범위 외)

---

## 2. 수행 작업 요약

| # | 주제 | 산출·결과 |
|---|------|-----------|
| 1 | Git 연동 | `origin` → GitHub, `main` ↔ `origin/main` 추적 |
| 2 | 브랜치 전략 | spec→red→green→refactoring→staging→main + spec 단계 가이드 |
| 3 | 레거시 분석 | 코드 스멜 18건, PRD 갭 18건 목록 |
| 4 | 아키텍처 | ECB 패키지 제안, FR/NFR 매핑 |
| 5 | 8계층+Hook | Model~Hook 역할 정의 (ECB·Dual-Track 맥락) |
| 6 | Harness | `pyproject.toml`, `src/{entity,control,boundary}`, `tests/*` 골격 |
| 7 | Rule | `.cursorrules` (55줄) |
| 8 | Rule 리뷰 | P0~P3 보강 제안 (E001~E007, Hook 분리 등) |
| 9 | Skill | `unit-converter-tdd` + D-* `reference.md` |
| 10 | Command | `/tdd-red`, `/review-ecb` |
| 11 | Loop 기준 | Test/Review Loop 성공 기준 5개 |
| 12 | Hook | `hooks.json` + `session-init.sh` (sessionStart) |
| 13 | 마무리 점검 | 8계층 ✅/⚠️/❌ 표 |
| 14 | PRD | `PRD.md` (FR-01~15, NFR, E001~E007) |
| 15 | README | ECB·TDD·Cursor 도구 반영 업데이트 |

---

## 3. 최종 산출물 목록

### 3.1 문서

| 파일 | 역할 |
|------|------|
| `PRD.md` | FR/NFR·에러 계약·마일스톤 SSOT |
| `README.md` | 실행·구조·TDD·Cursor 도구 안내 |
| `.cursorrules` | Agent 헌법 |

### 3.2 Cursor Agent

| 파일 | 역할 |
|------|------|
| `.cursor/skills/unit-converter-tdd/SKILL.md` | RED/GREEN/REFACTOR 절차 |
| `.cursor/skills/unit-converter-tdd/reference.md` | D-* TC ID 14건 |
| `.cursor/commands/tdd-red.md` | RED Phase slash command |
| `.cursor/commands/review-ecb.md` | ECB 계약 리뷰 (수정 금지) |
| `.cursor/hooks.json` | sessionStart Hook |
| `.cursor/hooks/session-init.sh` | 세션 컨텍스트 주입 |

### 3.3 Harness

| 파일 | 역할 |
|------|------|
| `pyproject.toml` | pytest ≥8.0, `testpaths`/`pythonpath` |

> **참고:** `src/`, `tests/` ECB 골격은 세션 중 생성되었으나 현재 워크트리에 없을 수 있음 — red 브랜치에서 재생성 필요.

---

## 4. 8계층 + Hook 최종 상태

| 계층 | 상태 | 비고 |
|------|:----:|------|
| Model | ⚠️ | IDE 설정만, 프로젝트 산출물 없음 |
| Agent | ⚠️ | rules·Skill·Command 있음, Ask/Agent 명시 분리 약함 |
| Harness | ⚠️ | `pyproject.toml`만, src/tests 골격·TC 0건 |
| Rule | ✅ | `.cursorrules` |
| Skill | ✅ | `unit-converter-tdd` |
| Command | ⚠️ | `/tdd-red`, `/review-ecb` (GREEN/REFACTOR 없음) |
| Tool/MCP | ⚠️ | pytest 전제, Hook pytest 연동 없음 |
| Test/Review Loop | ⚠️ | 문서화 완료, 실행 증거 없음 |
| Hook | ⚠️ | `sessionStart`만, red/src·pytest 게이트 미구현 |

---

## 5. Test/Review Loop 성공 기준 (정의됨)

1. **Rule** — `.cursorrules` 존재·ECB/Dual-Track/TDD 금지 문장
2. **RED Command** — `/tdd-red` 절차·선언·tests/만
3. **ECB Review** — `/review-ecb` PASS/FAIL 표, 수정 없음
4. **Skill** — Phase별 pytest 표 + `reference.md` D-* 대응
5. **Harness** — `pytest` RED FAIL / GREEN PASS (Hook은 향후)

---

## 6. 미완·다음 단계

| 우선순위 | 항목 |
|:--:|------|
| P0 | `src/`·`tests/` Harness 골격 복원, `D-CONV-01` RED TC |
| P0 | `.cursorrules` E001~E007·SSOT 단일화 보강 (리뷰 P0 반영) |
| P1 | Hook `afterFileEdit`(red→src), `afterShellExecution`(pytest) |
| P1 | `entity/constants.py`, `entity/exceptions.py` GREEN 구현 |
| P2 | `tdd-green` Command 또는 Skill만으로 GREEN 운영 결정 |
| P2 | `config/units.json`, U-* TC |

---

## 7. AI 활용 회고 (세션 관점)

| 도움이 된 점 | 한계 |
|-------------|------|
| 레거시 스멜·PRD 갭 구조화 | Rule/Skill/Command 중복 — Command 필요성 재검토 필요 |
| FR/NFR·ECB 매핑 일관성 | `int[6]` 1-index는 UnitConverter에 불필요 — Enum SSOT로 대체 권고 |
| Cursor 산출물 일괄 생성 | Hook `additional_context` 주입은 Cursor 버전 이슈 가능 |
| PRD·README·rules 정합 | 앱 코드·pytest 실행 증거 없음 — Loop 미폐쇄 |

---

## 8. 관련 링크

- GitHub: [msubkim-ship-it/UnitConverter_07](https://github.com/msubkim-ship-it/UnitConverter_07)
- Transcript: [../Prompting/01-session-transcript.md](../Prompting/01-session-transcript.md)

---

작성자: 김명섭  
리뷰어: 김민주, 김소민, 김연우, 김정균, 김준호
