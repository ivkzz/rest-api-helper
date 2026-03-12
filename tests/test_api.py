"""
Модуль юнит-тестов для API приложения.
"""
import pytest
from fastapi.testclient import TestClient

from src.main import app
from src.core.config import settings

client = TestClient(app)
API_KEY = settings.API_KEY


def test_root():
    """
    Тест корневого эндпоинта.
    """
    response = client.get("/")
    assert response.status_code == 200
    assert "Справочник организаций API работает" in response.json()["message"]


def test_auth_failure():
    """
    Тест ошибки авторизации (отсутствие или неверный API ключ).
    """
    # Без ключа
    response = client.get("/api/v1/organizations/1")
    assert response.status_code == 403

    # С неверным ключом
    response = client.get(
        "/api/v1/organizations/1",
        headers={"X-API-Key": "wrong-key"}
    )
    assert response.status_code == 403


def test_get_organization_by_id():
    """
    Тест получения организации по ID.
    """
    response = client.get(
        "/api/v1/organizations/1",
        headers={"X-API-Key": API_KEY}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert "name" in data
    assert "building" in data
    assert "activities" in data
    assert "phones" in data


def test_get_organization_not_found():
    """
    Тест получения несуществующей организации.
    """
    response = client.get(
        "/api/v1/organizations/99999",
        headers={"X-API-Key": API_KEY}
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Организация не найдена"


def test_get_orgs_in_building():
    """
    Тест получения списка организаций в здании.
    """
    # Здание ID 2 (Novosibirsk) в seed данных имеет организации
    response = client.get(
        "/api/v1/buildings/2/organizations",
        headers={"X-API-Key": API_KEY}
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1


def test_search_by_name():
    """
    Тест поиска по названию.
    """
    response = client.get(
        "/api/v1/organizations/search/name?name=SuperAuto",
        headers={"X-API-Key": API_KEY}
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert any("SuperAuto" in org["name"] for org in data)


def test_search_by_name_empty():
    """
    Тест поиска по названию, которое не существует.
    """
    response = client.get(
        "/api/v1/organizations/search/name?name=NonExistentOrgName123",
        headers={"X-API-Key": API_KEY}
    )
    assert response.status_code == 200
    assert response.json() == []


def test_search_activity_recursive():
    """
    Тест рекурсивного поиска по деятельности.
    """
    # Еда (Food) - ID 1. Находит 'Meat products' и 'Dairy products'
    response = client.get(
        "/api/v1/organizations/search/activity-recursive?activity_id=1",
        headers={"X-API-Key": API_KEY}
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1


def test_geo_search_radius():
    """
    Тест поиска в радиусе.
    """
    # Новосибирск: 54.9833, 82.8964. Ищем в радиусе 5 км.
    response = client.get(
        "/api/v1/organizations/search/geo?lat=54.9833&lon=82.8964&radius=5",
        headers={"X-API-Key": API_KEY}
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_geo_search_box():
    """
    Тест поиска в прямоугольной области.
    """
    # Область около Новосибирска
    url = "/api/v1/organizations/search/geo?lat_min=54.0&lon_min=82.0&lat_max=56.0&lon_max=84.0"
    response = client.get(
        url,
        headers={"X-API-Key": API_KEY}
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_geo_search_invalid_params():
    """
    Тест ошибки при недостаточном количестве параметров гео-поиска.
    """
    # Только широта
    response = client.get(
        "/api/v1/organizations/search/geo?lat=54.9833",
        headers={"X-API-Key": API_KEY}
    )
    assert response.status_code == 400
    assert "Необходимо указать параметры" in response.json()["detail"]


@pytest.mark.parametrize("activity_id", [1, 2, 3])
def test_get_orgs_by_activity(activity_id):
    """
    Тест получения организаций по конкретной деятельности (не рекурсивно).
    """
    response = client.get(
        f"/api/v1/activities/{activity_id}/organizations",
        headers={"X-API-Key": API_KEY}
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)
