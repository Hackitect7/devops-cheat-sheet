<style>
  table { table-layout: fixed; width: 100%; }
  td:nth-child(2) code { white-space: pre-wrap; overflow-wrap: anywhere; word-break: break-word; }
</style>

# ☸️ Kubernetes и kubectl

> 📘 Эта шпаргалка — практичный инструмент по `kubectl` и ключевым объектам Kubernetes. Она помогает быстро выполнять повседневные задачи (поиск и фильтрация ресурсов, деплой и масштабирование, отладка и доступ), не рыться в документации и сразу применять безопасные настройки и лучшие практики. Используйте её как «памятку при инцидентах», чек-лист перед релизом и набор готовых YAML-фрагментов для старта новых сервисов. Подойдёт новичкам и опытным инженерам: от базовых операций до профессиональных приёмов.

---

## 📂 Содержание

- [☸️ Kubernetes и kubectl](#️-kubernetes-и-kubectl)
  - [📂 Содержание](#-содержание)
  - [🔹 Основные команды](#-основные-команды)
  - [📄 Просмотр и фильтрация ресурсов](#-просмотр-и-фильтрация-ресурсов)
    - [Форматы вывода и JSONPath (для `kubectl get`)](#форматы-вывода-и-jsonpath-для-kubectl-get)
  - [🔧 Управление объектами](#-управление-объектами)
  - [📈 Масштабирование и релизы](#-масштабирование-и-релизы)
  - [🧰 Отладка, доступ и копирование](#-отладка-доступ-и-копирование)
  - [🌐 Сеть: Service, Ingress, NetworkPolicy](#-сеть-service-ingress-networkpolicy)
  - [🗄️ Хранилище: PV/PVC/StorageClass](#️-хранилище-pvpvcstorageclass)
    - [YAML-фрагменты: подключение PVC в Pod/Deployment](#yaml-фрагменты-подключение-pvc-в-poddeployment)
  - [🔐 Конфигурация и секреты](#-конфигурация-и-секреты)
    - [YAML-фрагменты: подключение ConfigMap/Secret в Pod](#yaml-фрагменты-подключение-configmapsecret-в-pod)
  - [🔑 RBAC и безопасность](#-rbac-и-безопасность)
  - [🧪 Ресурсы, пробы и HPA](#-ресурсы-пробы-и-hpa)
    - [YAML-фрагменты: ресурсы и пробы (вставляются в `containers[]`/`spec`)](#yaml-фрагменты-ресурсы-и-пробы-вставляются-в-containersspec)
  - [🧠 Продвинутые команды](#-продвинутые-команды)
  - [🤖 Автоматизация и лучшая практика](#-автоматизация-и-лучшая-практика)
  - [📦 Workloads: Deploy/STS/DS/Job/CronJob](#-workloads-deploystsdsjobcronjob)
  - [📌 Мини-шаблоны YAML](#-мини-шаблоны-yaml)
    - [Deployment + Service (ClusterIP)](#deployment--service-clusterip)
    - [Ingress (nginx-ingress) с TLS](#ingress-nginx-ingress-с-tls)
    - [PVC + использование тома в Pod](#pvc--использование-тома-в-pod)
    - [HPA v2 по CPU](#hpa-v2-по-cpu)
    - [NetworkPolicy: deny-all + allow из namespace web](#networkpolicy-deny-all--allow-из-namespace-web)
    - [RBAC: роль «только чтение» в namespace](#rbac-роль-только-чтение-в-namespace)
    - [Debug: эфемерный контейнер (через команду)](#debug-эфемерный-контейнер-через-команду)
  - [💡 Алиасы kubectl](#-алиасы-kubectl)
    - [Bash: автодополнение + базовый набор](#bash-автодополнение--базовый-набор)
    - [Zsh: автодополнение + базовый набор](#zsh-автодополнение--базовый-набор)
  - [📚 Дополнительные ресурсы](#-дополнительные-ресурсы)
    - [💡 Подсказки](#-подсказки)
    - [🌐 Полезные ссылки](#-полезные-ссылки)
      - [📘 Официальные справочники](#-официальные-справочники)
      - [📙 Сеть](#-сеть)
      - [📗 Масштабирование и метрики](#-масштабирование-и-метрики)
      - [📕 Хранилище](#-хранилище)
      - [📘 Безопасность и доступ](#-безопасность-и-доступ)
      - [📙 Workloads и основные объекты](#-workloads-и-основные-объекты)
      - [📗 Локальные кластеры](#-локальные-кластеры)
      - [📕 Плагины `kubectl`](#-плагины-kubectl)

---

## 🔹 Основные команды

> **Назначение:** базовые действия для подключения к кластеру, инвентаризации объектов и быстрой диагностики — версии, доступность, типы ресурсов, переключение контекстов, списки, подробности, логи и встроенная справка.

| Команда | Пример | Описание |
| ------- | ------ | -------- |
| [**`kubectl version`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#version) | | **Выводит версии клиента `kubectl` и сервера Kubernetes API. Используется для проверки соединения и совместимости** |
|         | `kubectl version --short` | Краткий удобный вывод версий |
|         | `kubectl version --client` | Показать только версию клиента (без запроса к серверу) |
|         | `kubectl version -o yaml` | Вывести в YAML для использования в CI/скриптах |
| [**`kubectl cluster-info`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#cluster-info) | | **Показывает адреса основных сервисов кластера (API server, DNS и др.). Применяется для быстрой проверки доступности** |
|         | `kubectl cluster-info` | Сводка по ключевым сервисам и их URL |
|         | `kubectl cluster-info dump --all-namespaces` | Собрать диагностический дамп (манифесты, события) для отладки |
|         | `kubectl --context prod cluster-info` | Запросить информацию для указанного контекста |
| [**`kubectl api-resources`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#api-resources) | | **Выводит список поддерживаемых типов ресурсов и их краткие имена. Полезно для проверки наличия CRD и соответствия манифестов** |
|         | `kubectl api-resources` | Базовый список ресурсов (kind, shortnames) |
|         | `kubectl api-resources -o wide` | Добавить группы/версии и дополнительные столбцы |
|         | `kubectl api-resources --namespaced=true` | Показать только namespaced-ресурсы (или `false` — кластерные) |
| [**`kubectl api-versions`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#api-versions) | | **Выводит все доступные группы/версии API в кластере. Нужна для сверки версий, используемых в манифестах** |
|         | `kubectl api-versions` | Полный перечень групп/версий API |
|         | `kubectl api-versions \| grep '^autoscaling/'` | Проверить наличие `autoscaling/v2` (HPA v2) |
|         | `kubectl api-versions \| grep -E '^(apps\|batch)/v1$'` | Убедиться, что доступны стабильные `apps/v1`, `batch/v1` |
| [**`kubectl config`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#config) | | **Управляет kubeconfig (кластеры, пользователи, контексты). Используется для переключения окружений и namespace по умолчанию** |
|         | `kubectl config get-contexts` | Список доступных контекстов |
|         | `kubectl config use-context prod` | Переключиться на контекст `prod` |
|         | `kubectl config set-context --current --namespace=dev` | Задать `dev` как namespace по умолчанию |
| [**`kubectl get`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#get) | | **Получает списки объектов. Базовая команда для инвентаризации и первичной диагностики** |
|         | `kubectl get nodes -o wide` | Состояние узлов с дополнительными полями (IP, роли) |
|         | `kubectl get all -A` | Все основные объекты во всех пространствах имён |
|         | `kubectl get pods -l app=web -A` | Вывести поды по label-селектору во всех `ns` |
| [**`kubectl describe`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#describe) | | **Печатает подробные сведения о ресурсе: спецификацию, текущее состояние, условия и связанные события. Используется для диагностики** |
|         | `kubectl describe node worker-1` | Показать роли, taints, условия готовности, capacity/allocatable и сводку по подам на узле |
|         | `kubectl describe pod web-xyz -n app` | Показать контейнеры, образы, переменные окружения, пробы, причины рестартов и события пода |
|         | `kubectl describe ingress web -n app` | Показать правила маршрутизации, аннотации контроллера, TLS-секцию и привязанные сервисы/пути |
| [**`kubectl logs`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#logs) | | **Выводит stdout/stderr контейнера. Применяется для анализа работы приложения и инцидентов** |
|         | `kubectl logs pod/web-xyz -n app -f` | Непрерывный вывод текущих логов (follow) |
|         | `kubectl logs pod/web-xyz -c nginx -n app --since=1h` | Логи выбранного контейнера за заданный период |
|         | `kubectl logs -l app=web -c nginx -n app --tail=200 -f` | Логи всех подов по label-селектору (массовый сбор) |
| [**`kubectl explain`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#explain) | | **Отображает справку по объектам и полям API: назначение, тип, вложенность и поддерживаемые значения** |
|         | `kubectl explain deploy.spec.strategy` | Описание стратегий развёртывания (RollingUpdate/Recreate) и их параметров |
|         | `kubectl explain pod.spec.containers.resources` | Структура и типы полей для `requests` и `limits` |
|         | `kubectl explain service.spec.ports` | Описание полей портов сервиса и вариантов конфигурации |

> ***Примечания:***  
> • `-A` показывает ресурсы во всех namespace; для точечных выборок используйте метки `-l key=value` и field-селекторы `--field-selector=...`.  
> • `describe` часто содержит полезные события внизу вывода — это первая подсказка при сбоях.  
> • `api-resources` подсказывает краткие имена ресурсов, пригодные в `kubectl get/describe`.  
> • Для предотвращения ошибок в окружениях держите актуальный контекст и namespace через `kubectl config`.

---

## 📄 Просмотр и фильтрация ресурсов

> **Назначение:** получить «картину состояния» кластера и быстро отфильтровать нужные объекты; посмотреть подробности ресурсов, логи и события; собрать метрики потребления; выбрать подходящий формат вывода и извлекать точечные данные для скриптов через JSONPath.

| Команда | Пример | Описание |
| ------- | ------ | -------- |
| [**`kubectl get`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#get) | | **Получает списки объектов с возможностью фильтрации и выбора формата вывода** |
|         | `kubectl get pods -n app -o wide` | Список подов в `app` с расширенными столбцами (IP, нода и т.п.) |
|         | `kubectl get pods -l app=web -A` | Фильтрация по меткам (label-selector) во всех неймспейсах |
|         | `kubectl get pods --field-selector=status.phase=Running -A` | Фильтрация по полям (field-selector), например только `Running` |
|         | `kubectl get deploy -w -n app` | «Наблюдать» изменения ресурса в реальном времени (`--watch`) |
| [**`kubectl describe`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#describe) | | **Показывает подробную спецификацию, текущее состояние и связанные события объекта** |
|         | `kubectl describe pod web-xyz -n app` | Детали пода: контейнеры, пробы, переменные окружения, события. |
|         | `kubectl describe node worker-1` | Состояние узла: роли, taints, условия, capacity/allocatable |
|         | `kubectl describe ingress web -n app` | Правила маршрутизации, аннотации контроллера, секция TLS |
| [**`kubectl logs`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#logs) | | **Выводит `stdout/stderr` контейнера для анализа работы приложения** |
|         | `kubectl logs pod/web-xyz -n app -f` | Непрерывный вывод текущих логов (`--follow`) |
|         | `kubectl logs pod/web-xyz -c nginx -n app --since=1h` | Логи выбранного контейнера за последний час |
|         | `kubectl logs -l app=web -c nginx -n app --tail=200 -f` | Логи всех подов по селектору меток (массовый сбор) |
| [**`kubectl get events`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#events) | | **Показывает события кластера для временной диагностики** |
|         | `kubectl get events -A --sort-by=.lastTimestamp` | Хронология событий во всех неймспейсах |
|         | `kubectl get events -n app --field-selector=involvedObject.name=web-xyz` | События, относящиеся к конкретному объекту |
|         | `kubectl get events -A --field-selector type=Warning` | Только предупреждения (если поле `type` поддерживается) |
| [**`kubectl top`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#top) | | **Показывает потребление CPU/памяти (требуется установленный metrics-server)** |
|         | `kubectl top pods -n app` | Использование ресурсов подами в `app` |
|         | `kubectl top nodes` | Сводка по узлам (CPU/Memory) |
|         | `kubectl top pods -l app=web -A` | Метрики только для подов с заданными метками |
| [**`kubectl explain`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#explain) | | **Справка по объектам и полям API (назначение, тип, вложенность)** |
|         | `kubectl explain deploy.spec.strategy` | Описание стратегий развёртывания и их параметров |
|         | `kubectl explain pod.spec.containers.resources` | Структура `requests`/`limits` и типы значений |
|         | `kubectl explain service.spec.ports` | Поля портов сервиса и варианты конфигурации |

### Форматы вывода и JSONPath (для `kubectl get`)

> **Назначение:** быстро получать данные в удобном виде для чтения, копирования в тикеты и последующей автоматизированной обработки (скрипты/CI).  
> **Полезно:** когда нужно вывести полную спецификацию ресурса, только имена объектов, свои столбцы, либо извлечь отдельные значения (например, IP, образ, статус).

**Форматы вывода (для `kubectl get`). Выбор формата результата для диагностики и последующей обработки**

| Пример | Описание |
| ------ | -------- |
| `-o wide` | Расширенные столбцы (узел, IP и др.) для удобного чтения |
| `-o yaml` / `-o json` | Полная спецификация объекта — удобно для diff/ревью и логов инцидентов |
| `-o name` | Только имена объектов (удобно для пайплайнов и последующей передачи в другие команды) |
| `-o custom-columns=NAME:.metadata.name,IP:.status.podIP` | Свои столбцы по нужным полям (подходит для отчётов/скриптов) |
| `-o jsonpath='{..image}'` | Готово к точечной выборке значений (см. примеры JSONPath ниже) |

**JSONPath (в составе `kubectl get`). Шаблоны для выборки конкретных данных из JSON-представления ресурсов**

| Пример | Описание |
| ------ | -------- |
| `kubectl get pod -n app -o jsonpath='{.items[*].status.podIP}'` | Вывести IP всех подов в namespace `app` |
| `kubectl get pod -n app -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.status.podIP}{"\n"}{end}'` | Таблица «имя пода → IP» по строкам (удобно копировать) |
| `kubectl get pod -n app -o jsonpath='{range .items[*]}{.metadata.name}{" => "}{range .spec.containers[*]}{.image}{" "}{end}{"\n"}{end}'` | Сопоставить каждый под со списком образов его контейнеров |

> ***Примечания:***  
> • Label-селекторы (`-l key=val`) и field-селекторы (`--field-selector=...`) можно комбинировать; `-A` показывает ресурсы во всех namespace.  
> • `--watch/-w` помогает наблюдать изменения в реальном времени; для одноразового снимка уберите `-w`.  
> • В `describe` внизу часто есть ключевые `Events`; для полной спецификации используйте `-o yaml` вместо `describe`.  
> • Логи: выбирайте контейнер `-c`, ограничивайте объём `--since`/`--tail`, собирайте массово по меткам `-l`.  
> • `kubectl top` требует установленный metrics-server; без него метрики CPU/RAM недоступны.  
> • Форматы вывода: `-o wide` для чтения, `-o name` для пайплайнов, `-o custom-columns=...` для табличных отчётов, `-o json|yaml` для машинной обработки.  
> • JSONPath: заключайте выражения в одинарные кавычки в bash (`-o jsonpath='{...}'`), экранируйте спецсимволы при необходимости; удобно вытаскивать IP, образы, статусы.  
> • События эфемерны и могут ротироваться; сортируйте по времени (`--sort-by=.lastTimestamp` или `.eventTime`) и, при необходимости, фильтруйте по объекту через `--field-selector=involvedObject.*`.

---

## 🔧 Управление объектами

> **Назначение:** привести объекты кластера к описанному состоянию (apply), заранее увидеть изменения (diff), вносить точечные правки без полного манифеста (patch), управлять образами и метаданными (set image/label/annotate) и безопасно перезапускать рабочие нагрузки (rollout restart).

| Команда | Пример | Описание |
| ------- | ------ | -------- |
| [**`kubectl apply`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#apply) | | **Создаёт/обновляет ресурсы по манифестам. Идемпотентно: приводит кластер к описанному состоянию** |
|         | `kubectl apply -f deploy.yaml` | Применить один файл манифеста |
|         | `kubectl apply -k overlays/prod` | Применить директорию Kustomize |
|         | `kubectl apply --server-side -f .` | Server-Side Apply (точный merge на стороне API-сервера) |
| [**`kubectl diff`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#diff) | | **Показывает различия между текущим состоянием кластера и манифестами (что изменится при `apply`)** |
|         | `kubectl diff -f .` | Сравнить все манифесты из текущей папки |
|         | `kubectl diff -k overlays/prod` | Сравнить результат рендера Kustomize |
|         | `kubectl diff --server-side -f deploy.yaml` | Дифф с учётом SSA-конфликтов полей |
| [**`kubectl delete`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#delete) | | **Удаляет ресурсы по типу/имени, селектору или файлу манифеста** |
|         | `kubectl delete -f deploy.yaml` | Удалить ресурс(ы), описанные в файле |
|         | `kubectl delete svc,ingress -l app=web -n app` | Удалить по label-селектору |
|         | `kubectl delete pod web-xyz --grace-period=0 --force -n app` | Форсированное удаление пода (аккуратно) |
| [**`kubectl edit`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#edit) | | **Открывает ресурс в `$EDITOR`, сохраняет изменения обратно в кластер** |
|         | `kubectl edit deployment web -n app` | Редактировать Deployment |
|         | `kubectl edit configmap app-cm -n app` | Редактировать ConfigMap |
|         | `KUBE_EDITOR="code --wait" kubectl edit svc web -n app` | Использовать нужный редактор |
| [**`kubectl patch`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#patch) | | **Частичное обновление ресурса без полного манифеста (merge/json/strategic)** |
|         | `kubectl patch deploy web -n app -p '{"spec":{"replicas":3}}' --type=merge` | Merge-patch: изменить реплики |
|         | `kubectl patch deploy web -n app --type=json -p='[{"op":"add","path":"/spec/template/metadata/annotations/checksum","value":"sha256:..."}]'` | JSON-patch: добавить аннотацию |
|         | `kubectl patch svc web -n app -p '{"spec":{"sessionAffinity":"ClientIP"}}' --type=merge` | Точечная настройка Service |
| [**`kubectl set image`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#set-image) | | **Меняет образ(ы) контейнеров у работающих workload-ов. Тригерит новый rollout** |
|         | `kubectl set image deploy/web app=repo:v2 -n app` | Обновить тег образа |
|         | `kubectl set image deploy/web app=repo@sha256:… -n app` | Обновить на образ по digest (immutable) |
|         | `kubectl set image ds/agent agent=org/agent:1.4 -n ops` | Обновить DaemonSet |
| [**`kubectl label`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#label) | | **Добавляет/изменяет метки (labels) для селекции и политики** |
|         | `kubectl label pod web-xyz tier=frontend --overwrite -n app` | Добавить/обновить метку пода |
|         | `kubectl label ns app istio-injection=enabled --overwrite` | Метка на namespace |
|         | `kubectl label pods -l app=web canary=true -n app` | Массово по селектору |
| [**`kubectl annotate`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#annotate) | | **Добавляет/изменяет аннотации (metadata) для служебных целей и триггеров** |
|         | `kubectl annotate deploy/web checksum/config=sha256:... --overwrite -n app` | Аннотация для триггера перезапуска по конфигу |
|         | `kubectl annotate svc web external-dns.alpha.kubernetes.io/hostname=app.example.com -n app` | Аннотация для интеграций (external-dns и др.) |
|         | `kubectl annotate pod web-xyz purpose=debug --overwrite -n app` | Временная пометка для отладки |
| [**`kubectl rollout restart`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#rollout) | | **Без изменения манифеста перезапускает поды workload-а (создаёт новую ReplicaSet-ревизию)** |
|         | `kubectl rollout restart deploy/web -n app` | Перезапустить Deployment |
|         | `kubectl rollout restart daemonset/agent -n ops` | Перезапустить DaemonSet |
|         | `kubectl rollout status deploy/web -n app` | Отслеживать завершение перезапуска |

> ***Примечания:***  
> • Перед `apply` в CI/CD запускайте `kubectl diff` и/или `--dry-run=server` — ловите ошибки схемы и неожиданные изменения заранее.  
> • Предпочитайте **Server-Side Apply**: `apply --server-side --field-manager=<имя>`; один стабильный `fieldManager` для всех пайплайнов уменьшает конфликты.  
> • `--force-conflicts` используйте только осознанно — вы перезаписываете владельца полей у других менеджеров.  
> • `patch` бывает `merge`/`json`/`strategic`: для CRD безопаснее `--type=json` или `merge`; `strategic` работает только для встроенных типов.  
> • `set image` лучше указывать по digest (`@sha256:…`) для иммутабельности; после изменения контролируйте `rollout status`.  
> • `label`/`annotate` всегда с `--overwrite`; аннотации типа `checksum/config=…` удобны как триггеры перезапуска.  
> • `delete` с селекторами используйте осторожно; явно задавайте `-n` и контекст; управляйте каскадом: `--cascade=foreground|background|orphan`.  
> • `edit` удобен для экстренных правок, но изменения не попадают в Git — закрепляйте итог в манифестах (GitOps).  
> • После `apply` полезно смотреть фактическую спеку `get -o yaml` — admission-webhook’и могли мутировать объект.  
> • Для повторяемости: фиксируйте порядок шагов `diff → apply → rollout status/wait` и тайм-ауты ожидания.

---

## 📈 Масштабирование и релизы

> **Назначение:** управлять масштабированием и жизненным циклом релизов — вручную менять число реплик, наблюдать прогресс развёртывания, смотреть историю и откатывать, временно приостанавливать/возобновлять обновления, безопасно перезапускать поды без изменения манифеста и включать автоскейлинг через HPA.

| Команда | Пример | Описание |
| ------- | ------ | -------- |
| [**`kubectl scale`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#scale) | | **Изменяет `spec.replicas` вручную для горизонтального масштабирования** |
|         | `kubectl scale deploy/web --replicas=3 -n app` | Масштабировать Deployment до 3 реплик |
|         | `kubectl scale sts/db --replicas=1 -n app` | Масштабировать StatefulSet (сохранит порядок) |
|         | `kubectl scale deploy -l app=web --replicas=0 -n app` | Массовое масштабирование по label-селектору |
| [**`kubectl rollout status`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#rollout) | | **Показывает состояние развёртывания (ожидание готовности новых подов)** |
|         | `kubectl rollout status deploy/web -n app` | Отслеживать прогресс rollout’а Deployment |
|         | `kubectl rollout status sts/db -n app --timeout=5m` | С таймаутом для StatefulSet |
|         | `kubectl rollout status ds/agent -n ops` | Проверить статус DaemonSet |
| [**`kubectl rollout history`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#rollout) | | **Показывает историю ревизий (ReplicaSet) для откатов и аудита** |
|         | `kubectl rollout history deploy/web -n app` | Краткая история ревизий |
|         | `kubectl rollout history deploy/web --revision=3 -n app` | Детали конкретной ревизии |
|         | `kubectl get rs -n app -l app=web -o wide` | Связанные ReplicaSet’ы и их параметры |
| [**`kubectl rollout undo`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#rollout) | | **Откатывает объект к предыдущей или указанной ревизии** |
|         | `kubectl rollout undo deploy/web -n app` | Откат к предыдущей ревизии |
|         | `kubectl rollout undo deploy/web --to-revision=3 -n app` | Откат на конкретную ревизию |
|         | `kubectl rollout status deploy/web -n app` | Контроль завершения отката |
| [**`kubectl rollout pause`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#rollout) | | **Приостанавливает обновления Deployment. Используется, чтобы внести несколько изменений без немедленного пересоздания подов** |
|         | `kubectl rollout pause deploy/web -n app` | Поставить на паузу обновления деплоя `web` в namespace `app` |
|         | `kubectl rollout pause deployment -l app=web -n app` | Поставить на паузу все деплои с меткой `app=web` |
|         | `kubectl rollout pause deploy/api -n app` | Пауза другого деплоя перед серией изменений |
| [**`kubectl set image`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#set-image) | | **Меняет образы контейнеров у рабочих нагрузок. Часто применяется во время паузы** |
|         | `kubectl set image deploy/web app=repo:v2 -n app` | Обновить контейнер `app` до тега `v2` |
|         | `kubectl set image deploy/web app=repo@sha256:... -n app` | Обновить образ по digest (immutable) |
|         | `kubectl set image deploy/web app=repo:v2 sidecar=side:v1 -n app` | Обновить несколько контейнеров в одном деплое |
| [**`kubectl rollout resume`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#rollout) | | **Возобновляет обновления Deployment. После внесённых изменений запускает rollout** |
|         | `kubectl rollout resume deploy/web -n app` | Возобновить обновления деплоя `web` |
|         | `kubectl rollout resume deployment -l app=web -n app` | Возобновить все деплои с меткой `app=web` |
|         | `kubectl rollout status deploy/web -n app` | Проверить, что rollout завершился успешно |
| [**`kubectl rollout restart`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#rollout) | | **Создаёт новую ревизию и перезапускает поды без изменения манифеста** |
|         | `kubectl rollout restart deploy/web -n app` | Обновить поды (например, после смены ConfigMap/Secret) |
|         | `kubectl rollout restart ds/agent -n ops` | Перезапуск DaemonSet |
|         | `kubectl rollout status deploy/web -n app` | Дождаться готовности после рестарта |
| [**`kubectl autoscale`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#autoscale) | | **Создаёт/обновляет HPA (autoscaling/v1) для масштабирования по CPU** |
|         | `kubectl autoscale deploy/web --cpu-percent=60 --min=2 --max=10 -n app` | HPA для Deployment по CPU |
|         | `kubectl get hpa -n app` | Проверить созданный HPA |
|         | `kubectl delete hpa web -n app` | Удалить HPA. *(Для памяти/кастом-метрик используйте YAML `autoscaling/v2`)* |

> ***Примечания:***  
> • `scale` и HPA: ручное изменение `.spec.replicas` будет перезаписано HPA; для ручного управления скорректируйте `minReplicas/maxReplicas` или удалите HPA.  
> • `rollout status` используйте с `--timeout` как гейт в CI; у Deployment настройте `progressDeadlineSeconds`.  
> • Паттерн `pause → apply/set image → resume` позволяет накопить несколько правок и раскатить их одним батчем.  
> • `rollout restart` добавляет аннотацию `kubectl.kubernetes.io/restartedAt` и перезапускает поды, но не меняет спецификацию.  
> • StatefulSet обновляется и масштабируется упорядоченно; для канареек используйте `updateStrategy.rollingUpdate.partition`, для параллельного старта — `podManagementPolicy: Parallel`.  
> • DaemonSet не масштабируется по репликам; контролируйте обновления через `updateStrategy` и `kubectl rollout status ds/...`.  
> • HPA v1 работает по CPU; для памяти/комбинированных/кастомных метрик используйте YAML `autoscaling/v2` и убедитесь, что установлен metrics-server.  
> • HPA обычно не масштабирует до нуля без внешних компонентов (например, KEDA).  
> • Контролируйте параметры стратегии деплоя: `maxSurge`/`maxUnavailable`, `revisionHistoryLimit`, `PodDisruptionBudget` — это снижает риск деградации.

---

## 🧰 Отладка, доступ и копирование

> **Назначение:** оперативная диагностика приложений и узлов — вход в контейнер (`exec`), подключение к уже работающему процессу (`attach`), локальный доступ к сервисам без внешней публикации (`port-forward`), перенос файлов (`cp`), безопасная отладка через эфемерные контейнеры (`debug`), а также обслуживание узлов и разбор их состояния (`describe node`, `cordon/drain/uncordon`).

| Команда | Пример | Описание |
| ------- | ------ | -------- |
| [**`kubectl exec`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#exec) | | **Выполняет команду внутри контейнера или открывает интерактивную оболочку. Используется для диагностики приложения** |
|         | `kubectl exec -it pod/web-xyz -n app -- bash` | Открыть интерактивную оболочку в контейнере (если нет `bash`, используйте `sh`) |
|         | `kubectl exec pod/web-xyz -n app -- printenv \| sort` | Выполнить одиночную команду и вывести результат |
|         | `kubectl exec -it pod/web-xyz -c app -n app -- sh` | Указать конкретный контейнер в поде |
| [**`kubectl attach`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#attach) | | **Подключается к уже запущенному процессу контейнера (PID 1). Не запускает новую оболочку** |
|         | `kubectl attach -it pod/web-xyz -n app` | Подключиться к основному процессу контейнера |
|         | `kubectl attach -it pod/web-xyz -c app -n app` | Подключиться к нужному контейнеру в поде |
|         | `kubectl attach pod/web-xyz -n app --sigusr1` | Отправить сигнал процессу (если поддерживается) |
| [**`kubectl port-forward`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#port-forward) | | **Пробрасывает локальный порт к порту пода/сервиса. Полезно для локальной проверки без публикации сервиса наружу** |
|         | `kubectl port-forward pod/web-xyz 8080:80 -n app` | Локальный `localhost:8080` → контейнерный порт `80` |
|         | `kubectl port-forward svc/web 8443:443 -n app` | Проброс к Service (распределяет на поды за сервисом) |
|         | `kubectl port-forward deploy/web 9090:9090 -n app` | Проброс к одному из подов Deployment’а |
| [**`kubectl cp`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#cp) | | **Копирует файлы/каталоги между локальной машиной и подом** |
|         | `kubectl cp app/pod:/var/log/app.log ./ -n app` | Скопировать файл из пода на локальную машину |
|         | `kubectl cp ./config.yml app/pod:/etc/app/config.yml -n app` | Загрузить файл в контейнер |
|         | `kubectl cp -c app app/pod:/data ./data -n app` | Указать контейнер (`-c`) при копировании |
| [**`kubectl debug`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#debug) | | **Запускает отладочный (эфемерный) контейнер рядом с целевым, не перезапуская приложение** |
|         | `kubectl debug pod/web-xyz --image=busybox:1.36 --target=app -n app` | Подключить эфемерный контейнер к поду и «прыгнуть» внутрь |
|         | `kubectl debug -it pod/web-xyz --image=busybox:1.36 -n app -- bash` | Интерактивная сессия в отладочном контейнере |
|         | `kubectl debug node/worker-1 -it --image=busybox:1.36` | Отладочный pod на конкретном узле для диагностики ноды |
| [**`kubectl describe node`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#describe) | | **Показывает детали узла: роли, taints, условия, capacity/allocatable, размещённые поды** |
|         | `kubectl describe node worker-1` | Диагностика проблем планирования или перегрузки узла |
|         | `kubectl get nodes -o wide` | Быстрый обзор IP/ролей перед подробной диагностикой |
|         | `kubectl top nodes` | Потребление CPU/памяти по узлам (если установлен metrics-server) |
| [**`kubectl cordon`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#cordon) | | **Помечает узел как `Unschedulable`. Новые поды на него не планируются; существующие остаются** |
|         | `kubectl cordon worker-1` | Запретить планирование на узле `worker-1` |
|         | `kubectl cordon worker-1 worker-2` | Пометить сразу несколько узлов |
|         | `kubectl get nodes` | Проверить, что статус у узла — `SchedulingDisabled` |
| [**`kubectl drain`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#drain) | | **Эвакуирует поды с узла и ставит его в `Unschedulable`. Уважает PDB, DaemonSet-поды не трогает** |
|         | `kubectl drain worker-1 --ignore-daemonsets --delete-emptydir-data --force --timeout=5m` | Типичный drain для обслуживания узла (удаляет `emptyDir`, форсит «несопровождаемые» поды) |
|         | `kubectl drain worker-1 --grace-period=60 --timeout=10m` | Задать время «мягкого» завершения подов и общий таймаут |
|         | `kubectl drain worker-1 --pod-selector='app!=critical' --ignore-daemonsets --delete-emptydir-data --force` | Эвакуировать только поды, подходящие под селектор |
| [**`kubectl uncordon`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#uncordon) | | **Снимает признак `Unschedulable`. На узел снова можно планировать поды** |
|         | `kubectl uncordon worker-1` | Вернуть узел в планирование |
|         | `kubectl uncordon worker-1 worker-2` | Включить несколько узлов |
|         | `kubectl get nodes -o wide` | Убедиться, что планирование разрешено |

> ***Примечания:***  
> • **`exec` vs `attach`:** `exec` запускает новый процесс (обычно оболочку) и не влияет на PID 1; `attach` «прилипает» к PID 1 и зависит от того, как он обрабатывает ввод/сигналы.  
> • **`port-forward`:** пробрасывает только TCP и по умолчанию слушает на `localhost`; нестабилен при перезапуске пода — для постоянного доступа используйте Service/Ingress/LoadBalancer.  
> • **`cp`:** под капотом использует `tar`; внутри контейнера должен быть доступен `tar`, иначе копируйте через `exec ... -- sh -c 'cat > /path/file'`; учитывайте, что завершающий `/` у путей меняет семантику копирования.  
> • **`debug` (эфемерные контейнеры):** не монтируют тома и порты, но разделяют неймспейсы с целевым контейнером — удобно ставить диагностические утилиты без изменения образа; для отладки ноды `kubectl debug node/...` создаёт привилегированный под — требуется соответствующий RBAC.  
> • **`describe node`:** смотрите `Taints`, `Conditions` и размещённые поды; для метрик — `kubectl top nodes` (нужен metrics-server).  
> • **`cordon`/`drain`/`uncordon`:** перед `drain` проверьте `PodDisruptionBudget` (`kubectl get pdb -A`); используйте `--ignore-daemonsets` и задавайте `--grace-period/--timeout`; `drain` удаляет лишь управляемые контроллерами поды — одиночные поды требуют `--force`.  
> • В проде избегайте «ручных» изменений внутри контейнера; фиксируйте находки в манифестах и применяйте через GitOps-поток.

---

## 🌐 Сеть: Service, Ingress, NetworkPolicy

> **Назначение:** проверить сетевую доступность сервисов, понять, куда идёт трафик (L4/L7), и увидеть, какие сетевые политики действуют. Полезно при «не открывается», 404/502, timeouts и изоляции по NetworkPolicy.

| Команда | Пример | Описание |
| ------- | ------ | -------- |
| [**`kubectl get svc`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#get) | | **Список Service и их параметры публикации (тип, IP, порты)** |
|         | `kubectl get svc web -n app -o wide` | Посмотреть тип (ClusterIP/NodePort/LB), IP и порты сервиса `web` |
|         | `kubectl get svc -l app=web -n app` | Отфильтровать сервисы по метке `app=web` |
|         | `kubectl get svc web -n app -o yaml` | Полная спецификация сервиса для диагностики/ревью |
| [**`kubectl get endpoints`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#get) | | **Показывает реальные backend-адреса (IP:порт) подов, на которые указывает Service** |
|         | `kubectl get endpoints web -n app -o wide` | Посмотреть IP и порты подов за сервисом `web` |
|         | `kubectl get endpoints -l app=web -n app` | Список эндпоинтов для сервисов с меткой `app=web` |
|         | `kubectl get endpoints web -n app -o yaml` | Полная спецификация эндпоинтов для подробной диагностики |
| [**`kubectl get endpointslices`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#get) | | **Показывает EndpointSlice — масштабируемое представление тех же backend-адресов** |
|         | `kubectl get endpointslices -n app` | Список всех EndpointSlice в namespace `app` |
|         | `kubectl get endpointslices -l kubernetes.io/service-name=web -n app -o yaml` | Слайсы, относящиеся к сервису `web`, с деталями |
|         | `kubectl get endpointslices -n app -o wide` | Краткая сводка по адресам/портам в слайсах |
| [**`kubectl describe ingress`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#describe) | | **Детали L7-маршрутизации: хосты/пути, аннотации контроллера, TLS** |
|         | `kubectl describe ingress web -n app` | Правила и backend-сервисы для Ingress `web` |
|         | `kubectl get ingress -A` | Быстрый обзор всех Ingress во всех `ns` |
|         | `kubectl get ingress web -n app -o yaml` | Проверить аннотации (time-outs, body-size и др.) |
| [**`kubectl exec`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#exec) | | **Выполняет команду внутри контейнера. Используется для внутрекластерной проверки сети (HTTP/DNS) из пода** |
|         | `kubectl exec -it pod/busy -n app -- curl -sS http://web:80/healthz` | Проверка HTTP-доступности сервиса `web` по имени |
|         | `kubectl exec -it pod/busy -n app -- wget -qO- http://10.0.0.5:8080/metrics` | Прямая проверка по Pod IP/порту |
|         | `kubectl exec -it pod/busy -n app -- nslookup web` | Проверка DNS-имени сервиса (service discovery) |
| [**`kubectl get networkpolicy`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#get) | | **Показывает список сетевых политик и их краткие параметры** |
|         | `kubectl get networkpolicy -A` | Все NetworkPolicy во всех неймспейсах |
|         | `kubectl get netpol -n app -o wide` | Полезные столбцы по политикам в `app` |
|         | `kubectl get netpol allow-from-web -n db -o yaml` | Полная спецификация конкретной политики |
| [**`kubectl describe networkpolicy`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#describe) | | **Детально показывает селекторы, направления (`Ingress/Egress`) и порты политики** |
|         | `kubectl describe networkpolicy allow-from-web -n db` | Разбор правил: откуда, куда, какие порты |
|         | `kubectl describe netpol -n app` | Детали всех политик в namespace `app` |
|         | `kubectl get events -n db --field-selector=involvedObject.kind=NetworkPolicy` | Связанные события (если есть) для диагностики |

> ***Примечания:***  
> • **Service ↔ Endpoints/EndpointSlice**: в обычном Service учитываются только *готовые* поды; чтобы публиковать неготовые, используйте `publishNotReadyAddresses: true`.  
> • **Headless Service (`ClusterIP: None`)**: не получает виртуальный IP; DNS возвращает A-записи подов — удобно для STS и прямых подключений.  
> • **ExternalName**: не имеет Endpoints вообще; это DNS-алиас на внешний FQDN — проверяйте через `kubectl get svc ... -o yaml`.  
> • **LoadBalancer/NodePort**: внешний доступ появляется, когда в `.status.loadBalancer` появился IP/hostname; `externalTrafficPolicy: Local` сохраняет исходный IP, но требует хотя бы один *готовый* под на ноде-эндоинте.  
> • **NodePort диапазон**: по умолчанию `30000–32767`, но может быть переопределён в конфигурации кластера.  
> • **Ingress**: работает только при наличии контроллера; проверяйте `ingressClassName`/класс и аннотации конкретного контроллера, а также валидность TLS-секрета.  
> • **DNS**: FQDN сервиса — `<svc>.<ns>.svc.cluster.local`; у headless сервисов DNS возвращает pod A-записи; для отладки полезны `nslookup/dig` из пода.  
> • **NetworkPolicy**: политики аддитивны и применяются только при поддержке CNI; начните с `default-deny` и далее добавляйте *точные* allow-правила.  
> • **Диагностика цепочки L7**: `Ingress → Service → Endpoints/EndpointSlice → Pod readiness` — отсутствие любого звена приведёт к 404/502/таймаутам.

---

## 🗄️ Хранилище: PV/PVC/StorageClass

> **Назначение:** быстро посмотреть доступные классы/тома, создать или расширить PVC, понять причины `Pending`/привязки и типичные ошибки.

| Команда | Пример | Описание |
| ------- | ------ | -------- |
| [**`kubectl get sc`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#get) | | **Показать доступные StorageClass и настройки** |
|         | `kubectl get sc` | Список SC и пометка `(default)` у класса по умолчанию |
|         | `kubectl get sc <name> -o yaml` | Проверить `allowVolumeExpansion`, параметры провайдера и аннотации |
|         | `kubectl get sc -o custom-columns=NAME:.metadata.name,DEFAULT:.metadata.annotations['storageclass.kubernetes.io/is-default-class'],BINDING:.volumeBindingMode` | Обзор default-класса и режима привязки (`WaitForFirstConsumer`/`Immediate`) |
| [**`kubectl get pv`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#get) | | **Посмотреть PV и ключевые поля** |
|         | `kubectl get pv -o wide` | Статус, размер, `RECLAIM POLICY`, привязка к PVC |
|         | `kubectl get pv -o custom-columns=NAME:.metadata.name,CLAIM:.spec.claimRef.name,SC:.spec.storageClassName,STATUS:.status.phase` | Кастомные столбцы для аудита привязок |
|         | `kubectl get pv <pv> -o jsonpath='{.spec.persistentVolumeReclaimPolicy}'` | Узнать `Delete`/`Retain` у конкретного PV |
| [**`kubectl get pvc`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#get) | | **Показать статус и параметры PVC** |
|         | `kubectl get pvc -n app -o wide` | Статус (`Pending/Bound`), размер и StorageClass |
|         | `kubectl get pvc data -n app -w` | Следить за изменением статуса (watch) |
|         | `kubectl get pvc data -n app -o jsonpath='{.status.capacity.storage}'` | Фактический размер после расширения |
| [**`kubectl apply`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#apply) | | **Создать объекты из манифеста (для PVC — заявить том нужного размера/режима)** |
|         | `kubectl apply -f pvc.yaml` | Создать PVC по манифесту |
|         | `kubectl apply --dry-run=server -f pvc.yaml` | Проверить валидность на API-сервере перед применением |
|         | `kubectl apply --server-side -f pvc.yaml` | Применить с SSA для корректного мерджа полей |
| [**`kubectl describe pvc`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#describe) | | **Подробности PVC и связанные события (диагностика `Pending`)** |
|         | `kubectl describe pvc data -n app` | Причины непривязки, несоответствие SC/размера/топологии |
|         | `kubectl describe pv <pv-name>` | Проверить соответствие `accessModes`/`capacity`/лейблы PV |
|         | `kubectl get events -n app --field-selector=involvedObject.name=data` | События, связанные с PVC `data` |
| [**`kubectl patch pvc`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#patch) | | **Изменить размер PVC (если SC поддерживает расширение)** |
|         | `kubectl patch pvc data -n app -p '{"spec":{"resources":{"requests":{"storage":"20Gi"}}}}'` | Увеличить PVC до `20Gi` |
|         | `kubectl patch pvc data -n app --type=json -p='[{"op":"replace","path":"/spec/resources/requests/storage","value":"30Gi"}]'` | Увеличить через JSON-patch |
|         | `kubectl get pvc data -n app -w` | Наблюдать статусы `FileSystemResizePending/Bound` |
| [**`kubectl patch pv`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#patch) | | **Сменить политику возврата PV** |
|         | `kubectl patch pv <pv> -p '{"spec":{"persistentVolumeReclaimPolicy":"Retain"}}'` | Сохранить данные после удаления PVC |
|         | `kubectl patch pv <pv> -p '{"spec":{"persistentVolumeReclaimPolicy":"Delete"}}'` | Вернуть удаление PV вместе с данными |
|         | `kubectl get pv <pv> -o jsonpath='{.spec.persistentVolumeReclaimPolicy}'` | Проверить текущую политику |
| [**`kubectl delete pvc`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#delete) | | **Удалить PVC** |
|         | `kubectl delete pvc data -n app` | Поведение с данными зависит от `reclaimPolicy` и драйвера |
|         | `kubectl delete pvc -l app=db -n app` | Массовое удаление по метке |
|         | `kubectl delete pvc data -n app --wait=false` | Не ждать завершения операции |
| [**`kubectl krew`**](https://krew.sigs.k8s.io/) | | **Управление плагинами для `kubectl`** |
|         | `kubectl krew install df-pv` | Установить плагин для просмотра занятости PV |
|         | `kubectl krew install neat` | Установить плагин для «очистки» YAML от служебных полей |
| [**`kubectl df-pv`**](https://github.com/yashbhutwala/kubectl-df-pv) | | **Быстрая сводка использования диска по PVC/PV** |
|         | `kubectl df-pv -n app` | Показать занятость по namespace `app` |
| [**`kubectl neat`**](https://github.com/itaysk/kubectl-neat) | | **Показывает «чистый» YAML без служебных полей** |
|         | `kubectl get pvc -n app -o yaml \| kubectl neat` | Удобно для ревью и документации |

### YAML-фрагменты: подключение PVC в Pod/Deployment

| Фрагмент | Назначение |
| -------- | ---------- |
| `volumeMounts: [{ name: data, mountPath: /data }]` | Точка монтирования тома в контейнере |
| `volumes: [{ name: data, persistentVolumeClaim: { claimName: data } }]` | Привязка PVC к Pod |
| `securityContext: { fsGroup: 1000 }` | Права на смонтированный том (по необходимости) |

> ***Примечания:***  
> • `volumeBindingMode` в StorageClass: `WaitForFirstConsumer` откладывает привязку PV до планирования пода — частая причина `Pending` при несоответствии зон/топологии.  
> • `RWX` требует соответствующего драйвера/ФС (например, NFS/CephFS); многие блочные CSI поддерживают только `RWO`.  
> • PVC обычно можно **только увеличивать**; уменьшение не поддерживается большинством драйверов и может привести к потере данных.  
> • Расширение тома может требовать перезапуска пода или ремонта; следите за стадиями `FileSystemResizePending/Bound`.  
> • Класс по умолчанию помечается аннотацией `storageclass.kubernetes.io/is-default-class: "true"`.  
> • Динамическое провижининг обычно создаёт PV с `reclaimPolicy: Delete`; при статическом PV часто используют `Retain`.  
> • Для `volumeMode: Block` поведение и процедуры расширения отличаются от файловых томов — проверяйте документацию CSI.

---

## 🔐 Конфигурация и секреты

> **Назначение:** быстро создать/просмотреть ConfigMap/Secret и корректно подключить их к подам; при необходимости — безопасно декодировать значения для диагностики.

| Команда | Пример | Описание |
| ------- | ------ | -------- |
| [**`kubectl create configmap`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#create-configmap) | | **Создаёт ConfigMap из литералов, файлов или env-файла** |
|         | `kubectl create configmap app-cm --from-literal=LOG=info -n app` | Создать из пары ключ/значение |
|         | `kubectl create configmap app-cm --from-file=config.yml -n app` | Создать из файла/каталога |
|         | `kubectl create configmap env-cm --from-env-file=.env -n app` | Создать из `.env` |
| [**`kubectl create secret generic`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#create-secret) | | **Создаёт Secret общего типа из литералов/файлов** |
|         | `kubectl create secret generic app-secret --from-literal=PASS=123 -n app` | Из литерала (значение будет base64 внутри кластера) |
|         | `kubectl create secret generic tls-extra --from-file=cert.pem --from-file=key.pem -n app` | Из файлов |
|         | `kubectl create secret generic cfg --from-file=config=conf.yml -n app` | Задать ключ (`config`) для файла |
| [**`kubectl create secret tls`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#create-secret) | | **Создаёт TLS-секрет из пары `--cert/--key`** |
|         | `kubectl create secret tls site-tls --cert=cert.pem --key=key.pem -n app` | TLS для Ingress/клиентских соединений |
|         | `kubectl get secret site-tls -n app -o yaml` | Проверить тип `kubernetes.io/tls` и ключи `tls.crt/tls.key` |
| [**`kubectl get secret`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#get) | | **Получить секреты и их спецификации. Подходит для `-o yaml/json/jsonpath`** |
|         | `kubectl get secrets -n app` | Список секретов в namespace |
|         | `kubectl get secret app-secret -n app -o yaml` | Полная спецификация; значения лежат в `.data` (base64) |
|         | `kubectl get secret app-secret -n app -o jsonpath='{.data}'` | Показать все ключи секрета (значения в base64) |
|         | `kubectl get secret app-secret -n app -o jsonpath='{.data.PASS}' \| base64 -d; echo` | Декодировать значение ключа `PASS` |
|         | `kubectl get secret app-secret -n app -o jsonpath="{.data.\*}" \| tr ' ' '\n' \| base64 -d` | Декодировать все значения (по одному на строку) |
| [**`kubectl describe secret`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#describe) | | **Человекочитаемая сводка: тип и список ключей (без значений)** |
|         | `kubectl describe secret app-secret -n app` | Тип секрета и перечень ключей |
|         | `kubectl describe secrets -n app` | Краткие сведения по всем секретам в namespace |
|         | `kubectl get events -n app --field-selector=involvedObject.kind=Secret,involvedObject.name=app-secret` | Связанные события (если фиксируются) |
| [**`kubectl delete`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#delete) | | **Удаление ConfigMap/Secret** |
|         | `kubectl delete secret app-secret -n app` | Удалить Secret |
|         | `kubectl delete configmap app-cm -n app` | Удалить ConfigMap |

### YAML-фрагменты: подключение ConfigMap/Secret в Pod

| Фрагмент | Назначение |
| -------- | ---------- |
| `envFrom: [ { configMapRef: { name: app-cm } }, { secretRef: { name: app-secret } } ]` | Подключить все пары как переменные окружения |
| `env: [ { name: LOG_LEVEL, valueFrom: { configMapKeyRef: { name: app-cm, key: LOG } } }, { name: DB_PASS, valueFrom: { secretKeyRef: { name: app-secret, key: PASS } } } ]` | Точечно взять ключи из CM/Secret в env |
| `volumes: [ { name: tls, secret: { secretName: site-tls } } ]` | Описать секрет-том в PodSpec |
| `volumeMounts: [ { name: tls, mountPath: /etc/tls, readOnly: true } ]` | Смонтировать секрет-том в контейнер |
| `{"apiVersion":"v1","kind":"Secret","metadata":{"name":"app-secret"},"type":"Opaque","stringData":{"PASS":"123"}}` | Пример секрета с stringData без ручного base64 |

> ***Примечания:***  
> • Secrets — это base64-кодирование, не шифрование; включайте шифрование на уровне кластера (Encryption at Rest через KMS).  
> • Для GitOps используйте `stringData` и внешнее шифрование (Sealed Secrets, SOPS, KMS).  
> • По возможности не прокидывайте секреты через `env`: они видны в `/proc/<pid>/environ` и могут попасть в логи; безопаснее монтировать как readOnly volume.  
> • Ставьте `immutable: true` для стабильных ConfigMap/Secret — меньше шанс случайного апдейта и меньше нагрузка на kubelet.  
> • Размер одного объекта ограничен ≈1 MiB; большие цепочки сертификатов делите или храните вне кластера.  
> • Используйте правильные типы: `kubernetes.io/tls` (ключи `tls.crt`/`tls.key`), `kubernetes.io/dockerconfigjson` (`.dockerconfigjson`) — это упрощает интеграции.  
> • Давайте узкие RBAC-права на Secret и namespace, ведите аудит операций `get/list/watch`.  
> • Декодируйте значения только на доверенных машинах; не публикуйте `kubectl get secret -o yaml` в общих логах.  
> • Для ротации секретов версионируйте ключи и используйте checksum-аннотации на PodTemplate, чтобы триггерить перезапуск подов.  
> • Секрет доступен только в своём namespace; для общего доступа предусмотрите отдельный механизм или продублируйте.

---

## 🔑 RBAC и безопасность

> **Назначение:** определить «кто вы» в кластере, проверить права на действия, посмотреть/назначить роли и биндинги, а также проверять доступ от имени другого субъекта (имперсонация).

| Команда | Пример | Описание |
| ------- | ------ | -------- |
| [**`kubectl auth whoami`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#auth) | | **Показывает текущего пользователя/группы по kubeconfig (или при имперсонации)** |
|         | `kubectl auth whoami` | Текущий субъект и его группы |
|         | `kubectl auth whoami --as=system:serviceaccount:app:deployer` | От имени сервис-аккаунта `app/deployer` |
|         | `kubectl auth whoami --as-group=devs --as-group=qa` | Добавить группы для проверки сценария |
| [**`kubectl auth can-i`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#auth) | | **Проверка разрешений (RBAC) на действие над ресурсом** |
|         | `kubectl auth can-i create deploy -n app` | Можно ли создавать Deployment в `app` |
|         | `kubectl auth can-i --list -n app` | Список всех разрешённых операций в `app` |
|         | `kubectl auth can-i get secrets --namespace app --resource-name app-secret` | Проверка доступа к конкретному объекту |
| [**`kubectl get role`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#get) | | **Список ролей в namespace** |
|         | `kubectl get role -n app` | Обзор ролей в `app` |
|         | `kubectl get role pod-reader -n app -o yaml` | Полная спецификация роли `pod-reader` |
| [**`kubectl get rolebinding`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#get) | | **Список привязок ролей в namespace** |
|         | `kubectl get rolebinding -n app` | Обзор биндингов в `app` |
|         | `kubectl get rolebinding view-user -n app -o yaml` | Полная спецификация привязки `view-user` |
| [**`kubectl get clusterrole`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#get) | | **Список кластерных ролей (глобальная область)** |
|         | `kubectl get clusterrole -o wide` | Расширенный вывод по ролям |
|         | `kubectl get clusterrole view -o yaml` | Полная спецификация роли `view` |
| [**`kubectl get clusterrolebinding`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#get) | | **Список кластерных привязок ролей** |
|         | `kubectl get clusterrolebinding` | Обзор кластерных привязок |
|         | `kubectl get clusterrolebinding -o wide` | Кому выданы кластерные роли |
|         | `kubectl get clusterrolebinding devs-read -o yaml` | Полная спецификация привязки `devs-read` |
| [**`kubectl describe role`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#describe) | | **Детали роли в namespace** |
|         | `kubectl describe role pod-reader -n app` | Правила роли `pod-reader` в `app` |
|         | `kubectl describe role -n app` | Все роли с деталями в `app` |
|         | `kubectl get role pod-reader -n app -o yaml` | YAML роли для ревью |
| [**`kubectl describe rolebinding`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#describe) | | **Детали привязок ролей в namespace** |
|         | `kubectl describe rolebinding view-user -n app` | Кому и какая роль назначена |
|         | `kubectl describe rolebinding -n app` | Все привязки с деталями в `app` |
|         | `kubectl get rolebinding view-user -n app -o yaml` | YAML привязки для ревью |
| [**`kubectl describe clusterrole`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#describe) | | **Детали кластерной роли** |
|         | `kubectl describe clusterrole view` | Правила роли `view` |
|         | `kubectl describe clusterrole admin` | Правила роли `admin` |
|         | `kubectl get clusterrole view -o yaml` | YAML роли `view` |
| [**`kubectl describe clusterrolebinding`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#describe) | | **Детали кластерных привязок ролей** |
|         | `kubectl describe clusterrolebinding devs-read` | Кому выдана роль `view` (пример) |
|         | `kubectl describe clusterrolebinding` | Все кластерные привязки с деталями |
|         | `kubectl get clusterrolebinding devs-read -o yaml` | YAML привязки `devs-read` |
| [**`kubectl create rolebinding`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#create-rolebinding) | | **Привязка роли/кластерной роли к пользователю/группе/SA в namespace** |
|         | `kubectl create rolebinding view-user --clusterrole=view --user=alice@example.com -n app` | Выдать `view` пользователю в `app` |
|         | `kubectl create rolebinding edit-devs --clusterrole=edit --group=devs -n app` | Выдать `edit` группе `devs` |
|         | `kubectl create rolebinding deployer-sa --clusterrole=edit --serviceaccount=app:deployer -n app` | Выдать `edit` сервис-аккаунту `app/deployer` |
| [**`kubectl create clusterrolebinding`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#create-clusterrolebinding) | | **Кластерная привязка роли — действует во всех namespace** |
|         | `kubectl create clusterrolebinding audit-admin --clusterrole=cluster-admin --user=security@example.com` | Полные права пользователю |
|         | `kubectl create clusterrolebinding devs-read --clusterrole=view --group=devs` | Чтение кластерно для группы |
|         | `kubectl create clusterrolebinding sa-ci --clusterrole=edit --serviceaccount=ci:runner` | `edit` для SA `ci/runner` во всех ns |
| [**`kubectl create role`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#create-role) | | **Создать роль с нужными действиями в namespace** |
|         | `kubectl create role pod-reader --verb=get,list,watch --resource=pods -n app` | Роль чтения Pod в `app` |
|         | `kubectl create role secret-reader --verb=get --resource=secrets -n app` | Роль чтения Secret |
|         | `kubectl get role pod-reader -n app -o yaml` | Проверить созданную роль |
| [**`kubectl create clusterrole`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#create-clusterrole) | | **Создать кластерную роль (глобальная область)** |
|         | `kubectl create clusterrole ns-reader --verb=get,list --resource=namespaces` | Чтение ресурсов `namespaces` |
|         | `kubectl get clusterrole ns-reader -o yaml` | Проверить правила роли |
|         | `kubectl delete clusterrole ns-reader` | Удалить роль при необходимости |
| [**`kubectl auth can-i`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#auth) | | **Проверка разрешений (RBAC) на действие над ресурсом** |
|         | `kubectl auth can-i create deploy -n app` | Можно ли создавать Deployment в `app` |
|         | `kubectl auth can-i --list -n app` | Список всех разрешённых операций в `app` |
|         | `kubectl auth can-i get pods --as alice@example.com -n app` | Проверка доступа от имени другого субъекта |

> ***Примечания:***  
> • **Role** и **RoleBinding** — действуют в пределах namespace; **ClusterRole** и **ClusterRoleBinding** — кластерно.  
> • **RoleBinding** может привязывать и `Role`, и `ClusterRole` в конкретном namespace.  
> • Сервис-аккаунт указывается как `system:serviceaccount:<ns>:<name>`.
> • `can-i --list` даёт быстрый обзор прав; для точной проверки конкретного объекта используйте `--resource-name`.  
> • Для узкой выдачи прав используйте `resourceNames` в правилах роли — это ограничит доступ до конкретных объектов.  
> • Aggregated ClusterRoles собираются по лейблам (`rbac.authorization.k8s.io/aggregate-to-*`) — удобно расширять стандартные `view/edit/admin` в организации.

---

## 🧪 Ресурсы, пробы и HPA

> **Назначение:** задать пределы ресурсов контейнеров, настроить проверки готовности/живости и включить автоматическое масштабирование по метрикам.

| Команда | Пример | Описание |
| ------- | ------ | -------- |
| [**`kubectl top`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#top) | | **Показать текущие метрики потребления CPU/памяти (требуется metrics-server)** |
|         | `kubectl top pods -n app` | Метрики подов в namespace `app` |
|         | `kubectl top pod web-xyz -n app --containers` | Метрики по контейнерам внутри пода |
|         | `kubectl top nodes` | Сводка по узлам |
| [**`kubectl set resources`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#set-resources) | | **Изменить `requests/limits` у Deployment/StatefulSet/Job и др** |
|         | `kubectl set resources deploy/web -n app --requests=cpu=200m,memory=128Mi --limits=cpu=500m,memory=256Mi` | Задать ресурсы для контейнеров деплоя |
|         | `kubectl set resources deploy -l app=web -n app --requests=cpu=300m --limits=cpu=1` | Массово по селектору |
|         | `kubectl set resources sts/db -n app --limits=memory=2Gi` | Только limit памяти для StatefulSet |
|         | `kubectl set resources deploy/web -c app -n app --requests=cpu=200m --limits=cpu=1` | Изменить ресурсы только контейнера `app` в деплое |
| [**`kubectl autoscale`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#autoscale) | | **Создать/обновить HPA (v1) по CPU** |
|         | `kubectl autoscale deploy/web --cpu-percent=60 --min=2 --max=10 -n app` | HPA по CPU для деплоя |
|         | `kubectl autoscale deploy/api --cpu-percent=75 --min=3 --max=15 -n app` | Другой таргет, другие пределы |
| [**`kubectl get hpa`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#get) | | **Список/спецификация HPA** |
|         | `kubectl get hpa -n app` | Все HPA в namespace |
|         | `kubectl get hpa web -n app -o yaml` | Полная спецификация HPA `web` |
|         | `kubectl get hpa web -n app -w` | Наблюдать изменения показателей/реплик |
| [**`kubectl describe hpa`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#describe) | | **Детали: текущие метрики, цель, состояние масштабирования** |
|         | `kubectl describe hpa web -n app` | Диагностика: что видит HPA и почему скейлит/не скейлит |
|         | `kubectl describe hpa -n app` | Все HPA в namespace |
|         | `kubectl get events -n app --field-selector=involvedObject.kind=HorizontalPodAutoscaler` | Связанные события (если фиксируются) |
| [**`kubectl delete hpa`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#delete) | | **Удалить горизонтальный автоскейлер** |
|         | `kubectl delete hpa web -n app` | Отключить HPA для деплоя `web` |
|         | `kubectl delete hpa --all -n app` | Удалить все HPA в namespace |
|         | `kubectl get hpa -n app` | Контроль, что удалены |

### YAML-фрагменты: ресурсы и пробы (вставляются в `containers[]`/`spec`)

| Фрагмент | Назначение |
| -------- | ---------- |
| `resources: { requests: { cpu: "100m", memory: "128Mi" }, limits: { cpu: "500m", memory: "256Mi" } }` | Базовый QoS и защита от OOM/троттлинга |
| `readinessProbe: { httpGet: { path: "/", port: 80 }, periodSeconds: 5, initialDelaySeconds: 3 }` | Готовность к приёму трафика (влияет на Service/Ingress) |
| `livenessProbe: { tcpSocket: { port: 80 }, initialDelaySeconds: 10, periodSeconds: 10, failureThreshold: 3 }` | Автовосстановление контейнера при «зависании» |
| `startupProbe: { httpGet: { path: "/healthz", port: 8080 }, failureThreshold: 30, periodSeconds: 5 }` | Даёт приложению время на старт, прежде чем проверять liveness |
| `{"apiVersion":"autoscaling/v2","kind":"HorizontalPodAutoscaler","metadata":{"name":"web","namespace":"app"},"spec":{"scaleTargetRef":{"apiVersion":"apps/v1","kind":"Deployment","name":"web"},"minReplicas":2,"maxReplicas":10,"metrics":[{"type":"Resource","resource":{"name":"cpu","target":{"type":"Utilization","averageUtilization":60}}}]}}` | Пример HPA v2 по CPU (аналог `kubectl autoscale`) |

> ***Примечания:***  
> • Классы QoS: **Guaranteed** (requests=limits для всех контейнеров), **Burstable** (частично заданы), **BestEffort** (нет requests/limits).  
> • `kubectl autoscale` управляет HPA v1 (CPU). Для памяти/комбинированных/кастомных метрик используйте YAML `autoscaling/v2` с `metrics`.  
> • Для работы `kubectl top`/HPA необходим установленный **metrics-server**.
> • Пока активна `startupProbe`, проверки `liveness/readiness` игнорируются — это нормально при долгом старте приложения.  
> • Единицы: CPU в millicores (`100m` = 0.1 vCPU), память — `Mi/Gi`; значения лучше указывать в кавычках в Helm-шаблонах.  
> • HPA изменяет `.spec.replicas`; ручное `scale` будет переезжаться HPA — корректируйте `minReplicas/maxReplicas` или временно удаляйте HPA.  
> • Для памяти/кастомных метрик используйте HPA **autoscaling/v2** и убедитесь, что есть провайдер метрик (metrics-server/Prometheus Adapter).  
> • Слишком агрессивные `livenessProbe` приводят к перезапускам; начинайте с мягких таймингов и увеличивайте `failureThreshold`.

---

## 🧠 Продвинутые команды

> **Назначение:** безопасные изменения и диагностика на проде — серверная валидация, дифф, точный merge (SSA), ожидание условий, глубокая справка и raw-эндпоинты.

| Команда | Пример | Описание |
| ------- | ------ | -------- |
| [**`kubectl apply`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#apply) | | **Применение манифестов, в том числе через Server-Side Apply** |
|         | `kubectl apply --server-side -f .` | Точный merge на стороне API-сервера (SSA) |
|         | `kubectl apply --server-side --field-manager=gitops -f .` | Явный владелец полей для GitOps-процессов |
|         | `kubectl apply -f . --prune -l app=web` | Удалить ресурсы с меткой, которых нет в текущем наборе манифестов |
| [**`kubectl diff`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#diff) | | **Показать различия между кластером и манифестами перед применением** |
|         | `kubectl diff -f .` | Дифф по файлам в каталоге |
|         | `kubectl diff --server-side -f .` | Дифф с учётом правил SSA |
|         | `kubectl diff -k overlays/prod` | Дифф результата kustomize-оверлея |
| [**`kubectl wait`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#wait) | | **Ожидание наступления условия у ресурса** |
|         | `kubectl wait deploy/web -n app --for=condition=available --timeout=90s` | Дождаться готовности Deployment |
|         | `kubectl wait job/batch-1 -n app --for=condition=complete --timeout=10m` | Дождаться завершения Job |
|         | `kubectl wait --for=delete pod/web-xyz -n app --timeout=60s` | Дождаться удаления объекта |
| [**`kubectl kustomize`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#kustomize) | | **Рендеринг итогового YAML из оверлея** |
|         | `kubectl kustomize overlays/prod` | Посмотреть, что будет применено |
|         | `kubectl apply -k overlays/prod` | Применить оверлей без Helm |
|         | `kubectl diff -k overlays/prod` | Проверить изменения перед применением |
| [**`kubectl explain`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#explain) | | **Глубокая справка по полям API** |
|         | `kubectl explain deployment.spec --recursive` | Дерево полей и типов целиком |
|         | `kubectl explain hpa.spec.metrics` | Структура метрик HPA v2 |
|         | `kubectl explain service.spec.sessionAffinity` | Детали конкретного поля |
| [**`kubectl get --raw`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#get) | | **Запрос низкоуровневых эндпоинтов API-сервера** |
|         | `kubectl get --raw /healthz` | Базовая проверка здоровья API |
|         | `kubectl get --raw /metrics` | Метрики API-сервера в Prometheus-формате |
|         | `kubectl get --raw /apis/metrics.k8s.io/v1beta1/nodes` | Метрики ресурсов от metrics-server |
| [**`kubectl auth reconcile`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#auth) | | **Идемпотентно привести RBAC к состоянию из YAML** |
|         | `kubectl auth reconcile -f rbac.yaml` | Создать/обновить роли и биндинги из файла |
|         | `kubectl auth reconcile -f rbac.yaml --remove-extra-permissions` | Убрать лишние права, не описанные в YAML |
|         | `kubectl auth can-i --list -n app` | Быстрая сверка прав после reconcile |
| [**`kubectl config`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#config) | | **Управление контекстами/namespace, чтобы не промахнуться окружением** |
|         | `kubectl config view --minify` | Показать активный контекст и namespace |
|         | `kubectl config get-contexts` | Список доступных контекстов |
|         | `kubectl config use-context prod` | Переключиться на контекст `prod` |
|         | `kubectl config set-context --current --namespace=app` | Задать namespace по умолчанию для текущего контекста |
| [**`kubectl get`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#get) | | **Фильтрация селекторами для точного выбора объектов** |
|         | `kubectl get pods -l 'app in (web,api)' -n app` | Отбор по меткам из множества значений |
|         | `kubectl get pods --field-selector=status.phase=Running -A` | Отбор по полю статуса |
|         | `kubectl get svc -l tier=frontend -A` | Быстрый выбор сервисов по роли |

> ***Примечания:***  
> • **SSA:** используй один и тот же `--field-manager` во всех пайплайнах, иначе появятся конфликты владения полями.  
> • **`--force-conflicts`:** применяй только осознанно — ты перезапишешь чужого «владельца» полей.  
> • **Prune:** всегда ставь чёткую метку `-l team=…/app=…` — без неё можно удалить «чужие» ресурсы.  
> • **`dry-run=server`** лучше client: проверяет схему CRD и admission-валидаторы.  
> • **`diff`** перед apply — обязательный шаг в проде, особенно с SSA.  
> • **`wait`** делай с тайм-аутом и точным условием (`available/complete/deleted`), иначе скрипт может зависнуть.  
> • **`get --raw`** зависит от включённых API и прав; не все кластеры публикуют одинаковые эндпоинты.

---

## 🤖 Автоматизация и лучшая практика

> **Назначение:** устойчивые пайплайны и безопасные релизы — валидация, дифф, ожидание, управляемые обновления и предсказуемые артефакты.

| Команда | Пример | Описание |
| ------- | ------ | -------- |
| [**`kubectl apply --dry-run=server`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#apply) | | **Валидация манифестов на API-сервере без записи** |
|         | `kubectl apply --dry-run=server -f .` | Проверить каталог манифестов в CI |
|         | `kubectl apply --dry-run=server -k overlays/prod` | Проверить оверлей окружения |
|         | `kubectl apply --dry-run=server -f deploy.yaml -o yaml` | Получить итоговую спеку для ревью |
| [**`kubectl rollout status`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#rollout) | | **Гейт в пайплайне: дождаться завершения обновления** |
|         | `kubectl rollout status deploy/web -n app` | Ждать готовности деплоя после apply |
|         | `kubectl rollout status sts/db -n app --timeout=10m` | Тайм-аут для stateful-нагрузки |
|         | `kubectl rollout history deploy/web -n app` | Проверить ревизии перед откатом |
| [**`kubectl set image`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#set-image) | | **Иммутабельные образы для повторяемых релизов** |
|         | `kubectl set image deploy/web app=repo@sha256:... -n app` | Фиксировать digest вместо плавающего тега |
|         | `kubectl rollout status deploy/web -n app` | Контроль успешного обновления |
|         | `kubectl rollout undo deploy/web -n app` | Быстрый откат при проблеме |
| [**`kubectl annotate`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#annotate) | | **Явные триггеры перезапуска по изменению конфигов/секретов** |
|         | `kubectl annotate deploy/web checksum/config=sha256:... -n app --overwrite` | Обновить аннотацию и запустить новый rollout |
|         | `kubectl rollout status deploy/web -n app` | Дождаться завершения перезапуска |
|         | `kubectl get deploy web -n app -o yaml` | Проверить, что аннотация попала в PodTemplate |
| [**`kubectl label`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#label) | | **Селективные релизы и выборки через метки** |
|         | `kubectl label deploy/web track=canary -n app --overwrite` | Пометить цель для канареечного маршрута |
|         | `kubectl get pods -l track=canary -n app` | Проверить, что реплики промаркированы |
|         | `kubectl delete pods -l track=canary -n app` | Оперировать только с целевой группой |
| [**`kubectl get`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#get) | | **Автоматизация через форматы вывода** |
|         | `kubectl get pods -l app=web -n app -o name` | Получить только имена для пайплайна |
|         | `kubectl get hpa -n app -o jsonpath='{.items[*].status.currentMetrics[*].resource.current.averageUtilization}'` | Извлечь метрики для принятия решения |
|         | `kubectl get events -A --sort-by=.lastTimestamp` | Хронология событий для быстрой диагностики релиза |
| [**`kubectl rollout pause\|resume`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#rollout) | | **Пакетное применение нескольких изменений с контролируемым запуском** |
|         | `kubectl rollout pause deploy/web -n app` | Поставить деплой на паузу перед серией правок |
|         | `kubectl apply -f changes/ -n app` | Внести пакет изменений во время паузы |
|         | `kubectl rollout resume deploy/web -n app` | Запустить rollout после накопленных изменений |
| [**`kubectl kustomize\|apply -k`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#kustomize) | | **Декларативные окружения без Helm** |
|         | `kubectl kustomize overlays/prod` | Рендер итоговой конфигурации |
|         | `kubectl diff -k overlays/prod` | Дифф перед применением |
|         | `kubectl apply -k overlays/prod` | Применить оверлей в целевом окружении |
| [**`kubectl krew`**](https://krew.sigs.k8s.io/) | | **Управление плагинами kubectl для расширения возможностей** |
|         | `kubectl krew install df-pv` | Плагин для обзора занятости PV |
|         | `kubectl krew install neat` | Плагин для «чистого» YAML без служебных полей |
|         | `kubectl krew list` | Посмотреть установленные плагины |
| [**`kubectl apply`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#apply) | | **Best practice: сетевые политики по умолчанию (default-deny) и явные allow** |
|         | `kubectl apply -f netpol/00-default-deny.yaml -n app` | Запретить весь трафик по умолчанию в `app` |
|         | `kubectl apply -f netpol/10-allow-web-to-api.yaml -n app` | Разрешить ровно нужные направления и порты |
|         | `kubectl get netpol -n app` | Проверить, что политики применены |
| [**`kubectl explain`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#explain) | | **Best practice: верификация настроек SecurityContext перед релизом** |
|         | `kubectl explain pod.spec.securityContext` | Справка по полям pod-level securityContext |
|         | `kubectl explain container.securityContext` | Поля container-level securityContext |
|         | `kubectl get deploy web -n app -o yaml` | Проверить, что рекомендуемые поля заданы в манифесте |

> ***Примечания:***  
> • **Идемпотентность:** все шаги должны давать одинаковый результат при повторном запуске.  
> • **Иммутабельные образы:** используем digest `@sha256:…`, а не плавающие теги.  
> • **Гейты:** `diff` → `apply` → `rollout status`/`wait` — фиксируй порядок и тайм-ауты.  
> • **Аннотации-триггеры:** checksum конфигов/секретов на PodTemplate — явный перезапуск без ручного вмешательства.  
> • **Селекторы:** единая система меток для окружений/приложений, чтобы `--prune` и выборки работали предсказуемо.  
> • **Метрики:** `kubectl top`/HPA требуют metrics-server; для памяти/кастом-метрик — HPA `autoscaling/v2` в YAML.  
> • **Разделение обязанностей:** GitOps-бот применяет манифесты с единым `--field-manager`, люди — только через PR и diff.  
> • **Безопасность:** минимальные RBAC, default-deny NetworkPolicy, PDB и ресурсы/лимиты в каждом workload.

---

## 📦 Workloads: Deploy/STS/DS/Job/CronJob

> **Назначение:** посмотреть и диагностировать основные типы рабочих нагрузок, создать разовые и периодические задачи, понять стратегию обновления и размещение подов.

| Команда | Пример | Описание |
| ------- | ------ | -------- |
| [**`kubectl get`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#get) | | **Быстрый обзор workload-ов** |
|         | `kubectl get deploy,sts,ds,job,cronjob -A` | Сводка по объектам во всех namespace |
|         | `kubectl get deploy -n app -o wide` | Список деплоев с дополнительными столбцами |
|         | `kubectl get ds -A` | Один под на узел: агенты, логгеры и т.п. |
| [**`kubectl describe deployment`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#describe) | | **Детали стратегии и состояния Deployment** |
|         | `kubectl describe deploy web -n app` | Реплики, стратегия RollingUpdate, события |
|         | `kubectl get rs -n app -l app=web -o wide` | Связанные ReplicaSet и их параметры |
|         | `kubectl rollout status deploy/web -n app` | Контроль прогресса обновления деплоя |
| [**`kubectl describe statefulset`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#describe) | | **Упорядоченные поды с именами и PVC** |
|         | `kubectl describe sts db -n app` | Порядок запуска/остановки, шаблон PVC |
|         | `kubectl get pod -l statefulset.kubernetes.io/pod-name -n app` | Проверить индивидуальные поды STS |
|         | `kubectl rollout status sts/db -n app` | Дождаться обновления STS |
| [**`kubectl describe daemonset`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#describe) | | **Один под на каждом подходящем узле** |
|         | `kubectl describe ds node-agent -A` | Узлы-таргеты, число доступных/желаемых |
|         | `kubectl get ds node-agent -A -o wide` | Версия образа и селекторы узлов |
|         | `kubectl rollout status ds/node-agent -n ops` | Прогресс обновления DaemonSet |
|         | `kubectl get ds -A -o custom-columns=NS:.metadata.namespace,NAME:.metadata.name \| tail -n +2 \| while read ns name; do kubectl -n "$ns" rollout status ds/"$name"; done` | Массово по всем ns (без `-A` у `rollout status`) |
| [**`kubectl create job`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#create) | | **Разовая задача до завершения** |
|         | `kubectl create job echo --image=alpine -- echo hi` | Простой Job с одной командой |
|         | `kubectl get jobs -n app -o wide` | Проверить старт/завершение Job |
|         | `kubectl logs -n app job/echo` | Логи пода(ов), запущенных Job |
| [**`kubectl create cronjob`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#create) | | **Периодическая задача по расписанию** |
|         | `kubectl create cronjob hello --image=busybox --schedule="*/5 * * * *" -- date` | Запускать каждые 5 минут |
|         | `kubectl get cronjob -n app -o wide` | Обзор расписаний и политики пропусков |
|         | `kubectl create job run-now --from=cronjob/hello -n app` | Запустить разово джобу из CronJob |
| [**`kubectl delete job`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#delete) | | **Удалить Job и управлять каскадным удалением его подов** |
|         | `kubectl delete job echo -n app --cascade=foreground` | Дождаться удаления связанных подов |
|         | `kubectl delete job -l app=batch -n app --cascade=background` | Удалить пачку Job по метке, поды удалятся в фоне |
|         | `kubectl delete job cleanup -n app --cascade=orphan` | Сохранить поды как «сироты», удалить только Job |
| [**`kubectl delete cronjob`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#delete) | | **Удалить расписание CronJob, при необходимости вместе с созданными Job** |
|         | `kubectl delete cronjob hello -n app` | Удалить только расписание, существующие Job останутся |
|         | `kubectl delete cronjob hello -n app --cascade=foreground` | Удалить CronJob и связанные Job |
|         | `kubectl delete cronjob -l team=ops -n app` | Массовое удаление CronJob по метке |

---

## 📌 Мини-шаблоны YAML

> **Назначение:** готовые «кусочки» для быстрого старта. Каждый блок можно положить в отдельный файл (`*.yaml`) или объединить через `---`, применить `kubectl apply -f <файл>` и сразу проверить результат.
>
> ***Как пользоваться:***
>
> 1) Сохраните шаблон в файл и при необходимости добавьте `metadata.namespace: <ns>`.
> 2) Проверьте, что используемые имена (`Service`, `Secret`, `StorageClass`) существуют или создаются вместе с шаблоном.
> 3) Примените: `kubectl apply -f <file.yaml>`.
> 4) Проверьте: `kubectl get ... -n <ns>` / `kubectl describe ... -n <ns>`.

### Deployment + Service (ClusterIP)

**Что это:** stateless-приложение (приложение без сохранения состояния) из 2 реплик и внутрекластерный сервис.  
**Когда нужно:** базовый веб-сервис, на который потом можно навесить Ingress.  
**Проверка:**

- `kubectl get deploy,rs,pod,svc -n <ns>`
- `kubectl rollout status deploy/web -n <ns>`

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web
  labels: { app: web }
spec:
  replicas: 2
  strategy:
    type: RollingUpdate
    rollingUpdate: { maxSurge: 1, maxUnavailable: 0 }
  selector:
    matchLabels: { app: web }
  template:
    metadata:
      labels: { app: web }
    spec:
      containers:
        - name: nginx
          image: nginx:1.27.1
          ports: [ { containerPort: 80 } ]
          resources:
            requests: { cpu: 100m, memory: 128Mi }
            limits:   { cpu: 500m, memory: 256Mi }
          readinessProbe:
            httpGet: { path: "/", port: 80 }
            initialDelaySeconds: 5
            periodSeconds: 5
          livenessProbe:
            httpGet: { path: "/", port: 80 }
            initialDelaySeconds: 15
            periodSeconds: 10
---
apiVersion: v1
kind: Service
metadata:
  name: web
spec:
  selector: { app: web }
  type: ClusterIP
  ports: [ { port: 80, targetPort: 80 } ]
```

### Ingress (nginx-ingress) с TLS

**Что это:** L7-маршрутизация HTTP(S) на Service web.  
**Важно:** нужен установленный Ingress-контроллер (например, ingress-nginx) и существующий TLS-секрет.  
**Проверка:**

- `kubectl get ingress -n <ns>`
- `kubectl describe ingress web -n <ns>`
- DNS должен указывать на внешний адрес контроллера

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: web
spec:
  ingressClassName: nginx
  tls:
    - hosts: [ "example.com" ]
      secretName: tls-example-com  # должен существовать (тип kubernetes.io/tls)
  rules:
    - host: example.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: web
                port: { number: 80 }
```

### PVC + использование тома в Pod

**Что это:** запрос на том (PVC) и Deployment, который пишет в этот том.  
**Важно:** storageClassName должен существовать и поддерживать нужные режимы (RWO/RWX).  
**Проверка:**

- `kubectl get pvc -n <ns>` → статус Bound
- `kubectl describe pvc data -n <ns>` → детали привязки

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: data
spec:
  accessModes: [ "ReadWriteOnce" ]
  storageClassName: standard
  resources: { requests: { storage: 10Gi } }
---
apiVersion: apps/v1
kind: Deployment
metadata: { name: writer }
spec:
  replicas: 1
  selector: { matchLabels: { app: writer } }
  template:
    metadata: { labels: { app: writer } }
    spec:
      containers:
        - name: app
          image: busybox
          command: ["sh","-c","while true; do date >> /data/out.txt; sleep 5; done"]
          volumeMounts: [ { name: data, mountPath: /data } ]
      volumes: [ { name: data, persistentVolumeClaim: { claimName: data } } ]
```

### HPA v2 по CPU

**Что это:** авто-масштабирование деплоя web по загрузке CPU.  
**Важно:** требуется metrics-server; YAML уровня autoscaling/v2.  
**Проверка:**

- `kubectl get hpa -n <ns>`
- `kubectl describe hpa web-hpa -n <ns>`

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata: { name: web-hpa }
spec:
  scaleTargetRef: { apiVersion: apps/v1, kind: Deployment, name: web }
  minReplicas: 2
  maxReplicas: 10
  metrics:
    - type: Resource
      resource:
        name: cpu
        target: { type: Utilization, averageUtilization: 60 }
```

### NetworkPolicy: deny-all + allow из namespace web

**Что это:** полное ограничение трафика в db и точечный доступ к поду postgres только из ns=web на порт 5432.  
**Важно:** CNI-плагин должен поддерживать NetworkPolicy.  
**Проверка:**

- `kubectl get netpol -n db`
- Трафик из других ns должен блокироваться

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata: { name: deny-all, namespace: db }
spec:
  podSelector: {}
  policyTypes: [ Ingress, Egress ]
---
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata: { name: allow-from-web, namespace: db }
spec:
  podSelector: { matchLabels: { app: postgres } }
  ingress:
    - from:
        - namespaceSelector: { matchLabels: { name: web } }
      ports: [ { protocol: TCP, port: 5432 } ]
```

> ⚠️ Для селектора namespace используйте реальную метку вашего `web`-неймспейса (например, выставьте её: `kubectl label ns web name=web`).

### RBAC: роль «только чтение» в namespace

**Что это:** Role с правами чтения базовых ресурсов и RoleBinding на пользователя.  
**Важно:** тип субъекта (User/Group/ServiceAccount) должен соответствовать вашей аутентификации.  
**Проверка:**

- `kubectl auth can-i list pods -n dev --as alice@example.com`

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata: { name: view-only, namespace: dev }
rules:
  - apiGroups: ["", "apps", "batch"]
    resources: ["pods", "services", "deployments", "jobs", "cronjobs"]
    verbs: ["get", "list", "watch"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata: { name: view-only-binding, namespace: dev }
subjects:
  - kind: User
    name: alice@example.com
    apiGroup: rbac.authorization.k8s.io
roleRef: { kind: Role, name: view-only, apiGroup: rbac.authorization.k8s.io }
```

### Debug: эфемерный контейнер (через команду)

**Что это:** добавление «временного» контейнера в существующий под, чтобы поставить утилиты и войти внутрь без изменения образа приложения.  
**Как использовать:** YAML не нужен — это операция командой. Нужен целевой под (ниже — пример простого пода для тренировки).  
**Добавить отладочный контейнер:**

- `kubectl debug pod/sample --image=busybox:1.36 --target=app -n <ns> -it -- sh`

**Пример пода (как цель для debug):**

```yaml
apiVersion: v1
kind: Pod
metadata: { name: sample }
spec:
  containers:
    - name: app
      image: ghcr.io/org/app:1.0.0
      command: ["sh","-c","sleep 3600"]
```

> ***Примечания:***  
• В шаблонах замените домен `example.com`, имена ns (`<ns>`), имена `StorageClass`, `Secret` и метки на ваши.  
• Объединять несколько объектов в одном файле можно через `---`; применяйте атомарно и проверяйте `rollout status` для workload-ов.  
• При ошибках применения смотрите `kubectl describe <obj> -n <ns>` и `kubectl get events -A --sort-by=.lastTimestamp`.

---

## 💡 Алиасы kubectl

> **Назначение:** ускорить повседневную работу с `kubectl` короткими командами и автодополнением по `Tab`.  
> **Куда вставлять:** в файл инициализации оболочки — **Bash:** `~/.bashrc` (или `~/.bash_profile` на macOS), **Zsh:** `~/.zshrc`. После правки выполните `source ~/.bashrc` или `source ~/.zshrc`.

### Bash: автодополнение + базовый набор

```bash
 # --- Автодополнение kubectl (должно быть ПЕРЕД complete -F ...) ---
 # Установит функции автодополнения в текущую сессию
source <(kubectl completion bash)

 # Короткий псевдоним и привязка автодополнения к нему
alias k=kubectl
complete -o default -F __start_kubectl k

 # --- Универсальные aliасы (безопасные и частые) ---
 # Инвентаризация
alias kg='kubectl get'                           # k g <resource> ...
alias kgp='kubectl get pods'                     # k g pods
alias kgpo='kubectl get pods -o wide'            # pods c доп. столбцами
alias kgs='kubectl get svc'                      # services
alias kgi='kubectl get ingress'                  # ingress
alias kgep='kubectl get endpoints'               # endpoints
alias kgn='kubectl get nodes -o wide'            # nodes
alias kgns='kubectl get ns'                      # namespaces
alias kga='kubectl get all -A'                   # все базовые ресурсы во всех ns

 # Детали/логи/наблюдение
alias kdesc='kubectl describe'                   # kdesc pod/<name> -n <ns>
alias kl='kubectl logs'                          # kl pod/<name> -n <ns>
alias klf='kubectl logs -f'                      # фоллоу логов
alias kgw='kubectl get -w'                       # watch: kgw pods -n <ns>

 # Применение/удаление/обновления
alias ka='kubectl apply -f'                      # ka manifest.yaml
alias kd='kubectl delete'                        # kd pod/<name> -n <ns>
alias kaf='kubectl apply -f'                     # явный apply из файла/папки
alias kdf='kubectl delete -f'                    # delete по файлу/папке
alias krr='kubectl rollout restart'              # рестарт workload’а
alias krs='kubectl rollout status'               # статус раскатки

 # Доступ и отладка
alias ke='kubectl exec -it'                      # интерактивный exec
alias kpf='kubectl port-forward'                 # проброс порта
alias kcp='kubectl cp'                           # копирование файлов
alias kex='kubectl explain'                      # справка по полям API

 # Форматы вывода
alias kgy='kubectl get -o yaml'                  # kgy deploy/<name> -n <ns>
alias kgj='kubectl get -o json'
alias kgnm='kubectl get -o name'

 # Быстрые функции для контекста/namespace (удобнее, чем постоянно писать -n/--context)
kns() { kubectl config set-context --current --namespace="${1:?usage: kns <namespace>}"; }
kctx() { kubectl config use-context "${1:?usage: kctx <context>}"; }
```

### Zsh: автодополнение + базовый набор

```zsh
 # --- Автодополнение kubectl для Zsh ---
autoload -Uz compinit && compinit
source <(kubectl completion zsh)

 # Псевдоним и привязка комплита
alias k=kubectl
compdef _kubectl k

 # Тот же набор алиасов, что и для Bash (можно скопировать блоки ниже)
alias kg='kubectl get'
alias kgp='kubectl get pods'
alias kgpo='kubectl get pods -o wide'
alias kgs='kubectl get svc'
alias kgi='kubectl get ingress'
alias kgep='kubectl get endpoints'
alias kgn='kubectl get nodes -o wide'
alias kgns='kubectl get ns'
alias kga='kubectl get all -A'

alias kdesc='kubectl describe'
alias kl='kubectl logs'
alias klf='kubectl logs -f'
alias kgw='kubectl get -w'

alias ka='kubectl apply -f'
alias kd='kubectl delete'
alias kaf='kubectl apply -f'
alias kdf='kubectl delete -f'
alias krr='kubectl rollout restart'
alias krs='kubectl rollout status'

alias ke='kubectl exec -it'
alias kpf='kubectl port-forward'
alias kcp='kubectl cp'
alias kex='kubectl explain'

alias kgy='kubectl get -o yaml'
alias kgj='kubectl get -o json'
alias kgnm='kubectl get -o name'

kns() { kubectl config set-context --current --namespace="${1:?usage: kns <namespace>}"; }
kctx() { kubectl config use-context "${1:?usage: kctx <context>}"; }
```

> ***Примечания:***  
> • Сначала подключайте **completion**, потом объявляйте `alias k=kubectl` и привязывайте комплит (`complete ...` или `compdef`).  
> • Функции `kns/kctx` меняют текущие значения в `kubeconfig` — это безопаснее, чем забытый `-n` в проде.  
> • Избегайте «агрессивных» алиасов вроде безусловного `delete -A` — они опасны на больших кластерах.  
> • Если используете `kubectx/kubens`, можно заменить функции `kctx/kns` на одноимённые утилиты.  
> • Для постоянной «наблюдалки» можно завести `kw() { watch -n 1 kubectl "$@"; }` (пакет `watch` требуется отдельно).

---

## 📚 Дополнительные ресурсы

> **Назначение**: быстрые ссылки на официальные справочники и проверенные инструменты, чтобы углубляться ровно туда, где нужно — сеть, хранение, безопасность, автоскейлинг, GitOps, локальные кластеры.

### 💡 Подсказки

- Выбирай версию документации под свой кластер (селектор версии в правом верхнем углу доков).
- Сверяй совместимость клиента/сервера: `kubectl` ↔ API-server (Version Skew).
- Для Ingress/CNI/CSI всегда читай доку **конкретного** контроллера/драйвера — аннотации и поведение отличаются.
- Ищешь точное поле/тип? Используй **Kubernetes API Reference** + `kubectl explain <kind>.<path>`.
- Для пошаговых действий — раздел **Tasks**, для теории — **Concepts**.
- Избегай устаревших статей (особенно про флаги/аннотации) — ориентир ≤ 12–18 месяцев.
- Внутри команды фиксируй ссылки на **конкретную минорную версию** доков, чтобы избежать «drift».

### 🌐 Полезные ссылки

#### 📘 Официальные справочники

| Ресурс | Описание |
| ------ | -------- |
| [Kubernetes документация](https://kubernetes.io/docs/home/) | Главная документация Kubernetes: концепции, руководства, задачи |
| [Справочник kubectl](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/) | Полный список команд `kubectl` |
| [Kubectl шпаргалка](https://kubernetes.io/docs/reference/kubectl/cheatsheet/) | Официальная шпаргалка по `kubectl` |
| [Kubernetes API Reference](https://kubernetes.io/docs/reference/kubernetes-api/) | Полное описание API объектов |
| [Совместимость версий (Version Skew)](https://kubernetes.io/docs/setup/release/version-skew-policy/) | Совместимость версий клиента/сервера и компонент |

#### 📙 Сеть

| Ресурс | Описание |
| ------ | -------- |
| [Сервисы](https://kubernetes.io/docs/concepts/services-networking/service/) | Типы сервисов и публикация портов |
| [Ingress](https://kubernetes.io/docs/concepts/services-networking/ingress/) | L7-маршрутизация к сервисам |
| [Сетевые политики](https://kubernetes.io/docs/concepts/services-networking/network-policies/) | L3/L4 политики и применение |

#### 📗 Масштабирование и метрики

| Ресурс | Описание |
| ------ | -------- |
| [HPA v2](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/) | Автоскейлинг по CPU/памяти/кастомным метрикам |
| [metrics-server](https://github.com/kubernetes-sigs/metrics-server) | Источник метрик для `kubectl top` и HPA |

#### 📕 Хранилище

| Ресурс | Описание |
| ------ | -------- |
| [Постоянные тома (PV/PVC)](https://kubernetes.io/docs/concepts/storage/persistent-volumes/) | Политики возврата, привязка |
| [Классы хранения (StorageClass)](https://kubernetes.io/docs/concepts/storage/storage-classes/) | Динамическое провижининг |
| [CSI драйверы (каталог)](https://kubernetes-csi.github.io/docs/drivers.html) | Список драйверов CSI |

#### 📘 Безопасность и доступ

| Ресурс | Описание |
| ------ | -------- |
| [Pod стандарт безопасности](https://kubernetes.io/docs/concepts/security/pod-security-standards/) | Базовые профили безопасности подов |
| [RBAC](https://kubernetes.io/docs/reference/access-authn-authz/rbac/) | Роли, привязки, права |
| [Секреты](https://kubernetes.io/docs/concepts/configuration/secret/) | Типы секретов и способы использования |
| [Эфемерные контейнеры / kubectl debug](https://kubernetes.io/docs/tasks/debug/debug-application/debug-running-pod/#ephemeral-container) | Отладка без изменения образа |

#### 📙 Workloads и основные объекты

| Ресурс | Описание |
| ------ | -------- |
| [Deployments](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/) | Статлесс-приложения и раскатка |
| [StatefulSet](https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/) | Сохранение идентичности/томов |
| [DaemonSet](https://kubernetes.io/docs/concepts/workloads/controllers/daemonset/) | По одному поду на узел |
| [Jobs/CronJobs](https://kubernetes.io/docs/concepts/workloads/controllers/job/) | Пакетные и периодические задачи |
| [ConfigMap](https://kubernetes.io/docs/concepts/configuration/configmap/) | Конфигурация приложений |

#### 📗 Локальные кластеры

| Ресурс | Описание |
| ------ | -------- |
| [kind](https://kind.sigs.k8s.io/) | Kubernetes в Docker для CI/локальной разработки |
| [minikube](https://minikube.sigs.k8s.io/docs/) | Одноузловой кластер локально |

#### 📕 Плагины `kubectl`

| Ресурс | Описание |
| ------ | -------- |
| [Krew](https://krew.sigs.k8s.io/) | Менеджер плагинов для `kubectl` |
| [kubectl-neat](https://github.com/itaysk/kubectl-neat) | «Чистый» YAML без служебных полей |
| [kubectx / kubens](https://github.com/ahmetb/kubectx) | Быстрое переключение контекстов и namespace |
