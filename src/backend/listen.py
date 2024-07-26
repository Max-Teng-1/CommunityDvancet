import threading
import time
import os
import glob
from datetime import datetime, timedelta
from fastapi import FastAPI
from typing import List
from jose import jwt

from src.backend.routers.helper import get_aus_time_str, str_to_datetime
from src.backend.config import config
from src.backend.db.models.user import User
from src.backend.db.session import get_db


# register listen function
def register_scheduler(app: FastAPI):
    stop_event = threading.Event()

    @app.on_event("startup")
    async def startup_event():
        pass
        # initial_super_admin()

    @app.on_event("shutdown")
    async def shutdown_event():
        stop_event.set()

