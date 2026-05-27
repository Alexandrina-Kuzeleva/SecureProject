![Build](https://img.shields.io/badge/build-passing-brightgreen) 
![Python](https://img.shields.io/badge/python-3.10-blue?logo=python) 
![FastAPI](https://img.shields.io/badge/FastAPI-%E2%9C%93-brightgreen) 
![Docker](https://img.shields.io/badge/docker-enabled-2496ed?logo=docker) 
![Postgres](https://img.shields.io/badge/postgres-ready-336791?logo=postgresql) 
![Fernet](https://img.shields.io/badge/encryption-Fernet-orange) 
![License](https://img.shields.io/badge/license-MIT-blue)

# Secure File Manager

Описание:
Secure File Manager — безопасное веб-приложение для загрузки, хранения и управления файлами. В проекте реализованы меры безопасности: шифрование файлов (Fernet), проверка прав доступа, CSP и другие механизмы защиты.

Ключевые возможности:
- Регистрация и аутентификация пользователей
- Ролевой доступ (User / Admin)
- Безопасная загрузка и скачивание файлов
- Опциональное шифрование файлов с помощью Fernet
- Логирование и мониторинг действий

Технологии:
- FastAPI — API-сервер
- Docker & Docker Compose — контейнеризация
- Postgres — база данных (через Docker-контейнер)
- Fernet (cryptography) — симметричное шифрование файлов
- Pydantic — валидация запросов и схем

Инструкция по запуску (локально):

1. Клонируйте репозиторий:

```bash
git clone https://github.com/Alexandrina-Kuzeleva/SecureProject.git
cd SecureProject
```

2. Создайте файл окружения (пример):

```bash
cp .env.example .env
# Отредактируйте .env (ключи, доступ к БД и т.д.)
```

3. Запустите сервисы через Docker Compose:

```bash
docker-compose up -d
```

4. Проверка работы:
- Откройте браузер: http://localhost:8000/docs — авто-документация Swagger/OpenAPI
- При необходимости просмотрите логи: `docker-compose logs -f`

Описание API:
Полная документация API доступна в Swagger UI по адресу `/docs` после старта приложения (например, http://localhost:8000/docs). Там описаны все маршруты, схемы запросов/ответов и примеры.

![panel](images/panel.png)
