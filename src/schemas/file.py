import datetime as dt
from enum import Enum

from pydantic import UUID4, BaseModel, Field


class DBFieldsEnum(str, Enum):
    file_name = 'file_name'
    create_date = 'create_date'
    path = 'path'
    file_size = 'file_size'


class FileBase(BaseModel):
    path: str | None = Field(None)


class FileCreate(BaseModel):
    path: str = Field(default='')


class FileDownload(FileCreate):
    compression: bool = Field(default=False)


class FileOptions(BaseModel):
    path: str | None = Field(default='')
    extension: str | None = Field(default='')
    order_by: DBFieldsEnum
    limit: int = Field(default=10)


class FileSearch(BaseModel):
    search_query: str | None = Field(None)
    options: FileOptions


class FileDB(FileBase):
    file_id: UUID4
    file_name: str | None
    create_date: dt.datetime | None
    file_size: int | None
    is_downloadable: bool | None
    user_id: UUID4 | None

    class Config:
        orm_mode = True
