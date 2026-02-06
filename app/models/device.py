from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, JSON, Text

from app.mixins.id_mixins import UUIDMixin
from app.mixins.modified_time_mixins import ModifiedTimeMixin
from app.models.base import Base
from app.models.room import Room
from app.models.group import Group


class Device(Base, UUIDMixin, ModifiedTimeMixin):
    __tablename__ = 'devices'
    
    title: Mapped[str]
    model: Mapped[str | None]
    inventory_number: Mapped[str | None]
    serial_number: Mapped[str | None]
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"))
    room: Mapped["Room"] = relationship(back_populates="devices")
    group_id: Mapped[int] = mapped_column(ForeignKey("groups.id"))
    group: Mapped["Group"] = relationship(back_populates="devices")
    properties: Mapped[dict | None] = mapped_column(JSON)
    notes: Mapped[Text | None]
    
    
    