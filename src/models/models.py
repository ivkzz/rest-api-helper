"""
Модуль SQLAlchemy моделей для базы данных.
"""
# pylint: disable=too-few-public-methods
from sqlalchemy import Column, Float, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

from src.core.database import Base

# Таблица для связи "многие ко многим" между Организациями и Деятельностями
organization_activity = Table(
    "organization_activity",
    Base.metadata,
    Column("organization_id", Integer, ForeignKey("organizations.id"), primary_key=True),
    Column("activity_id", Integer, ForeignKey("activities.id"), primary_key=True),
)


class Building(Base):
    """
    Модель Здания.
    """
    __tablename__ = "buildings"

    id = Column(Integer, primary_key=True, index=True)
    address = Column(String, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)

    organizations = relationship("Organization", back_populates="building")


class Activity(Base):
    """
    Модель Деятельности (категории).
    Поддерживает древовидную структуру (вложенность).
    """
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    parent_id = Column(Integer, ForeignKey("activities.id"), nullable=True)

    parent = relationship("Activity", remote_side=[id], backref="children")
    organizations = relationship(
        "Organization", secondary=organization_activity, back_populates="activities"
    )


class Organization(Base):
    """
    Модель Организации.
    """
    __tablename__ = "organizations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    building_id = Column(Integer, ForeignKey("buildings.id"), nullable=False)

    building = relationship("Building", back_populates="organizations")
    phones = relationship("Phone", back_populates="organization", cascade="all, delete-orphan")
    activities = relationship(
        "Activity", secondary=organization_activity, back_populates="organizations"
    )


class Phone(Base):
    """
    Модель номера телефона организации.
    """
    __tablename__ = "phones"

    id = Column(Integer, primary_key=True, index=True)
    number = Column(String, nullable=False)
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)

    organization = relationship("Organization", back_populates="phones")
