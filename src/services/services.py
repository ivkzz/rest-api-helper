"""
Модуль бизнес-логики для работы с организациями, зданиями и деятельностью.
"""
import math
from typing import List, Optional

from sqlalchemy import and_
from sqlalchemy.orm import Session, joinedload

from src.models.models import Activity, Building, Organization


def get_building_by_id(db: Session, building_id: int) -> Optional[Building]:
    """
    Получение здания по идентификатору.
    """
    return db.query(Building).filter(Building.id == building_id).first()


def get_organizations_in_building(db: Session, building_id: int) -> List[Organization]:
    """
    Список всех организаций находящихся в конкретном здании.
    """
    return db.query(Organization).filter(Organization.building_id == building_id).all()


def get_organizations_by_activity(db: Session, activity_id: int) -> List[Organization]:
    """
    Список всех организаций, которые относятся к указанному виду деятельности.
    """
    return db.query(Organization).join(Organization.activities).filter(
        Activity.id == activity_id
    ).all()


def get_organization_by_id(db: Session, organization_id: int) -> Optional[Organization]:
    """
    Вывод информации об организации по её идентификатору.
    """
    return db.query(Organization).options(
        joinedload(Organization.building),
        joinedload(Organization.activities),
        joinedload(Organization.phones)
    ).filter(Organization.id == organization_id).first()


def get_activity_sub_ids(db: Session, activity_id: int) -> List[int]:
    """
    Получение списка идентификаторов деятельности и всех её потомков.
    """
    result_ids = [activity_id]
    # 2 уровень
    level2 = db.query(Activity.id).filter(Activity.parent_id == activity_id).all()
    level2_ids = [r[0] for r in level2]
    result_ids.extend(level2_ids)
    # 3 уровень
    if level2_ids:
        level3 = db.query(Activity.id).filter(Activity.parent_id.in_(level2_ids)).all()
        result_ids.extend([r[0] for r in level3])
    return result_ids


def search_organizations_by_activity_recursive(db: Session, activity_id: int) -> List[Organization]:
    """
    Поиск организаций по виду деятельности, включая всех потомков.
    """
    activity_ids = get_activity_sub_ids(db, activity_id)
    return db.query(Organization).join(Organization.activities).filter(
        Activity.id.in_(activity_ids)
    ).distinct().all()


def search_organizations_by_name(db: Session, name: str) -> List[Organization]:
    """
    Поиск организации по названию.
    """
    return db.query(Organization).filter(Organization.name.ilike(f"%{name}%")).all()


def _haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Расчет расстояния между двумя точками по формуле Гаверсинуса.
    """
    # 6371 - радиус Земли в км
    radius = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    val_a = (math.sin(dlat / 2) ** 2 +
             math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
             math.sin(dlon / 2) ** 2)
    val_c = 2 * math.asin(math.sqrt(val_a))
    return radius * val_c


def get_organizations_in_radius(
    db: Session, latitude: float, longitude: float, radius_km: float
) -> List[Organization]:
    """
    Список организаций в заданном радиусе (формула Гаверсинуса).
    """
    # Сначала грубая фильтрация (bounding box) для производительности
    deg_per_km = 1.0 / 111.0
    lat_delta = radius_km * deg_per_km
    lon_delta = radius_km * deg_per_km / math.cos(math.radians(latitude))

    query = db.query(Organization).join(Organization.building).filter(
        and_(
            Building.latitude >= latitude - lat_delta,
            Building.latitude <= latitude + lat_delta,
            Building.longitude >= longitude - lon_delta,
            Building.longitude <= longitude + lon_delta
        )
    )

    candidates = query.all()
    return [org for org in candidates if _haversine(
        latitude, longitude, org.building.latitude, org.building.longitude
    ) <= radius_km]


def get_organizations_in_box(
    db_session: Session, lat_min: float, lon_min: float, lat_max: float, lon_max: float
) -> List[Organization]:
    """
    Список организаций, которые находятся в заданной прямоугольной области.
    """
    return db_session.query(Organization).join(Organization.building).filter(
        and_(
            Building.latitude >= lat_min,
            Building.latitude <= lat_max,
            Building.longitude >= lon_min,
            Building.longitude <= lon_max
        )
    ).all()
