#!/bin/bash

# Функция для проверки существования таблицы alembic_version
check_alembic_table() {
    echo "Проверяем существование таблицы alembic_version..."
    python -c "
import pathlib
import asyncio
from sqlalchemy import text

from app.core.database import get_async_session
async def check_table():
    try:
        async with get_async_session() as conn:
            result = await conn.execute(text(\"SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'alembic_version')\"))
            exists = result.scalar()
            return exists
    except Exception as e:
        print(f'Ошибка при проверке таблицы: {e}')
        return False
exists = asyncio.run(check_table())
print(f'Таблица alembic_version существует: {exists}')
exit(0 if exists else 1)
"
}

# Функция для применения миграций
apply_migrations() {
    echo "Применяем миграции Alembic..."
    alembic upgrade head
}

# Функция для создания начальных миграций (если нужно)
create_initial_migration() {

    echo "--- $PWD"
    echo "Создаем начальную миграцию..."
    alembic revision --autogenerate -m "initial"
    alembic upgrade head
}

# Основная логика
echo "Запуск миграций базы данных..."

# Ждем пока база данных будет готова
echo "Ждем подключения к базе данных..."
sleep 5

# Проверяем существование таблицы alembic_version
if check_alembic_table; then
    echo "Таблица alembic_version найдена, применяем существующие миграции..."
    apply_migrations
else
    echo "Таблица alembic_version не найдена, создаем начальные миграции..."
    create_initial_migration
fi

echo "Миграции завершены, запускаем приложение..."
exec uvicorn app.main:create_app --host 0.0.0.0 --port 7000