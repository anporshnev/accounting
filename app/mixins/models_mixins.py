from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, mapped_column


class IDMixins:
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)