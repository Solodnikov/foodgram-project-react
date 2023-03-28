# praktikum_new_diplom

![workflow status](https://github.com/solodnikov/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg?event=push&branch=master)
![](https://img.shields.io/badge/Django-3.2.18-orange)
![](https://img.shields.io/badge/Python-3.7-brightgreen)
![](https://img.shields.io/badge/DjangoRestFramework-3.14.0-red)


# Продуктовый помощник Foodgram

### Описание
Сервис, на котором пользователи будут публиковать рецепты, добавлять чужие рецепты в избранное и подписываться на публикации других авторов. Сервис «Список покупок» позволит пользователям создавать список продуктов, которые нужно купить для приготовления выбранных блюд.

# Порядок запуска
## Запуск проекта локально
Клонировать репозиторий и перейти в него:
```
git clone https://github.com/Solodnikov/foodgram-project-react.git
```

Создать и активировать виртуальное окружение, обновить pip и установить зависимости:
```
python -m venv venv
source venv/Scripts/activate
python -m pip install --upgrade pip
pip install -r backend/requirements.txt
```

## Для запуска локально:
```
cd backend
python manage.py runserver
```

Создать базу данных:
```
cd backend
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

Загрузить данные по ингредиентам:
```
python manage.py importcsv
```

Заупстить сервер:
```
python manage.py runserver
```

Для запуска frontend(через bash):
- запустить bash
- найти директорию проекта foodgram-project-react
- пройти в директорию infra.
```
cd infra
docker-compose up --build
```

## Для работы с удаленным сервером:
* Выполните вход на свой удаленный сервер
```
ssh <username>@<host>
```

* Установите docker на сервер:
```
sudo apt install docker.io 
```
* Установите docker-compose на сервер:
```
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```
* Локально отредактируйте файл infra/nginx.conf и в строке server_name впишите свой IP
* Скопируйте файлы docker-compose.yml и nginx.conf из директории infra на сервер:
```
scp docker-compose.yml <username>@<host>:/home/<username>/<appname>/docker-compose.yml
scp nginx.conf <username>@<host>:/home/<username>/<appname>/nginx.conf
```
* Для работы с Workflow добавьте в Secrets GitHub переменные окружения для работы:
    ```
    DB_ENGINE=<django.db.backends.postgresql>
    DB_NAME=<имя базы данных postgres>
    DB_USER=<пользователь бд>
    DB_PASSWORD=<пароль>
    DB_HOST=<db>
    DB_PORT=<5432>
    DOCKER_PASSWORD=<пароль от DockerHub>
    DOCKER_USERNAME=<имя пользователя>
    SECRET_KEY=<секретный ключ проекта django>
    USER=<username для подключения к серверу>
    HOST=<IP сервера>
    PASSPHRASE=<пароль для сервера, если он установлен>
    SSH_KEY=<ваш SSH ключ (для получения команда: cat ~/.ssh/id_rsa)>
    TELEGRAM_TO=<ID чата, в который придет сообщение>
    TELEGRAM_TOKEN=<токен вашего бота>
    ```
    Workflow состоит из четырех шагов:
     - Проверка кода на соответствие PEP8;
     - Сборка и публикация образа бекенда и фронтэнда на DockerHub;
     - Автоматический деплой на удаленный сервер;
     - Отправка уведомления в телеграм-чат.  
  
    - Создать суперпользователя Django:
    ```
    sudo docker-compose exec backend python manage.py createsuperuser
    ```
    - Проект будет доступен по вашему IP или доменному имени(если создано).

## Проект доступен
- Проект запущен и доступен по http://nymnym.bounceme.net/signin
- Админ панель http://nymnym.bounceme.net/admin
- Админ логин: alex
- Админ пароль: alex@example.com