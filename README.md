***

# Оглавление
- [Домашняя работа №1](#домашняя-работа-1)
  - [Настройка jupyterhub и Postgres](#1-настройка-jupyterhub-и-postgres)
  - [Скриншоты](#2-Скриншоты)
  - [Заключение](#Заключение)
- [Домашняя работа №2](#домашняя-работа-2)
  - [Настройка jupyterhub и Postgres](#1-настройка-jupyterhub-и-postgres)
  - [Скриншоты](#Скриншоты)
  - [Заключение](#Заключение)

***

# Домашняя работа №1
***
Необходимо:

1. Развернуть jupyterhub и Postgres.

2. Зарегестрировать 3 пользователей в jupyterhub.

3. Настроить соеденение Postgres с jupyterhub с помощью библиотеки psycopg2
***

## 1. Настройка jupyterhub и Postgres

### 1.1 Сборка кастомного образа jupyterhub.

Был взят базовый образ jupyterhub и на его основе составлен [Dockerfile](https://github.com/Zubaev/jupyterhub_docker_postgres/blob/main/jupyterhub/Dockerfile) для сборки кастомного образа в который добавлены следующие библиотеки:

**1. ``oauthenticator``** - 
Библиотека для аутентификации пользователей через протокол OAuth2.
Позволяет пользователям авторизовываться через внешние провайдеры (например, GitHub, Google, Microsoft), что упрощает управление учётными записями.

**3. `dockerspawner`** - 
Расширение JupyterHub для запуска отдельных Docker-контейнеров для каждого пользователя.
Обеспечивает полную изоляцию рабочих сред пользователей, что особенно важно в многопользовательских системах.

**4. `jupyterhub-nativeauthenticator`** - 
Библиотека для локальной аутентификации на основе имени пользователя и пароля.
Полезна для случаев, когда требуется использовать локальные учётные записи без интеграции с внешними провайдерами.

**5. `prometheus-client`** - 
Библиотека для интеграции с системой мониторинга Prometheus.
Помогает администраторам собирать метрики производительности и состояния системы, что необходимо для оптимизации работы JupyterHub.
***
Основные методы и настройки Jupyterhub описаны конфигурационным файлом [jupyterhub_config.py](https://github.com/Zubaev/jupyterhub_docker_postgres/blob/main/jupyterhub/jupyterhub_config.py) который определяет настройки и поведение JupyterHub-сервера.

Аутентификация :
- `c.JupyterHub.authenticator_class` = `NativeAuthenticator`: Используется локальный аутентификатор `NativeAuthenticator`, который позволяет пользователям регистрироваться через форму с логином и паролем.

- `c.NativeAuthenticator.open_signup` = `True`: Разрешает новым пользователям самостоятельно регистрироваться на платформе.

- `c.JupyterHub.spawner_class` = `DockerSpawner`: Используется спонер DockerSpawner, который запускает отдельный Docker-контейнер для каждого пользователя.

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

***
Настроить Мониторинг.

- Дашборд активности пользователей в юпитер (количество операций в день)

- Дашборд по топовым тетрадкам (сколько подъедают)

- Дашборд топовых таблиц в постресе с их владельцами

Настроить алерты.

- Настроить алерт при заходе пользователя на сервер по ssh на почту.

- Настроить почтовый алерт при потребление общим количеством контейнеров мощности более чем на 80 % - алертить.

***


Для сбора метрик и их экспорта, а так же визуализации будем использовать следующие инстументы:

`Prometheus` - Система мониторинга и сбора метрик. Является одним из самых популярных решений для мониторинга.

`prometheuscommunity/postgres-exporter:v0.10.0` - Exporter для сбора метрик PostgreSQL. Преобразует статистику PostgreSQL в формат, понятный Prometheus.

`jupyterhub-metrics-exporter` - Кастомный [exporter](notebook_metrics/jupyterhub_notebook_files_metrics.py) который собирает данные о размерах тетрадок jupyterhub и преобразует их в формат Prometheus.

`gcr.io/cadvisor/cadvisor:latest` - Инструмент для анализа использования ресурсов и выполнения контейнеров. Автоматически обнаруживает все контейнеры на хосте и собирает статистику об их работе.

для построения дашбордов 

`Grafana` - Платформа для визуализации данных и создания дашбордов. Поддерживает множество источников данных, включая Prometheus.

Для алертов

`prom/alertmanager:v0.25.0` - Система управления оповещениями для Prometheus. Обрабатывает алерты, отправляемые Prometheus, и доставляет их через различные каналы (email, Slack, PagerDuty и др.).

***

Допишем все необходимые образы в [Docker-compose](https://github.com/Zubaev/jupyterhub_docker_postgres/blob/main/docker-compose.yaml) 

Пропишем все необходимые jobs в конфигурационный файл [prometheus.yml](https://github.com/Zubaev/jupyterhub_docker_postgres/blob/main/prometheus/prometheus.yml)

Для `prometheuscommunity/postgres-exporter:v0.10.0` необходимо настроить файл [queries.yaml](https://github.com/Zubaev/jupyterhub_docker_postgres/blob/main/postgres-exporter/queries.yaml) который содержит конфигурацию будущей метрики и запрос в базу данных

Для `prom/alertmanager:v0.25.0` необходимо так же настроить файлы [alertmanager.yml](https://github.com/Zubaev/jupyterhub_docker_postgres/blob/main/alerts/alertmanager.yml)


```yaml
smarthost: 'smtp.yandex.ru:587' #это протокол передачи почты
    auth_username: 'magazubaev92@yandex.ru' #почта с которой будут отправляться уведомления
    auth_password: '**пароль-приложение** ' #пароль приложение необходимо сгенерировать для почты
```

[example.rules.yml](https://github.com/Zubaev/jupyterhub_docker_postgres/blob/main/alerts/example.rules.yml) 

```yaml
    expr: sum(rate(container_cpu_usage_seconds_total{image!=""}[1m])) * 100 > 80 #Если общее использование CPU превышает 80%, срабатывает алерт.
```
Проверим работу всех exporter в prometheus/target

![2025-02-23_16-55-41](https://github.com/user-attachments/assets/93feb05f-444b-40b0-9834-63a406e45147)



