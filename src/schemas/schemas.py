from pydantic import BaseModel


class UserRegister(BaseModel):
    username: str
    email: str
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


class UserInfo(BaseModel):
    username: str
    email: str


class UserVerificationRequest(BaseModel):
    user_name: str
    verification_code: str


class BaseUpdateRequest(BaseModel):
    pass


class UpdateUsernameRequest(BaseUpdateRequest):
    username: str


class UpdateEmailRequest(BaseUpdateRequest):
    email: str


class UpdatePasswordRequest(BaseUpdateRequest):
    current_password: str
    new_password: str


class AccessToken(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str or None = None


class AuthenticationError:
    USER_NOT_FOUND = "User not found"
    WRONG_PASSWORD = "Incorrect password"
