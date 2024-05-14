from fastapi import HTTPException as BaseHTTPException, status

from src.api.enums import ResponseError, ResponseErrorCode


class HTTPException(BaseHTTPException):
    def __init__(self, status_code: int, detail: ResponseError):
        super().__init__(status_code=status_code, detail=detail.model_dump())


missing_token = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail=ResponseError(code=ResponseErrorCode.MISSING_TOKEN)
)

invalid_credentials = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail=ResponseError(code=ResponseErrorCode.INVALID_USER_CREDENTIALS)
)

duplicate_user = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail=ResponseError(code=ResponseErrorCode.USER_ALREADY_EXISTS)
)

invalid_token = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail=ResponseError(code=ResponseErrorCode.INVALID_TOKEN)
)

invalid_token_type = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail=ResponseError(code=ResponseErrorCode.INVALID_TOKEN_TYPE)
)

expired_token = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail=ResponseError(code=ResponseErrorCode.TOKEN_EXPIRED)
)

user_not_found = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail=ResponseError(code=ResponseErrorCode.USER_NOT_FOUND)
)

user_already_verified = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail=ResponseError(code=ResponseErrorCode.USER_ALREADY_VERIFIED)
)

unsupported_file_type = HTTPException(
    status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
    detail=ResponseError(code=ResponseErrorCode.UNSUPPORTED_FILE_TYPE)
)

incorrect_document_file = HTTPException(
    status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
    detail=ResponseError(code=ResponseErrorCode.INCORRECT_DOCUMENT_FILE)
)

category_not_found = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail=ResponseError(code=ResponseErrorCode.CATEGORY_NOT_FOUND)
)

subcategory_not_found = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail=ResponseError(code=ResponseErrorCode.SUBCATEGORY_NOT_FOUND)
)

post_not_found = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail=ResponseError(code=ResponseErrorCode.POST_NOT_FOUND)
)

missing_arguments = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail=ResponseError(code=ResponseErrorCode.MISSING_ARGUMENTS)
)