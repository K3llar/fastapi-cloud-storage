import os

from fastapi import HTTPException

from http import HTTPStatus

import src.services.constants as cst


async def check_file_exist(path: str):
    if os.path.exists(path):
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail=cst.EXIST_FILE.format(
                path
            )
        )
