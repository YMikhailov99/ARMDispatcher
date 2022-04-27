# АРМ Диспетчера

Все атрибуты строки подключения к ДБ и сама строка в docker-compose.yml  

Логин/пароль админа АРМа по умолчанию в CRUD.queries в функции check_admin.  
Логин: Admin  
Пароль: demo-123

## Сборка

    docker-compose build

## Запуск

    docker-compose up
## API звонка
POST-запрос на 

    {host}/incoming_call?barrier_number=barrier_uid
Отправлять при поступлении звонка.