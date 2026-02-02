from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

from app.mixins.models_mixins import IDMixins
from app.models.base import Base



class Room(IDMixins, Base):
    __tablename__ = 'rooms'

    title: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)