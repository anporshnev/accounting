from sqlalchemy import BigInteger, UUID
from sqlalchemy.orm import Mapped, mapped_column
import uuid


class IdMixin:
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    
class UUIDMixin:
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)