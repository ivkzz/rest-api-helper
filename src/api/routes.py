"""
Модуль API роутов для работы со справочником.
"""
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Security
from fastapi.security.api_key import APIKeyHeader
from sqlalchemy.orm import Session

from src.core.config import settings
from src.core.database import get_db
from src.schemas.schemas import OrganizationSchema
from src.services import services

router = APIRouter()

# Определение заголовка для API ключа
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


async def get_api_key(api_key: str = Security(api_key_header)):
    """
    Проверка статического API ключа.
    """
    if api_key != settings.API_KEY:
        raise HTTPException(
            status_code=403,
            detail="Невалидный API ключ"
        )
    return api_key


@router.get(
    "/buildings/{building_id}/organizations",
    response_model=List[OrganizationSchema],
    dependencies=[Depends(get_api_key)]
)
def get_orgs_in_building(building_id: int, db: Session = Depends(get_db)):
    """
    Список всех организаций, находящихся в конкретном здании.
    """
    return services.get_organizations_in_building(db, building_id)


@router.get(
    "/activities/{activity_id}/organizations",
    response_model=List[OrganizationSchema],
    dependencies=[Depends(get_api_key)]
)
def get_orgs_by_activity(activity_id: int, db: Session = Depends(get_db)):
    """
    Список всех организаций, которые относятся к указанному виду деятельности.
    """
    return services.get_organizations_by_activity(db, activity_id)


@router.get(
    "/organizations/search/geo",
    response_model=List[OrganizationSchema],
    dependencies=[Depends(get_api_key)]
)
# pylint: disable=too-many-arguments, too-many-positional-arguments
def search_organizations_geo(
    lat: Optional[float] = None,
    lon: Optional[float] = None,
    radius: Optional[float] = None,
    lat_min: Optional[float] = None,
    lon_min: Optional[float] = None,
    lat_max: Optional[float] = None,
    lon_max: Optional[float] = None,
    db: Session = Depends(get_db)
):
    """
    Поиск организаций в радиусе или прямоугольной области.
    """
    if lat is not None and lon is not None and radius is not None:
        return services.get_organizations_in_radius(db, lat, lon, radius)

    if (lat_min is not None and lon_min is not None and
            lat_max is not None and lon_max is not None):
        return services.get_organizations_in_box(
            db,
            lat_min,
            lon_min,
            lat_max,
            lon_max
        )

    raise HTTPException(
        status_code=400,
        detail="Необходимо указать параметры для поиска по радиусу (lat, lon, radius) "
               "или по области (lat_min, lon_min, lat_max, lon_max)"
    )


@router.get(
    "/organizations/{org_id}",
    response_model=OrganizationSchema,
    dependencies=[Depends(get_api_key)]
)
def get_organization(org_id: int, db: Session = Depends(get_db)):
    """
    Вывод информации об организации по её идентификатору.
    """
    db_org = services.get_organization_by_id(db, org_id)
    if db_org is None:
        raise HTTPException(status_code=404, detail="Организация не найдена")
    return db_org


@router.get(
    "/organizations/search/activity-recursive",
    response_model=List[OrganizationSchema],
    dependencies=[Depends(get_api_key)]
)
def search_orgs_activity_recursive(
    activity_id: int = Query(...),
    db: Session = Depends(get_db)
):
    """
    Поиск организаций по виду деятельности, включая всех потомков.
    """
    return services.search_organizations_by_activity_recursive(db, activity_id)


@router.get(
    "/organizations/search/name",
    response_model=List[OrganizationSchema],
    dependencies=[Depends(get_api_key)]
)
def search_orgs_by_name(
    name: str = Query(...),
    db: Session = Depends(get_db)
):
    """
    Поиск организации по названию.
    """
    return services.search_organizations_by_name(db, name)
