# Petsy

Минимальный веб-сервис для управления карточками питомцев.

## Возможности

- Проверка состояния сервиса (`GET /health`)
- CRUD для питомцев:
  - `POST /pets`
  - `GET /pets`
  - `GET /pets/{pet_id}`
  - `PATCH /pets/{pet_id}`
  - `DELETE /pets/{pet_id}`
- Фильтрация списка по `pet_type` и `vaccinated`
- Swagger UI: `/docs`

## Быстрый старт

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
uvicorn app.main:app --reload
```

Сервис будет доступен на `http://127.0.0.1:8000`.

## Запуск тестов

```bash
pytest
```
