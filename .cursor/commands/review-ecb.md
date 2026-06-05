# Review ECB — 계약 위반 리뷰 (코드 수정 금지)

UnitConverter_07 **ECB·계약** 정적 리뷰만 수행한다. **파일 수정·생성·삭제 금지.** `.cursorrules`, [PRD.md](../../PRD.md), `.cursor/skills/unit-converter-tdd/SKILL.md` 기준.

## 필수 선언

**응답 첫 줄:**

```
Phase: review | Layer: all | Track: —
```

## 절차

1. **스캔 범위** — `src/entity/`, `src/control/`, `src/boundary/`, `tests/entity/`, `tests/control/`, `tests/boundary/` (레거시 `UnitConverter.py` 포함 여부 명시)
2. **체크 4항** — 아래 계약별로 위반만 수집 (위반 없으면 `PASS`)
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

### 2. ErrorCode Enum SSOT (E001~E007)

- SSOT: `src/entity/exceptions.py`에 **`ErrorCode` Enum**(또는 동등 타입)으로 **E001~E007** 정의
- 매핑: E001 형식 · E002 숫자 · E003 음수 · E004 미등록 · E005 빈 단위 · E006 등록 문법 · E007 중복
- control/boundary는 import 후 사용·표면화만; entity 밖에 동일 코드 중복 정의 금지
- Logic TC: `ErrorCode.E00x`로 assert — 사용자 메시지 문자열 하드코딩만으로 검증 금지
- raise 레이어: [PRD §3.4](../../PRD.md) 준수 (E003 등)
- **금지 (레거시 패턴)**: `int[6]` 1-index 배열, `codes[0]` 등 0-based 에러 슬롯, 길이 6 고정 int 테이블이 Enum SSOT와 병존

### 3. MagicConstant SSOT

- 변환 비율·기준 단위명: **`src/entity/constants.py` 단일 SSOT** (정의·참조의 정본)
- `config/units.json`은 boundary **로드·주입용** 데이터; 수치를 `src/**`·`tests/**`에 **리터럴 복사** 금지
- 위반: `3.28084`, `1.09361` 등이 `constants.py` 밖에 산재; `.cursorrules`의 “JSON도 SSOT” 이중 정의
- 허용: `from entity.constants import FEET_PER_METER` 등; boundary는 로드 후 control/Registry에 주입

### 4. Logic Track Domain Mock

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
| 2 | ErrorCode Enum | FAIL | … | … | `exceptions.py`에 Enum SSOT |
| 3 | MagicConstant SSOT | FAIL | … | … | `constants.py`로 수치 일원화 |
| 4 | Logic Domain Mock | FAIL | … | … | … |

- **결과:** `PASS` | `FAIL` | `N/A` (해당 파일 없음)
- **심각도:** import 역방향·Logic Mock → **Critical** / SSOT 산재·Enum 미사용·int[6] 잔존 → **Warning**

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
