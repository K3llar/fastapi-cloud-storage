import datetime as dt
import os
import zipfile
from http import HTTPStatus
from io import BytesIO
from uuid import UUID

from fastapi import File, HTTPException, UploadFile
from fastapi.responses import FileResponse, StreamingResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

import src.api.validators as vld
import src.services.constants as cst
from src.models import FileRegister
from src.schemas.file import FileDownload
from src.schemas.user import UserDB


async def upload(file: UploadFile = File(...),
                 path: str = '',
                 user_id: UUID = None) -> int:
    file_path = os.getcwd() + cst.USER_FOLDER.format(user_id) + path
    try:
        os.makedirs(file_path, exist_ok=True)
    except FileExistsError:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=cst.BAD_FOLDER.format(path)
        )
    try:
        contents = file.file.read()
        file_name = file_path + file.filename.replace(' ', '-')
    except Exception:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=cst.BAD_FILE
        )
    await vld.check_file_exist(file_name)
    try:
        with open(file_name, 'wb') as f:
            f.write(contents)
    except OSError:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail=cst.BAD_W_FILE.format(file_name)
        )
    finally:
        file.file.close()
    file_size = os.stat(file_name).st_size
    return file_size


async def download_from_direct_path(
        req_data: {FileDownload},
        user: UserDB
) -> File:
    path, compression = req_data.values()
    base_folder = os.getcwd() + cst.USER_FOLDER.format(user.id)
    file_path = base_folder + path
    if not os.path.exists(file_path):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=cst.NOT_FOUND.format(path)
        )
    if os.path.isfile(file_path):
        if not compression:
            return FileResponse(path=file_path)
        return await download_zipped(
            path=path,
            base_folder=base_folder,
            file_list=[path, ]
        )
    if os.path.isdir(file_path):
        file_list = [os.path.join(dirpath, f).split(str(user.id))[1] for
                     (dirpath, dirnames, filenames) in os.walk(file_path)
                     for f in filenames]
        return await download_zipped(
            path=path,
            base_folder=base_folder,
            file_list=file_list
        )


async def download_from_uuid(
        req_data: {FileDownload},
        user: UserDB,
        session: AsyncSession
) -> File:
    obj_id, compression = req_data.values()
    base_folder = os.getcwd() + cst.USER_FOLDER.format(user.id)
    file = await get_file_by_id(obj_id, session)
    await vld.check_file_owner(file, user)
    file_path = file.path
    if compression:
        return await download_zipped(
            path=file_path,
            base_folder=base_folder,
            file_list=[file_path, ]
        )
    return FileResponse(path=base_folder + file.path)


async def get_file_by_id(
        obj_id: str,
        session: AsyncSession
) -> FileRegister:
    file = await session.execute(select(FileRegister).where(
        FileRegister.file_id == obj_id
    ))
    file = file.scalars().first()
    if not file:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=cst.NOT_FOUND.format(obj_id)
        )
    return file


async def download_zipped(path: str = 'root',
                          base_folder: str = None,
                          file_list: list = None):
    io = BytesIO()
    zip_sub_dir = '{}_{}'.format(path, dt.datetime.now())
    zip_filename = '{}.zip'.format(zip_sub_dir)
    with zipfile.ZipFile(
            io,
            mode='w',
            compression=zipfile.ZIP_DEFLATED) as zip:
        for fpath in file_list:
            zip.write(filename=base_folder + fpath, arcname=fpath)
        zip.close()
    return StreamingResponse(
        iter([io.getvalue()]),
        media_type='application/x-zip-compressed',
        headers={
            'Content-Disposition':
                'attachment;filename={}'.format(zip_filename)
        }
    )


async def get_file_links_by_user(
        session: AsyncSession,
        user: UserDB
) -> list[FileRegister]:
    all_files = await session.execute(
        select(FileRegister).where(
            FileRegister.user_id == user.id
        )
    )
    all_files = all_files.scalars().all()
    return all_files
