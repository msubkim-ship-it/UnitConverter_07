# TDD RED — 실패 테스트 먼저

UnitConverter_07 Dual-Track TDD **RED 단계**만 수행한다. `.cursorrules`와 `.cursor/skills/unit-converter-tdd/`를 따른다.

## 필수 선언

**응답 첫 줄**에 반드시 선언한다:

```
Phase: red | Layer: entity|control|boundary | Track: Logic|UI
```

예: `Phase: red | Layer: entity | Track: Logic`

## 절차

1. **ID 확인** — `.cursor/skills/unit-converter-tdd/reference.md`에서 대상 TC ID(D-* / U-*)를 확인·명시한다. Logic→`D-*`+`test_d_*`, UI→`U-*`+`test_u_*`.
2. **브랜치** — `red` 브랜치인지 확인한다. 아니면 전환을 제안하고 진행하지 않는다.
3. **AAA 테스트 작성** — `tests/{layer}/`에만 파일 추가·수정한다.
   - **Arrange**: SSOT(`entity/constants.py` 참조 예정) 기준 입력값 준비. MagicConstant 리터럴 산재 금지.
   - **Act**: 아직 없거나 stub인 src API를 호출 (import는 RED에서 허용, **구현은 green**).
   - **Assert**: FR/NFR·E001~E007 중 해당 TC가 검증할 **실패 조건**을 명확히 assert. Logic Track은 예외 **코드(E00x)** assert.
4. **TC 메타** — docstring 또는 `@pytest.mark`에 TC ID 표기 (예: `D-CONV-01`).
5. **pytest FAIL** — 아래 예시 명령으로 실행하고 **exit code ≠ 0**을 확인한다.
6. **보고** — 하단 보고 항목을 작성한다.

## pytest 예시 (bash)

```bash
# 대상 TC 파일만 (RED 확인)
pytest tests/entity/test_d_conversion.py -v

# Layer 전체 수집 확인
pytest tests/entity/ --collect-only -q

# UI Track boundary 예시
pytest tests/boundary/test_u_cli.py -v
```

**RED 게이트:** 최소 1개 이상 **FAILED** 또는 **ERROR**(미구현 import). exit code = 0이면 RED 미완 — assert 강화 또는 대상 API 미연결을 점검한다.

## 보고

작업 종료 시 한국어로 보고한다:

| 항목 | 내용 |
|------|------|
| 선언 | `Phase: red \| Layer: … \| Track: …` |
| 테스트 ID | 추가한 D-* / U-* 목록 |
| FAIL 요약 | pytest 출력에서 FAILED/ERROR TC명·원인 1~2줄 |
| 변경 파일 | `tests/` 하위 경로만 (src/ 변경 없음 확인) |
| pytest | 실행 명령·exit code |
| 다음 | GREEN 대상 TC ID·Layer |

## 금지

- `src/` **수정·생성** (구현은 GREEN)
- Logic Track(entity/control)에서 **Domain Mock** — `MagicMock`, `patch` on UnitRegistry/ConversionService 등
- **assert 완화·삭제**, `@pytest.mark.skip`, `@pytest.mark.xfail`, `NotImplementedError` stub으로 통과시키기
- `@pytest.mark.skip` 없는 GREEN 코드 선행 작성
- Golden Master(`tests/**/golden/**`) 무단 생성·갱신
- **git commit** (사용자 명시 요청 없이)
