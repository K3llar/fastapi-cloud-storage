import os
from uuid import UUID

from http import HTTPStatus

from fastapi import File, UploadFile, HTTPException
from fastapi.responses import FileResponse

import src.services.constants as cst
import src.api.validators as vld


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
    # if os.path.exists(file_name):
    #     raise HTTPException(
    #             status_code=HTTPStatus.CONFLICT,
    #             detail=cst.EXIST_FILE.format(
    #                 path + file.filename.replace(' ', '-')
    #             )
    #         )
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


async def download(path: str = '',
                   user_id: UUID = None):
    file_path = os.getcwd() + cst.USER_FOLDER.format(user_id) + path
    if not os.path.exists(file_path):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f'File <{path}> not found'
        )
    return FileResponse(path=file_path)
