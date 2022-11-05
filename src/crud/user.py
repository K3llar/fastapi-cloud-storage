from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import FileRegister
from schemas.user import UserDB


async def get_links_by_user(
        session: AsyncSession,
        user: UserDB
) -> list[FileRegister]:
    all_links = await session.execute(
        select(FileRegister).where(
            FileRegister.user_id == user.id
        )
    )
    all_links = all_links.scalars().all()
    return all_links
