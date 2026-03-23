import os

from sqlalchemy import *
from sqlalchemy.orm import Session

from persistance.models import Base


class Database:
    engine = None
    session = None

    def __init__(self):
        self.engine = create_engine(os.getenv("DB_URL"))
        self.session = Session(self.engine)
        Base.metadata.create_all(self.engine)

db = Database()