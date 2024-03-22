from sqlalchemy import String, Date
from datetime import date

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Contact(Base):
    __tablename__ = 'contacts'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), index=True)
    last_name: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(50))
    phone_number: Mapped[str] = mapped_column(nullable=False)
    birthday: Mapped[date] = mapped_column(Date, nullable=False)


