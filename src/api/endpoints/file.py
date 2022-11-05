from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from core.db import get_async_session
from core.user import current_user
from crud.file import file_download, file_search, upload_new_file
from models.file import FileRegister
from schemas.file import FileCreate, FileDB, FileDownload, FileSearch
from schemas.user import UserDB
from services.file import get_file_links_by_user

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
        file_schema: FileDownload = Depends(),
        session: AsyncSession = Depends(get_async_session),
        user: UserDB = Depends(current_user)
) -> File:
    """
    Загрузка файла из хранилища.
    Допускается загрузка через указание полного пути до файла
    или UUID записи.
    Для загрузки единичного файла присутствует опция загрузки
    в виде zip-архива.
    Загрузка каталога осуществляется только полному пути и
    скачивание происходит только в виде zip-архива.
    """
    file = await file_download(
        file_schema,
        session,
        user
    )
    return file


@router.get('/list',
            response_model=list[FileDB],
            response_model_exclude={
                'user_id'
            })
async def get_all_files_by_user(
        session: AsyncSession = Depends(get_async_session),
        user: UserDB = Depends(current_user)
) -> list[FileRegister]:
    """Получение списка всех файлов пользователя"""
    all_files = await get_file_links_by_user(session, user)
    return all_files


@router.post('/search',
             response_model=list[FileDB],
             response_model_exclude={
                 'user_id'
             })
async def search_files_by_user_param(
        file_schema: FileSearch,
        session: AsyncSession = Depends(get_async_session),
        user: UserDB = Depends(current_user)
) -> list[FileRegister]:
    """
    Поиск файлов пользователя с учетом параметров:
    search_query - по вхождению строки в имя файла
    options {
            path - по расположению (необязательный параметр
                                    если не указывать, то поиск
                                    будет по корневому каталогу)
            extension - по расширению файла (необязательный параметр)
            order_by - сортировка по полю
                        file_name - по названию файла, default
                        create_date - по дате создания
                        path - по пути
                        file_size - по размеру файла
            limit - количество выводимых записей, default = 10
            }
    """
    file_data = file_schema.dict()
    search_query, options = file_data.values()
    return await file_search(
        search_query,
        options,
        session,
        user
    )
