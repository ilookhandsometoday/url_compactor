from sqlalchemy import Column, Integer, String
from database import Base


class Link(Base):
    __tablename__ = 'link'
    ID = Column(Integer, primary_key=True, autoincrement=True)
    original_link = Column(String, nullable=False)
