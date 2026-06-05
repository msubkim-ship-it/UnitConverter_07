# GREEN Minimal — 최소 구현으로 테스트 통과

RED에서 실패한 TC를 **최소 `src/` 구현**으로 통과시킨다.  
ECB: `boundary → control → entity`. **다음:** UI 출력은 `/golden-master`, 구조 개선은 `/refactor-smell`.

## 필수 선언

```
Phase: green | Layer: entity|control|boundary | Track: Logic|UI
```

## 절차

1. **대상 TC** — RED FAIL 목록·TC ID 명시.
2. **브랜치** — `green` (또는 `red`에서 `green` 전환 제안 후 진행).
3. **Layer 순서** — **entity → control → boundary** (의존 방향).
   - entity: `constants.py`, `exceptions.py`, `Unit`, 변환 규칙
   - control: `UnitRegistry`, `ConversionService`, 검증
   - boundary: Parser, Formatter, CLI (UI TC일 때)
4. **최소 구현** — RED TC 통과에 **필요한 코드만**. 요청 밖 FR 추가 금지.
5. **SSOT** — `3.28084`, `1.09361` → `entity/constants.py`만. 테스트는 import 참조.
6. **E00x** — `entity/exceptions.py` SSOT, raise 레이어 준수.
7. **pytest PASS** — Layer → 전체.

```bash
pytest tests/entity/test_d_conversion.py -v
pytest tests/entity/ -v
pytest -v
```

**GREEN 게이트:** exit = 0.

## 보고

| 항목 | 내용 |
|------|------|
| TC ID | 통과시킨 D-* / U-* |
| 변경 파일 | `src/{layer}/` 목록 |
| ECB | import 위반 없음 |
| pytest | exit code = 0 |
| 다음 | boundary UI → `/golden-master` / smells → `/refactor-smell` |

## 금지

- TC assert 완화·삭제·skip·xfail
- Logic Track domain Mock으로 통과
- 레거시 `UnitConverter.py`에 domain 로직 추가
- **git commit** (사용자 요청 없이)
