from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database import engine, Base
from app.routers import auth, tasks
from app.config import settings
from app.routers import auth, tasks, users


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Создаём таблицы при старте (в продакшене лучше использовать Alembic)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    description="REST API для управления задачами с JWT авторизацией",
    lifespan=lifespan,
)

# Подключаем роутеры
app.include_router(auth.router)
app.include_router(tasks.router)
app.include_router(users.router)

@app.get("/health")
async def health_check():
    return {"status": "healthy", "app": settings.APP_NAME}