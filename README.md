#  Бэкнэд часть сайта Crystal Lake

## Инструкция по запуску:

1) Находясь в папке с проектом создайте .env файл со следующим содержанием:
```bash
DB_NAME=ваше имя базы данных
DB_USER=ваш логин к базе данных
DB_PASSWORD=ваш пароль к базе данных
DB_PORT=ваш порт для базы данных (должен быть свободен)
APACHE_PORT=порт для апачи
```
Пример:
```bash
DB_NAME=crystal_lake
DB_USER=user
DB_PASSWORD=passwd
DB_PORT=5454
APACHE_PORT=8000
```
2) Соберите и запустите контейнеры:
```
docker-compose up --build
```