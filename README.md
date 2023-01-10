### Что это за проект?:smiley_cat:
Всё просто: Yatube_api - это API одноимённого сервиса yatube реализованный на Django Rest API.
Он предоставляет интерфейс для удобного взаимодействия с бизнес-логикой сервиса в формате JSON.

### Начало взаимодействия с API :old_key:
После запуска проекта, в версии V1 доступны для GET-запросов все [эндпоинты](http://127.0.0.1:8000/redoc) кроме списка подписок http://127.0.0.1:8000/api/v1/follow/
Для получения полного доступа к интерфейсу необходимо получить JWT-токен отправив POST запрос
с именем пользователя и паролем в формате:

```
{
"username": "string",
"password": "string"
}
```
на адрес http://127.0.0.1:8000/api/v1/jwt/create/. В ответ придёт JSON ответ вида:

```
{
"refresh": "string",
"access": "string"
}
```
Токен из строки "access" необходимо отправлять в headers запроса с ключом Authorization. Значение ключа в виде Bearer "ваш токен без ковычек".
Срок действия токена - 24 часа. Необходимо обновление по истечении срока.

### Документация проекта: :blue_book:
После запуска проекта (python3 manage.py runserver) документация со списком эндпоинтов доступна по ссылке:
http://127.0.0.1:8000/redoc


### Как запустить проект:
Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:Artem4es/api_final_yatube.git
```

```
cd api_final_yatube
```
Cоздать и активировать виртуальное окружение:
```
python3 -m venv venv
```
```
source env/bin/activate
```
Установить зависимости из файла requirements.txt:
```
python3 -m pip install --upgrade pip
```
```
pip install -r requirements.txt
```
Выполнить миграции:
```
python3 manage.py makemigrations
python3 manage.py migrate
```
Запустить проект:
```
python3 manage.py runserver
```
