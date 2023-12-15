# Проект Просепт:
[![MSPP CI/CD](https://github.com/photo-booking/backend/actions/workflows/trigger_to_main_repo.yml/badge.svg)](https://github.com/photo-booking/backend/actions/workflows/trigger_to_main_repo.yml/badge.svg)

Цель проекта - 



## Оглавление:
- [Технологии](#технологии)
- [Описание работы](#описание-работы)
- [Установка и запуск](#установка-и-запуск)
- [Удаление](#удаление)
- [Авторы](#авторы)



## Технологии:
<details><summary>Развернуть</summary>

**Языки программирования, библиотеки и модули:**

[![Python](https://img.shields.io/badge/Python-v3.11-blue?logo=python)](https://www.python.org/)
[![Chanels](https://img.shields.io/badge/chanels-v3.0.4-blue?logo=python)]
[![Daphne](https://img.shields.io/badge/daphe-v3.0.2-blue?logo=python)]
[![Djoser](https://img.shields.io/badge/djoser-v2.2-blue?logo=python)]
[![Social-OAuth](https://img.shields.io/badge/Social_Oauth-v5.2-blue?logo=python)]()
[![Pillow](https://img.shields.io/badge/Pillow-v10.0-blue?logo=python)](https://pillow.readthedocs.io/en/stable/)
[![Redis](https://img.shields.io/badge/Redis-v2.0-blue?logo=python)](https://redis.io/docs/connect/clients/python/)
[![logging](https://img.shields.io/badge/logging-v1-blue?logo=python)](https://docs.python.org/3/library/logging.html)
[![uvicorn](https://img.shields.io/badge/uvicorn-v1-blue?logo=python)](https://www.uvicorn.org/)


**Фреймворк, расширения и библиотеки:**

[![Django](https://img.shields.io/badge/Django-v4.1-blue?logo=Django)](https://www.djangoproject.com/)


**База данных:**

[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?logo=PostgreSQL)](https://www.postgresql.org/)


**CI/CD:**

[![GitHub_Actions](https://img.shields.io/badge/-GitHub_Actions-464646?logo=GitHub)](https://docs.github.com/en/actions)
[![docker_hub](https://img.shields.io/badge/-Docker_Hub-464646?logo=docker)](https://hub.docker.com/)
[![docker_compose](https://img.shields.io/badge/-Docker%20Compose-464646?logo=docker)](https://docs.docker.com/compose/)
[![Nginx](https://img.shields.io/badge/-NGINX-464646?logo=NGINX)](https://nginx.org/ru/)

[⬆️Оглавление](#оглавление)
</details>



## Описание работы:
Сервис поддерживает следующие базовые функции:

**Главная страница:**

- Основная информация для пользовтелей
- Меню для перехода по страницам
- Вывод топовых исполнителей на главной страницей, возможность перейти на их страницу или просмотра всех специалистов

**Регистрация:**

- Выбор регистрации как пользователь или исполнитель
- Возможность регистрации через Gmail или Vkontakte как пользователь

**Личный кабинет:**

- Редактирование личной информации
- Настройка уведомлений
- Просмотр оставленных отзывов для фотографов
- Чат с исполнителями
- Удаление аккаунта

Для исполнителей:
- Возможность выбора 5 работ(фото + видео) для предсвления на главной странице
- Чат с клиентами
- Добавление и удаление личных проектов

**Просмотр страниц исполнителей:**

- Возможность соритровки и фильтрации по специализации, виду съемок, стоимости
- Возможность просматривать 5 проектов каждого исполнителя

**Чат с пользователями:**

-
-

[⬆️Оглавление](#оглавление)



## Установка и запуск:
Удобно использовать принцип copy-paste - копировать команды из GitHub Readme и вставлять в командную строку Git Bash или IDE (например VSCode).
#### Предварительные условия:
<details><summary>Развернуть</summary>

Предполагается, что пользователь:
 - создал аккаунт [DockerHub](https://hub.docker.com/), если запуск будет производиться на удаленном сервере.
 - установил [Docker](https://docs.docker.com/engine/install/) и [Docker Compose](https://docs.docker.com/compose/install/) на локальной машине или на удаленном сервере, где проект будет запускаться в контейнерах. Проверить наличие можно выполнив команды:
    ```bash
    docker --version && docker-compose --version
    ```
</details>
<hr>
<details><summary>Локальный запуск</summary>

1. Клонируйте репозиторий с GitHub и в **.env**-файле введите данные для переменных окружения (значения даны для примера, но их можно оставить; подсказки даны в комментариях):
```bash
git clone https://github.com/Prosept-marking/backend.git && \
cd backend && \
cp .env_example .env && \
nano .env
```
Для работы сервиса необходимо задать значения минимум пяти переменным окружения: `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`, , `DB_HOST`, `DB_PORT`.


2. Запуск - из корневой директории проекта выполните команду:
```bash
docker compose up -d --build
```
Проект будет развернут в четырех docker-контейнерах (db, backend, frontend, nginx) по адресу `http://localhost:80`.

3. Остановить docker и удалить контейнеры можно командой из корневой директории проекта:
```bash
docker compose down
```
Если также необходимо удалить тома базы данных и статики:
```bash
docker compose down -v
```
<hr></details>
<details><summary>Запуск на удаленном сервере</summary>

1. Создайте `Actions.Secrets` согласно списку ниже (значения указаны для примера) + переменные окружения из `env_example` файла:
```py

# Данные удаленного сервера и ssh-подключения:
HOST  # публичный IP-адрес вашего удаленного сервера
USER
SSH_KEY
SSH_PASSPHRASE

#  Переменные для работы с PostgreSQL.
POSTGRES_HOST=db
POSTGRES_DB=postgres
POSTGRES_PORT=5432
POSTGRES_USER=postgres
POSTGRES_PASSWORD=12345

# Переменные для создания суперюзера.
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_EMAIL=admin@admin.com
DJANGO_SUPERUSER_PASSWORD=admpass
```

4. Запустите вручную `workflow`, чтобы автоматически развернуть проект в четырех docker-контейнерах (db, backend, frontend, nginx) на удаленном сервере.
</details>
<hr>

При первом запуске будут автоматически произведены следующие действия:
  * выполнятся миграции БД
  * создастся суперюзер (пользователь с правами админа) с учетными данными из переменных окружения `DJANGO_SUPERUSER_USERNAME`, `DJANGO_SUPERUSER_EMAIL`, `DJANGO_SUPERUSER_PASSWORD`.
  * соберется статика

Вход в админ-зону осуществляется по адресу: http://`hostname`/admin/ , где `hostname`:
  * `localhost`
  * Доменное имя удаленного сервера, например `prosept.hopto.org`

[⬆️Оглавление](#оглавление)



## Удаление:
Для удаления проекта выполните команду:
```bash
cd .. && rm -fr backend
```

[⬆️Оглавление](#оглавление)



## Авторы:

[Vladislav Kuznetsov](https://github.com/VladislavCR)

[German Leontiev](https://github.com/Leontiev93)

[Vladislav Iakovenko](https://github.com/dzheronimo)

[⬆️В начало](#Проект-MSPP)
