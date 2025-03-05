***

# Оглавление
- [Домашняя работа №1](#домашняя-работа-1)
  - [Настройка jupyterhub и Postgres](#1-настройка-jupyterhub-и-postgres)
  - [Скриншоты](#2-Скриншоты)
  - [Заключение](#Заключение)
- [Домашняя работа №2](#домашняя-работа-2)
  - [1.Используемые инструменты для мониторинга, сбора метрик и визуализации.](#1-Конфигурация-системы-мониторинга-на-базе-Prometheus-и-Grafana)
  - [2. Добавление сервисов в Docker Compose](#2-Добавление-сервисов-в-Docker-Compose)
  - [3. Дашборды](#3-Дашборды)
    - [3.1 Дашборд Активности пользователей и Размера тетрадок Jupyterhub.](#31-Дашборд-Активности-пользователей-и-Размера-тетрадок-Jupyterhub)
    - [3.2 Дашборд размера таблиц в PostgreSQL.](#32-Дашборд-размера-таблиц-в-PostgreSQL)
    - [3.4 Дашборд используемых ресурсов контейнерами](#34-Дашборд-используемых-ресурсов-контейнерами)
  - [4. Алерты](#4-Алерты)
    - [4.1 Алерт использования CPU на 80%](#41-Алерт-использования-CPU-на-80)
    - [4.2 Алерт входа по SSH на сервер.](#42-Алерт-входа-по-SSH-на-сервер)
  - [Итог](#Итог)

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

Соберем [docker-compose](https://github.com/Zubaev/jupyterhub_docker_postgres/blob/main/jupyterhub/docker-compose.yaml) файл с необходимыми настройками.
Контейнеры добавим в общую сеть `jupyter-network` 

Запустим сборку командой `docker-compose up -d` 

<img width="671" alt="Снимок экрана 2025-03-05 224350" src="https://github.com/user-attachments/assets/6ed08900-cacd-481a-a91c-6ee0ccb366d9" />

Если все сделано правильно `Jupyterhub` будем доступен по адресу  


`http://localhost:8000`

![2025-03-05_23-05-46](https://github.com/user-attachments/assets/8f593a5e-277d-4c44-9a3f-0dc4f60c66c5)


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
## Техническое задание

### Настроить Мониторинг.

- Дашборд активности пользователей в юпитер (количество операций в день)

- Дашборд по топовым тетрадкам (сколько подъедают)

- Дашборд топовых таблиц в постресе с их владельцами
  
- Дашборды должны быть публичными

### Настроить алерты.

- Настроить алерт при заходе пользователя на сервер по ssh на почту.

- Настроить почтовый алерт при потребление общим количеством контейнеров мощности более чем на 80 % - алертить.

***
## 1. Конфигурация системы мониторинга на базе Prometheus и Grafana.

Для сбора метрик и их экспорта, а так же визуализации будем использовать следующие образы:

`Prometheus` - Основной инструмент для сбора и хранения метрик от различных источников.

`Grafana` - Платформа для визуализации данных и создания дашбордов. Поддерживает множество источников данных, включая Prometheus.

`prometheuscommunity/postgres-exporter:v0.10.0` - Exporter для сбора метрик PostgreSQL. Преобразует статистику PostgreSQL в формат, понятный Prometheus.

`jupyterhub-metrics-exporter` - Кастомный [exporter](notebook_metrics/jupyterhub_notebook_files_metrics.py) который собирает данные о размерах тетрадок jupyterhub и преобразует их в формат понятный Prometheus.

`gcr.io/cadvisor/cadvisor:latest` - Мониторинг потребления ресурсов (CPU, память, диск, сеть) для всех контейнеров на хост-машине.

Для алертов

`prom/alertmanager:v0.25.0` - Система управления оповещениями для Prometheus. Обрабатывает алерты, отправляемые Prometheus, и доставляет их через различные каналы (email, Slack, PagerDuty и др.).

***
## 2. Добавление сервисов в Docker Compose

1. Для создания полнофункциональной системы мониторинга на основе `Prometheus` и `Grafana` допишем все необходимые образы в [Docker-compose](https://github.com/Zubaev/jupyterhub_docker_postgres/blob/main/docker-compose.yaml) 

2. Для корректной работы `Prometheus` необходимо определить все `scrape jobs` в файле **[prometheus.yml](https://github.com/Zubaev/jupyterhub_docker_postgres/blob/main/prometheus/prometheus.yml)**. Этот файл определяет, какие сервисы и эндпоинты Prometheus должен мониторить для сбора метрик. 

3. Для работы с образом **`prometheuscommunity/postgres-exporter:v0.10.0`** требуется настроить файл **`queries.yaml`**. Этот файл содержит конфигурацию пользовательских метрик и SQL-запросы, которые будут выполняться для сбора данных из базы данных PostgreSQL. (Взял старую версию v0.10.0 так-как **`queries.yaml`** не используется в последних версиях)

**[queries.yaml](https://github.com/Zubaev/jupyterhub_docker_postgres/blob/main/postgres-exporter/queries.yaml)**
```yaml

table_sizes:  #название метрики
  query: |; #содержит запрос в базу даных                 
  metrics:    #Определение метрик, которые будут использоваться для обработки и представления данных, полученных из запроса.
    - schema_name:             
        usage: "LABEL"
        description: "Name of the schema"

```

4. Для `prom/alertmanager:v0.25.0` необходимо настроить файлы **`alertmanager.yml`** и **`example.rules.yml`**

- `alertmanager.yml` : Отвечает за управление и доставку алертов (кому и как отправлять уведомления).

- `example.rules.yml` : Определяет условия для генерации алертов (когда и почему срабатывает алерт).

[alertmanager.yml](https://github.com/Zubaev/jupyterhub_docker_postgres/blob/main/alerts/alertmanager.yml)
```yaml
  email_configs:
  - to: 'magazubaev92@gmail.com' #Почта получателя Алерта 
    from: 'magazubaev92@yandex.ru' #Почта с которой будет отправляться Алерт
    smarthost: 'smtp.yandex.ru:587' # Адрес SMTP-сервера и порт для отправки писем
    auth_username: 'magazubaev92@yandex.ru'  # Электронная почта, с которой будут отправляться уведомления
    auth_password: 'Пароль приложения' # Пароль приложения (необходимо сгенерировать в настройках аккаунта Yandex)
```

[example.rules.yml](https://github.com/Zubaev/jupyterhub_docker_postgres/blob/main/alerts/example.rules.yml)

```yaml
    expr: sum(rate(container_cpu_usage_seconds_total{image!=""}[1m])) * 100 > 80 #Если общее использование CPU превышает 80%, срабатывает алерт.
```

Соберем наш образ командой  `Docker-compose up -d`
И убедимся, что все работает.
<img width="392" alt="Снимок экрана 2025-02-23 175244" src="https://github.com/user-attachments/assets/04073b3f-ac46-4264-a83d-3dda058ecd2d" />

Проверьте работу: 

- `Prometheus` по адресу `http://localhost:9090`

- `Grafana` по адресу `http://localhost:3000`

Чтобы войти в `Grafana` по умолчанию используется ЛОГИН `admin` ПАРОЛЬ `admin` после система предложит вам изменить пароль (если при сборке образа вы не задали другие учетные данные)
![2025-02-24_11-56-12](https://github.com/user-attachments/assets/3ab2ec7e-14e9-44a8-a485-b30b0319de57)


Проверим работу всех exporter в `prometheus`.

`http://localhost:9090/targets`

Убедимся, что `State` у всех `exporter` имеет статус UP (значит все `exporter` передают наши метрики в `prometheus`)

![2025-02-23_18-27-32](https://github.com/user-attachments/assets/8e433c92-d37c-484c-8c7a-1a70c54e23a6)

Переходим в `http://localhost:9090/alerts` и проверяем добавился ли наш алерт 
![2025-02-23_19-16-00](https://github.com/user-attachments/assets/f48c656f-2c6f-4d11-9bce-6cd5ff576261)


Добавим источник данных в `Grafana` заходим в раздел `Data sources` и добавляем  `prometheus` в графе `Connection` прописываем `host` и `port`
![2025-02-23_18-13-37](https://github.com/user-attachments/assets/54177072-c343-412d-853e-1e9d31f0dc6d)
наши контейнеры находятся в общей сети `jupyter-network` поэтому обращаемся по названию конрейнера и порту(если контейнеры находятся в разных сетях обращаться необходимо по IP либо localhost и внешнему порту который вы прокинули наружу).

Добавим дашборд для проверки работоспособности:

1. Выберем раздел `dashboards`
2. Add visualization (Если хотеите импортировать какой то определенный дашборд шелкаем `Import a dashboard` и импортируем необходимы дашборд)
![2025-02-24_12-10-38](https://github.com/user-attachments/assets/ca8e9add-ed83-4af2-b231-185a79ee395a)

Визуализация метрики:

1. Выбираем метрику.
2. Выбираем `Legend` подпись для графиков
3. Установим необходимую единицу измерения
![2025-02-24_12-15-12](https://github.com/user-attachments/assets/2f38bb9d-f716-448d-8153-49341a42f01d)


## 3. Дашборды
### 3.1 Дашборд Активности пользователей и Размера тетрадок Jupyterhub.

Метрики:
- `jupyterhub_total_users` - количество зарегистрированых пользователей
- `jupyterhub_active_users{period="24h"}` - количество активных пользователей за 24 часа
- `jupyterhub_running_servers` - количество запушенных серверов
- `sum(jupyterhub_request_duration_seconds_count)` - количество запросов
- `jupyterhub_notebook_file_size_bytes` - кастомная метрика [exporter](notebook_metrics/jupyterhub_notebook_files_metrics.py) которая передает размеры тетрадок jupyterhub

[публичная ссылка на дашборд](http://grafana.zmshardbro.keenetic.name/public-dashboards/ae9326c461d24592882e0aa162dbc6fc)

![2025-02-23_18-56-03](https://github.com/user-attachments/assets/81e2b3ae-ae0b-46a5-91f7-cdb752cb10c0)

### 3.2 Дашборд размера таблиц в PostgreSQL.

Гистограмы отражают топ 10 самых больших таблиц и их пользователей в моем случае таблицы 4 поэтому показано только 4.

На графике отражается динамика добавления данных в таблицы, когда и сколько килобайт данных добавлены в таблицу.

Метрика:
- `table_sizes_size_bytes` - была определена внутри **[queries.yaml](https://github.com/Zubaev/jupyterhub_docker_postgres/blob/main/postgres-exporter/queries.yaml)**

[публичная ссылка на дашборд](http://grafana.zmshardbro.keenetic.name/public-dashboards/6dfa9d32535d404091b5f09669a28926)

![2025-02-23_18-35-23](https://github.com/user-attachments/assets/816040f1-cc21-482e-b293-d107974da18e)

### 3.4 Дашборд используемых ресурсов контейнерами 

Метрика - Описание(Название графика)

`sum(rate(container_cpu_usage_seconds_total{name=~".+"}[5m])) by (name) * 100` - среднее использование CPU для каждого контейнера в процентах за последние 5 минут. (**CPU Usage**)

`sum(container_memory_rss{name=~".+"}) by (name)` - суммарный объем физической памяти используемый каждым контейнером. (**Memory Usage**)

`sum(container_memory_cache{name=~".+"}) by (name)` - суммарный объем памяти кэша , используемый каждым контейнером. (**Memory Cashed**)

`sum(rate(container_network_receive_bytes_total{name=~".+"}[5m])) by (name)` - отражает общее количество байтов, принятых контейнером через сеть с момента его запуска. (**Received Network Traffic**)

`sum(rate(container_network_transmit_bytes_total{name=~".+"}[5m])) by (name)` - суммарная скорость передачи данных (в байтах в секунду) через сеть для всех контейнеров за последние 5 минут. (**Sent Network Traffic**)

`(time() - container_start_time_seconds{name=~".+"})/86400` - время работы контейнера в днях. (**Containers Info**)

[Ссылки на публичный дашборд](http://grafana.zmshardbro.keenetic.name/public-dashboards/a333d210bd0a4308be838a6eb252d0e1)

![2025-02-27_05-07-23](https://github.com/user-attachments/assets/9f9d5161-6a8b-475f-8a25-430de7527c64)


## 4. Алерты

### 4.1 Алерт использования CPU на 80%

Проверим приходят ли оповещения, для проверки работоспособности я временно снизил парог чтобы при загрузке 30% приходил алерт, все работает!)
![2025-02-23_19-18-26](https://github.com/user-attachments/assets/87da2c50-77d6-40f7-898e-9194b626afd1)


### 4.2 Алерт входа по SSH на сервер.

1. установим необходимые зависимости
```
sudo apt-get install postfix mailutils -y
```
2. Настройка Postfix
Создайте файл паролей:
```
sudo nano /etc/postfix/sasl_passwd
```

Перед настройкой Postfix необходимо иметь пароль приложения. Это делается в разделе безопасности вашей учетной записи почты.

`'smtp.yandex.ru:587'` - Адрес SMTP-сервера и порт для отправки писем

<img width="568" alt="Снимок экрана 2025-02-24 135449" src="https://github.com/user-attachments/assets/69fc55ed-a9be-4f90-bf06-bf948a371ab8" />


Сохраните изменения, а затем измените разрешения файла, так чтобы его мог просматривать только пользователь root:
```
sudo chmod 600 /etc/postfix/sasl_passwd  
```

Откройте основной файл конфигурации Postfix:
```
sudo nano /etc/postfix/main.cf 
```

В файле main.cf найдите параметр relayhost и измените строку на:
```bash
relayhost = [smtp.yandex.ru]:587 #если вы используете yandex
```

Ниже этой строки добавьте следующее:
```bash
relayhost = [smtp.yandex.ru]:587

smtp_use_tls = yes
smtp_sasl_auth_enable = yes
smtp_sasl_security_options =
smtp_sasl_password_maps = hash:/etc/postfix/sasl_passwd
smtp_tls_CAfile = /etc/ssl/certs/ca-certificates.crt

mynetworks = [::ffff:127.0.0.0]/104 [::1]/128 #эти строки неоходимо заменить
mailbox_size_limit = 0 #эти строки неоходимо заменить
recipient_delimiter = + #эти строки неоходимо заменить
inet_interfaces = all #эти строки неоходимо заменить
inet_protocols = ipv4 #эти строки неоходимо заменить
```

Далее нужно скомпилировать и хешировать содержимое файла sasl_password, который мы создали ранее, с помощью команды:
```
sudo postmap /etc/postfix/sasl_passwd
```
Перезапустите Postfix:

```
sudo systemctl restart postfix  
```

Включите Postfix для запуска при старте:

```
sudo systemctl enable postfix
```

3. Создание оповещения о входе по SSH

Введите команду:
```
sudo nano /etc/profile
```

В конце файла добавьте следующее:

```bash
if [ -n "$SSH_CLIENT" ]; then
    TEXT="$(date): ssh login to ${USER}@$(hostname -f)"
    TEXT="$TEXT from $(echo $SSH_CLIENT | awk '{print $1}')"
    echo "$TEXT" | mail -s "ssh login" magazubaev92@gmail.com -a "From:magazubaev92@yandex.ru"
fi

```
`magazubaev92@gmail.com` - почта получателя
`magazubaev92@yandex.ru` - почта отправителя

Проверяем работоспособность
![2025-02-24_14-13-08](https://github.com/user-attachments/assets/d8743948-12eb-4c5e-a92e-d7caa1ba4f7b)

# Итог

В рамках выполнения второго домашнего задания мы приобрели практические навыки в настройке комплексной системы мониторинга, основанной на следующих ключевых компонентах:

`Prometheus` : Изучили основы конфигурации `Prometheus` для сбора и хранения метрик различных сервисов. Настроили `scrape jobs` для сбора данных с разных источников.

`Grafana` : Научились создавать дашборды для визуализации собранных метрик, что позволяет эффективно анализировать состояние системы и выявлять тренды.

Система оповещений : Реализовали настройку `Alertmanager` для автоматического реагирования на критические ситуации. Настроили правила алертов, которые позволяют своевременно получать уведомления о проблемах на почту.
В результате работы мы создали полноценную инфраструктуру мониторинга, способную обеспечивать прозрачность производительности системы, оперативное обнаружение проблем и автоматическое информирование ответственных лиц о чрезвычайных ситуациях.
