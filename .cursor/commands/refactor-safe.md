# REFACTOR Safe — 테스트 동결·안전 리팩터

`/refactor-smell` 진단 중 **선택한 항목**만 `src/`에서 구조 개선한다. **동작·TC 불변**이 최우선.

## 필수 선언

```
Phase: refactor | Layer: entity|control|boundary | Track: Logic|UI
```

## 절차

1. **대상** — `/refactor-smell` 표에서 사용자가 지정한 스멜 ID·항목만.
2. **브랜치** — `refactoring` 필수.
3. **TC 동결** — `tests/` **수정 금지** (추가·삭제·assert 변경·golden 갱신 금지).
4. **안전 리팩터** — `src/`만:
   - extract class/module (SRP)
   - Registry·Formatter Strategy (OCP)
   - constants/exceptions SSOT 정리
   - import ECB 정리
   - **동작 변경·FR 추가 금지**
5. **매 수정 후 pytest**

```bash
pytest -v
```

**REFACTOR 게이트:** exit = 0 유지, 실패 시 **즉시 롤백** 후 원인 보고.

6. **ECB 재확인** — `/review-ecb` 권장 (선택).

## 보고

| 항목 | 내용 |
|------|------|
| refactor 항목 | 스멜 # · 변경 요약 |
| 변경 파일 | `src/`만 |
| pytest | 전후 exit = 0 |
| TC 동결 | tests/ 미변경 확인 |
| 다음 | staging merge 또는 추가 smell |

## 금지

- `tests/**` 수정, golden 무단 갱신
- assert 완화·skip·xfail로 green 유지
- refactor 중 **새 기능** (FR 범위 밖)
- import 역방향 도입
- **git commit** (사용자 요청 없이)
