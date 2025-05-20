## Запуск проекта

1. Создайте папку с проектом и склонируйте репозиторйй:
```bash
mkdir streaming-service
streaming-service
git clone <repository-url>
```

2. Настройте переменные окружения в файле .env.


3. Соберите и запустите контейнеры:
```bash
docker-compose up --build
```

4. Примените миграции:
```bash
alembic upgrade head
```

Приложение будет доступно по адресу: `http://localhost:8000`
Протестировать работу эндпоинтов можно через сваггер:  `http://localhost:8000/docs`

