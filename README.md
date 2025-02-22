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

