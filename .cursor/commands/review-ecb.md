# Review ECB — 계약 위반 리뷰 (코드 수정 금지)

UnitConverter_07 **ECB·계약** 정적 리뷰만 수행한다. **파일 수정·생성·삭제 금지.** `.cursorrules`와 `.cursor/skills/unit-converter-tdd/SKILL.md` 기준.

## 필수 선언

**응답 첫 줄:**

```
Phase: review | Layer: all | Track: —
```

## 절차

1. **스캔 범위** — `src/entity/`, `src/control/`, `src/boundary/`, `tests/entity/`, `tests/control/`, `tests/boundary/` (레거시 `UnitConverter.py` 포함 여부 명시)
2. **체크 5항** — 아래 계약별로 위반만 수집 (위반 없으면 `PASS`)
3. **표 출력** — 하단 **리뷰 결과 표** 형식만 사용. 수정 제안은 `권고` 열에 1줄 이내
4. **요약** — 위반 건수·심각도(Critical/Warning) 2~3줄

## 체크 항목 (계약)

### 1. ECB import 방향

```
boundary → control → entity (단방향)
```

| 레이어 | 허용 | 금지 |
|--------|------|------|
| entity | stdlib | control, boundary, I/O |
| control | entity | boundary |
| boundary | control, entity | — |

tests: `tests/entity`→`src/entity` / `tests/control`→`src/control`,`src/entity` / `tests/boundary`→`src/*`

### 2. entity E001~E005

- SSOT: `src/entity/exceptions.py` (또는 entity 계약 파일)에 **E001~E005** 정의
- E001 형식 오류 · E002 숫자 실패 · E003 음수 · E004 미등록 단위 · E005 빈 단위명
- **entity**가 코드·int 값·타입 SSOT; control/boundary는 import 후 사용만
- 위반: entity 밖에 E001~E005 정의, 문자열 하드코딩만 존재, raise 레이어 불일치(E003 외 entity 전용 규칙 등)

### 3. int[6] 1-index

- entity 에러/상태 계약: **길이 6, 인덱스 1~6 사용 (1-index)**
- 매핑: `[1]=E001`, `[2]=E002`, `[3]=E003`, `[4]=E004`, `[5]=E005`, `[6]=E006` (또는 `[6]` reserved — 코드 주석·SSOT와 일치해야 함)
- **인덱스 0 사용 금지**; 0-based enum/배열 접근 금지
- 위반: `codes[0]`, `range(6)` 0~5 매핑, 길이 ≠6, E00x와 int 인덱스 불일치

### 4. MagicConstant SSOT

- 변환 비율·기준 단위: **`src/entity/constants.py` 단일 SSOT**
- `3.28084`, `1.09361` 등 리터럴이 `src/**`, `tests/**`에 **산재**하면 위반
- `config/units.json`은 boundary 로드용; 수치를 테스트/코드에 **복사** 금지
- 허용: `from entity.constants import METER_TO_FEET` 또는 SSOT re-export

### 5. Logic Track Domain Mock

- 대상: `tests/entity/test_d_*`, `tests/control/test_d_*`
- **금지**: `MagicMock`, `Mock`, `patch` on `UnitRegistry`, `ConversionService`, entity domain 클래스/함수
- **허용**: 실제 domain 객체, InMemory Registry(실 구현), 순수 입력값·상수(SSOT import)

---

## 리뷰 결과 표 (출력 형식)

위반 **0건**이면:

| # | 체크 | 결과 | 파일:줄 | 위반 내용 | 권고 |
|---|------|------|---------|-----------|------|
| — | 전체 | **PASS** | — | — | — |

위반 **1건 이상**이면 항목별 1행:

| # | 체크 | 결과 | 파일:줄 | 위반 내용 | 권고 |
|---|------|------|---------|-----------|------|
| 1 | import 방향 | FAIL | `src/entity/foo.py:3` | entity가 control import | import 제거·역할 이동 |
| 2 | E001~E005 | FAIL | … | … | … |
| 3 | int[6] 1-index | FAIL | … | … | … |
| 4 | MagicConstant SSOT | FAIL | … | … | … |
| 5 | Logic Domain Mock | FAIL | … | … | … |

- **결과:** `PASS` | `FAIL` | `N/A` (해당 파일 없음)
- **심각도:** import 역방향·Logic Mock → **Critical** / SSOT 산재·int index → **Warning**

## 보고 요약 (표 다음 2~3줄)

```
위반 N건 (Critical X / Warning Y)
PASS: … / FAIL: …
다음 조치: (코드 수정은 사용자 요청 후 별도 Phase)
```

## 금지

- **코드·테스트·설정 파일 수정** (리뷰 전용)
- pytest 실행으로 green/red 판정 (Test Loop는 `/tdd-red` 등 별도)
- 위반 없는데 스타일·리팩터 제안 나열
- **git commit**
