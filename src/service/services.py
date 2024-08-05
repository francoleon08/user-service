import os
import secrets
import string
from datetime import datetime, timedelta
from typing import Union, Tuple

from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status, BackgroundTasks
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt
from passlib.context import CryptContext

from ..model import models
from ..schemas import schemas
from ..utils import utils_email
from ..database.database import session

load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES'))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def login_for_access_token(from_data: OAuth2PasswordRequestForm = Depends()):
    user, error = authenticate_user(from_data.username, from_data.password)
    if error:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=error,
                            headers={"WWW-Authenticate": "Bearer"})

    user_verified: models.UserVerification = get_user_verification(user)
    if user_verified.is_verified is False:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="User not verified",
                            headers={"WWW-Authenticate": "Bearer"})
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}


def authenticate_user(username: str, current_password: str) -> Union[Tuple[None, str], Tuple[models.User, None]]:
    user = get_user_by_username(username)
    if not user:
        return None, schemas.AuthenticationError.USER_NOT_FOUND
    if not verify_password(current_password, user.password):
        return None, schemas.AuthenticationError.WRONG_PASSWORD
    return user, None


def get_user_by_username(username) -> models.User or None:
    return session.query(models.User).filter(username == models.User.username).first()


def get_user_verification(user: models.User) -> models.UserVerification or None:
    return session.query(models.UserVerification).filter(user.id == models.UserVerification.user_id).first()


def verify_password(current_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(current_password, hashed_password)


def create_access_token(data: dict, expires_delta: timedelta or None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def register_user(user: schemas.UserRegister, background_tasks: BackgroundTasks):
    user_register = register_user_in_database(user)
    verification_code = register_verification_in_database(user_register)

    background_tasks.add_task(
        utils_email.send_verification_email,
        user_register.email,
        user_register.username,
        verification_code)

    return schemas.UserInfo(
        username=user_register.username,
        email=user_register.email
    )


def register_user_in_database(user):
    hashed_password = hash_password(user.password)
    user_register = models.User(username=user.username, email=user.email, password=hashed_password)
    session.add(user_register)
    session.commit()
    session.refresh(user_register)
    return user_register


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def register_verification_in_database(user_register):
    verification = models.UserVerification(
        user_id=user_register.id,
        verification_code=generate_verification_code()
    )
    session.add(verification)
    session.commit()
    session.refresh(verification)
    return verification.verification_code


def generate_verification_code() -> str:
    characters = string.ascii_letters + string.digits
    return ''.join(secrets.choice(characters) for _ in range(6))


def verify_user(user_name: str, verification_code: str):
    user_verification = get_user_verification(get_user_by_username(user_name))
    if user_verification is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Verification code not found"
        )
    if user_verification.verification_code != verification_code:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid verification code"
        )
    if user_verification.is_verified:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User is already verified"
        )
    user_verification.is_verified = True
    session.commit()
    return True


def get_user_by_id(user_id: int) -> models.User or None:
    return session.query(models.User).filter(user_id == models.User.id).first()


def update_username_by_id(user_id: int, username_update: schemas.UpdateUsernameRequest) -> models.User or None:
    user = get_user_by_id(user_id)
    if user is None:
        return None
    if user.username == username_update.username:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username is the same"
        )
    user.username = username_update.username
    session.commit()
    session.refresh(user)
    return user


def update_email_by_id(user_id: int, email_update: schemas.UpdateEmailRequest) -> models.User or None:
    user = get_user_by_id(user_id)
    if user is None:
        return None
    if user.email == email_update.email:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email is the same"
        )
    user.email = email_update.email
    session.commit()
    session.refresh(user)
    return user


def update_password_by_id(user_id: int, update_password: schemas.UpdatePasswordRequest) -> models.User or None:
    user = get_user_by_id(user_id)
    if user is None:
        return None
    if not verify_password(update_password.current_password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Wrong password"
        )
    user.password = hash_password(update_password.new_password)
    session.commit()
    session.refresh(user)
    return user


def delete_user(user_id: int):
    user = get_user_by_id(user_id)
    if user is None:
        return None
    user_verification = get_user_verification(user)
    session.delete(user_verification)
    session.delete(user)
    session.commit()
    return user
