from fastapi import APIRouter
from . import user_router, admin_router


api_router = APIRouter()


api_router.include_router(user_router.router, tags=['User'], prefix='/user')
api_router.include_router(admin_router.router, tags=['Admin'], prefix='/admin')

