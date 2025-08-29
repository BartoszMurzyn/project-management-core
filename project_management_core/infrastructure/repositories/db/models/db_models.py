from sqlalchemy import Column, ForeignKey, Integer, String, Text, DateTime, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.now().replace(tzinfo=None))
    owned_projects = relationship("Project", back_populates="owner")

class Project(Base):
    __tablename__ = 'projects'
    id = Column(Integer, primary_key=True,autoincrement=True)
    name = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    owner = relationship("User", back_populates="owned_projects")
    members = relationship("ProjectMember", back_populates="project")

class ProjectMember(Base):
    __tablename__='project_members'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    project_id = Column(Integer, ForeignKey('projects.id'), nullable=False)
    role = Column(String(50), nullable=False, default="participant")
    joined_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    __table_args__ = (UniqueConstraint('user_id', 'project_id'),)
    user = relationship("User")
    project = relationship("Project", back_populates='members')