# Golden Master — UI 출력 스냅샷 (boundary)

**UI Track(boundary)** CLI·Formatter 출력을 Golden Master로 검증한다.  
경로: `tests/boundary/golden/` (또는 `tests/**/golden/**`).  
**선행:** `/green-minimal`로 U-* 또는 표 출력 TC 통과 후.

## 필수 선언

```
Phase: green|refactor | Layer: boundary | Track: UI
```

## 절차

1. **대상 U-*** — `U-CLI-01`, `U-FMT-01`, `U-FMT-02` 등 PRD §7.2.
2. **브랜치** — `green` 또는 `refactoring` (출력 불변 전제).
3. **테스트 작성** — `tests/boundary/test_u_*.py`
   - stdin/stdout `capsys` 또는 `tmp_path` Mock **허용**
   - control·entity **Mock 금지** — 실제 boundary→control→entity 경로
4. **Golden 파일**
   - 기대 출력: `tests/boundary/golden/{tc_id}.txt` (또는 `.json`/`.csv`)
   - 테스트: 실제 출력 vs golden `diff` 비교
5. **신규·갱신 규칙**
   - **사용자 명시 승인 전** golden 파일 쓰기·덮어쓰기 **금지**
   - Agent는 **diff만 제시**하고 승인 요청
   - 승인 후에만 golden 생성/갱신
6. **pytest** — `pytest tests/boundary/test_u_*.py -v`

## 예시 구조

```text
tests/boundary/
├── test_u_cli.py
└── golden/
    ├── U-CLI-01_table.txt
    ├── U-FMT-01_json.json
    └── U-FMT-02_csv.csv
```

## 보고

| 항목 | 내용 |
|------|------|
| U-* TC | 대상 ID |
| golden | 신규/기존/diff 요약 |
| 승인 | 사용자 승인 여부 |
| pytest | exit code |
| 다음 | `/refactor-smell` |

## 금지

- 사용자 승인 없이 `golden/**` 생성·수정
- control·entity Mock으로 boundary 통과
- Logic Track `test_d_*`에 golden 혼용
- **git commit** (사용자 요청 없이)
