<div class="badge_container" style="display: flex; justify-content: center;">

![Python Version](https://img.shields.io/badge/python-3.11-blue.svg)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Docker-compose](https://img.shields.io/badge/docker-compose-orange.svg)](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-compose-on-ubuntu-22-04)
![Linux (Ubuntu)](https://img.shields.io/badge/linux-ubuntu-green.svg)
</div>
<h1 align="center" style="color: #B5E5E8;">Blog FastAPI</h1>

### Описание проекта:
Блог написаный на FastAPI.
- CRUD Author
- CRUD Categorie
- CRUD Tag
- CRUD Post (GET/POST/PATCH/DELETE)

### Инструменты разработки

**Стек:**
- Python 
- FastAPI 
- SQLalchemy
- PostgreSQL
- Docker

## Разработка

##### 1) Клонировать репозиторий

    git clone 

##### 2) Создать виртуальное окружение

    python -m venv venv
    
##### 3) Активировать виртуальное окружение


##### 4) Устанавливить зависимости:

    pip install -r requirements.txt

##### 5) Запустить Docker 
    
    make build

##### 6) Выполнить команду для выполнения миграций

    alembic upgrade head
    
##### 7) Запустить сервер

    uvicorn main:app --reload
    
##### 8) Перейти по адресу

    http://127.0.0.1:8000/docs
    
## License

Copyright (c) 2024 Aleshichev Igor



