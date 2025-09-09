from datetime import datetime, timezone

from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class UserModel(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.now().replace(tzinfo=None))
    owned_projects = relationship("ProjectModel", back_populates="owner")

class ProjectModel(Base):
    __tablename__ = 'projects'
    id = Column(Integer, primary_key=True,autoincrement=True)
    name = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.now().replace(tzinfo=None))
    owner = relationship("UserModel", back_populates="owned_projects")
    members = relationship("ProjectMember", back_populates="project")

class ProjectMember(Base):
    __tablename__='project_members'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    project_id = Column(Integer, ForeignKey('projects.id'), nullable=False)
    role = Column(String(50), nullable=False, default="participant")
    joined_at = Column(DateTime, default=datetime.now().replace(tzinfo=None))
    __table_args__ = (UniqueConstraint('user_id', 'project_id'),)
    user = relationship("UserModel")
    project = relationship("ProjectModel", back_populates='members')

class DocumentModel(Base):
    __tablename__ = 'documents'
    id = Column(Integer, primary_key= True, autoincrement= True)
    original_filename = Column(String(255), nullable = False)
    generated_filename = Column(String(255), nullable = False)
    file_path = Column(String(500), nullable = False)
    file_size = Column(Integer, nullable= False)
    content_type = Column(String(255), nullable = False)
    project_id = Column(Integer, ForeignKey('projects.id'), nullable= False)
    uploaded_by = Column(Integer, ForeignKey('users.id'), nullable=False)
    uploaded_at = Column(DateTime, default=datetime.now().replace(tzinfo=None))

    project = relationship("ProjectModel")
    user = relationship("UserModel")
