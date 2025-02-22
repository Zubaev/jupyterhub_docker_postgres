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

Было решено взять базовый образ jupyterhub и установить в него необходимые нам библиотеки для расширения функциональности JupyterHub. Ниже приведены описания каждой из установленных библиотек:

1. oauthenticator
- Описание : Библиотека, которая предоставляет поддержку аутентификации через протокол OAuth2. Позволяет пользователям авторизовываться через внешние провайдеры, такие как GitHub, Google, Microsoft и другие.
- Назначение : Упрощает процесс управления учётными записями пользователей, позволяя использовать уже существующие аккаунты вместо создания новых.
2. dockerspawner
- Описание : Расширение JupyterHub, которое позволяет запускать отдельные Docker-контейнеры для каждого пользователя при их входе в систему.
- Назначение : Обеспечивает изоляцию рабочих сред пользователей, что особенно важно в многопользовательских системах.
3. jupyterhub-nativeauthenticator
- Описание : Библиотека, предоставляющая простой механизм локальной аутентификации на основе имени пользователя и пароля.
- Назначение : Полезна для случаев, когда требуется использовать локальные учётные записи без интеграции с внешними провайдерами аутентификации.
4. prometheus-client
- Описание : Библиотека для интеграции с системой мониторинга Prometheus. Позволяет собирать метрики производительности и состояния JupyterHub.
- Назначение : Помогает администраторам отслеживать работу системы, выявлять проблемы и оптимизировать её производительность.

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

