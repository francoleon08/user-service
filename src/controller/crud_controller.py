from fastapi import APIRouter, Depends, HTTPException, status

from ..auth.jwt_handler import get_current_user, check_authorization_user
from ..model import models
from ..schemas import schemas
from ..service import services

crud_router = APIRouter()


@crud_router.get("/api/user/{user_id}", status_code=status.HTTP_200_OK, response_model=schemas.UserInfo)
async def get_user_info_by_id(user_id: int, current_user: models.User = Depends(get_current_user)):
    check_authorization_user(current_user, user_id)
    user = services.get_user_by_id(user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID={user_id} not found."
        )
    return schemas.UserInfo(
        username=user.username,
        email=user.email
    )


@crud_router.put("/api/user/{user_id}/username", status_code=status.HTTP_200_OK)
async def update_username_by_id(user_id: int,
                                update_username: schemas.UpdateUsernameRequest,
                                current_user: models.User = Depends(get_current_user)):
    return update_user_field(
        user_id,
        update_username,
        services.update_username_by_id,
        current_user
    )


@crud_router.put("/api/user/{user_id}/email", status_code=status.HTTP_200_OK)
async def update_email_by_id(user_id: int,
                             update_email: schemas.UpdateEmailRequest,
                             current_user: models.User = Depends(get_current_user)):
    return update_user_field(
        user_id,
        update_email,
        services.update_email_by_id,
        current_user
    )


@crud_router.put("/api/user/{user_id}/password", status_code=status.HTTP_200_OK)
async def update_password_by_id(user_id: int,
                                update_password: schemas.UpdatePasswordRequest,
                                current_user: models.User = Depends(get_current_user)):
    return update_user_field(
        user_id,
        update_password,
        services.update_password_by_id,
        current_user
    )


def update_user_field(user_id: int,
                      field_update: schemas.BaseUpdateRequest,
                      update_function,
                      current_user: models.User):
    check_authorization_user(current_user, user_id)
    try:
        updated_user = update_function(user_id, field_update)
        if updated_user:
            return schemas.UserInfo(
                username=updated_user.username,
                email=updated_user.email
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with ID {user_id} not found."
            )
    except Exception as e:
        raise e


@crud_router.delete("/api/user/{user_id}", status_code=status.HTTP_200_OK)
async def delete_user_by_id(user_id: int,
                            current_user: models.User = Depends(get_current_user)):
    check_authorization_user(current_user, user_id)
    if services.delete_user(user_id) is not None:
        return {"message": "User deleted successfully"}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User not found"
    )
