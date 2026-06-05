# 06 — UnitConverter_07 REFACTOR Smell 진단 세션 보고서

| 항목 | 내용 |
|------|------|
| 프로젝트 | UnitConverter_07 |
| 저장소 | https://github.com/msubkim-ship-it/UnitConverter_07 |
| 세션 일자 | 2026-06-05 |
| 브랜치 | `refactoring` |
| Phase | REFACTOR Smell — entity / Logic+UI Track (진단만) |
| 대응 Transcript | [Prompting/06-session-transcript.md](../Prompting/06-session-transcript.md) |
| 작성 | AI Agent 세션 산출물 정리 |

---

## 1. 세션 목적

05 세션 **Golden Master·GREEN PASS** 이후, `/refactor-smell`로 `src/`·`tests/` 코드 스멜을 **읽기 전용** 진단한다.

- GREEN 선행 게이트: `python -m pytest tests/ -v` → exit **0**
- 스캔 범위: `src/` (entity 2파일), `tests/` (D-LOC-01·헬퍼·conftest)
- **코드 수정·commit 금지** — `/refactor-safe` 후보 선정만
- Change Budget: 파일≤3 · 클래스≤1 · 메서드≤3

---

## 2. 수행 작업 요약

| # | 주제 | 산출·결과 |
|---|------|-----------|
| 1 | GREEN 게이트 | exit code **0** — 2 passed (`test_d_loc_01`, `test_d_loc_01_step_a_success`) |
| 2 | 브랜치 확인 | `refactoring` (refactor-smell 권장 브랜치 일치) |
| 3 | src/ 스캔 | `entity/constants.py`, `entity/loc.py` — ECB·SSOT 양호 |
| 4 | tests/ 스캔 | conftest `grid_g1`, `test_d_loc_01`, `_approval.py` — DRY·Magic Number 잔존 |
| 5 | PRD 대조 | MagicConstant SSOT 개선; Act API 명명(`find_blank_coords`) 잔존 |
| 6 | 스멜 표 | Critical **0** / P0 **1** / P1 **2** / P2 **2** |
| 7 | refactor-safe 후보 | 후보 A(권장): `get_g1_ratios_row_major()` + 별칭 |
| 8 | Export | 본 보고서 + `06-session-transcript.md` |

---

## 3. GREEN 게이트 증거

| 항목 | 내용 |
|------|------|
| 명령 | `python -m pytest tests/ -v` |
| exit code | **0** |
| 수집 | 2 |
| 결과 | **2 PASSED** |
| 판정 | 스캔 진행 허용 |

---

## 4. 스멜 진단 요약

| # | 우선순위 | 스멜 | 위치 | refactor-safe |
|---|--------|------|------|---------------|
| 1 | **P0** | Mysterious Name | `src/entity/loc.py:find_blank_coords` | ✅ 후보 A |
| 2 | P1 | Duplicated Code | `tests/conftest.py:grid_g1` ↔ `RATIOS_ROW_MAJOR` | ❌ tests 동결 |
| 3 | P1 | Duplicated Code | `tests/entity/test_d_loc_01.py:test_d_loc_01` | ❌ tests 동결 |
| 4 | P2 | Magic Number | `tests/conftest.py:grid_g1` (`1.0` 리터럴) | ❌ tests 동결 |
| 5 | P2 | Thin Wrapper | `src/entity/loc.py:find_blank_coords` | ✅ 후보 B (#1 통합) |
| 6 | — | ECB 위반 | — | **PASS** |
| 7 | — | Long Method | — | **PASS** |
| 8 | — | Feature Envy | — | **PASS** (boundary 미존재) |

**스캔 범위 밖 (레거시 참고):** `UnitConverter.py:main` — Long Method(32줄), Magic Number ×4, if-elif OCP 위반.

---

## 5. PRD·초기 레거시 대비

| 구분 | 초기 레거시 | 현재 `src/`·`tests/` |
|------|------------|----------------------|
| MagicConstant SSOT | `UnitConverter.py` 리터럴 ×4 | `entity/constants.py` 단일 — **개선** |
| ECB | 단일 파일 혼재 | entity 단방향 — **양호** |
| SRP/OCP | `main()` God function | control/boundary **미구현** |
| E001~E007 | 없음 | `exceptions.py` **미구현** |
| Act API 명명 | — | `find_blank_coords()` — ratio 반환과 불일치 — **잔존** |

---

## 6. `/refactor-safe` 권고

| 후보 | 스멜 # | 예상 diff | Budget |
|------|--------|-----------|--------|
| **A (권장)** | #1 | `loc.py`: `get_g1_ratios_row_major()` + `find_blank_coords` 별칭 | 파일 1 · 메서드 1~2 |
| B | #1+#5 | A + `G1Ratios` NamedTuple (`constants.py` + `loc.py`) | 파일 2 · 클래스 1 |

**TC 동결 제약:** #2~#4는 `tests/` 수정 필요 → `/refactor-safe` 범위 밖.

---

## 7. ECB·TDD 점검

| 점검 | 결과 |
|------|------|
| ECB import | ✅ entity → stdlib + `entity.constants`만 |
| MagicConstant SSOT (`src/`) | ✅ 리터럴 `constants.py` 단일 |
| entity E001~E005 emit | ✅ 해당 없음 |
| 코드 수정 | ✅ 없음 (진단만) |
| pytest | ✅ exit 0 유지 |

---

## 8. 미완·다음 단계

| 우선순위 | 항목 |
|:--:|------|
| P0 | `/refactor-safe` — **#1 Mysterious Name** (후보 A) |
| P1 | spec/red — conftest `grid_g1` → `RATIOS_ROW_MAJOR` 직접 참조 (#2, #4) |
| P1 | RED/리뷰 — `test_d_loc_01` assert 단일화 (#3) |
| P2 | `/review-ecb` — refactor-safe 완료 후 import·SSOT 재확인 |
| P2 | `/red-skeleton` — D-LOC-02, D-LOC-03 |

---

## 9. AI 활용 회고

| 도움이 된 점 | 한계 |
|-------------|------|
| GREEN PASS 선행 확인 후 스캔 — TDD 게이트 준수 | Harness 초기 단계 — `src/` 스멜 후보가 제한적 |
| TC 동결 제약과 tests/ 스멜 분리 — refactor-safe 범위 명확화 | P1 스멜(#2~#4)은 tests 수정 없이 해결 불가 |
| Change Budget 내 후보 A/B 구체화 | `find_blank_coords` 명명은 spec 설계 의도와 충돌 가능 — 팀 합의 필요 |

---

## 10. 관련 링크

- 이전 보고: [05-session-report.md](./05-session-report.md)
- Transcript: [../Prompting/06-session-transcript.md](../Prompting/06-session-transcript.md)
- Source: `agent-transcripts/f397b246-04cf-4f16-ac7c-65488c639f03.jsonl`

---

작성자: 김명섭  
리뷰어: 김민주, 김소민, 김연우, 김정균, 김준호
