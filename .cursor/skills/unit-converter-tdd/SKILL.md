---
name: unit-converter-tdd
description: UnitConverter_07 Dual-Track TDD·ECB 개발 시 Agent가 따를 절차. UnitConverter, ECB, red/green/refactoring, D-/U- TC, entity/control/boundary 작업 시 적용.
---

# UnitConverter Dual-Track TDD Skill

`.cursorrules` 헌법을 따르며, 본 Skill은 **실행 절차**를 정의한다. D-* TC ID 목록은 [reference.md](reference.md) 참조.

## 언제 이 Skill을 켜는가

다음 중 **하나라도** 해당하면 본 Skill을 읽고 절차를 따른다.

- UnitConverter_07에서 **spec / red / green / refactoring** 브랜치 작업
- `tests/**/test_d_*` 또는 `test_u_*` TC 작성·구현·리팩터
- `src/entity`, `src/control`, `src/boundary` 코드 변경
- 사용자가 **TDD**, **Dual-Track**, **ECB**, **RED/GREEN** 키워드 사용
- pytest 실패/통과 게이트 확인 또는 Test/Review Loop 수행

**켜지 않는 경우:** README만 수정, git remote 설정, Harness 골격 외 인프라만 다룰 때.

---

## 응답 선언 (매 턴)

```
[Phase: RED|GREEN|REFACTOR | Layer: entity|control|boundary | Track: Logic|UI]
```

---

## Logic Track vs UI Track

| 구분 | Logic Track | UI Track |
|------|-------------|----------|
| 대상 레이어 | entity, control | boundary |
| TC ID | `D-*` | `U-*` |
| 파일 | `tests/{layer}/test_d_*.py` | `tests/{layer}/test_u_*.py` |
| Mock | **금지** — 실제 domain 객체·변환 로직 | **허용** — stdin/stdout, 파일 I/O, tmp_path |
| 금지 Mock | `MagicMock`, `patch` on ConversionService/UnitRegistry/Unit | control·entity Mock으로 boundary 테스트 통과 |
| import | tests/entity→src/entity / tests/control→src/control+entity / tests/boundary→src/* | 동일 |

---

## ECB · Mock · E001~E007

### ECB import (단방향)

```
boundary → control → entity
```

| 레이어 | import 허용 | import 금지 |
|--------|-------------|-------------|
| entity | stdlib만 | control, boundary, I/O |
| control | entity | boundary |
| boundary | control, entity | — |

MagicConstant(3.28084, 1.09361 등)는 `entity/constants.py` SSOT만 참조. 테스트·코드에 리터럴 산재 금지.

### 에러 코드 SSOT (`entity/exceptions.py`)

| 코드 | 의미 | raise 레이어 | boundary 역할 |
|------|------|--------------|---------------|
| E001 | 형식 오류 (콜론 없음·빈 입력) | control | 사용자 메시지 출력 |
| E002 | 숫자 변환 실패 | control | 사용자 메시지 출력 |
| E003 | 음수 값 | entity/control | 사용자 메시지 출력 |
| E004 | 미등록 단위 | control | 사용자 메시지 출력 |
| E005 | 빈 단위명 | control | 사용자 메시지 출력 |
| E006 | 등록 문법 오류 (`1 cubit = …`) | control | 사용자 메시지 출력 |
| E007 | 중복 단위·설정 충돌 | control | 사용자 메시지 출력 |

- Logic TC: 예외 **코드(E00x)** assert — 메시지 문자열 하드코딩 금지
- UI TC: boundary가 코드→메시지 변환 결과 assert
- Golden Master(`tests/boundary/golden/**`) 갱신: **U-* GREEN 후**, **사용자 명시 승인 전까지 diff만 제시**, Agent가 단독 재생성 금지. Logic Track `test_d_*`에 golden **혼용 금지**.

---

## Harness — pytest 수집 규칙

| 규칙 | 내용 |
|------|------|
| **`tests/{layer}/__init__.py` 금지** | `entity` / `control` / `boundary` 테스트 디렉터리에 `__init__.py`를 두지 않는다 — `src/` 패키지 import shadowing 방지 |
| 허용 헬퍼 | `tests/conftest.py`, `tests/_approval.py` (tests 루트) |
| Golden 경로 | `tests/boundary/golden/` — boundary `test_u_*` 전용 |
| Golden 시점 | `/green-minimal`로 U-* PASS **후** `/golden-master` |

---

## RED Phase (5~7단계)

1. **선언** — Phase/Layer/Track·대상 TC ID( reference.md ) 명시
2. **브랜치 확인** — `red` 브랜치인지 확인; 아니면 사용자에게 전환 제안
3. **TC 설계** — FR/NFR·E001~E007 중 이번 TC가 검증할 항목 1줄 기술
4. **파일 생성** — `tests/{layer}/test_d_*` 또는 `test_u_*` 에 **실패하는 assert**만 작성
5. **금지 준수** — `src/` 수정 금지, skip/xfail/NotImplementedError stub 금지, Mock은 Track 규칙 따름
6. **pytest 실행** — `pytest tests/{layer}/test_d_<file>.py -v` (또는 test_u_)
7. **RED 확인** — exit code ≠ 0, 실패 TC ID·원인을 완료 보고에 기록

---

## GREEN Phase (5~7단계)

1. **선언** — Phase/Layer/Track·통과 목표 TC ID 명시
2. **브랜치 확인** — `green` 브랜치(또는 red→green 전환 후)
3. **최소 구현** — 실패 TC를 통과시키는 **최소** 코드만 `src/{layer}/` 에 추가
4. **ECB·SSOT** — import 방향·constants 참조·E00x raise 위치 준수
5. **금지 준수** — TC assert 완화·삭제·skip/xfail 금지; 요청 범위 밖 기능 추가 금지
6. **pytest 실행** — `pytest tests/{layer}/ -v` → Layer 전체, 이후 `pytest -v` (전체)
7. **GREEN 확인** — exit code = 0; 통과 TC 목록을 완료 보고에 기록

---

## REFACTOR Phase (5~7단계)

1. **선언** — Phase/Layer/Track·리팩터 목표(중복 제거·SRP·OCP) 명시
2. **브랜치 확인** — `refactoring` 브랜치
3. **구조 개선** — `src/` 만 수정; 동작 변경 없이 가독성·확장성 개선
4. **TC 동결** — TC 추가·삭제·assert 변경 **금지** (동작 동일성 유지)
5. **ECB 재검증** — import 역방향·MagicConstant 산재 없음 확인
6. **pytest 실행** — `pytest -v` 전체; REFACTOR 전후 결과 동일해야 함
7. **REFACTOR 확인** — exit code = 0; 변경 요약·PRD(OCP/SRP) 부합 여부 보고

---

## Test/Review Loop — pytest 실행 시점

| 시점 | 명령 | 기대 결과 |
|------|------|-----------|
| RED 직후 | `pytest tests/{layer}/test_d_<target>.py -v` | **FAILED** (exit ≠ 0) |
| RED 마무리 | `pytest tests/{layer}/ -v --collect-only` | 새 TC 수집 확인 |
| GREEN Layer 완료 | `pytest tests/{layer}/ -v` | **PASSED** |
| GREEN 마무리 | `pytest -v` | **전체 PASSED** |
| REFACTOR 중 | `pytest -v` | 매 수정 후 **PASSED** 유지 |
| staging merge 전 | `pytest -v` + PRD·E001~E007 대조 | **전체 PASSED** + Review 체크리스트 |
| Golden Master 비교 | `pytest tests/boundary/test_u_* -v` | diff 시 승인 대기 |

Review Loop 순서: **RED FAIL 확인 → GREEN PASS → PRD/에러코드 대조 → REFACTOR PASS → staging 전체 PASS**

---

## 완료 보고 항목

작업 종료 시 아래를 한국어로 보고한다.

1. **선언** — `[Phase | Layer | Track]`
2. **브랜치** — 현재 브랜치명
3. **TC** — 추가/수정한 TC ID 목록 (D-* / U-*)
4. **pytest** — 실행 명령·exit code·FAILED/PASSED 요약
5. **변경 파일** — `tests/` / `src/` 경로 목록
6. **ECB** — import 위반·SSOT 위반 여부 (없으면 "없음")
7. **E00x** — 새로 다룬 에러 코드
8. **미완** — 다음 Phase·Layer·TC ID

---

## 금지 사항 (TDD 게이트)

- assert 완화·삭제, `@pytest.mark.skip`, `@pytest.mark.xfail` 로 green 만들기
- red에서 `src/` 편집, spec에서 구현 본문 작성
- Logic Track domain Mock, 테스트·코드에 MagicConstant 리터럴 산재
- Golden Master 무단 갱신, **git commit** (사용자 요청 없이)

---

## 관련 파일

- 헌법: `.cursorrules`
- D-* TC ID: [reference.md](reference.md)
- Harness: `pyproject.toml`, `tests/`, `src/`
