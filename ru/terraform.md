# 🌍 Terraform Cheat Sheet

> 📘 Terraform — инструмент для создания и управления инфраструктурой через код (IaC). Позволяет конфигурировать облака, сети, ВМ, БД и многое другое.

---

## 📂 Содержание

- [🌍 Terraform Cheat Sheet](#-terraform-cheat-sheet)
  - [📂 Содержание](#-содержание)
  - [🔹 Основные команды](#-основные-команды)
  - [🔧 Работа с состоянием](#-работа-с-состоянием)
  - [📦 Модули и плагины](#-модули-и-плагины)
  - [🌐 Backends и Workspaces](#-backends-и-workspaces)
  - [🧠 Полезные переменные и переменные среды](#-полезные-переменные-и-переменные-среды)
  - [📁 Пример структуры проекта](#-пример-структуры-проекта)
  - [📝 Полезные советы](#-полезные-советы)

---

## 🔹 Основные команды

```bash
terraform init                 # Инициализация (загрузка провайдеров)
terraform validate             # Проверка конфигурации
terraform plan                 # План изменений
terraform apply                # Применить план
terraform destroy              # Удалить инфраструктуру
terraform output               # Показать выходные переменные
terraform show                 # Состояние в читаемом виде
terraform refresh              # Обновить состояние с реальностью
```

---

## 🔧 Работа с состоянием

```bash
terraform state list           # Список ресурсов в state
terraform state show resource  # Информация о ресурсе
terraform state mv             # Переместить ресурс в state
terraform state rm             # Удалить ресурс из state
terraform taint resource       # Отметить как повреждённый
terraform untaint resource     # Убрать пометку
terraform import resource ID   # Импортировать внешний ресурс
```

---

## 📦 Модули и плагины

```bash
terraform get                  # Загрузить модули
terraform init -upgrade        # Обновить провайдеры
terraform providers            # Используемые провайдеры
terraform module               # Работа с модулями (0.13+)
```

---

## 🌐 Backends и Workspaces

```bash
terraform workspace list       # Список окружений
terraform workspace new dev    # Создать workspace
terraform workspace select dev # Переключиться
terraform backend config       # Конфигурация бэкенда
terraform login                # Вход в Terraform Cloud
```

---

## 🧠 Полезные переменные и переменные среды

```hcl
# variables.tf
variable "region" {
  default = "us-west-1"
}

# terraform.tfvars
region = "us-east-1"
```

```bash
export TF_VAR_region=us-west-2      # Переопределение через ENV
export TF_LOG=DEBUG                 # Логгирование
export TF_LOG_PATH=terraform.log    # Файл логов
```

---

## 📁 Пример структуры проекта

```text
project/
├── main.tf
├── variables.tf
├── outputs.tf
├── terraform.tfvars
├── modules/
│   └── vpc/
│       └── main.tf
```

---

## 📝 Полезные советы

- ✅ Используй `terraform plan -out=tfplan` перед `apply`:

  ```bash
  terraform apply tfplan
  ```

- ✅ Проверяй `.terraform.lock.hcl` при обновлении провайдеров

- ✅ Добавь `.terraform` и `.tfstate` в `.gitignore`:

  ```bash
  .terraform/
  *.tfstate
  *.tfstate.backup
  crash.log
  terraform.tfvars
  ```
