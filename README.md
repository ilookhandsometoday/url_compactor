# Сервис для сжатия ссылок
Docker version 24.0.2, build cb74dfc

docker-compose version 1.29.2, build unknown

Версии используемых пакетов прописаны в requirements.txt

Написано под Python 3.10

База данных - PostgreSQL

# Что нужно знать для деплоя
Данные для запуска сервис получает из переменных окружения
URL_COMPACTOR_HOST - хост, на котором будет развернут сервис\
URL_COMPACTOR_PORT - порт на котором будет развернут сервис\
URL_COMPACTOR_DOMAIN - домен, который будет использоваться для создания короткой ссылки (если эта переменная окружения будет равна da.net, то сервис будет генерировать короткие ссылки вида da.net/hkjhl)\
URL_COMPACTOR_DATABASE - URL базы данных, формат: postgresql+asyncpg://{username}:{password}@{host}:{port}/{dbname}\
Если деплой будет в Docker-контейнер, то данные переменные окружения должны быть прописаны в секции environment в docker-compose (либо установлены при запуске контейнера, если не используется compose).

Dockerfile.example можно использовать как готовый Dockerfile, а вот в docker-compose.yml необходимо внести изменения перед docker-compose up -d (если точнее, то нужно поменять переменные окружения в соответствии с их семантикой, описанной выше)

После запуска сервиса, автодокументацию (SWAGGER) можно посмотреть открыв /docs в браузере. На этой же страницe можно поотправлять запросы в сервис

Таблицы в БД заранее нет необходимости; если их нет, сервис на старте сам создаст нужные таблицы.

