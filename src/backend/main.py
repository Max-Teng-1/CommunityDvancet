import uvicorn

from src.backend.core.server import create_app
from src.backend.db import session
from src.backend.config import config


app = create_app()


if __name__ == '__main__':
    uvicorn.run(app, host=config.HOST, port=config.PORT, reload=False)

