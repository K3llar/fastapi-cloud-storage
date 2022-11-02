import os
from http import HTTPStatus

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import UploadFile, HTTPException
from fastapi.responses import FileResponse

import src.services.constants as cst
from src.models.file import FileRegister
from src.schemas.file import FileCreate
from src.schemas.user import UserDB

from src.services.file import upload, download


async def upload_new_file(
        file_schema: FileCreate,
        file: UploadFile,
        session: AsyncSession,
        user: UserDB
) -> FileRegister:
    if file:
        new_file_data = file_schema.dict()
        file_size = await upload(file, new_file_data['path'], user.id)
        new_file_data['user_id'] = user.id
        new_file_data['file_name'] = file.filename.replace(' ', '-')
        new_file_data['path'] += new_file_data['file_name']
        new_file_data['file_size'] = file_size
    else:
        raise HTTPException(
            status_code=HTTPStatus.EXPECTATION_FAILED,
            detail=cst.INPUT_FILE
        )
    db_file = FileRegister(**new_file_data)
    session.add(db_file)
    await session.commit()
    await session.refresh(db_file)
    return db_file


async def file_download(
        file_schema: FileCreate,
        user: UserDB
):
    file_data = file_schema.dict()
    file = await download(file_data['path'], user.id)
    return file
