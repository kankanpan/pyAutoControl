from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import TIMESTAMP as Timestamp
from sqlalchemy.sql.functions import current_timestamp

from api.database import Base

class User(Base):
    __tablename__ = "users"

    name = Column(String)
    id = Column(Integer, primary_key=True, index=True, autoincrement=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    insert_at = Column(Timestamp, default=current_timestamp())
    is_admin = Column(Boolean, default=False, nullable=False)
    is_active = Column(Boolean, default=False, nullable=False)
    department_id = Column(String, ForeignKey("departments.id"), index=True, nullable=False)

    hashed_password = Column(String)

    department = relationship("Department", back_populates="users")

class Department(Base):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True, nullable=False)
    name = Column(String, index=True, nullable=False)
    description = Column(Text)
    insert_at = Column(Timestamp, default=current_timestamp())
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    users = relationship("User", back_populates="departments")
    data = relationship("Data", back_populates="departments")

class Data(Base):
    __tablename__ = "data"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True, nullable=False)
    file_path = Column(Text, index=True, nullable=False)
    insert_at = Column(Timestamp, default=current_timestamp())
    department_id = Column(Integer, ForeignKey('departments.id'))

    department = relationship("Department", back_populates="data")

class Beamtime(Base):
    __tablename__ = "beamtimes"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True, nullable=False)
    title = Column(String, index=True)
    start_at = Column(DateTime, index=True, nullable=False)
    end_at = Column(DateTime, index=True, nullable=False)
    description = Column(Text)
    insert_at = Column(Timestamp, default=current_timestamp())
    department_id = Column(Integer, ForeignKey('departments.id'))

    department = relationship("Department", back_populates="beamtimes")

class Accesslog(Base):
    __tablename__ = "accesslogs"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True, nullable=False)
    text = Column(Text, index=True, nullable=False)
    insert_at = Column(Timestamp, default=current_timestamp())
    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship("User", back_populates="accesslogs")
