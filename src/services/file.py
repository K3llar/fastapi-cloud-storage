import os
from uuid import UUID

from http import HTTPStatus

from fastapi import File, UploadFile, HTTPException

import src.services.constants as cst


# async def upload(file: UploadFile = File(...),
#                  path: str = '',
#                  user_id: UUID = None):
#     file_path = os.getcwd() + cst.USER_FOLDER.format(user_id) + path
#     os.makedirs(file_path, exist_ok=True)
#     try:
#         contents = file.file.read()
#         file_name = file_path + file.filename.replace(' ', '-')
#         if os.path.exists(file_name):
#             print(True)
#             return HTTPException(
#                 status_code=HTTPStatus.CONFLICT,
#                 detail=cst.INPUT_FILE.format(
#                     path + file.filename.replace(' ', '-')
#                 )
#             )
#         with open(file_name, 'wb') as f:
#             f.write(contents)
#     except Exception:
#         return {'message': 'There was an error uploading file'}
#     finally:
#         file.file.close()


async def upload(file: UploadFile = File(...),
                 path: str = '',
                 user_id: UUID = None):
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
    if os.path.exists(file_name):
        raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail=cst.EXIST_FILE.format(
                    path + file.filename.replace(' ', '-')
                )
            )
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
