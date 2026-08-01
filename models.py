from sqlalchemy import Column, Integer, String
from database import Base

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    branch = Column(String(50), nullable=False)

    marks1 = Column(Integer, nullable=False)
    marks2 = Column(Integer, nullable=False)
    marks3 = Column(Integer, nullable=False)

    email = Column(String(100), unique=True, nullable=False)
    phone = Column(String(15), nullable=False)


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(300), nullable=False)

    is_active = Column(String(10), default="True")
    is_admin = Column(String(10), default="False")
    