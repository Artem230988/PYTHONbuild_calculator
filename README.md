# backend
# Calculator_mvp
Задача: реализовать API для строительного калькулятора

Технологии: 
 - Python3 
 - Django
 - СУБД PostgreSQL (через отдельный docker образ)
 - Описание API - Swagger OpenApi Version 2

Описание приложения:

## Installation guide
```
docker-compose up --build
```
Для создания суперпользователя необходимо войти в запущенный контйнер
```
docker exec -it mvp_calculator_container bash
python3 manage.py createsuperuser
```
Документация swagger:
127.0.0.1:8000/swagger/

Вход в админку:
127.0.0.1:8000/admin/ (логин и пароль суперпользователя)
