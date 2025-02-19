Техническое задание

Мониторинг

1. Дашборд активности пользователей в юпитер (количество операций в день)
2. Дашборд по топовым тетрадкам (сколько подъедают).
   
2.1 Для вычисления подъедаемой памяти ноутбуками пришлось воспользоваться самодельным exporter (Благо базовые знания python в сумме с ИИ) родили сей 
[чудо](https://github.com/Zubaev/jupyterhub_docker_postgres/blob/main/notebook_metrics/jupyterhub_notebook_files_metrics.py) на свет, он не идеален в прод врядли пойдет, но я его все равно люблю)))) как он работает можно разобраться по коментариям в самом скрипте
![jupyter](https://github.com/user-attachments/assets/7f9e683e-f394-45a3-a859-d0ee179101d8)

4. Дашборд топовых таблиц в постресе с их владельцами
![1 дашборд постгрес](https://github.com/user-attachments/assets/1c9805fa-2e1a-4612-b70a-de6cdc937efd)
![размер таблиц дебивер 2](https://github.com/user-attachments/assets/0c3dbace-0aa8-4fb4-b347-bab08db2a06d)

5. Дашборды должны быть публичными
6. Настроить алерт при заходе пользователя на сервер по ssh на почту.
![Алерт ssh](https://github.com/user-attachments/assets/d3987bad-17f4-4622-bddb-4a897e64dfc5)


7. Настроить почтовый алерт при потребление общим количеством контейнеров мощности более чем на 80 % - алертить.
![Алерт загрузки ЦПУ](https://github.com/user-attachments/assets/aac5aaa4-8f24-4eb4-894e-c34b4830e004)
