from enum import IntEnum

from pydantic import BaseModel


class ResponseErrorCode(IntEnum):
    MISSING_TOKEN = 10000
    INVALID_TOKEN = 10001
    INVALID_TOKEN_TYPE = 10002
    TOKEN_EXPIRED = 10003

    INVALID_USER_CREDENTIALS = 10100
    USER_ALREADY_EXISTS = 10101
    USER_ALREADY_VERIFIED = 10102
    USER_NOT_FOUND = 10103

    UNSUPPORTED_FILE_TYPE = 10200

    CATEGORY_NOT_FOUND = 10300
    SUBCATEGORY_NOT_FOUND = 10301
    POST_NOT_FOUND = 10302
    MISSING_ARGUMENTS = 10303


class ResponseError(BaseModel):
    code: ResponseErrorCode
