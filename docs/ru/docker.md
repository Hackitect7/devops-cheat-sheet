# 🐳 Шпаргалка по Docker

> 📘 Docker — это изолированные контейнеры для запуска приложений. Здесь собраны команды для работы с образами, контейнерами, сетями, томами, а также Docker Compose и Swarm.

---

## 📂 Содержание

- [🐳 Шпаргалка по Docker](#-шпаргалка-по-docker)
  - [📂 Содержание](#-содержание)
  - [📦 Основные команды](#-основные-команды)
  - [🔁 Управление контейнерами](#-управление-контейнерами)
  - [🧱 Образы и Dockerfile](#-образы-и-dockerfile)
  - [🔌 Сети и тома](#-сети-и-тома)
  - [🧩 Плагины Docker](#-плагины-docker)
  - [📋 Docker Compose](#-docker-compose)
  - [📤 Экспорт и импорт](#-экспорт-и-импорт)
  - [🧹 Очистка и диагностика](#-очистка-и-диагностика)
  - [🐝 Docker Swarm](#-docker-swarm)
  - [💼 Продвинутое использование Docker](#-продвинутое-использование-docker)
    - [🚀 Профессиональные команды Docker](#-профессиональные-команды-docker)
    - [🛠 Полезные практики и автоматизация Docker](#-полезные-практики-и-автоматизация-docker)
    - [🐞 Отладка и профилирование контейнеров Docker](#-отладка-и-профилирование-контейнеров-docker)
  - [💼 Продвинутое использование Docker Compose](#-продвинутое-использование-docker-compose)
    - [🚀 Профессиональные команды Docker Compose](#-профессиональные-команды-docker-compose)
    - [🛠 Полезные практики и автоматизация с Docker Compose](#-полезные-практики-и-автоматизация-с-docker-compose)
    - [🐞 Отладка и профилирование сервисов в Docker Compose](#-отладка-и-профилирование-сервисов-в-docker-compose)
  - [Дополнительные ресурсы](#дополнительные-ресурсы)
    - [🚫 Игнорирование файлов с помощью `.dockerignore`](#-игнорирование-файлов-с-помощью-dockerignore)
    - [⚡ Упрощение команд с помощью алиасов](#-упрощение-команд-с-помощью-алиасов)
    - [🧠 Подсказка: советы по работе с Docker](#-подсказка-советы-по-работе-с-docker)
    - [🌐 Полезные ссылки](#-полезные-ссылки)

---

## 📦 Основные команды

| Команда | Пример | Описание |
| ------- | ------ | -------- |
| [**`docker`**](https://docs.docker.com/reference/cli/docker/) | | **Главная команда для работы с Docker. Используется для запуска подкоманд и управления контейнерами, образами, сетями и томами** |
| [**`docker version`**](https://docs.docker.com/reference/cli/docker/version/) | | **Показать версию установленного Docker (клиента и сервера). Полезно для проверки установки** |
|         | `docker version --format '{{.Client.APIVersion}}'` | Показать только версию API клиента Docker |
|         | `docker version --format '{{.Server.Version}}'` | Показать только версию сервера (Docker Engine) |
|         | `docker version --format '{{json .}}'` | Вывести полную информацию о версии в формате JSON |
| [**`docker system info`**](https://docs.docker.com/engine/reference/commandline/info/) | | **Показать общую информацию о системе Docker: количество контейнеров, образов, ресурсов** |
|         | `docker info` | Покажет данные о Docker: версии, сети, количество контейнеров и образов |
|         | `docker info --format '{{json .}}'` | Выведет информацию в формате JSON — удобно для автоматической обработки |
|         | `docker info --format '{{.NCPU}} CPUs, {{.MemTotal}} bytes RAM'` | Отобразит количество процессоров и общий объём памяти |
|         | `docker info --format '{{.Driver}}'` | Выведет драйвер хранилища, используемый Docker |
| [**`docker image pull`**](https://docs.docker.com/reference/cli/docker/image/pull/) | | **Скачать образ из Docker Hub или другого реестра. Без образа контейнер запустить нельзя** |
|         | `docker pull ubuntu` | Скачает последний доступный образ Ubuntu |
|         | `docker pull nginx:alpine` | Скачает лёгкий образ Nginx на основе Alpine Linux |
|         | `docker pull redis:7` | Скачает образ Redis версии 7 |
| [**`docker container run`**](https://docs.docker.com/engine/reference/commandline/run/) | | **Создать и запустить новый контейнер из образа** |
|         | `docker run -it ubuntu bash` | Запустит Ubuntu с интерактивным терминалом Bash |
|         | `docker run -d nginx` | Запустит Nginx в фоновом режиме |
|         | `docker run -p 8080:80 nginx` | Запустит Nginx и свяжет порт 80 контейнера с портом 8080 на компьютере |
| [**`docker container ls`**](https://docs.docker.com/reference/cli/docker/container/ls/) | | **Показать список запущенных контейнеров** |
|         | `docker ps` | Отобразит только работающие контейнеры |
|         | `docker ps -a` | Покажет все контейнеры, включая остановленные |
|         | `docker ps --format '{{.Names}}'` | Выведет только имена контейнеров |
| [**`docker container start`**](https://docs.docker.com/reference/cli/docker/container/start/) | | **Запустить один или несколько остановленных контейнеров** |
|         | `docker start container_name` | Запустит контейнер с указанным именем |
|         | `docker start $(docker ps -aq)` | Запустит все контейнеры |
|         | `docker start -ai container_name` | Запустит контейнер и подключит к нему интерактивный терминал |
| [**`docker container stop`**](https://docs.docker.com/engine/reference/commandline/stop/) | | **Остановить запущенный контейнер** |
|         | `docker stop container_name` | Остановит контейнер с именем |
|         | `docker stop $(docker ps -q)` | Остановит все работающие контейнеры |
|         | `docker stop -t 5 container_name` | Остановит контейнер, давая ему 5 секунд на завершение процессов |
| [**`docker container restart`**](https://docs.docker.com/reference/commandline/restart/) | | **Перезапустить контейнер** |
|         | `docker restart container_name` | Перезапустить указанный контейнер |
|         | `docker restart $(docker ps -q)` | Перезапустить все работающие контейнеры |
|         | `docker restart -t 10 container_name` | Перезапустить контейнер с задержкой 10 секунд |
| [**`docker container rm`**](https://docs.docker.com/engine/reference/commandline/rm/) | | **Удалить контейнер** |
|         | `docker rm container_name` | Удалит конкретный остановленный контейнер |
|         | `docker rm $(docker ps -aq)` | Удалит все остановленные контейнеры |
|         | `docker rm -f container_name` | Принудительно удалит работающий контейнер |
| [**`docker image ls`**](https://docs.docker.com/engine/reference/commandline/images/) | | **Показать список загруженных образов** |
|         | `docker images` | Отобразит все образы, которые есть на компьютере |
|         | `docker images -a` | Покажет все образы, включая промежуточные слои |
|         | `docker images --format '{{.Repository}}:{{.Tag}}'` | Выведет только имя и тег образа |
| [**`docker image rm`**](https://docs.docker.com/reference/cli/docker/image/rm/) | | **Удалить один или несколько образов из локального хранилища** |
|         | `docker rmi test1:latest` | Удалить образ с тегом `latest` репозитория `test1` |
|         | `docker rmi 1a2b3c4d5e6f` | Удалить образ по его ID |
|         | `docker rmi $(docker images -q)` | Удалить все образы (осторожно!) |

---

## 🔁 Управление контейнерами

| Команда | Пример | Описание |
| ------- | ------ | -------- |
| [**`docker container exec`**](https://docs.docker.com/engine/reference/commandline/exec/) | | **Выполнить команду внутри запущенного контейнера** |
|         | `docker exec -it container bash` | Запустить интерактивный bash внутри контейнера с именем `container` |
|         | `docker exec container ls /app` | Выполнить команду `ls` в директории `/app` контейнера |
|         | `docker exec -d container touch /tmp/testfile` | Запустить команду в контейнере в фоне (без ожидания) |
| [**`docker container logs`**](https://docs.docker.com/engine/reference/commandline/logs/) | | **Просмотреть логи контейнера** |
|         | `docker logs container` | Показать все логи контейнера `container` |
|         | `docker logs -f container` | Просматривать логи в реальном времени (фоллоу) |
|         | `docker logs --tail 50 container` | Показать последние 50 строк из логов |
| [**`docker inspect`**](https://docs.docker.com/engine/reference/commandline/inspect/) | | **Получить подробную информацию о контейнере или образе в формате JSON** |
|         | `docker inspect container` | Вывести детали контейнера `container` |
|         | `docker inspect --format '{{.NetworkSettings.IPAddress}}' container` | Вывести IP адрес контейнера |
| [**`docker container stats`**](https://docs.docker.com/reference/cli/docker/container/stats/) | | **Показать статистику использования ресурсов контейнерами в реальном времени** |
|         | `docker stats` | Показать загрузку CPU, памяти, сети и диска для всех контейнеров |
|         | `docker stats container_name` | Показать статистику только для указанного контейнера |
|         | `docker stats --no-stream` | Показать статистику однократно и выйти |
| [**`docker container rename`**](https://docs.docker.com/engine/reference/commandline/rename/) | | **Переименовать контейнер** |
|         | `docker rename old_name new_name` | Переименовать контейнер с `old_name` на `new_name` |
| [**`docker container cp`**](https://docs.docker.com/engine/reference/commandline/cp/) | | **Копировать файлы между контейнером и хостом** |
|         | `docker cp container:/src/file.txt ./file.txt` | Скопировать файл из контейнера в текущую папку на хосте |
|         | `docker cp ./config.yaml container:/app/config.yaml` | Скопировать файл с хоста в контейнер |
|         | `docker cp CONTAINER:/var/logs/app.log - \| tar x -O \| grep "ERROR"` | Скопировать файл лога из контейнера и сразу через конвейер вывести строки с ошибками (ERROR) без сохранения файла на диск |
| [**`docker container top`**](https://docs.docker.com/engine/reference/commandline/top/) | | **Показать запущенные процессы внутри контейнера** |
|         | `docker top container` | Показать процессы контейнера с именем `container` |
| [**`docker container pause`**](https://docs.docker.com/engine/reference/commandline/pause/) | | **Приостановить все процессы контейнера** |
|         | `docker pause container` | Приостановить контейнер `container` |
| [**`docker container unpause`**](https://docs.docker.com/engine/reference/commandline/unpause/) | | **Возобновить работу приостановленного контейнера** |
|         | `docker unpause container` | Возобновить контейнер `container` |
| [**`docker container update`**](https://docs.docker.com/engine/reference/commandline/update/) | | **Обновить настройки контейнера без перезапуска** |
|         | `docker update --memory 500m container` | Ограничить память контейнера до 500 МБ |

---

## 🧱 Образы и Dockerfile

| Команда | Пример | Описание |
| ------- | ------ | -------- |
| [**`docker buildx build`**](https://docs.docker.com/engine/reference/commandline/build/) | | **Создать Docker образ из Dockerfile** |
|         | `docker build -t my_image .` | Собрать образ с тегом `my_image` из текущей директории |
|         | `docker build -t my_image:1.0 .` | Собрать образ с тегом версии `1.0` |
|         | `docker build --no-cache -t my_image .` | Собрать образ без использования кэша, для чистой сборки |
| [**`docker container commit`**](https://docs.docker.com/engine/reference/commandline/commit/) | | **Создать образ из текущего состояния контейнера** |
|         | `docker commit container my_img:v1` | Создать образ `my_img` с тегом `v1` из контейнера `container` |
|         | `docker commit -m "Added config" container my_img:v2` | Создать образ с комментарием |
|         | `docker commit -a "John Doe" container my_img:latest` | Создать образ с указанием автора |
| [**`docker image tag`**](https://docs.docker.com/engine/reference/commandline/tag/) | | **Добавить или изменить тег образа** |
|         | `docker tag my_image myrepo/my_image:latest` | Добавить тег для загрузки в реестр `myrepo` |
|         | `docker tag my_image:1.0 my_image:stable` | Создать тег `stable` для образа с тегом `1.0` |
|         | `docker tag my_image my_image:backup` | Добавить тег `backup` для локального образа |
| [**`docker image push`**](https://docs.docker.com/engine/reference/commandline/push/) | | **Отправить образ в Docker Hub или другой реестр** |
|         | `docker push myrepo/my_image:latest` | Отправить образ с тегом `latest` в репозиторий `myrepo` |
|         | `docker push myrepo/my_image:1.0` | Отправить образ с тегом `1.0` |
|         | `docker push myrepo/my_image` | Отправить образ с тегом по умолчанию `latest` |
| [**`docker login`**](https://docs.docker.com/engine/reference/commandline/login/) | | **Авторизоваться в Docker Hub или другом реестре** |
|         | `docker login` | Ввести логин и пароль для Docker Hub в интерактивном режиме |
|         | `docker login myregistry.local:5000` | Войти в приватный реестр |
|         | `docker login -u username -p password` | Авторизоваться с указанием имени и пароля (не рекомендуется) |
| [**`docker logout`**](https://docs.docker.com/engine/reference/commandline/logout/) | | **Выйти из Docker Hub или другого реестра** |
|         | `docker logout` | Выйти из Docker Hub |
|         | `docker logout myregistry.local:5000` | Выйти из приватного реестра |
| [**`HEALTHCHECK`**](https://docs.docker.com/reference/dockerfile/#healthcheck) | | **Инструкция Dockerfile для автоматической проверки состояния контейнера** |
|         | `HEALTHCHECK --interval=30s --timeout=5s --retries=3 CMD curl -f http://localhost/ \|\| exit 1` | Добавить проверку доступности сервиса внутри контейнера каждые 30 секунд |
|         | `docker inspect --format='{{json .State.Health}}' container_name` | Проверить результат выполнения healthcheck у запущенного контейнера |

---

## 🔌 Сети и тома

| Команда | Пример | Описание |
| ------- | ------ | -------- |
| [**`docker network ls`**](https://docs.docker.com/reference/cli/docker/network/ls/) | | **Показать список всех Docker сетей** |
|         | `docker network ls` | Показать все созданные сети Docker |
|         | `docker network ls --filter driver=bridge` | Показать только сети с драйвером `bridge` |
|         | `docker network ls --format '{{.Name}}'` | Показать только имена сетей |
| [**`docker network create`**](https://docs.docker.com/reference/cli/docker/network/create/) | | **Создать новую Docker сеть** |
|         | `docker network create my_net` | Создать сеть с именем `my_net` с настройками по умолчанию |
|         | `docker network create --driver bridge my_bridge_net` | Создать сеть с драйвером `bridge` |
|         | `docker network create --subnet=192.168.10.0/24 my_custom_net` | Создать сеть с указанием подсети |
| [**`docker network connect`**](https://docs.docker.com/reference/cli/docker/network/connect/) | | **Подключить контейнер к сети** |
|         | `docker network connect my_net container` | Подключить контейнер с именем `container` к сети `my_net` |
|         | `docker network connect --alias db_net my_net container` | Подключить с алиасом `db_net` |
|         | | |
| [**`docker network disconnect`**](https://docs.docker.com/reference/cli/docker/network/disconnect/) | | **Отключить контейнер от сети** |
|         | `docker network disconnect my_net container` | Отключить контейнер `container` от сети `my_net` |
|         | | |
| [**`docker volume ls`**](https://docs.docker.com/reference/cli/docker/volume/ls/) | | **Показать список всех Docker томов** |
|         | `docker volume ls` | Показать все тома, созданные в Docker |
|         | `docker volume ls --filter dangling=true` | Показать неиспользуемые тома |
|         | | |
| [**`docker volume create`**](https://docs.docker.com/reference/cli/docker/volume/create/) | | **Создать новый Docker том** |
|         | `docker volume create my_vol` | Создать том с именем `my_vol` |
|         | `docker volume create --driver local --opt type=tmpfs my_tmp_vol` | Создать временный том с использованием tmpfs |
|         | | |
| [**`docker volume inspect`**](https://docs.docker.com/reference/cli/docker/volume/inspect/) | | **Показать подробную информацию о томе** |
|         | `docker volume inspect my_vol` | Вывести детали тома `my_vol` в формате JSON |
|         | | |
| [**`docker volume rm`**](https://docs.docker.com/reference/cli/docker/volume/rm/) | | **Удалить один или несколько томов** |
|         | `docker volume rm my_vol` | Удалить том с именем `my_vol` |
|         | `docker volume rm $(docker volume ls -qf dangling=true)` | Удалить все неиспользуемые тома |

---

## 🧩 Плагины Docker

| Команда | Пример | Описание |
| ------- | ------ | -------- |
| [**`docker plugin ls`**](https://docs.docker.com/reference/cli/docker/plugin/ls/) | | **Показать список установленных плагинов Docker** |
|         | `docker plugin ls` | Отобразить список всех плагинов и их статус |
| [**`docker plugin install`**](https://docs.docker.com/reference/cli/docker/plugin/install/) | | **Установить плагин Docker из реестра** |
|         | `docker plugin install vieux/sshfs` | Установить плагин SSHFS для томов |
|         | `docker plugin install store/weaveworks/net-plugin:latest_release` | Установить сетевой плагин Weave |
| [**`docker plugin disable`**](https://docs.docker.com/reference/cli/docker/plugin/disable/) | | **Отключить установленный плагин** |
|         | `docker plugin disable vieux/sshfs` | Отключить плагин SSHFS |
| [**`docker plugin enable`**](https://docs.docker.com/reference/cli/docker/plugin/enable/) | | **Включить ранее отключённый плагин** |
|         | `docker plugin enable vieux/sshfs` | Включить плагин SSHFS |
| [**`docker plugin rm`**](https://docs.docker.com/reference/cli/docker/plugin/rm/) | | **Удалить плагин Docker** |
|         | `docker plugin rm vieux/sshfs` | Удалить плагин SSHFS |

---

## 📋 Docker Compose

| Команда | Пример | Описание |
| ------- | ------ | -------- |
| [**`docker compose up`**](https://docs.docker.com/compose/reference/up/) | | **Запустить контейнеры, описанные в `docker-compose.yml`** |
|         | `docker compose up` | Запустить все сервисы в текущей директории в интерактивном режиме |
|         | `docker compose up -d` | Запустить сервисы в фоне (detached mode) |
|         | `docker compose up --build` | Построить образы перед запуском сервисов |
| [**`docker compose down`**](https://docs.docker.com/compose/reference/down/) | | **Остановить и удалить все контейнеры, сети и тома, созданные `up`** |
|         | `docker compose down` | Остановить все запущенные сервисы и удалить связанные ресурсы |
|         | `docker compose down --volumes` | Удалить также все тома, созданные Compose |
|         | `docker compose down --rmi all` | Удалить также все образы, созданные Compose |
| [**`docker compose logs`**](https://docs.docker.com/compose/reference/logs/) | | **Просмотреть логи всех или отдельных сервисов** |
|         | `docker compose logs` | Показать логи всех сервисов |
|         | `docker compose logs -f` | Смотреть логи в реальном времени (follow) |
|         | `docker compose logs web` | Показать логи только для сервиса с именем `web` |
| [**`docker compose exec`**](https://docs.docker.com/compose/reference/exec/) | | **Выполнить команду внутри запущенного контейнера сервиса** |
|         | `docker compose exec web bash` | Войти в контейнер сервиса `web` с интерактивным bash |
|         | `docker compose exec db ls /var/lib/postgresql` | Выполнить команду `ls` внутри контейнера базы данных |
|         | `docker compose exec -d worker touch /tmp/done` | Выполнить команду в контейнере `worker` в фоне |
| [**`docker compose build`**](https://docs.docker.com/compose/reference/build/) | | **Построить или пересобрать образы сервисов** |
|         | `docker compose build` | Построить все образы, описанные в `docker-compose.yml` |
|         | `docker compose build web` | Построить только образ сервиса `web` |
|         | `docker compose build --no-cache` | Построить образы без использования кэша |
| [**`docker compose ps`**](https://docs.docker.com/compose/reference/ps/) | | Показать статус всех сервисов и контейнеров |
|         | `docker compose ps -a` | Показать все контейнеры, включая остановленные |
|         | `docker compose ps --services` | Показать только имена сервисов |
| [**`docker compose pull`**](https://docs.docker.com/compose/reference/pull/) | | Скачать/обновить образы сервисов из реестра |
|         | `docker compose pull web` | Скачать образ только для сервиса `web` |
|         | `docker compose pull --ignore-pull-failures` | Продолжить загрузку, даже если некоторые образы не удалось скачать |
| [**`docker compose restart`**](https://docs.docker.com/compose/reference/restart/) | | Перезапустить все или указанные сервисы |
|         | `docker compose restart db` | Перезапустить только сервис `db` |
|         | `docker compose restart -t 10` | Перезапустить сервисы с таймаутом 10 секунд |
| [**`docker compose config`**](https://docs.docker.com/compose/reference/config/) | | Вывести итоговую конфигурацию Compose в формате YAML |
|         | `docker compose config --services` | Показать список всех сервисов из конфигурации |
|         | `docker compose config --volumes` | Показать все тома, определённые в конфигурации |
| [**`docker compose start`**](https://docs.docker.com/compose/reference/start/) | | Запустить остановленные сервисы без пересоздания |
|         | `docker compose start web` | Запустить сервис `web` |
|         | `docker compose start db api` | Запустить сразу несколько сервисов |
| [**`docker compose stop`**](https://docs.docker.com/compose/reference/stop/) | | Остановить сервисы без удаления контейнеров |
|         | `docker compose stop web` | Остановить сервис `web` |
|         | `docker compose stop -t 5` | Остановить сервисы с таймаутом 5 секунд |

---

## 📤 Экспорт и импорт

| Команда | Пример | Описание |
| ------- | ------ | -------- |
| [**`docker image save`**](https://docs.docker.com/reference/cli/docker/image/save/) | | **Сохранить один или несколько образов Docker в файл в формате tar для последующего импорта или передачи** |
|         | `docker save -o image.tar my_img:tag` | Сохранить образ Docker в архивный файл tar |
|         | `docker save my_image > my_image.tar` | Альтернативный способ сохранить образ в файл |
|         | `docker save -o redis_latest.tar redis:latest` | Сохранить конкретный образ Redis в файл |
| [**`docker image load`**](https://docs.docker.com/reference/cli/docker/image/load/) | | **Загрузить образы Docker из файла tar, сохранённого ранее** |
|         | `docker load < image.tar` | Загрузить образ Docker из файла tar |
|         | `docker load --input redis_latest.tar` | Загрузить образ с указанием файла через параметр |
|         | `docker load --quiet < my_image.tar` | Загрузить образ без вывода прогресса |
| [**`docker container export`**](https://docs.docker.com/reference/cli/docker/container/export/) | | **Экспортировать файловую систему контейнера в tar-архив без истории и метаданных образа** |
|         | `docker export container > file.tar` | Экспортировать файловую систему контейнера в архив |
|         | `docker export my_container > my_container_fs.tar` | Экспортировать контейнер по имени |
|         | `docker export -o container_fs.tar container_id` | Экспортировать по ID контейнера с использованием флага -o |
| [**`docker image import`**](https://docs.docker.com/reference/cli/docker/image/import/) | | **Создать новый образ из tar-архива файловой системы** |
|         | `docker import file.tar new_img` | Импортировать файл архива как новый образ Docker |
|         | `docker import https://example.com/image.tar my_new_image` | Импортировать образ напрямую из URL |
|         | `docker import - my_image < file.tar` | Импортировать из стандартного ввода |

---

## 🧹 Очистка и диагностика

| Команда | Пример | Описание |
| ------- | ------ | -------- |
| [**`docker system df`**](https://docs.docker.com/reference/cli/docker/system/df/) | | **Показать использование дискового пространства Docker: объёмы, образы, контейнеры и кэш сборки** |
|         | `docker system df -v` | Подробный вывод с информацией по каждому образу, контейнеру и тому |
|         | `docker system df --format '{{json .}}'` | Вывести информацию в формате JSON |
| [**`docker system prune`**](https://docs.docker.com/reference/cli/docker/system/prune/) | | **Удалить все неиспользуемые данные Docker: остановленные контейнеры, неиспользуемые сети, висячие образы и кэш сборки** |
|         | `docker system prune -a` | Удалить неиспользуемые образы, включая промежуточные |
|         | `docker system prune --volumes` | Удалить неиспользуемые тома вместе с другими ресурсами |
| [**`docker image prune`**](https://docs.docker.com/reference/cli/docker/image/prune/) | | **Удалить неиспользуемые образы Docker, включая висячие слои** |
|         | `docker image prune -a` | Удалить все неиспользуемые образы, включая висячие |
|         | `docker image prune --filter "until=24h"` | Удалить образы старше 24 часов |
| [**`docker container prune`**](https://docs.docker.com/reference/cli/docker/container/prune/) | | **Удалить остановленные контейнеры, соответствующие фильтрам, или все, если фильтр не задан** |
|         | `docker container prune --filter "until=24h"` | Удалить остановленные контейнеры старше 24 часов |
|         | `docker container prune --force` | Удалить без запроса подтверждения |

---

## 🐝 Docker Swarm

| Команда | Пример | Описание |
| ------- | ------ | -------- |
| [**`docker swarm init`**](https://docs.docker.com/reference/cli/docker/swarm/init/) | | **Инициализировать новый кластер Docker Swarm на текущем узле** |
|         | `docker swarm init --advertise-addr 192.168.1.100` | Инициализировать кластер с указанием IP адреса |
|         | `docker swarm init --listen-addr 0.0.0.0:2377` | Инициализация с указанием порта прослушивания |
| [**`docker service create`**](https://docs.docker.com/reference/cli/docker/service/create/) | | **Создать новый сервис в кластере Swarm** |
|         | `docker service create --name nginx nginx` | Создать сервис Nginx в Swarm |
|         | `docker service create --replicas 3 --name web webserver` | Создать сервис с 3 репликами |
|         | `docker service create --name redis --publish 6379:6379 redis` | Создать сервис с пробросом порта |
| [**`docker stack deploy`**](https://docs.docker.com/reference/cli/docker/stack/deploy/) | | **Развернуть стек сервисов в кластере Swarm на основе Compose-файла** |
|         | `docker stack deploy -c docker-compose.yml mystack` | Деплой стека из файла compose |
|         | `docker stack deploy --with-registry-auth -c compose.yml mystack` | Деплой с передачей авторизации в реестр |
|         | `docker stack deploy -c swarm-compose.yml mystack` | Использование другого compose файла для стека |
| [**`docker stack rm`**](https://docs.docker.com/reference/cli/docker/stack/rm/) | | **Удалить один или несколько стеков из кластера Swarm** |
|         | `docker stack rm mystack` | Удалить стек `mystack` |
|         | `docker stack rm` | Удалить все стеки (не рекомендуется) |
|         | `docker stack rm mystack && docker swarm leave --force` | Удалить стек и выйти из Swarm |

---

## 💼 Продвинутое использование Docker

### 🚀 Профессиональные команды Docker

| Команда | Пример | Описание |
| ------- | ------ | -------- |
| [**`docker buildx`**](https://docs.docker.com/reference/cli/docker/buildx/) | | **Расширенный инструмент сборки образов, заменяющий `docker build`. Поддерживает мультиплатформенность, кэширование, параллельную сборку и экспорт в различные форматы. Полезен для CI/CD и кроссплатформенной разработки** |
|         | `docker buildx build --platform linux/arm64,linux/amd64 -t myimg:multi .` | Собрать мультиплатформенный образ (ARM и x86 одновременно) |
|         | `docker buildx build --load -t localimg .` | Собрать образ и загрузить его в локальный кеш Docker Engine |
|         | `docker buildx build --push --platform linux/amd64,linux/arm64 -t repo/app:latest .` | Собрать и опубликовать мультиплатформенный образ в реестр |
| [**`docker context`**](https://docs.docker.com/reference/cli/docker/context/) | | **Управление контекстами Docker для работы с удалёнными или несколькими окружениями. Позволяет быстро переключаться между локальным и удалённым Docker Engine** |
|         | `docker context create myremote --docker "host=ssh://user@host"` | Создать контекст для подключения к удалённому Docker-хосту |
|         | `docker context use myremote` | Переключиться на удалённый контекст |
|         | `docker context ls` | Показать список доступных контекстов и активный из них |
| [**`docker system events`**](https://docs.docker.com/reference/cli/docker/system/events/) | | **Прослушивание событий Docker в реальном времени, с фильтрацией по типу события (например, запуск контейнера). Полезно для мониторинга и автоматизации** |
|         | `docker events --filter 'event=start'` | Показать только события запуска контейнеров |
|         | `docker events --since 1h --until 10m` | Показать события за последний час до 10 минут назад |
|         | `docker events --filter 'type=network'` | Показать только события, связанные с сетями |
|         | `docker events --filter 'image=nginx'` | Показать события, связанные с образом `nginx` |
| [**`docker container update`**](https://docs.docker.com/reference/cli/docker/container/update/) | | **Изменение лимитов ресурсов и настроек работающего контейнера без его перезапуска** |
|         | `docker update --cpus 2 --memory 1g my_container` | Установить лимит в 2 CPU и 1 ГБ RAM |
|         | `docker update --restart unless-stopped my_container` | Задать политику автоперезапуска `unless-stopped` |
|         | `docker update --pids-limit 200 my_container` | Ограничить количество процессов до 200 |
| [**`docker container diff`**](https://docs.docker.com/reference/cli/docker/container/diff/) | | **Показывает изменения в файловой системе контейнера по сравнению с исходным образом. Полезно для отладки и аудита** |
|         | `docker diff my_container` | Показать все изменения в файловой системе контейнера |
|         | `docker diff my_container \| grep '^A'` | Показать только добавленные файлы (`A` — Added) |
| [**`docker image history`**](https://docs.docker.com/reference/cli/docker/image/history/) | | **Отображает историю слоёв образа: команды сборки, размер каждого слоя и время создания. Полезно для оптимизации и аудита** |
|         | `docker history my_image` | Показать историю слоёв образа |
|         | `docker history --no-trunc my_image` | Показать полные команды сборки без сокращений |
|         | `docker history --format "{{.CreatedBy}}: {{.Size}}" my_image` | Вывести только команды сборки и размеры слоёв |

### 🛠 Полезные практики и автоматизация Docker

- **Минимизируй размер образов**  
  Используй базовые образы на основе `alpine` или `scratch` для минимального размера.  
  Для объединения слоёв можно применять `--squash` при сборке (требует включения экспериментальных функций).  
  Также удаляй временные файлы и кеши в одном слое:

  ```dockerfile
  RUN apk add --no-cache curl && rm -rf /var/cache/apk/*
  ```

- **Минимизируй количество слоёв**
  Объединяй команды в одном `RUN`, чтобы уменьшить количество слоёв и итоговый размер образа:

  ```dockerfile
  RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*
  ```

- **Оптимизируй сборку Dockerfile**  
  Разделяй сборку на этапы (multi-stage build), чтобы в финальном образе были только необходимые файлы.
  Сначала копируй и устанавливай зависимости, затем код — это увеличит кэшируемость слоёв и ускорит повторные сборки.
- **Разделяй секреты и конфиги**  
  Никогда не храни `.env`, ключи API или приватные сертификаты внутри образа.
  Для конфигураций используй:
  - `docker secret` (в Swarm)
  - переменные окружения (`-e VAR=value` или `.env`)
  - внешние тома для конфигов
- **Секреты при сборке (BuildKit)**
  Для безопасной передачи секретов в процессе сборки используйте флаг `--secret`:

  ```bash
  docker buildx build --secret id=mysecret,src=./secret.txt .
  ```

  В Dockerfile секрет доступен в /run/secrets/mysecret:

  ```dockerfile
  RUN --mount=type=secret,id=mysecret cat /run/secrets/mysecret
  ```

  🛡 Это исключает сохранение секретов в слоях образа.
- **Rootless Docker**
  Запуск Docker без прав root повышает безопасность и снижает риск компрометации хоста.
  Для включения:

  ```bash
  dockerd-rootless-setuptool.sh install
  export PATH=/usr/bin:$PATH
  ```

  Проверить:

  ```bash
  docker info | grep Rootless
  ```

  ⚠ Некоторые функции (например, проброс портов <1024) будут недоступны.
- **Проверка образов на уязвимости**
  Используй встроенные инструменты:

  ```bash
  docker scan my_image
  ```

  Или новый CLI:

  ```bash
  docker scout cves my_image
  ```

  Это поможет находить уязвимости в базовых образах и зависимостях.
- **Следи за ресурсами**  
  Ограничивай контейнеры по памяти, CPU и количеству процессов:

  ```bash
  docker run --memory=512m --cpus="1.5" --pids-limit=200 myimage
  ```

  Это предотвращает чрезмерное потребление ресурсов.
  Также можно ограничить I/O:

  ```bash
  docker run --device-read-bps /dev/sda:1mb --device-write-bps /dev/sda:1mb myimage
  ```

  Это полезно для контейнеров, которые не должны перегружать дисковую подсистему.
- **Автоматическая очистка**
  Регулярно удаляй неиспользуемые образы, контейнеры, тома и сети:

  ```bash
  docker system prune -af --volumes
  ```

  > ⚠ Будь осторожен: эта команда удалит все неиспользуемые ресурсы.
  
  Для выборочной очистки используй:

  ```bash
  docker image prune --filter "until=24h"
  ```

- **CI/CD интеграция**
  Встраивай сборку, тестирование и деплой в пайплайны GitHub Actions, GitLab CI, Jenkins.
  Пример шага GitHub Actions:

  ```yaml
  - run: docker build -t myapp:${GITHUB_SHA} .
  - run: docker push myapp:${GITHUB_SHA}
  ```

- **Логирование и мониторинг**
  Подключай драйверы логирования (`--log-driver`) к централизованным системам: ELK, Loki, Splunk.
  Используй Prometheus + cAdvisor для метрик по контейнерам.
- **Развёртывание в продакшене**
  Разделяй конфиги для разработки и продакшена через `docker-compose.override.yml`.
  Для высокой доступности и масштабирования используй:
  - Docker Swarm
  - Kubernetes

### 🐞 Отладка и профилирование контейнеров Docker

| Команда | Пример | Описание |
| ------- | ------ | -------- |
| [**`docker container exec`**](https://docs.docker.com/reference/cli/docker/container/exec/) | | **Выполняет команду внутри запущенного контейнера, предоставляя интерактивный доступ или возможность запускать процессы в изолированной среде контейнера** |
|         | `docker exec -it my_container bash` | Запустить интерактивный терминал (bash) в работающем контейнере |
|         | `docker exec -it my_container sh` | Запустить минимальный shell в контейнере (если bash недоступен) |
|         | `docker exec my_container ls /app` | Выполнить команду внутри контейнера без интерактивного режима |
| [**`docker container logs`**](https://docs.docker.com/reference/cli/docker/container/logs/) | | **Отображает логи указанного контейнера, позволяя просматривать вывод и события, связанные с его работой, для диагностики и мониторинга** |
|         | `docker logs -f --tail 100 my_container` | Просмотреть последние 100 строк логов с выводом в реальном времени |
|         | `docker logs my_container` | Показать все доступные логи контейнера |
|         | `docker logs --since 1h my_container` | Показать логи за последний час |
| [**`docker inspect`**](https://docs.docker.com/reference/cli/docker/inspect/) | | **Выводит подробную информацию о Docker-объекте (контейнере, образе, сети и т.д.) в формате JSON, включая конфигурацию и состояние** |
|         | `docker inspect my_container` | Получить полную информацию о контейнере в формате JSON |
|         | `docker inspect --format '{{.State.Pid}}' my_container` | Получить PID основного процесса контейнера на хосте |
|         | `docker inspect --format '{{.NetworkSettings.IPAddress}}' my_container` | Показать IP-адрес контейнера |
| [**`nsenter`**](https://man7.org/linux/man-pages/man1/nsenter.1.html) (с `strace`) | | **Утилита Linux для подключения к пространствам имён другого процесса (в данном случае — контейнера). В связке с `strace` позволяет отслеживать системные вызовы процессов внутри контейнера для отладки** |
|         | `nsenter --target $(docker inspect --format '{{.State.Pid}}' my_container) --mount --uts --ipc --net --pid strace -p 1` | Подключиться к пространствам имён контейнера и трассировать системные вызовы процесса |
|         | `nsenter --target $(docker inspect --format '{{.State.Pid}}' my_container) --mount --uts --ipc --net --pid bash` | Открыть bash в пространстве имён контейнера |
|         | `nsenter --target $(docker inspect --format '{{.State.Pid}}' my_container) --net netstat -tulnp` | Просмотреть открытые порты контейнера |
| [**`tcpdump`**](https://www.tcpdump.org/manpages/tcpdump.1.html) (в контейнере) | `docker exec -it my_container tcpdump -i any` | **Консольная утилита для перехвата и анализа сетевого трафика. В контейнере используется для диагностики сетевых проблем, анализа пакетов и мониторинга соединений** |
|         | `docker exec -it my_container tcpdump -i any` | Захват и анализ сетевого трафика внутри контейнера |
|         | `docker exec -it my_container tcpdump -nn port 80` | Захват трафика только по порту 80 |
|         | `docker exec -it my_container tcpdump -w /tmp/dump.pcap` | Сохранить трафик в файл для последующего анализа |
| [**`docker container stats`**](https://docs.docker.com/reference/cli/docker/container/stats/) | | **Показывает текущие показатели использования ресурсов (CPU, память, сеть, диск) для одного или нескольких контейнеров в реальном времени** |
|         | `docker stats my_container` | Отобразить использование CPU, памяти, сети и диска контейнером в реальном времени |
|         | `docker stats` | Показать статистику по всем контейнерам |
|         | `docker stats --no-stream` | Вывести статистику один раз и завершить |
| [**`docker container top`**](https://docs.docker.com/reference/cli/docker/container/top/) | | **Отображает список процессов, запущенных внутри контейнера, аналогично команде ps в Linux, для анализа активности контейнера** |
|         | `docker top my_container` | Показать список процессов, запущенных внутри контейнера |
|         | `docker top my_container aux` | Использовать другой формат вывода, аналогичный `ps aux` |
|         | `docker top my_container -eo pid,cmd` | Вывести только PID и команду процесса |
| [**`docker diff`**](https://docs.docker.com/reference/cli/docker/container/diff/) | | **Показывает изменения в файловой системе контейнера по сравнению с его исходным образом, указывая добавленные, изменённые или удалённые файлы** |
|         | `docker diff my_container` | Показать изменения в файловой системе контейнера по сравнению с исходным образом |
|         | `docker diff my_container \| grep '^A'` | Показать только добавленные файлы (`A` — Added) |
|         | `docker diff my_container \| grep '^C'` | Показать только изменённые файлы (`C` — Changed) |
| [**`docker cp`**](https://docs.docker.com/reference/cli/docker/container/cp/) | | **Копирует файлы и каталоги между контейнером и хост-машиной, обеспечивая обмен данными и резервное копирование** |
|         | `docker cp my_container:/path/to/file ./file` | Скопировать файл из контейнера на хост |
|         | `docker cp ./config.yaml my_container:/app/config.yaml` | Скопировать файл с хоста в контейнер |
|         | `docker cp my_container:/var/log/app.log - \| tar x -O \| grep "ERROR"` | Скопировать файл лога и отфильтровать строки с ошибками без сохранения на диск |

> 💡 Для сложной отладки можно использовать `nsenter`, `strace`, `tcpdump`, `gdb` и другие низкоуровневые инструменты.

---

## 💼 Продвинутое использование Docker Compose

### 🚀 Профессиональные команды Docker Compose

| Команда | Пример | Описание |
| ------- | ------ | -------- |
| [**`docker compose up`**](https://docs.docker.com/reference/cli/docker/compose/up/) | | **Запуск и управление жизненным циклом указанных сервисов из файла docker-compose.yml с возможностью работы в фоне** |
|         | `docker compose up -d web db` | Запускает в фоне только сервисы `web` и `db` |
|         | `docker compose up --build` | Пересобирает образы перед запуском сервисов |
|         | `docker compose up --remove-orphans` | Удаляет контейнеры, не описанные в текущем compose-файле |
| [**`docker compose build`**](https://docs.docker.com/reference/cli/docker/compose/build/) | | **Сборка образов для сервисов по описанию в compose-файле с управлением кэшем и параллелизмом** |
|         | `docker compose build --no-cache` | Полная пересборка образов без использования кэша |
|         | `docker compose build --parallel` | Сборка всех сервисов одновременно для ускорения процесса |
|         | `docker compose build web` | Сборка образа только для сервиса `web` |
| [**`docker compose pull`**](https://docs.docker.com/reference/cli/docker/compose/pull/) | | **Загрузка последних версий образов из реестра для всех или указанных сервисов** |
|         | `docker compose pull` | Скачивает образы для всех сервисов |
|         | `docker compose pull db` | Скачивает образ только для сервиса `db` |
|         | `docker compose pull --ignore-pull-failures` | Продолжает выполнение, игнорируя ошибки при загрузке образов |
| [**`docker compose restart`**](https://docs.docker.com/reference/cli/docker/compose/restart/) | | **Перезапуск всех или указанных сервисов без пересоздания контейнеров** |
|         | `docker compose restart` | Перезапускает все сервисы в текущем проекте |
|         | `docker compose restart worker` | Перезапускает только сервис `worker` |
|         | `docker compose restart web db` | Перезапускает сразу несколько сервисов |
| [**`docker compose exec`**](https://docs.docker.com/reference/cli/docker/compose/exec/) | | **Выполнение команды внутри работающего контейнера сервиса с возможностью интерактивного режима** |
|         | `docker compose exec db psql -U user -d database` | Запускает psql в контейнере сервиса `db` |
|         | `docker compose exec web sh` | Открывает shell внутри контейнера `web` |
|         | `docker compose exec api curl http://localhost:8080` | Выполняет curl-запрос из контейнера сервиса `api` |
| [**`docker compose config`**](https://docs.docker.com/reference/cli/docker/compose/config/) | | **Вывод итоговой конфигурации Compose с учётом всех файлов и переменных окружения** |
|         | `docker compose config` | Показать объединённую конфигурацию в YAML |
|         | `docker compose config --services` | Вывести список всех сервисов |
|         | `docker compose config --environment` | Показать все переменные окружения, используемые сервисами |
| [**`docker compose watch`**](https://docs.docker.com/reference/cli/docker/compose/watch/) | | **Автоматически перезапускает сервисы при изменении исходных файлов, полезно для разработки** |
|         | `docker compose watch` | Запустить наблюдение за изменениями файлов и перезапуск сервисов |
| [**`docker compose events`**](https://docs.docker.com/reference/cli/docker/compose/events/) | | **Поток событий Compose: запуск, остановка, обновление сервисов** |
|         | `docker compose events --json` | Получать события в формате JSON |
| [**`docker compose rm`**](https://docs.docker.com/reference/cli/docker/compose/rm/) | | **Удалить остановленные контейнеры сервисов** |
|         | `docker compose rm web db` | Удалить контейнеры сервисов `web` и `db` |
| [**`docker compose pause`**](https://docs.docker.com/reference/cli/docker/compose/pause/) | | **Приостановить работу сервисов** |
|         | `docker compose pause api` | Приостановить сервис `api` |
| [**`docker compose unpause`**](https://docs.docker.com/reference/cli/docker/compose/unpause/) | | **Возобновить работу приостановленных сервисов** |
|         | `docker compose unpause api` | Возобновить сервис `api` |
| [**`docker compose create`**](https://docs.docker.com/reference/cli/docker/compose/create/) | | **Создать контейнеры без их запуска** |
|         | `docker compose create web db` | Создать контейнеры для `web` и `db`, но не запускать |
| [**`docker compose images`**](https://docs.docker.com/reference/cli/docker/compose/images/) | | **Показать список образов, используемых сервисами** |
|         | `docker compose images` | Вывести список образов всех сервисов |
| [**`docker compose top`**](https://docs.docker.com/reference/cli/docker/compose/top/) | | **Показать процессы, запущенные внутри контейнеров сервисов** |
|         | `docker compose top web` | Показать процессы внутри контейнеров сервиса `web` |

### 🛠 Полезные практики и автоматизация с Docker Compose

- **Разделение окружений**  
  Используйте отдельные файлы `docker-compose.override.yml` для разных сред — `development`, `staging`, `production`. Это помогает изолировать конфигурации и избежать конфликтов между настройками.
  Также можно комбинировать несколько файлов конфигурации через флаг `-f`:

  ```bash
  docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d
  ```

  Для управления переменными окружения применяйте разные `.env` файлы (`.env.dev`, `.env.prod` и т.п.).
- **Безопасное хранение секретов**  
  Не включайте чувствительные данные (пароли, токены) напрямую в файлы Compose. Вместо этого применяйте:
  - `.env` файлы для переменных окружения  (обратите внимание, что `.env` не шифруются и не должны попадать в публичные репозитории)
  - `docker secret` и `docker config` для безопасного управления секретами и конфигурациями в Docker Swarm
  - внешние тома для конфигурационных файлов с секретами
  - внешние системы управления секретами (например, HashiCorp Vault, AWS Secrets Manager)
- **Порядок запуска с `depends_on` и `healthcheck`**
  Чтобы сервисы ждали готовности зависимостей:

  ```yaml
  services:
    db:
      image: postgres
      healthcheck:
        test: ["CMD-SHELL", "pg_isready -U postgres"]
        interval: 10s
        retries: 5
    api:
      image: my_api
      depends_on:
        db:
          condition: service_healthy
  ```

- **Минимизация времени простоя при обновлениях**  
  Перед обновлением сервисов запускайте:
  
  ```bash
  docker compose pull && docker compose up -d --remove-orphans
  ```

  Опция `-d` обеспечивает запуск в фоне, а `--remove-orphans` удаляет контейнеры, не описанные в текущих конфигурациях.
  При необходимости можно полностью остановить и удалить старые контейнеры:

  ```bash
  docker compose down --remove-orphans
  ```

  Это гарантирует загрузку актуальных образов и удаление неиспользуемых контейнеров без остановки сервисов.
- **Горячая замена кода для разработки**
  Используйте `volumes` для монтирования локальных директорий в контейнеры. Это позволяет мгновенно применять изменения кода без необходимости пересобирать образы.
  При этом следите за правами доступа и особенностями кэширования файловой системы, особенно на Windows и macOS, чтобы избежать проблем с производительностью.
- **Горячая замена кода без volume (Compose 2.22+)**

  ```yaml
  develop:
    watch:
      - path: ./src
        action: sync
        target: /app
  ```

- **Централизованное логирование сервисов**
  Перенаправляйте логи контейнеров в системы мониторинга и агрегации логов, такие как ELK Stack, Loki, Prometheus и Fluentd, для удобного анализа и алертинга.
  Для интеграции используйте драйверы логирования Docker (`--log-driver`), которые обеспечивают централизованный сбор и обработку логов.
  Подключайте драйверы логирования к контейнерам через logging:

  ```yaml
  services:
    api:
      image: my_api
      logging:
        driver: "json-file"
        options:
          max-size: "10m"
          max-file: "3"
  ```

- **Автоматический перезапуск сервисов**
  В `docker-compose.yml` настройте политику рестарта сервисов:

  ```yaml
  restart: unless-stopped
  ```

  Другие варианты политики рестарта:
  - `no` — без автоперезапуска (по умолчанию)
  - `always` — всегда перезапускать контейнер
  - `on-failure` — перезапускать только при ошибках (с опциональным числом попыток)
  
  В продакшене `unless-stopped` — оптимальный выбор для обеспечения устойчивости сервисов.
  Это обеспечит автоматическое восстановление сервисов после сбоев или перезагрузки хоста.
- **Профили сервисов**  
  Позволяют запускать только определённые группы сервисов:

  ```yaml
  services:
    db:
      image: postgres
      profiles: ["backend"]
    web:
      image: nginx
      profiles: ["frontend"]
  ```

  Запуск только профиля frontend:

  ```bash
  docker compose --profile frontend up
  ```

### 🐞 Отладка и профилирование сервисов в Docker Compose

| Команда | Пример | Описание |
| ------- | ------ | -------- |
| [**`docker compose exec`**](https://docs.docker.com/reference/cli/docker/compose/exec/) | | **Выполняет команду внутри запущенного сервиса, предоставляя доступ в контейнер или запуск отдельных процессов** |
|         | `docker compose exec web sh` | Открыть shell внутри контейнера сервиса `web` |
|         | `docker compose exec db psql -U user -d database` | Выполнить команду psql внутри контейнера сервиса `db` |
| [**`docker compose logs`**](https://docs.docker.com/reference/cli/docker/compose/logs/) | | **Просмотр логов сервисов для диагностики и мониторинга** |
|         | `docker compose logs -f db` | Просмотр логов сервиса `db` в режиме реального времени |
|         | `docker compose logs --tail=50 api` | Показать последние 50 строк логов сервиса `api` |
|         | `docker compose logs --since=1h web` | Показать логи за последний час для сервиса `web` |
| [**`docker inspect`**](https://docs.docker.com/reference/cli/docker/inspect/) | | **Просмотр детальной информации о контейнере, запущенном сервисе** |
|         | `docker inspect $(docker compose ps -q web)` | Получить JSON с подробной информацией о контейнере сервиса `web` |
| [**`docker container stats`**](https://docs.docker.com/reference/cli/docker/container/stats/) | | **Мониторинг ресурсов контейнеров, запущенных сервисов** |
|         | `docker stats $(docker compose ps -q worker)` | Отслеживание использования CPU, памяти и других ресурсов контейнера сервиса `worker` |
| [**`docker compose run --rm`**](https://docs.docker.com/reference/cli/docker/compose/run/) | | **Запуск временного контейнера с настройками сервисов, полезно для отладки** |
|         | `docker compose run --rm web sh` | Запустить одноразовый контейнер сервиса `web` с интерактивным shell |
| [**`docker container cp`**](https://docs.docker.com/reference/cli/docker/container/cp/) | | **Копирование файлов между хостом и контейнером** |
|         | `docker cp $(docker compose ps -q db):/dump.sql ./dump.sql` | Скопировать файл из контейнера сервиса `db` на хост |

> 💡 Для удобства отладки сложных многосервисных конфигураций используйте `docker compose run --rm`, чтобы запускать отдельные контейнеры с необходимыми сетями и томами без влияния на основные сервисы.

---

## Дополнительные ресурсы

### 🚫 Игнорирование файлов с помощью `.dockerignore`

Добавляй в файл `.dockerignore` файлы и папки, которые не должны попадать в образ, чтобы уменьшить размер и ускорить сборку:

```text
node_modules/
*.log
.env
```

### ⚡ Упрощение команд с помощью алиасов

Можно создать алиасы для часто используемых команд, чтобы запускать их быстрее:

```bash
alias dcu="docker compose up -d"
alias dcd="docker compose down"
alias dcb="docker compose build"
```

### 🧠 Подсказка: советы по работе с Docker

- Не пытайся запомнить всё — используй docker `--help` или `docker <command> --help` для изучения команд.
- Практикуйся регулярно и экспериментируй с простыми проектами.
- Следи за размером образов и убирай лишние файлы через `.dockerignore`.

### 🌐 Полезные ссылки

📘 **Официальная документация Docker** - подробное руководство и справочник по всем аспектам работы с Docker:
[https://docs.docker.com/](https://docs.docker.com/)

📙 **Шпаргалка по Docker** - полная официальная шпаргалка по Docker:
[https://dockerlabs.collabnix.com/docker/cheatsheet/](https://dockerlabs.collabnix.com/docker/cheatsheet/)

📗 **Docker Hub** - образы и реестры:
[https://hub.docker.com/](https://hub.docker.com/)
