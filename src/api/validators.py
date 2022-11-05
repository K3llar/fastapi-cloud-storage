import os

from pathlib import Path

from http import HTTPStatus

from fastapi import HTTPException

import src.services.constants as cst
from src.models.file import FileRegister
from src.schemas.user import UserDB


async def check_file_exist(path: Path):
    if Path(path).exists():
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail=cst.EXIST_FILE.format(
                path
            )
        )


async def check_folder_exist(path: Path):
    if not Path(path).exists():
        Path(path).mkdir(parents=True, exist_ok=True)


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
