"""
Модуль Pydantic схем для API.
"""
# pylint: disable=too-few-public-methods
from typing import List, Optional

from pydantic import BaseModel


class PhoneSchema(BaseModel):
    """
    Схема номера телефона.
    """
    id: int
    number: str

    class ConfigDict:
        """
        Конфигурация схемы.
        """
        from_attributes = True


class ActivityBase(BaseModel):
    """
    Базовая схема деятельности.
    """
    name: str


class ActivitySchema(ActivityBase):
    """
    Полная схема деятельности.
    """
    id: int
    parent_id: Optional[int] = None

    class ConfigDict:
        """
        Конфигурация схемы.
        """
        from_attributes = True


class BuildingBase(BaseModel):
    """
    Базовая схема здания.
    """
    address: str
    latitude: float
    longitude: float


class BuildingSchema(BuildingBase):
    """
    Полная схема здания.
    """
    id: int

    class ConfigDict:
        """
        Конфигурация схемы.
        """
        from_attributes = True


class OrganizationBase(BaseModel):
    """
    Базовая схема организации.
    """
    name: str
    building_id: int


class OrganizationSchema(OrganizationBase):
    """
    Полная схема организации.
    """
    id: int
    building: BuildingSchema
    activities: List[ActivitySchema]
    phones: List[PhoneSchema]

    class ConfigDict:
        """
        Конфигурация схемы.
        """
        from_attributes = True


class OrganizationCreate(OrganizationBase):
    """
    Схема создания организации.
    """
    activity_ids: List[int]
    phone_numbers: List[str]
