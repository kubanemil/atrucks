# Тестовое задание ATrucks

## Описание

Этот проект использует базу данных PostgreSQL, и DRF для веб-приложения. Проект настроен для запуска в среде **Docker**.

## Установка

1. Отклонируйте репу.
2. Запустите:
    ```sh
    docker-compose up
    ```
3. Идите к адресу `http://localhost:8000/api/docs` чтобы протестить вручную.

## Тестирование

Запустить тесты для ручки:
```sh
docker exec -it atrucks-api-1 /bin/bash -c "python manage.py test phone"
```
