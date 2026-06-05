# Unit Converter (Python)

![unit-converter](./unit-converter.jpg)

길이 단위 변환 CLI. 입력 `단위:값`(예: `meter:2.5`)을 받아 등록된 **다른 모든 단위**로 변환해 출력한다.

> **요구사항 상세:** [PRD.md](./PRD.md)  
> **개발 헌법:** [.cursorrules](./.cursorrules)  
> **세션 보고:** [Report/](./Report/) · 최신 [06-session-report.md](./Report/06-session-report.md)

---

## Overview

- 사용자 입력(`단위:값`) 기반 다중 단위 변환
- **ECB** 아키텍처 + **Dual-Track TDD**로 확장·검증
- OCP/SRP — 단위·포맷·설정 추가 시 기존 코드 변경 최소화
- pytest로 변환 정확도·입력 검증·CLI 표면화 보장

## 프로젝트 구조

```text
UnitConverter_07/
├── PRD.md                      # FR/NFR·에러 계약·마일스톤 (SSOT)
├── .cursorrules                # ECB + Dual-Track TDD 헌법
├── pyproject.toml              # pytest Harness (pythonpath=src)
├── config/units.json           # boundary 로드용 (수치 SSOT는 entity/constants.py)
├── UnitConverter.py            # 레거시 CLI (점진 교체 예정)
├── src/
│   ├── entity/                 # 도메인·상수·에러 SSOT
│   ├── control/                # 변환·Registry·검증
│   └── boundary/               # CLI·Parser·Formatter·Config
├── tests/
│   ├── entity/                 # Logic Track — test_d_*
│   ├── control/
│   ├── boundary/               # UI Track — test_u_*
│   │   └── golden/             # Golden Master (U-* GREEN 후, 승인 후 갱신)
│   ├── _approval.py            # assert_matches_golden() — boundary 전용
│   └── conftest.py             # 공유 fixture (grid_g1 등)
├── Report/                     # 세션·회고 보고서 (01~06)
├── Prompting/                  # 설계 세션 transcript (01~06)
└── .cursor/
    ├── commands/               # TDD slash commands (아래 표)
    ├── skills/unit-converter-tdd/
    └── hooks.json              # sessionStart 컨텍스트 주입
```

**의존 방향:** `boundary → control → entity` (단방향)

### 현재 진행 상태

| 항목 | 상태 |
|------|------|
| 브랜치 | `refactoring` (D-LOC-01 GREEN + 리뷰 반영) |
| pytest | **1 passed** — `test_d_loc_01` (Logic Track) |
| entity | `constants.py` (비율 SSOT), `loc.py` (`get_g1_ratios_row_major()`) |
| control / boundary | 미구현 |
| Golden Master | **U-* GREEN 후** `tests/boundary/golden/` — entity Logic Track 혼용 금지 |
| 레거시 실행 | `UnitConverter.py`만 CLI 동작 (ECB 마이그레이션 전) |
| PR | [PR_SUMMARY.md](./PR_SUMMARY.md) — green→staging, **2 commits** 기준 |

### Harness — `tests/{layer}/__init__.py` 재생성 금지

`tests/entity/`, `tests/control/`, `tests/boundary/` 아래 **`__init__.py`를 만들지 않는다.**

| 이유 | pytest가 `tests/entity/` 등을 Python 패키지로 등록하면 `import entity` 시 `src/entity` 대신 테스트 디렉터리가 먼저 로드됨 |
| 증상 | `ModuleNotFoundError: No module named 'entity.constants'` (04 세션) |
| 허용 | `tests/conftest.py`, `tests/_approval.py` 등 **tests 루트** 헬퍼만 |
| Golden | Logic `test_d_*`에 golden **금지** — boundary `test_u_*` + `/golden-master`만 |

---

## 빠른 시작

### 가상환경

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

pip install -e ".[dev]"
```

### 실행 (레거시)

```bash
python UnitConverter.py
```

### 테스트

```bash
pytest -v
pytest tests/entity/ -v                              # Logic Track (D-*)
pytest tests/boundary/ -v                            # UI Track (U-*)
pytest tests/entity/test_d_loc_01.py::test_d_loc_01 -v   # D-LOC-01 GREEN
```

**Golden Master** — boundary **U-* GREEN** 후에만 (`tests/boundary/golden/`):

```bash
# 예: U-CLI-01 GREEN 이후, 사용자 승인 후 baseline 생성
UPDATE_GOLDEN=1 pytest tests/boundary/test_u_cli.py::test_u_cli_01 -v
pytest tests/boundary/test_u_cli.py::test_u_cli_01 -v   # matched 확인
```

```bash
deactivate
```

---

## 사용 예시

**정상 입력**

```text
meter:2.5
```

**출력 (표 형식, 소수 1자리 — 목표 동작)**

```text
2.5 meter = 8.2 feet
2.5 meter = 2.7 yard
```

**입력 검증 (ECB 목표)**

| 입력 | 에러 코드 | boundary 역할 |
|------|-----------|---------------|
| `meter:-2.5` | E003 | 사용자 메시지 출력 |
| `meter2.5` (`:` 없음) | E001 | 사용자 메시지 출력 |
| `meter:abc` | E002 | 사용자 메시지 출력 |

**동적 단위 등록 (추가 요구)**

```text
1 cubit = 0.4572 meter
```

---

## 기본·품질 요구사항

| 구분 | 내용 |
|------|------|
| 입력 | `단위:값`, 기본 단위 meter / feet / yard |
| 변환 | meter 기준; feet↔yard 간접 계산 |
| 상수 SSOT | `src/entity/constants.py` (리터럴 산재 금지) |
| 에러 SSOT | `src/entity/exceptions.py` (E001~E007) |
| 품질 | OCP, SRP, ECB, Dual-Track TDD ([PRD.md](./PRD.md)) |

| 관계 | 비율 |
|------|------|
| meter → feet | 1 m = **3.28084** ft |
| meter → yard | 1 m = **1.09361** yd |

## 추가 요구사항

| 항목 | 설명 |
|------|------|
| 설정 외부화 | JSON/YAML에서 변환 비율 로드 |
| 동적 등록 | `1 cubit = 0.4572 meter` 런타임 등록 |
| 출력 포맷 | JSON / CSV / 표 |

---

## 개발 방식 (Dual-Track TDD)

| Track | 레이어 | TC ID | 테스트 파일 | Mock |
|-------|--------|-------|-------------|------|
| Logic | entity, control | `D-*` | `test_d_*.py` | Domain Mock **금지** |
| UI | boundary | `U-*` | `test_u_*.py` | stdin/stdout·파일 I/O 허용 |

**브랜치:** `spec → red → green → refactoring → staging → main`

| Phase | 수정 범위 | pytest |
|-------|-----------|--------|
| RED | `tests/`만 | exit ≠ 0 (FAIL) |
| GREEN | `src/` 최소 구현 | exit = 0 (PASS) |
| REFACTOR | `src/` 구조 개선 (TC 동결) | PASS 유지 |

### TDD 워크플로 (Cursor Commands)

권장 순서:

```text
/red-test-plan → /red-skeleton → /green-minimal → /golden-master → /refactor-smell → /refactor-safe
```

| Command | Phase | 역할 |
|---------|-------|------|
| `/red-test-plan` | red-plan | TC·FR·파일 계획표만 (코드 없음) |
| `/red-skeleton` | red | `tests/` 실패 골격 + pytest FAIL |
| `/green-minimal` | green | `src/` 최소 구현 + pytest PASS |
| `/golden-master` | green/refactor | **boundary U-*** 출력 스냅샷 (승인 후 golden) |
| `/refactor-smell` | 진단 | 스멜 표만 (수정 없음) |
| `/refactor-safe` | refactor | `src/` 리팩터, tests 동결 |
| `/tdd-red` | red | plan+skeleton 단일 RED (레거시) |
| `/review-ecb` | 리뷰 | ECB·계약 위반 표 (수정 없음) |

Skill: `.cursor/skills/unit-converter-tdd/` · Hook: `sessionStart` → `.cursorrules` 주입

### 테스트 ID (요약)

**Logic — PRD §7.1 / [reference.md](./.cursor/skills/unit-converter-tdd/reference.md)**

| 묶음 | ID |
|------|-----|
| 변환 | D-CONV-01 ~ 06 |
| 등록 | D-REG-01 ~ 02 |
| 에러 | D-ERR-01 ~ 06 |

**Logic — SSOT 위치 (PRD §3.5·§7.1)**

| ID | 검증 | 상태 |
|----|------|------|
| D-LOC-01 | `constants` ratio SSOT (G1 row-major) | ✅ GREEN |
| D-LOC-02 | `exceptions` E001~E007 SSOT | ⬜ 미착수 |
| D-LOC-03 | `BASE_UNIT == "meter"` | ⬜ 미착수 |

**UI — PRD §7.2**

| ID | 검증 |
|----|------|
| U-CLI-01 | CLI 표 출력 |
| U-FMT-01/02 | JSON / CSV |
| U-CFG-01 | 설정 파일 로드 |
| U-REG-01 | 등록 입력 CLI |

**UI — 입력 표면화 (PRD §3.6·§7.2)**

| ID | 검증 |
|----|------|
| U-IN-01 | 음수 입력 → E003 메시지 (`grid=None`, 기본 Registry) |
| U-IN-02 | `:` 없는 형식 → E001 메시지 |

---

## 생성형AI를 활용한 Activities (6시간)

1. **문제 코드 및 기본 요구사항 분석** (0.5시간) — 레거시·[PRD.md](./PRD.md) 갭 분석  
2. **기본 요구사항 및 품질 요구사항 구현** (2시간) — ECB, SRP, 입력 검증  
3. **TC 구현** (0.5시간) — D-* / U-* RED → GREEN  
4. **추가 요구사항 구현** (2시간) — 설정·동적 등록·출력 포맷  
5. **회고 및 발표** (1시간) — AI 활용·TC·리팩터링 회고  

---

## 문서

| 파일 | 역할 |
|------|------|
| [PRD.md](./PRD.md) | FR/NFR, E001~E007, 마일스톤 |
| [.cursorrules](./.cursorrules) | Agent 개발 헌법 |
| [.cursor/skills/unit-converter-tdd/](./.cursor/skills/unit-converter-tdd/) | RED/GREEN/REFACTOR 절차 |
| [PR_SUMMARY.md](./PR_SUMMARY.md) | green→staging PR 본문 (2 commits · pytest 게이트) |
| [Report/](./Report/) | 세션 보고서 목록 ([README](./Report/README.md)) — 01 설계 ~ **06 refactor-smell** |
| [Prompting/](./Prompting/) | Transcript Export ([README](./Prompting/README.md)) — 01 ~ **06** |

---

작성자: 김명섭  
리뷰어: 김민주, 김소민, 김연우, 김정균, 김준호
