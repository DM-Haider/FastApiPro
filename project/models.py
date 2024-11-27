from sqlalchemy import  Column, Integer, String

from engine import Base
# from engine import Base


class User(Base):
    __tablename__ = "users"

    # id = Mapped[int] = mapped_column(primary_key=True)
    # username = Mapped[str] = mapped_column(unique=True , default=None)
    # hashed_password = Mapped[str] = mapped_column()

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    token = Column(String)
