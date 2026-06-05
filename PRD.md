# PRD — UnitConverter_07

| 항목 | 내용 |
|------|------|
| 프로젝트 | UnitConverter_07 |
| 도메인 | 길이 단위 변환 (Length Unit Conversion) |
| 버전 | 0.2.0 |
| 기준 문서 | README.md, `.cursorrules` |
| 아키텍처 | ECB (boundary → control → entity) |
| 개발 방식 | Dual-Track TDD |

---

## 1. 개요

### 1.1 목적

사용자가 입력한 길이(`단위:값`)를 기반으로, 등록된 **모든 다른 단위**로 변환하여 출력하는 CLI 프로그램을 제공한다. 새 단위·출력 포맷·설정 소스 추가 시 **기존 코드 변경을 최소화**하고, 변환 로직은 **테스트로 검증**한다.

### 1.2 사용자

- 길이 단위를 변환해야 하는 일반 사용자 (CLI)
- 단위·비율·포맷을 확장하는 개발자

### 1.3 범위

| 포함 | 제외 |
|------|------|
| meter/feet/yard 기본 변환 | 무게·온도 등 다른 물리량 |
| 동적 단위 등록 | GUI |
| JSON/YAML 설정 로드 | 원격 API 실시간 환율 |
| JSON/CSV/표 출력 | 다국어 UI |

---

## 2. 비즈니스 규칙

### 2.1 변환 비율 (기준 단위: meter)

| 단위 | 비율 |
|------|------|
| meter | 1 (기준) |
| feet | 1 meter = **3.28084** feet |
| yard | 1 meter = **1.09361** yard |

- feet ↔ yard 변환은 **meter 기준 간접 계산**으로 수행한다.
- 모든 변환 공식: `value_in_target = value_in_meter × (target_ratio / meter_ratio)` (meter 기준 환산 후 적용).

### 2.2 출력 형식

- 기본 표 형식: `{입력값} {입력단위} = {결과값} {대상단위}`
- 예: `2.5 meter = 8.2 feet` (소수 **1자리 반올림**, 상세 정밀도는 TC에서 정의)
- **입력 단위 자신으로의 변환은 출력에서 제외**한다.

### 2.3 MagicConstant SSOT

- 변환 비율·기준 단위 상수는 `src/entity/constants.py`에 **단일 정의**한다. (요구 ID: **FR-LOC-01**)
- `config/units.json`(또는 YAML)은 boundary가 로드하여 control에 주입하며, 수치를 코드·테스트에 **리터럴 복사 금지**.
- 에러 코드 enum은 `src/entity/exceptions.py`에 **단일 정의**한다. (**FR-LOC-02**)
- 기준 단위명(`meter`)은 `entity/constants.py`의 `BASE_UNIT` 등으로 **단일 정의**한다. (**FR-LOC-03**)

---

## 3. 기능 요구사항 (FR)

### 3.1 입력·변환

| ID | 요구사항 | 우선순위 | 완료 기준 |
|----|----------|----------|-----------|
| FR-01 | `단위:값` 형식 입력 수신 (예: `meter:2.5`) | P0 | 파싱 성공 시 단위·숫자 분리 |
| FR-02 | 입력값을 **등록된 다른 모든 단위**로 변환 출력 | P0 | 입력 단위 제외, 나머지 전부 출력 |
| FR-03 | 기본 단위 meter, feet, yard 지원 | P0 | 앱 시작 시 3단위 등록 |
| FR-04 | FR-02 출력 소수 1자리 반올림 (표 포맷) | P0 | `2.5 meter = 8.2 feet` 형식 |
| FR-05 | meter ↔ feet ↔ yard 정확 변환 | P0 | D-CONV-01~06 통과 |
| FR-06 | feet ↔ yard는 meter 기반 간접 변환 | P0 | D-CONV-05 통과 |

### 3.2 설정·확장

| ID | 요구사항 | 우선순위 | 완료 기준 |
|----|----------|----------|-----------|
| FR-07 | 변환 비율을 외부 설정(JSON/YAML)에서 로드 | P1 | 설정 파일 변경만으로 비율 반영 |
| FR-08 | 런타임 동적 단위 등록 (`1 cubit = 0.4572 meter`) | P1 | 등록 후 변환 가능 (D-REG-01) |
| FR-09 | 출력 포맷 선택: JSON / CSV / 표 | P1 | 동일 입력·3종 포맷 출력 |

### 3.3 입력 검증·에러

| ID | 요구사항 | 우선순위 | 완료 기준 |
|----|----------|----------|-----------|
| FR-10 | 음수 입력 거부 | P0 | E003 발생 |
| FR-11 | 잘못된 형식 거부 (`:` 없음, 빈 입력, 숫자 아님) | P0 | E001 / E002 |
| FR-12 | 미등록 단위 거부 | P0 | E004 |
| FR-13 | 빈 단위명 거부 | P0 | E005 |
| FR-14 | 등록 문법 오류 거부 | P1 | E006 |
| FR-15 | 중복 단위·설정 충돌 거부 | P1 | E007 |

### 3.4 에러 코드 계약 (SSOT: `src/entity/exceptions.py`)

| 코드 | 의미 | raise 주체 |
|------|------|------------|
| E001 | 형식 오류 (콜론 없음·빈 입력) | control |
| E002 | 숫자 변환 실패 | control |
| E003 | 음수 값 | entity / control |
| E004 | 미등록 단위 | control |
| E005 | 빈 단위명 | control |
| E006 | 등록 문법 오류 | control |
| E007 | 중복 단위·설정 충돌 | control |

- boundary: 에러 **코드 → 사용자 메시지** 변환·출력만 담당. (요구 ID: **FR-IN-01**~**02**)
- Logic TC: 메시지 문자열이 아닌 **코드(E00x)** 로 assert.
- UI TC: boundary가 출력한 **사용자 메시지**·exit code로 assert (stdin/stdout Mock 허용).

### 3.5 SSOT 위치 (Location)

| ID | 요구사항 | 우선순위 | 완료 기준 |
|----|----------|----------|-----------|
| FR-LOC-01 | 변환 비율 상수는 `entity/constants.py`만 정의·참조 | P0 | D-LOC-01 PASS; 테스트·src에 `3.28084`/`1.09361` 리터럴 0건 |
| FR-LOC-02 | E001~E007는 `entity/exceptions.py`의 `ErrorCode`만 정의 | P0 | D-LOC-02 PASS |
| FR-LOC-03 | 기준 단위명 SSOT (`BASE_UNIT == "meter"`) | P0 | D-LOC-03 PASS |

### 3.6 CLI 입력 표면화 (boundary)

| ID | 요구사항 | 우선순위 | 완료 기준 |
|----|----------|----------|-----------|
| FR-IN-01 | 음수 입력 시 FR-10·E003을 CLI에 표면화 (exit ≠ 0) | P0 | U-IN-01 PASS (`meter:-2.5`, 기본 Registry `grid=None`) |
| FR-IN-02 | `:` 없는 형식 시 FR-11·E001을 CLI에 표면화 | P0 | U-IN-02 PASS (`meter2.5`) |

---

## 4. 비기능 요구사항 (NFR)

| ID | 요구사항 | 완료 기준 |
|----|----------|-----------|
| NFR-01 | **OCP** — 단위·포맷·설정 소스 추가 시 기존 entity/control 최소 수정 | Registry·Formatter Strategy |
| NFR-02 | **SRP** — 클래스·모듈당 단일 책임 | ECB 레이어별 1역할 |
| NFR-03 | **ECB** — boundary → control → entity 단방향 import | import 역방향 0건 |
| NFR-04 | **테스트 가능** — CLI 없이 entity/control 단위 테스트 | pytest Logic Track |
| NFR-05 | **Dual-Track** — Logic Mock 금지 / UI(boundary) I/O Mock 허용 | test_d_* / test_u_* 분리 |
| NFR-06 | **변환 정확도 TC** — D-CONV-* 전부 PASS | pytest |
| NFR-07 | **입력 검증 TC** — D-ERR-* 전부 PASS | pytest |
| NFR-08 | **추가 요구 TC** — FR-07~09 + D-REG-* PASS | pytest |
| NFR-09 | Python ≥ 3.10, pytest ≥ 8.0 | `pyproject.toml` |
| NFR-10 | **SSOT 위치 TC** — D-LOC-* 전부 PASS | pytest |
| NFR-11 | **입력 표면화 TC** — U-IN-* (M1) PASS | pytest |

---

## 5. 아키텍처 (ECB)

```
boundary → control → entity
```

| Layer | 경로 | 책임 |
|-------|------|------|
| entity | `src/entity/` | Unit, ConversionRatio, constants, exceptions (SSOT) |
| control | `src/control/` | ConversionService, UnitRegistry, 검증 오케스트레이션 |
| boundary | `src/boundary/` | CLI, InputParser, OutputFormatter, ConfigLoader |

### 5.1 확장 포인트 (OCP)

| 확장 | 방식 |
|------|------|
| 새 단위 | Registry.register() 또는 config 추가 |
| 새 출력 포맷 | OutputFormatter 구현체 추가 |
| 새 설정 포맷 | ConfigLoader 구현체 추가 |

---

## 6. 입출력 명세

### 6.1 변환 입력

```
meter:2.5
```

### 6.2 변환 출력 (표)

```
2.5 meter = 8.2 feet
2.5 meter = 2.7 yard
```

### 6.3 동적 등록 입력

```
1 cubit = 0.4572 meter
```

### 6.4 입력 검증 예시 (에러)

| 입력 | 코드 | boundary 출력 |
|------|------|---------------|
| `meter:-2.5` | E003 | FR-IN-01 — 음수 거부 메시지 |
| `meter2.5` | E001 | FR-IN-02 — 형식 오류 메시지 |
| `meter:abc` | E002 | (Logic D-ERR-02 / UI 확장 시) |

### 6.5 설정 파일 (`config/units.json`)

저장소 샘플: [config/units.json](./config/units.json) (boundary 로드용; 수치 정본은 `entity/constants.py`).

```json
{
  "base_unit": "meter",
  "units": {
    "meter": 1.0,
    "feet": 3.28084,
    "yard": 1.09361
  },
  "precision": 1
}
```

---

## 7. 테스트 요구사항

### 7.1 Logic Track (D-*)

| TC ID | FR/NFR | 검증 항목 |
|-------|--------|-----------|
| D-CONV-01 | FR-05 | meter → feet |
| D-CONV-02 | FR-05 | meter → yard |
| D-CONV-03 | FR-05 | feet → meter |
| D-CONV-04 | FR-05 | yard → meter |
| D-CONV-05 | FR-06 | feet ↔ yard |
| D-CONV-06 | FR-02 | 입력 단위 제외 전 단위 |
| D-REG-01 | FR-08 | 동적 등록 후 변환 |
| D-REG-02 | FR-15 | 중복 등록 → E007 |
| D-ERR-01 | FR-11 | E001 |
| D-ERR-02 | FR-11 | E002 |
| D-ERR-03 | FR-10 | E003 |
| D-ERR-04 | FR-12 | E004 |
| D-ERR-05 | FR-13 | E005 |
| D-ERR-06 | FR-14 | E006 |
| D-LOC-01 | FR-LOC-01 | `constants` ratio SSOT (row-major, 리터럴 없음) |
| D-LOC-02 | FR-LOC-02 | `ErrorCode` E001~E007 정의 |
| D-LOC-03 | FR-LOC-03 | `BASE_UNIT == "meter"` |

파일: `tests/{entity,control}/test_d_*.py` (D-LOC-*는 주로 `tests/entity/`)

| 묶음 | ID |
|------|-----|
| 변환 | D-CONV-01 ~ 06 |
| 등록 | D-REG-01 ~ 02 |
| 에러 | D-ERR-01 ~ 06 |
| SSOT 위치 | D-LOC-01 ~ 03 |

### 7.2 UI Track (U-*)

| TC ID | FR | 검증 항목 (예시) |
|-------|-----|------------------|
| U-IN-01 | FR-IN-01, FR-10 | `meter:-2.5` → E003 메시지, exit ≠ 0 |
| U-IN-02 | FR-IN-02, FR-11 | `meter2.5` → E001 메시지, exit ≠ 0 |
| U-CLI-01 | FR-01,04 | CLI 표 출력 |
| U-FMT-01 | FR-09 | JSON 출력 |
| U-FMT-02 | FR-09 | CSV 출력 |
| U-CFG-01 | FR-07 | 설정 파일 로드 |
| U-REG-01 | FR-08 | 등록 입력 CLI |

파일: `tests/boundary/test_u_*.py` — stdin/stdout·파일 I/O Mock 허용; control·entity Domain Mock **금지**.

| 묶음 | ID |
|------|-----|
| 입력 표면화 | U-IN-01 ~ 02 |
| CLI·포맷 | U-CLI-01, U-FMT-01/02 |
| 설정·등록 | U-CFG-01, U-REG-01 |

### 7.3 TDD 게이트

| Phase | 허용 수정 | pytest 기대 |
|-------|-----------|-------------|
| RED | `tests/`만 | exit ≠ 0 (FAIL) |
| GREEN | `src/` (최소) | exit = 0 (PASS) |
| REFACTOR | `src/` (구조) | exit = 0 유지 |

---

## 8. 마일스톤

| 단계 | 산출물 | FR/NFR |
|------|--------|--------|
| M1 기본 | ECB 골격, FR-01~06, FR-10~13, FR-LOC-01~03, FR-IN-01~02 | P0 |
| M2 품질 | OCP/SRP 리팩터, D-CONV/ERR/REG/LOC·U-IN PASS | NFR-01~11 |
| M3 추가 | FR-07~09, FR-14~15, U-* | P1 |
| M4 통합 | staging merge, README 실행 가이드 정합 | 전체 |

---

## 9. 레거시·참고

| 항목 | 상태 |
|------|------|
| `UnitConverter.py` | 레거시 — boundary thin wrapper로 점진 교체 |
| `README.md` | 실행·실습 가이드 (본 PRD와 요구사항 동기화) |
| `.cursorrules` | 개발 헌법 (본 PRD NFR과 정합) |
| `.cursor/skills/unit-converter-tdd/reference.md` | D-* TC ID SSOT (D-LOC 포함) |
| `.cursor/commands/` | `/red-test-plan` ~ `/refactor-safe` TDD 워크플로 |

---

## 10. 변경 이력

| 버전 | 일자 | 변경 |
|------|------|------|
| 0.1.0 | 2026-06-05 | 초안 — README·ECB·Dual-Track·E001~E007 통합 |
| 0.2.0 | 2026-06-05 | FR-LOC/FR-IN, D-LOC/U-IN TC, NFR-10~11, README·TDD 커맨드 정합 |
