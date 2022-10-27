from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.ext.asyncio import AsyncSession

# from src.core.db import get_async_session
from src.core.user import auth_backend, current_user, fastapi_users
# from src.crud.user import get_links_by_user
# from src.models import Link
# from src.schemas.link import LinkDB
# from src.schemas.user import UserDB

router = APIRouter()

router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix='/auth/jwt',
    tags=['auth'],
)
router.include_router(
    fastapi_users.get_register_router(),
    prefix='/auth',
    tags=['auth'],
)
router.include_router(
    fastapi_users.get_users_router(),
    prefix='/users',
    tags=['users'],
)


# @router.get(
#     '/users/me/my_links',
#     tags=['users'],
#     response_model=list[LinkDB],
#     response_model_exclude={
#         'link_id',
#         'user_id'
#     }
# )
# async def get_my_links(
#         session: AsyncSession = Depends(get_async_session),
#         user: UserDB = Depends(current_user)
# ) -> list[Link]:
#     """Возвращает все актуальные записи пользователя"""
#     all_links = await get_links_by_user(session, user)
#     return all_links


@router.delete(
    '/users/{id}',
    tags=['users'],
    deprecated=True
)
def delete_user(id: str):
    """Не используйте удаление, деактивируйте пользователей."""
    raise HTTPException(
        status_code=HTTPStatus.METHOD_NOT_ALLOWED,
        detail="Удаление пользователей запрещено!"
    )
