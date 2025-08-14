# 🎯 Helm Cheat Sheet

> 📘 Helm — это менеджер пакетов для Kubernetes. Он позволяет управлять приложениями через чарт-файлы, выполнять установки, обновления и откаты с высокой скоростью и надёжностью.

---

## 📂 Содержание

- [🎯 Helm Cheat Sheet](#-helm-cheat-sheet)
  - [📂 Содержание](#-содержание)
  - [📦 Основные команды](#-основные-команды)
  - [📥 Установка и обновление чартов](#-установка-и-обновление-чартов)
  - [🧰 Работа с чартами](#-работа-с-чартами)
  - [⚙️ Helm + Kubernetes](#️-helm--kubernetes)
  - [📁 Настройки и переменные](#-настройки-и-переменные)
  - [🧠 Расширенные функции](#-расширенные-функции)
  - [📌 Примеры](#-примеры)

---

## 📦 Основные команды

```bash
helm help                      # Справка
helm version                   # Версия Helm
helm repo add stable URL       # Добавить репозиторий
helm repo update               # Обновить все репозитории
helm repo list                 # Список репозиториев
helm search hub nginx          # Поиск в Helm Hub
helm search repo nginx         # Поиск в локальных репо
```

---

## 📥 Установка и обновление чартов

```bash
helm install my-release stable/nginx             # Установка чарта
helm upgrade my-release stable/nginx             # Обновление чарта
helm upgrade --install my-release stable/nginx   # Установка или обновление
helm uninstall my-release                        # Удаление релиза
helm list                                        # Список релизов
helm status my-release                           # Статус релиза
```

---

## 🧰 Работа с чартами

```bash
helm create my-chart                  # Новый чарт
helm lint ./my-chart                  # Проверка чарта
helm package ./my-chart               # Упаковка в .tgz
helm template my-release ./my-chart   # Рендеринг YAML без установки
helm dependency update ./my-chart     # Обновить зависимости
```

---

## ⚙️ Helm + Kubernetes

```bash
helm install --namespace dev ...     # Установка в namespace
helm uninstall --namespace dev ...   # Удаление
helm list --namespace dev            # Список релизов в namespace
helm install ... --kube-context ctx  # Установка в другой контекст
helm upgrade ... --kube-context ctx  # Обновление в контексте
```

---

## 📁 Настройки и переменные

```bash
helm install --values values.yaml ...            # Передать values.yaml
helm install --set key=value ...                 # Указать вручную
helm upgrade --set image.tag=2.0 ...             # При обновлении
helm get values my-release                       # Показать values
helm get all my-release                          # Вся информация
```

---

## 🧠 Расширенные функции

```bash
helm rollback my-release 1                       # Откат на версию
helm history my-release                          # История релизов
helm test my-release                             # Запуск тестов
helm dependency build ./my-chart                 # Сборка зависимостей
helm push ./my-chart my-repo                     # Отправка чарта
```

---

## 📌 Примеры

📄 `values.yaml`

```yaml
replicaCount: 2
image:
  repository: nginx
  tag: stable
  pullPolicy: IfNotPresent
```

📄 Установка с custom values:

```bash
helm install my-release ./my-chart --values values.yaml
```
