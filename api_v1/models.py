from datetime import datetime

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, \
    declared_attr


class Base(DeclarativeBase):
    __abstract__ = True
    id: Mapped[int] = mapped_column(primary_key=True)

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}s"


class Image(Base):
    title: Mapped[str]
    path: Mapped[str]
    uploaded_at: Mapped[datetime]
    resolution: Mapped[str]
    size: Mapped[int]
