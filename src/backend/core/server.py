import traceback
from fastapi import FastAPI, Request, Response
from fastapi.exceptions import RequestValidationError, ValidationError
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.errors import ServerErrorMiddleware
from sqlalchemy.exc import DataError

from src.backend.listen import register_scheduler
from src.backend.routers import api_router
from src.backend.config import config


def create_app() -> FastAPI:
    """
    generate api object
    :return:
    """
    app = FastAPI(
        debug=config.DEBUG,
        title=config.TITLE,
        description=config.DESCRIPTION,
        docs_url=config.DOCS_URL,
        openapi_url=config.OPENAPI_URL,
        redoc_url=config.REDOC_URL
    )
    register_scheduler(app)
    register_router(app)
    register_cors(app)
    register_hook(app)
    return app


def register_router(app: FastAPI) -> None:
    """
    :param app:
    :return:
    """
    app.include_router(
        api_router,
    )

def register_hook(app: FastAPI) -> None:
    """
    https://fastapi.tiangolo.com/tutorial/middleware/
    :param app:
    :return:
    """

    @app.middleware("http")
    def logger_request(request: Request, call_next) -> Response:
        response = call_next(request)
        return response

def register_cors(app: FastAPI) -> None:
    """
    :param app:
    :return:
    """
    # if config.DEBUG:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

