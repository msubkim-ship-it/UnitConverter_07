# Unit Converter (Python)

![unit-converter](./unit-converter.jpg)

길이 단위 변환 CLI. 입력 `단위:값`(예: `meter:2.5`)을 받아 등록된 **다른 모든 단위**로 변환해 출력한다.

> **요구사항 상세:** [PRD.md](./PRD.md)  
> **개발 헌법:** [.cursorrules](./.cursorrules)

---

## Overview

- 사용자 입력(`단위:값`) 기반 다중 단위 변환
- **ECB** 아키텍처 + **Dual-Track TDD**로 확장·검증
- OCP/SRP — 단위·포맷·설정 추가 시 기존 코드 변경 최소화
- pytest로 변환 정확도·입력 검증 보장

## 프로젝트 구조

```text
UnitConverter_07/
├── PRD.md                 # 기능·비기능 요구사항 (FR/NFR)
├── .cursorrules           # ECB + Dual-Track TDD 헌법
├── pyproject.toml         # pytest Harness
├── UnitConverter.py       # 레거시 CLI (점진 교체 예정)
├── src/
│   ├── entity/            # 도메인·상수·에러 SSOT
│   ├── control/           # 변환·Registry·검증
│   └── boundary/          # CLI·Parser·Formatter·Config
├── tests/
│   ├── entity/            # Logic Track — test_d_*
│   ├── control/
│   └── boundary/          # UI Track — test_u_*
└── .cursor/
    ├── commands/          # /tdd-red, /review-ecb
    ├── skills/            # unit-converter-tdd
    └── hooks.json         # sessionStart 컨텍스트 주입
```

**의존 방향:** `boundary → control → entity` (단방향)

---

## 빠른 시작

### 가상환경

```bash
# 생성
python -m venv venv

# 활성화 (Windows)
venv\Scripts\activate

# 활성화 (macOS/Linux)
source venv/bin/activate

# 개발 의존성 (pytest)
pip install -e ".[dev]"
```

### 실행 (레거시)

```bash
python UnitConverter.py
```

### 테스트

```bash
pytest -v
pytest tests/entity/ -v          # Logic Track
pytest tests/boundary/ -v        # UI Track
```

```bash
deactivate   # 가상환경 비활성화
```

---

## 사용 예시

**입력**

```text
meter:2.5
```

**출력 (표 형식, 소수 1자리)**

```text
2.5 meter = 8.2 feet
2.5 meter = 2.7 yard
```

**동적 단위 등록 (추가 요구)**

```text
1 cubit = 0.4572 meter
```

---

## 기본 요구사항

1. 입력 형식 `단위:값` — 위 예시와 같이 변환·출력
2. 기본 지원 단위: **meter**, **feet**, **yard**
3. 새 단위 추가 시 기존 코드 변경 최소화 (**OCP**)
4. 단위 간 변환 정확도 **테스트 코드**로 검증

## 비즈니스 로직

| 관계 | 비율 |
|------|------|
| meter → feet | 1 m = **3.28084** ft |
| meter → yard | 1 m = **1.09361** yd |
| feet ↔ yard | meter 기준 간접 계산 |

변환 상수 SSOT: `src/entity/constants.py` (리터럴 산재 금지)

## 품질 요구사항

- **OCP** — Registry·Formatter Strategy로 확장
- **SRP** — ECB 레이어당 단일 책임
- **입력 검증** — 음수, 잘못된 형식, 미등록 단위 (에러 코드 E001~E007, [PRD.md](./PRD.md) 참고)

## 추가 요구사항

| 항목 | 설명 |
|------|------|
| 설정 외부화 | JSON/YAML에서 변환 비율 로드 |
| 동적 등록 | `1 cubit = 0.4572 meter` 런타임 등록 |
| 출력 포맷 | JSON / CSV / 표 |

---

## 개발 방식 (Dual-Track TDD)

| Track | 대상 | 테스트 | Mock |
|-------|------|--------|------|
| Logic | entity, control | `D-*` / `test_d_*` | Domain Mock **금지** |
| UI | boundary | `U-*` / `test_u_*` | stdin/stdout·파일 I/O 허용 |

**브랜치:** `spec → red → green → refactoring → staging → main`

| Phase | 수정 범위 | pytest |
|-------|-----------|--------|
| RED | `tests/`만 | exit ≠ 0 (FAIL) |
| GREEN | `src/` 최소 구현 | exit = 0 (PASS) |
| REFACTOR | `src/` 구조 개선 | PASS 유지 |

### Cursor 도구

| 도구 | 용도 |
|------|------|
| `/tdd-red` | RED Phase — 실패 테스트 먼저 |
| `/review-ecb` | ECB·계약 위반 리뷰 (코드 수정 없음) |
| Skill `unit-converter-tdd` | RED/GREEN/REFACTOR 절차 |
| Hook `sessionStart` | 세션 컨텍스트·`.cursorrules` SSOT 주입 |

D-* TC ID: `.cursor/skills/unit-converter-tdd/reference.md`

---

## 생성형AI를 활용한 Activities (6시간)

1. **문제 코드 및 기본 요구사항 분석** (0.5시간)  
   - 레거시 `UnitConverter.py` 구조·로직, [PRD.md](./PRD.md) 갭 분석
2. **기본 요구사항 및 품질 요구사항 구현** (2시간)  
   - ECB 인터페이스, SRP 클래스, 입력 검증
3. **TC 구현** (0.5시간)  
   - 변환·입력 검증 D-* / U-* TC (RED → GREEN)
4. **추가 요구사항 구현** (2시간)  
   - 설정 외부화, 동적 등록, 출력 포맷 + TC
5. **회고 및 발표** (1시간)  
   - 목표 달성도, AI 활용, TC·리팩터링 회고

---

## 문서

| 파일 | 역할 |
|------|------|
| [PRD.md](./PRD.md) | FR/NFR, 에러 계약, 마일스톤 |
| [.cursorrules](./.cursorrules) | Agent 개발 헌법 |
| `.cursor/skills/unit-converter-tdd/` | TDD 실행 절차 |

---

작성자: 김명섭  
리뷰어: 김민주, 김소민, 김연우, 김정균, 김준호
