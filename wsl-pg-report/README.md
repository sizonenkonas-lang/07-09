# Отчёт: развёртывание WSL + SDK + PostgreSQL

## 1. Установка WSL и Ubuntu 24.04
Установка компонентов WSL и дистрибутива Ubuntu через PowerShell.
![wsl-1](screens/01-wsl-1.png)
![wsl-2](screens/01-wsl-2.png)
![wsl-3](screens/01-wsl-3.png)
![wsl-4](screens/01-wsl-4.png)

## 2. Создание пользователя sizonenko-a-s

Создан пользователь по шаблону фамилия-инициалы, настроен пароль и sudo.
Создание пользователя - ввод логина 
![user-1](screens/02-user-1.png)
![user-2](screens/02-user-2.png)

Первый вход в систему и настройка прав sudo (исправление ошибки с паролем через root)
![user-3](screens/02-user-3.png)

Успешный вход под созданным пользователем.
![user-4](screens/02-user-4.png)

Проверка работы sudo - обновление списка пакетов
![user-5](screens/02-user-5.png)

## 3. Обновление системы

Проверка текущей даты и времени в системе
![apt-1](screens/03-apt-1.png)

Обновление списка пакетов и установка обновлений (команда 'apt upgrade').
![apt-2](screens/03-apt-2.png)

Завершение процесса обновления.
![apt-3](screens/03-apt-3.png)

Установка базовых утилит (build-essential, git и др.)
![apt-4](screens/03-apt-4.png)

Завершение процесса обновления
![apt-5](screens/03-apt-5.png)

## 4. SDK / интерпретатор Python
Установка Python 3, менеджера пакетов pip и модуля venv.
![sdk-1](screens/04-sdk-1.png)

Процесс распаковки и настройки пакетов Python.
![sdk-2](screens/04-sdk-2.png)

Проверка установки - вывод версий Python и pip.
![sdk-3](screens/04-sdk-3.png)

## 5. СУБД PostgreSQL
Установка PostgreSQL и дополнительных утилит (команда 'apt install').
![pg-1](screens/05-pg-1.png)

Процесс распаковки и первичной инициализации кластера базы данных.
![pg-2](screens/05-pg-2.png)

Проверка статуса службы PostgreSQL (статус 'active', ошибок нет).
![pg-3](screens/05-pg-3.png)
![pg-4](screens/05-pg-4.png)

Проверка установленной версии PostgreSQL 
![pg-5](screens/05-pg-5.png)

## 6. Создание БД и проверка подключения 
Создание пользователя БД 'myuser' и базы данных 'testdb'.
![db-1](screens/06-db-1.png)
![db-2](screens/06-db-2.png)

Вывод списка баз данных (команда '\l') - база 'testdb' успешно создана.
![db-3](screens/06-db-3.png)
![db-4](screens/06-db-4.png)

Подключение к базе 'testdb' от имени пользователя 'meuser' и проверка версии ('SELECT version();').
![db-5](screens/06-db-5.png)
![db-6](screens/06-db-6.png)

## 7. Создание MD файла для отчета
Создание папки для проекта и папки для картинок.
![pic-1](screens/07-pic-1.png)

Пустое окно текстового редактора.
![pic-2](screens/07-pic-2.png)

Готовый отчет.
![pic-3](screens/07-pic-3.png)

