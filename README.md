#  Бэкнэд часть сайта Crystal Lake

## Инструкция по запуску:

1) Находясь в папке с проектом создайте .env файл со следующим содержанием:
```bash
DB_NAME=ваше имя базы данных
DB_USER=ваш логин к базе данных
DB_PASSWORD=ваш пароль к базе данных
DB_PORT=ваш порт для базы данных (должен быть свободен)
APACHE_PORT=порт для апачи
KEY=ваш секретный ключ джанго
DEV=запустить ли в режими разработки
```
Пример:
```bash
DB_NAME=crystal_lake
DB_USER=user
DB_PASSWORD=passwd
DB_PORT=5454
APACHE_PORT=8000
KEY=@@)*r3&2f0=%t^@bnom9@916(z=3-2e_iqqr90(r_v@foum(q^
DEV=true
```
2) Соберите и запустите контейнеры:
```
docker-compose up --build
```
3) Для создания суперпользователя выполните скрипт [create_superuser.sh](./create_superuser.sh), который первым аргументом принимает номер телефона RU формата, а вторым пароль. Пример:
```
./create_superuser.sh +79999999999 qwe
```

