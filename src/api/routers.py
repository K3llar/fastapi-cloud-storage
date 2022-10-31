from fastapi import APIRouter

from src.api.endpoints import user_router, file_router

main_router = APIRouter()
main_router.include_router(user_router)
main_router.include_router(file_router)
