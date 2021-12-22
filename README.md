# Description
Скрипт для парсинга сайта OpenCVE и работы в YouTrack
`main.py` - основной скрипт, который заводит задачи в Панель мониторинга YouTrack
`remove_repetitions.py` - скрипт, который удаляет повторяющиеся задачи
`changing_issues.py` - скрипт, который обновляет задачи на основе парсинга сайта OpenCVE

## Install
Для установки запустить 
```pip3 install -r requirements.txt```

## Usage
Перед началом работы необходимо создать файл `.env` и добавить в него необходимые ссылки и креды.

Создать `.env` файл

```sh
touch .env
```

Добавить креды и ссылки в `.env`

```
YOU_TRACK_TOKEN='<YOUR_TOKEN>'
URL1_VAL='<YOUR_URL1>'
URL_VAL='<YOUR_URL>'
USERNAME_VAL='<YOUR_USERNAME>'
PASSWORD_VAL='<YOUR_USERNAME>'
YOU_TRACK_PROJECT_ID = '<YOU_TRACK_PROJECT_ID>'
YOU_TRACK_BASE_URL = '<YOU_TRACK_BASE_URL>'
URL2_VAL = '<YOUR_URL2>'
URL_GET_PRODUCTS = '<URL_GET_PRODUCTS>'
URL_GET_VERSIONS = '<URL_GET_VERSIONS>'
MAIN_URL = "<MAIN_URL>'
```

```
python3 main.py
```


Для автоматической работы скрипта следует использовать `cron`
Например запуск скрипта каждый час:
```
0 * * * * cd parsing_opencve && python3 parsing_opencve/main.py 
```

