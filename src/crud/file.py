import os
from http import HTTPStatus

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import UploadFile, HTTPException

import src.services.constants as cst
from src.models.file import FileRegister
from src.schemas.file import FileCreate
from src.schemas.user import UserDB

from src.services.file import upload


async def upload_new_file(
        file_schema: FileCreate,
        file: UploadFile,
        session: AsyncSession,
        user: UserDB
) -> FileRegister:
    # print(file_schema)
    if file:
        new_file_data = file_schema.dict()
        await upload(file, new_file_data['path'], user.id)
        new_file_data['user_id'] = user.id
        new_file_data['file_name'] = file.filename.replace(' ', '-')
        new_file_data['path'] += new_file_data['file_name']
        new_file_data['file_size'] = file.__sizeof__()
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
