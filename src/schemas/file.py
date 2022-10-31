import datetime as dt

from pydantic import UUID4, BaseModel, Field


class FileBase(BaseModel):
    path: str | None = Field(None)


class FileCreate(BaseModel):
    path: str = Field(default='')


class FileDB(FileBase):
    file_id: UUID4
    file_name: str | None
    create_date: dt.datetime | None
    file_size: int | None
    is_downloadable: bool | None
    user_id: UUID4 | None

    class Config:
        orm_mode = True
