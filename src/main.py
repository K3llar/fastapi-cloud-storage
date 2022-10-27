import uvicorn
from fastapi import FastAPI

from src.api.routers import main_router
from src.core.config import settings
from src.core.init_db import create_first_superuser

app = FastAPI(title=settings.app_title,
              description=settings.description)

app.include_router(main_router)


@app.on_event('startup')
async def startup():
    await create_first_superuser()


if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host=settings.project_host,
        port=settings.project_port
    )
