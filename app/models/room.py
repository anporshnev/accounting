from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String

from app.mixins.id_mixins import IdMixin
from app.models.base import Base
from app.models.device  import Device



class Room(Base, IdMixin):
    __tablename__ = 'rooms'

    title: Mapped[str] = mapped_column(String(100), unique=True)
    devices: Mapped[list["Device"]] = relationship(back_populates="room")