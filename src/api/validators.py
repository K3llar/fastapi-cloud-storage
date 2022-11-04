import os

from fastapi import HTTPException

from http import HTTPStatus

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.file import FileRegister

import src.services.constants as cst
from src.schemas.user import UserDB


async def check_file_exist(path: str):
    if os.path.exists(path):
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail=cst.EXIST_FILE.format(
                path
            )
        )


async def check_file_owner(
        file_obj: FileRegister,
        user: UserDB
) -> None:
    if user:
        if file_obj.user_id != user.id:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=cst.NOT_FOUND.format(file_obj.file_id)
            )
    else:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=cst.NOT_FOUND.format(file_obj.file_id)
        )
