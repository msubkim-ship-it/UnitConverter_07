"""Map ErrorCode SSOT to user-facing messages (boundary only)."""

from entity.exceptions import ErrorCode

ERROR_MESSAGES: dict[ErrorCode, str] = {
    ErrorCode.E001: "형식 오류: `단위:값` 형식이 필요합니다. (예: meter:2.5)",
    ErrorCode.E002: "숫자 변환 실패",
    ErrorCode.E003: "음수는 허용되지 않습니다.",
    ErrorCode.E004: "미등록 단위입니다.",
    ErrorCode.E005: "단위명이 비어 있습니다.",
    ErrorCode.E006: "등록 문법 오류: `1 cubit = 0.4572 meter` 형식이 필요합니다.",
    ErrorCode.E007: "이미 등록된 단위입니다.",
}


def message_for(code: ErrorCode) -> str:
    return ERROR_MESSAGES[code]
