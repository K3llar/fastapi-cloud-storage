import uuid
from http import HTTPStatus

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import UploadFile, HTTPException
from fastapi.responses import FileResponse, StreamingResponse

import src.services.constants as cst
from src.models import FileRegister
from src.schemas.file import FileCreate, FileSearch
from src.schemas.user import UserDB

from src.services.file import (upload,
                               download_from_direct_path,
                               download_from_uuid)


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
        session: AsyncSession,
        user: UserDB,
) -> FileResponse | StreamingResponse:
    file_data = file_schema.dict()
    path = file_data.get('path')
    try:
        uuid.UUID(path)
        file = await download_from_uuid(file_data, user, session)
    except ValueError:
        file = await download_from_direct_path(file_data, user)
    return file


# async def file_search(
#         search_query: str,
#         options: dict,
#         session: AsyncSession,
#         user: UserDB,
# ) -> list[FileRegister]:
#     files = await session.execute(
#         select(FileRegister).where(
#             FileRegister.user_id == user.id
#         ).where(
#             FileRegister.path.startswith(options.get('path'))
#         )
#     )
#     files = files.scalars().all()
#     return files


async def file_search(
        search_query: str,
        options: dict,
        session: AsyncSession,
        user: UserDB,
) -> list[FileRegister]:
    files = await session.execute(
        select(FileRegister).where(
            FileRegister.user_id == user.id,
            FileRegister.path.startswith(options.get('path')),
            FileRegister.file_name.endswith(options.get('extension'))
        ).filter(FileRegister.file_name.contains(search_query)
                 ).limit(options.get('limit')
                         ).order_by(options.get('order_by')))
    files = files.scalars().all()
    return files
