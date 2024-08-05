from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from fastapi.security import OAuth2PasswordRequestForm
from ..schemas import schemas
from ..service import services

auth_router = APIRouter()


@auth_router.post("/api/login", status_code=status.HTTP_200_OK)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        return services.login_for_access_token(form_data)
    except HTTPException as e:
        raise e


@auth_router.post("/api/register", status_code=status.HTTP_201_CREATED)
async def register_user(user: schemas.UserRegister, background_tasks: BackgroundTasks):
    try:
        result = await services.register_user(user, background_tasks)
        if result:
            return result
    except Exception as e:
        raise e


@auth_router.put("/api/verify", status_code=status.HTTP_200_OK)
def verify_user_endpoint(verification_request: schemas.UserVerificationRequest):
    try:
        success = services.verify_user(verification_request.user_name, verification_request.verification_code)
        if success:
            return {"message": "Verified successfully"}
    except HTTPException as e:
        raise e
