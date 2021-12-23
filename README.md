# Description
Скрипт для парсинга сайта OpenCVE и работы в YouTrack
```
main.py - основной скрипт, который заводит задачи в Панель мониторинга YouTrack
remove_repetitions.py - скрипт, который удаляет повторяющиеся задачи
changing_issues.py - скрипт, который обновляет задачи на основе парсинга сайта OpenCVE
```

## Usage
Перед началом работы необходимо создать файл `.env` и добавить в него необходимые ссылки и креды.

Создать `.env` файл

```sh
touch parsing_OpenCVE_for_YouTrack/app/.env
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

## Install
Для установки запустить
```shell
git clone https://github.com/eeenvik1/parsing_OpenCVE_for_YouTrack.git
cd parsing_OpenCVE_for_YouTrack
docker build -t <SET_IMAGE_NAME> .
docker run --name <SET_CONTAINER_NAME> -e PYTHONUNBUFFERED=1 <IMAGE_NAME>
```

## Usage
```shell
docker start <CONTAINER_NAME>
```


## Example
Пример работы скрипта main.py
![alt text](https://github.com/eeenvik1/parsing_OpenCVE_for_YouTrack/blob/main/exmple_youtrack(main.py).png?raw=true)
