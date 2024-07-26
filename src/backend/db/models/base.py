from sqlalchemy import Integer, Column
from sqlalchemy.orm import as_declarative
# from sqlalchemy.ext.declarative import as_declarative


@as_declarative()
class Base:
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    def __init__(self, **kwargs):
        pass

    __name__: str

