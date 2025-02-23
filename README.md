***

# Оглавление
- [Домашняя работа №1](#домашняя-работа-1)
  - [Настройка jupyterhub и Postgres](#1-настройка-jupyterhub-и-postgres)
  - [Скриншоты](#Скриншоты)
  - [Заключение](#Заключение)
- [Домашняя работа №2](#домашняя-работа-2)
  - [Настройка jupyterhub и Postgres](#1-настройка-jupyterhub-и-postgres)
  - [Скриншоты](#Скриншоты)
  - [Заключение](#Заключение)

***

# Домашняя работа №1

## 1. Настройка jupyterhub и Postgres

### 1.1 Сборка кастомного образа jupyterhub.

Был взят базовый образ jupyterhub и на его основе составлен [Dockerfile](https://github.com/Zubaev/jupyterhub_docker_postgres/blob/main/jupyterhub/Dockerfile) для сборки кастомного образа в который добавлены следующие библиотеки:

- **1. oauthenticator** - 
Библиотека для аутентификации пользователей через протокол OAuth2.
Позволяет пользователям авторизовываться через внешние провайдеры (например, GitHub, Google, Microsoft), что упрощает управление учётными записями.
- **3. dockerspawner** - 
Расширение JupyterHub для запуска отдельных Docker-контейнеров для каждого пользователя.
Обеспечивает полную изоляцию рабочих сред пользователей, что особенно важно в многопользовательских системах.
- **4. jupyterhub-nativeauthenticator** - 
Библиотека для локальной аутентификации на основе имени пользователя и пароля.
Полезна для случаев, когда требуется использовать локальные учётные записи без интеграции с внешними провайдерами.
- **5. prometheus-client** - 
Библиотека для интеграции с системой мониторинга Prometheus.
Помогает администраторам собирать метрики производительности и состояния системы, что необходимо для оптимизации работы JupyterHub.
***
Основные методы и настройки Jupyterhub описаны в конфигурационным файлом [jupyterhub_config.py](https://github.com/Zubaev/jupyterhub_docker_postgres/blob/main/jupyterhub/jupyterhub_config.py) который определяет настройки и поведение JupyterHub-сервера.

Аутентификация :
- c.JupyterHub.authenticator_class = NativeAuthenticator: Используется локальный аутентификатор NativeAuthenticator, который позволяет пользователям регистрироваться через форму с логином и паролем.

- c.NativeAuthenticator.open_signup = True: Разрешает новым пользователям самостоятельно регистрироваться на платформе.

- c.JupyterHub.spawner_class = DockerSpawner: Используется спонер DockerSpawner, который запускает отдельный Docker-контейнер для каждого пользователя.

***
**Postgres** взят оффициальный образ postgres:16
***
Для взаимодействия Postgres и Jupyterhub на основе базового образа составлен [Dockerfile](https://github.com/Zubaev/jupyterhub_docker_postgres/blob/main/notebook_custom/Dockerfile.not) для сборки кастомного образа с библиотекой psycopg2-binary которая позволяет сооединяться тетрадкам jupyterhub c Postgres
***

Ниже описан Docker-compose сборки
```yaml
services:
  db_postgres:
    image: postgres:16
    volumes:
    - /var/lib/postgresql/data:/var/lib/postgresql/data
    container_name: zubaev
    environment:
      POSTGRES_USER: zms
      POSTGRES_PASSWORD: 123456
      POSTGRES_DB: test_db
    ports:
      - "5434:5432"
    restart: unless-stopped
    networks:
      - jupyter-network
  jupyterhub:
    build: .
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
      - /srv/jupyterhub/data:/srv/jupyterhub/data
      - ./jupyterhub_config.py:/srv/jupyterhub/jupyterhub_config.py
    ports:
      - "8000:8000"
    networks:
      - jupyter-network
volumes:
  jupyterhub_data:
networks:
  jupyter-network:
    name: jupyter-network
```
***

## 2. Скриншоты

Скриншот регистрации нового пользователя

![2025-02-23_12-15-28](https://github.com/user-attachments/assets/5adf3368-138a-4ee7-bd18-d04762a56f8c)

Список зарегистрированных пользователей 

![2025-02-23_12-22-58](https://github.com/user-attachments/assets/43c0fcd2-d77e-44b6-82ff-9d11ad7a4cd8)

Создание таблицы в Postgres через Jupyterhub 

![2025-02-23_12-40-58](https://github.com/user-attachments/assets/9a935283-c2c0-4817-8a32-accd323e8d9e)


## Заключение
В ходе выполнения домашнего задания мы научились разворачивать jupytehub c возможностью регистрации новых пользователей, а так же подключаться через Jupyterhub к базе данных Postgres и монипулировать данными.


# Домашняя работа №2

ДЗ2. Мониторинг

Дашборд активности пользователей в юпитер (количество операций в день)
Дашборд по топовым тетрадкам (сколько подъедают)
Дашборд топовых таблиц в постресе с их владельцами

Дашборды должны быть публичными


ДЗ2. Настроить алерт при заходе пользователя на сервер по ssh на почту.


ДЗ2. Настроить почтовый алерт при потребление общим количеством контейнеров мощности более чем на 80 % - алертить.

балансировщик

