import datetime as dt
import uuid

from fastapi_users_db_sqlalchemy.guid import GUID
from sqlalchemy import (Boolean, Column, ForeignKey,
                        Text, DateTime, Integer)
from sqlalchemy_utils import UUIDType

from src.core.db import Base


class FileRegister(Base):
    __tablename__ = 'File_register'
    file_id = Column(UUIDType(binary=True), primary_key=True, default=uuid.uuid4)
    file_name = Column(Text(), nullable=False, index=True)
    create_date = Column(DateTime, default=dt.datetime.now)
    path = Column(Text(), nullable=False, unique=True)
    file_size = Column(Integer(), nullable=False)
    is_downloadable = Column(Boolean, default=True)
    user_id = Column(GUID, ForeignKey('user.id'), default=None)

