# 🌐 Deploy Static Website with NGINX in Docker

> 📦 Простой сценарий развертывания статического сайта через Docker и NGINX. Подходит для локальной разработки или быстрого запуска на VPS.

---

## 📝 Структура проекта

```text
static-site/
├── index.html
├── nginx.conf
└── Dockerfile
```

---

## 📄 index.html

```html
<!DOCTYPE html>
<html>
<head>
  <title>Hello World</title>
</head>
<body>
  <h1>Hello from Docker + NGINX!</h1>
</body>
</html>
```

---

## ⚙️ nginx.conf

```nginx
events {}
http {
  server {
    listen 80;
    location / {
      root /usr/share/nginx/html;
      index index.html;
    }
  }
}
```

---

## 🐳 Dockerfile

```Dockerfile
FROM nginx:alpine
COPY index.html /usr/share/nginx/html/
COPY nginx.conf /etc/nginx/nginx.conf
```

---

## 🚀 Команды для запуска

```bash
docker build -t static-nginx .
docker run -d -p 8080:80 static-nginx
```

Теперь сайт доступен по адресу: [http://localhost:8080](http://localhost:8080)

---

## ✅ Примечания

- Можно использовать `docker-compose.yml` для более гибкой настройки.
- Отлично подходит для быстрой публикации на VPS или в CI/CD.
