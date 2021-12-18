# parsing_OpenCVE_for_YouTrack
Скрипт позволяет заводить задачи в Панель мониторинга YouTrack на основе парсинга сайта OpenCVE

## Использование
Перед началом работы необходимо создать файл `.env` и добавить в него необходимые ссылки и креды.

Создать `.env` файл

```sh
touch .env
```

Добавить креды и ссылки в `.env`

```
YOU_TRACK_TOKEN='<YOUR_TOKEN>'
URL1_VAL='<YOUR_URL1>'
URL_VAL='<YOUR_URL1>'
USERNAME_VAL='<YOUR_USERNAME>'
PASSWORD_VAL='<YOUR_USERNAME>'
```
 

Для автоматической работы скрипта следует использовать `cron`
