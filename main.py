import uvicorn
from loguru import logger
from src.settings import settings

if __name__ == '__main__':
    logger.info(f'start server http://{settings.host}:{settings.port}/docs#')
    uvicorn.run(
        "app.main:create_app",
        host=settings.host,
        port=settings.port,
        reload=True,
    )
