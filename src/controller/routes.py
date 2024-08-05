from fastapi import APIRouter

from .auth_controller import auth_router
from .crud_controller import crud_router

app = APIRouter()

app.include_router(auth_router)

app.include_router(crud_router)
