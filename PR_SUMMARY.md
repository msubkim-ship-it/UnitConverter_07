# PR Summary — `green` → `staging`

> GitHub PR 본문 복사용. 리뷰 반영 기준 (2026-06-05).

## Summary

- **D-LOC-01 (Logic Track):** `entity/constants.py`에 변환 비율 MagicConstant SSOT (`FEET_PER_METER`, `YARD_PER_METER`, `RATIOS_ROW_MAJOR`)
- **Act API:** `get_g1_ratios_row_major()` — G1 row-major ratio tuple 반환 (`find_blank_coords` → rename)
- **Golden Master:** entity Logic Track에서 분리 — **U-* GREEN 후** `tests/boundary/golden/` + `/golden-master` 적용
- **Harness:** `tests/{entity,control,boundary}/__init__.py` 재생성 금지 (import shadowing 방지)

## Commits (2)

| # | SHA | 메시지 |
|---|-----|--------|
| 1 | `90a7bcf` | `[GREEN] D-LOC-01 entity constants SSOT and find_blank_coords` |
| 2 | `db81a09` | `Add D-LOC-01 Golden Master harness and session 05 docs.` |

> 커밋 2의 entity golden은 리뷰에 따라 제거됨. Golden harness(`tests/_approval.py`)는 boundary 경로(`tests/boundary/golden/`)로 정렬.

## Test plan

- [x] `python -m pytest tests/ -v` → **1 passed** (`test_d_loc_01`)
- [x] `python -m pytest tests/entity/test_d_loc_01.py::test_d_loc_01 -v` → PASSED
- [ ] Golden — U-CLI-01 등 **boundary U-* GREEN** 후 `/golden-master`로 추가

## 변경 파일 (리뷰 반영)

| 경로 | 변경 |
|------|------|
| `src/entity/loc.py` | `get_g1_ratios_row_major()` rename |
| `tests/entity/test_d_loc_01.py` | Logic assert만 유지 (golden TC 제거) |
| `tests/_approval.py` | golden root → `tests/boundary/golden/` |
| `tests/golden/` | entity golden 삭제 (boundary U-* 대기) |
| `README.md`, `SKILL.md` | Harness·Golden 가이드 |
| `PR_SUMMARY.md` | 본 문서 |

## ECB

- entity → stdlib + `entity.constants`만
- MagicConstant 리터럴: `constants.py` 단일 SSOT
- Golden: UI Track(boundary) 전용 — Logic `test_d_*` 혼용 금지
