from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

from app.mixins.id_mixins import IdMixin
from app.models.base import Base



class Group(Base, IdMixin):
    __tablename__ = 'groups'
    
    title: Mapped[str] = mapped_column(String(100), unique=True)