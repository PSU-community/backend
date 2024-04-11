from fastapi import HTTPException, status

invalid_credentials = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid email or password"
)

duplicate_user = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="User with this email already exists"
)

invalid_token_type = HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token type",
        )