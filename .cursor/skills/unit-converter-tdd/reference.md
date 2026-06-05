# D-* Logic Track TC ID

| ID | 검증 항목 |
|----|-----------|
| D-CONV-01 | meter → feet 변환 정확도 |
| D-CONV-02 | meter → yard 변환 정확도 |
| D-CONV-03 | feet → meter 역변환 |
| D-CONV-04 | yard → meter 역변환 |
| D-CONV-05 | feet ↔ yard (meter 기준 간접 변환) |
| D-CONV-06 | 입력 단위 제외, 나머지 전 단위 변환 |
| D-REG-01 | 동적 단위 등록 후 변환 가능 |
| D-REG-02 | 중복 단위 등록 → E007 |
| D-ERR-01 | 형식 오류 → E001 |
| D-ERR-02 | 숫자 변환 실패 → E002 |
| D-ERR-03 | 음수 입력 → E003 |
| D-ERR-04 | 미등록 단위 → E004 |
| D-ERR-05 | 빈 단위명 → E005 |
| D-ERR-06 | 등록 문법 오류 → E006 |
| D-LOC-01 | 변환 비율 `entity/constants.py` SSOT |
| D-LOC-02 | `ErrorCode` E001~E007 `entity/exceptions.py` SSOT |
| D-LOC-03 | `BASE_UNIT == "meter"` SSOT |

# U-* UI Track TC ID (PRD §7.2)

| ID | 검증 항목 |
|----|-----------|
| U-IN-01 | 음수 입력 → E003 CLI 메시지 |
| U-IN-02 | `:` 없음 → E001 CLI 메시지 |
| U-CLI-01 | CLI 표 출력 |
| U-FMT-01 | JSON 출력 |
| U-FMT-02 | CSV 출력 |
| U-CFG-01 | 설정 파일 로드 |
| U-REG-01 | 등록 입력 CLI |
