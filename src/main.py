"""
Главный модуль приложения FastAPI.
"""
from fastapi import FastAPI

from src.api.routes import router

app = FastAPI(
    title="Справочник организаций",
    description="REST API для справочника Организаций, Зданий и Деятельности",
    version="1.0.0",
)

# Подключение роутов
app.include_router(router, prefix="/api/v1")


@app.get("/")
def root():
    """
    Корневой эндпоинт для проверки работоспособности.
    """
    return {
        "message": "Справочник организаций API работает. "
                   "Перейдите на /docs для просмотра документации."
    }
