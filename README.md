#  Бэкнэд часть сайта Crystal Lake

## Инструкция по запуску:

1) Находясь в папке с проектом создайте .env файл со следующим содержанием:
```bash
DB_NAME=ваше имя базы данных
DB_USER=ваш логин к базе данных
DB_PASSWORD=ваш пароль к базе данных
DB_HOST=ваше имя хоста базы данных
DB_PORT=ваш порт для базы данных

```
2) Запустите контейнеры:
```
docker-compose up --build
```