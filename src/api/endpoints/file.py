import os

from fastapi import APIRouter, File, UploadFile, Depends, Form
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.db import get_async_session
from src.core.user import current_user
from src.models.file import FileRegister
from src.schemas.file import FileDB, FileCreate
from src.schemas.user import UserDB

from src.crud.file import upload_new_file, file_download

router = APIRouter()


@router.post('/upload',
             response_model=FileDB,
             response_model_exclude={
                 'user_id',
             })
async def upload_file(
        file_schema: FileCreate = Depends(),
        file: UploadFile = File(...),
        session: AsyncSession = Depends(get_async_session),
        user: UserDB = Depends(current_user)
) -> FileRegister:
    """Сохранение файла в хранилище и создание записи в БД"""
    new_file = await upload_new_file(
        file_schema,
        file,
        session,
        user
    )
    return new_file


@router.post('/download')
async def download_file(
        file_schema: FileCreate = Depends(),
        user: UserDB = Depends(current_user)
) -> File:
    file = await file_download(
        file_schema,
        user
    )
    return file

# @router.post('/upload')
# async def upload(files: list[UploadFile] = File(...)):
#     path = '/storage/user/'
#     chunk_size = 1024 * 1024
#     for file in files:
#         try:
#             file_name = os.getcwd() + path + file.filename.replace(' ', '-')
#             with open(file_name, 'wb') as f:
#                 while contents := file.file.read(chunk_size):
#                     f.write(contents)
#         except Exception:
#             return {'message': 'There was an error uploading file(s)'}
#         finally:
#             file.file.close()
#     return {'message': f'Successfully uploaded {[file.filename for file in files]}'}
