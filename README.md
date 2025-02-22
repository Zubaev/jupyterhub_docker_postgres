# Оглавление
- [Домашняя работа №1](#домашняя-работа-1)
  - [Настройка jupyterhub и Postgres](#настройка-jupyterhub-и-postgres)
  - [Подзаголовок 1.2](#подзаголовок-12)
- [Заголовок 2](#заголовок-2)


вцвцвцвцв
цвцвцв


цвцвцвцвцв



цвцвцвцвц



цвцвцвц




цвцв
# Домашняя работа №1
[c;s[c;
[c;[sc;

s;c[sc;


sc;[sc;s


цвцв


цвцвцв


цвцвцв



цвцвцвцвц


цвцвцвц


цвцвцвцв



цвцвцвцв



цвцвцв

cs;[c;s[c;
## Настройка jupyterhub и Postgres

За онову взят базовый образ jupyterhub и установить в него необходимые нам библиотеки для расширения функциональности JupyterHub. Ниже приведены описания каждой из установленных библиотек:

В образ добавлены следующие библиотеки, каждая из которых выполняет свою уникальную роль:

1. oauthenticator

Описание : Библиотека для аутентификации пользователей через протокол OAuth2.
Назначение : Позволяет пользователям авторизовываться через внешние провайдеры (например, GitHub, Google, Microsoft), что упрощает управление учётными записями.

3. dockerspawner

Описание : Расширение JupyterHub для запуска отдельных Docker-контейнеров для каждого пользователя.
Назначение : Обеспечивает полную изоляцию рабочих сред пользователей, что особенно важно в многопользовательских системах.

4. jupyterhub-nativeauthenticator

Описание : Библиотека для локальной аутентификации на основе имени пользователя и пароля.
Назначение : Полезна для случаев, когда требуется использовать локальные учётные записи без интеграции с внешними провайдерами.

5. prometheus-client

Описание : Библиотека для интеграции с системой мониторинга Prometheus.
Назначение : Помогает администраторам собирать метрики производительности и состояния системы, что необходимо для оптимизации работы JupyterHub.

[Dockerfile](https://github.com/Zubaev/jupyterhub_docker_postgres/blob/main/jupyterhub/Dockerfile)

[jupyterhub_config.py](https://github.com/Zubaev/jupyterhub_docker_postgres/blob/main/jupyterhub/jupyterhub_config.py)

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

