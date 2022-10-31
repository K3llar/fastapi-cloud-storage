import os

from fastapi import HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from http import HTTPStatus

from src.models.file import FileRegister


async def create_folder(path: str):
    full_path = os.getcwd() + path
