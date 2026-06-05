# Unit Converter (Python)

![unit-converter](./unit-converter.jpg)

길이 단위 변환 CLI. 입력 `단위:값`(예: `meter:2.5`)을 받아 등록된 **다른 모든 단위**로 변환해 출력한다.

> **요구사항 상세:** [PRD.md](./PRD.md)  
> **개발 헌법:** [.cursorrules](./.cursorrules)  
> **세션 보고:** [Report/01-session-report.md](./Report/01-session-report.md)

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
│   └── boundary/               # UI Track — test_u_*
├── Report/                     # 세션·회고 보고서
├── Prompting/                  # 설계 세션 transcript
└── .cursor/
    ├── commands/               # TDD slash commands (아래 표)
    ├── skills/unit-converter-tdd/
    └── hooks.json              # sessionStart 컨텍스트 주입
```

**의존 방향:** `boundary → control → entity` (단방향)

> **현재 Harness:** `red` 브랜치에서 `src/`·`tests/` ECB 골격·TC를 RED → GREEN 순으로 채웁니다. 레거시 실행은 `UnitConverter.py`만 사용 가능합니다.

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
pytest tests/entity/ -v          # Logic Track (D-*)
pytest tests/boundary/ -v        # UI Track (U-*)
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
| `/golden-master` | green/refactor | boundary 출력 스냅샷 (승인 후 golden) |
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

| ID | 검증 |
|----|------|
| D-LOC-01 ~ 03 | `constants` / `exceptions` / `BASE_UNIT` SSOT |

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
| [Report/](./Report/) | 세션 보고서 ([01](./Report/01-session-report.md), [02](./Report/02-session-report.md)) |
| [Prompting/](./Prompting/) | 세션 Transcript Export |

---

작성자: 김명섭  
리뷰어: 김민주, 김소민, 김연우, 김정균, 김준호
