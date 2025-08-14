# ☸️ Kubernetes (kubectl) Cheat Sheet

> 📘 Kubernetes — это система оркестрации контейнеров. Ниже представлены команды kubectl для управления подами, деплойментами, сервисами, namespace, конфигурацией и масштабированием.

---

## 📂 Содержание

- [☸️ Kubernetes (kubectl) Cheat Sheet](#️-kubernetes-kubectl-cheat-sheet)
  - [📂 Содержание](#-содержание)
  - [🔹 Базовые команды](#-базовые-команды)
  - [🔧 Управление ресурсами](#-управление-ресурсами)
  - [📈 Масштабирование и развертывание](#-масштабирование-и-развертывание)
  - [📦 ConfigMaps и Secrets](#-configmaps-и-secrets)
  - [⚙️ Работа с конфигурацией](#️-работа-с-конфигурацией)
  - [🧠 Расширенные команды](#-расширенные-команды)
  - [📌 Примеры YAML](#-примеры-yaml)
  - [🧠 Полезности](#-полезности)

---

## 🔹 Базовые команды

```bash
kubectl version --short              # Версия клиента/сервера
kubectl cluster-info                 # Информация о кластере
kubectl get nodes                    # Список нод
kubectl get pods                     # Список подов
kubectl get services                 # Список сервисов
kubectl get namespaces               # Все namespaces
kubectl describe pod pod-name        # Подробности пода
kubectl logs pod-name                # Логи пода
kubectl delete pod pod-name          # Удалить под
kubectl create namespace dev         # Создать namespace
```

---

## 🔧 Управление ресурсами

```bash
kubectl apply -f deploy.yaml         # Применить манифест
kubectl delete -f deploy.yaml        # Удалить ресурс
kubectl edit deployment my-app       # Редактирование в редакторе
kubectl exec -it pod-name -- bash    # Войти в под
kubectl port-forward pod 8080:80     # Проброс портов
```

---

## 📈 Масштабирование и развертывание

```bash
kubectl scale deployment my-app --replicas=3                            # Масштабирование
kubectl rollout status deployment/my-app                                # Статус деплоя
kubectl rollout undo deployment/my-app                                  # Откат
kubectl rollout history deployment/my-app                               # История версий
kubectl autoscale deployment my-app --cpu-percent=50 --min=1 --max=10
```

---

## 📦 ConfigMaps и Secrets

```bash
kubectl get configmaps                                                # Список ConfigMap
kubectl get secrets                                                   # Список Secret
kubectl create configmap my-config --from-literal=key=value
kubectl create secret generic my-secret --from-literal=password=12345
```

---

## ⚙️ Работа с конфигурацией

```bash
kubectl config view                                           # Текущий kubeconfig
kubectl config use-context context                            # Переключить контекст
kubectl label pod mypod env=dev                               # Добавить label
kubectl annotate pod mypod desc="Test"
kubectl patch deployment my-app -p '{"spec":{"replicas":2}}'
```

---

## 🧠 Расширенные команды

```bash
kubectl top pods                                # Ресурсы подов
kubectl top nodes                               # Ресурсы нод
kubectl cordon node-name                        # Запрет планирования
kubectl uncordon node-name                      # Разрешить планирование
kubectl drain node-name --ignore-daemonsets
kubectl taint nodes node key=value:NoSchedule
kubectl get events                              # События
kubectl get ingress                             # Ingress ресурсы
kubectl get crds                                # Custom Resources
kubectl api-resources                           # Доступные API ресурсы
kubectl api-versions                            # Доступные версии API
```

---

## 📌 Примеры YAML

```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
spec:
  replicas: 2
  selector:
    matchLabels:
      app: my-app
  template:
    metadata:
      labels:
        app: my-app
    spec:
      containers:
        - name: app
          image: nginx
          ports:
            - containerPort: 80
```

---

## 🧠 Полезности

- ✅ Проверка статуса rollout:

  ```bash
  watch kubectl rollout status deployment/my-app
  ```

- ✅ Проверка зависаний:

  ```bash
  kubectl describe pod <pod> | grep -i events -A 10
  ```

- ✅ Debug-под:

  ```bash
  kubectl debug pod-name
  ```
