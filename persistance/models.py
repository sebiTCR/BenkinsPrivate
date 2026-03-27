from tokenize import String
from typing import List
from dataclasses import dataclass

from sqlalchemy import (String, Enum, ForeignKey,)
from sqlalchemy.orm import DeclarativeBase, Mapped, relationship, MappedAsDataclass
from sqlalchemy.testing.schema import mapped_column


class BuildStatus:
    NONE=0,
    SUCCESS=1,
    BUILDING=2,
    FAILED=3



class Base(DeclarativeBase):
    pass


class Project(MappedAsDataclass, Base):
        __tablename__ = "project"

        builds: Mapped[List["Build"]] = relationship(init=False)
        id: Mapped[int] = mapped_column(init=False, primary_key=True)
        name: Mapped[str] = mapped_column(String(30))
        version: Mapped[str] = mapped_column(String(10))
        status: Mapped[int] = mapped_column()
        path: Mapped[str] = mapped_column()


class Build(MappedAsDataclass, Base):
    __tablename__ = "builds"
    id: Mapped[int] = mapped_column(primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("project.id"))
    version: Mapped[str] = mapped_column()
    file_path: Mapped[str] = mapped_column()