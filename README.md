# BMS Buy Bot

### Бот для автоматической покупке проходок на майнкрафт сервер (в моем случае BMS) c авто добавлением в вайт лист

---

## Установка модулей

- успользуя pip requirements.txt

```
$ pip install -r requirements.txt
```

- успользуя pip устанавливая по отдельности каждый модуль

```
$ pip install disnake
```

```
$ pip install pypayment
```

```
$ pip install paramiko
```

---

# Добавления в вайт лист

Сразу скажу, что мне не удавалось нормально установить подлключения по RCON и поэтому прибег к костылю, с подключением по ftp, получения файла, его редактированию и перезаписью через ftp.

```python
/sftp.py # в данном файле храниться весь код для подключения и передачи файлов

/MCApi.py # а здесь находиться функция для добавления в ВЛ
```

### Получить/Отправить файл

```python
download_file_sftp(hostname, port, username, password, remote_filepath, local_filepath)
upload_file_sftp(hostname, port, username, password, local_filepath, remote_filepath)

# hostname - ip адрес хоста
# port - порт
# username - имя пользователя
# password - пароль
# local_filepath - локальный путь
# remote_filepath - путь на хосте
```

### Добавить в вайтлист

```python
whitelist_add(nick, uuid)
# nick - ник
# uuid - тут понятно
```

- Не забудьте изменить данные сервера в `config.py`

# Оплата

Оплату реализовал с помощью сервиса PayOk.

```python
/payment.py # код для оплаты и обратки платежей
```

### Создать платеж

```python
create_pay(amount, description)
# amount - сумма
# description - описание
```

### Проверить платеж

```python
check_pay()
```

---

- Не забудьте изменить данные в `config.py`

# БазаДанных

Казалось бы, зачем нужна БД в данном боте? Но есть один случай, чтобы в нее записывался никнейм и id пользователя дискорд который на этот ник покупет проходку. Это нужно, если несколько игроков одновремено совершают покупку и их никнеймы не перемещались (в случае с переменными)

```python
/sqlApi.py # код для работы с БД
```

### Выбрать никнейм из id

```python
select_nick_from_db(id)
# id - id пользователя дискорд
```

### Добавить в БД

```python
add_to_db(id, nickname)
# id - id пользователя дискорд
# nickname - ник из базы
```

# McApi

Скрип для добавления в вайтлист, получения uuid и отправки на сервер по ftp

```python
/MCApi.py # код со всеми выше перечислеными функциями
```

### Получить uuid

```python
get_uuid(username)
# username - ник по которому получать uuid
```

### Добавить ник в ВЛ

```python
add_to_json(uuid, nickname) # сначала добавляем в whitelist.json
whitelist_add(uuid, nickname) # потом отправляем на сервер

# uuid - uuid
# nickname - никнейм
```

Не забудьте изменить данные в `config.py`

# Discord Бот

Основной код бота

```python
/main.py # основной код
```

Не забудьте изменить данные в `config.py`
