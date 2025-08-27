# Руководство по структуре и разработке проекта шпаргалки (Quarto)

Версия документа: **v1.0**\
Автор: Hackitect7 (Алексей)

---

## Цели проекта

- Единый комплект **шаблонов QMD** для всех языков.
- **Локализация** в YAML-файлах без авто‑переводов — только подстановка подготовленных строк.
- **Конвенция ключей** и единые правила именования.
- **Одностраничные шпаргалки** по каждому языку + **англоязычная главная страница** с описанием проекта и выбором языка.
- Таблицы **всегда** умещаются в ширину контейнера, **без горизонтальной прокрутки**.
- Полная автоматизация сборки (локально и в CI/CD, GitHub Actions/Pages).

---

## Термины

- **Шаблон** — QMD-файл с плейсхолдерами `{{< var ... >}}` (без текста конкретного языка).
- **Локаль** — YAML-файл со строками для одного языка.
- **Профиль** — Quarto-профиль (например, `_quarto-ru.yml`), определяющий `metadata-files`, `output-dir`, язык и набор рендеримых страниц.

---

## Структура проекта (v1.0)

```
.
├─ _quarto.yml                 # базовые настройки сайта и домашней страницы (EN)
├─ _quarto-en.yml              # профиль EN → рендер /en/
├─ _quarto-ru.yml              # профиль RU → рендер /ru/
├─ styles.css                  # общий стиль (в т.ч. правила для таблиц без скролла)
├─ pages/
│   └─ home.qmd               # главная (EN): описание проекта, выбор языка, ссылки на /en/ и /ru/
├─ templates/                  # шаблоны разделов (QMD с плейсхолдерами)
│   ├─ cheatsheet.qmd         # одностраничная шпаргалка (include всех разделов)
│   ├─ linux.qmd
│   ├─ docker.qmd
│   ├─ git.qmd
│   ├─ kubernetes.qmd
│   └─ ... (другие темы)
├─ locales/
│   ├─ en/
│   │   ├─ _site.yml          # общие EN-строки (navbar, общие подписи, ссылки)
│   │   ├─ linux.yml
│   │   ├─ docker.yml
│   │   ├─ git.yml
│   │   └─ kubernetes.yml
│   └─ ru/
│       ├─ _site.yml
│       ├─ linux.yml
│       ├─ docker.yml
│       ├─ git.yml
│       └─ kubernetes.yml
├─ scripts/
│   └─ l10n_check.py          # проверка соответствия ключей в шаблонах и YAML
├─ docs/
│   └─ PROJECT_GUIDE.md       # этот документ
└─ .github/
    └─ workflows/
        └─ build.yml          # CI: рендер и публикация
```

---

## Конвенция ключей (v1.0)

### Формат ключа

```
<filename>.<chapter>.<section>.<item>.<field>
```

- **filename** — имя шаблона без расширения (`linux`, `docker`, `git`, `kubernetes`).
- **chapter** — крупный раздел страницы (`basic`, `intermediate`, `advanced`, `network`, `files`, `packages`, `monitoring`, `scripts`, `dev-debug`, `misc`, …).
- **section** — вложенный блок внутри главы; если не требуется, используем `_root`.
- **item** — элемент внутри секции:
  - обычно конкретная команда (`ls`, `chmod`, `curl`, …),
  - либо служебные элементы: `columns` (заголовки таблицы), `notes` (заметки), `meta` (заголовок/описание).
- **field** — конкретное поле: `title`, `desc`, `ex1`, `ex2`, `tip1`, `note1`, `link1`, `label` и т. п.

### Правила именования

- Только **латиница**, **нижний регистр**, разделитель — точка.
- Составные слова — **kebab-case**: `file-systems`, `system-monitoring`.
- Имена команд — как в CLI: `git`, `ls`, `ip-route`, `hostnamectl`.
- Не используем точку внутри токена (кроме разделителей сегментов ключа).
- `_root` — зарезервированный маркер «без секции».
- Резервные поля: `title`, `desc`, `exN` (N=1..n), `tipN`, `noteN`, `linkN`, `label` — не использовать для иных целей.

### Примеры

- Заголовок страницы: `linux.meta._root.title`
- Описание под заголовком: `linux.meta._root.desc`
- Заголовки таблицы «Базовые»: `linux.basic._root.columns.command|example|description`
- Команда `cat`: `linux.basic._root.cat.desc|ex1|ex2|ex3`
- Команда `chmod`: `linux.intermediate._root.chmod.desc|ex1|ex2|ex3`

### Общие ключи (непривязанные к файлу)

- Заголовки столбцов для всех шаблонов: `common.table.columns.command|example|description`
- Повторяющиеся callout‑фразы: `common.callouts.sudo-warn`
- Частые ссылки: `common.links.man-pages`, `common.links.tldr`

---

## Шаблоны и включения

### Главная шпаргалка

`templates/cheatsheet.qmd` включает разделы через `include` (каждый раздел — отдельный шаблон):

```markdown
---
title: "{{< var common.site.title >}}"
page-layout: article
---

{{< include templates/linux.qmd >}}
{{< include templates/docker.qmd >}}
{{< include templates/git.qmd >}}
{{< include templates/kubernetes.qmd >}}
```

### Пример шаблона раздела (фрагмент `templates/linux.qmd`)

```markdown
# {{< var linux.meta._root.title >}}

> {{< var linux.meta._root.desc >}}

## {{< var linux.basic._root.title >}}

| {{< var common.table.columns.command >}}                | {{< var common.table.columns.example >}} | {{< var common.table.columns.description >}} |
| ------------------------------------------------------- | ---------------------------------------- | -------------------------------------------- |
| [**`cat`**](https://tldr.inbrowser.app/pages/linux/cat) |                                          | {{< var linux.basic._root.cat.desc >}}       |
|                                                         | `cat file.txt`                           | {{< var linux.basic._root.cat.ex1 >}}        |
|                                                         | `cat file1 file2`                        | {{< var linux.basic._root.cat.ex2 >}}        |
|                                                         | `cat file1 file2 > merged.txt`           | {{< var linux.basic._root.cat.ex3 >}}        |
```

> В шаблонах **нет** текстов конкретного языка; только структура и плейсхолдеры.

---

## Локали

### Разбиение по главам (Подход №1)

- Для каждого языка — папка `locales/<lang>/`.
- Общие строки (navbar, заголовки столбцов, ссылки) — в `_site.yml`.
- Тематические строки — в `<filename>.yml` (например, `linux.yml`).

#### Пример `locales/en/_site.yml`

```yaml
common:
  site:
    title: "DevOps Commands & Scenarios Cheat Sheet"
  table:
    columns:
      command: "Command"
      example: "Example"
      description: "Description"
  callouts:
    sudo-warn: "Be careful with sudo: always check the command before running."
  links:
    man-pages: "https://man7.org/linux/man-pages/"
    tldr: "https://tldr.sh/"
```

#### Пример `locales/en/linux.yml` (фрагмент)

```yaml
linux:
  meta:
    _root:
      title: "🐧 Linux Command Line"
      desc: "Basic and advanced commands for navigation, files, processes, networking, and automation."

  basic:
    _root:
      title: "🔹 Basic commands"
      columns: {}
      cat:
        desc: "Show file content or concatenate multiple files"
        ex1: "View file content"
        ex2: "Concatenate and output two files"
        ex3: "Concatenate files and save to a new file"
    # ...
```

> Структура ключей в `ru/` зеркалирует `en/` один к одному.

---

## Профили Quarto и рендеринг

### Базовый конфиг `_quarto.yml`

- Назначение: рендер главной страницы `/` (англ.) и общие настройки сайта.
- Включает тему, TOC, CSS, поиск, навбар.

### Профили `_quarto-en.yml` и `_quarto-ru.yml`

- Назначение: рендер одностраничной шпаргалки в подпапки `/en/` и `/ru/`.
- Определяют `metadata-files` для языка, `output-dir` и `render` (какие файлы собирать).

### Команды

```bash
# Главная страница (EN)
quarto render

# Полная шпаргалка EN
quarto render --profile en

# Полная шпаргалка RU
quarto render --profile ru
```

---

## Правила для таблиц (без горизонтальной прокрутки)

### CSS (styles.css)

```css
/* Универсальная сетка для таблиц шпаргалки */
table {
  table-layout: fixed;
  width: 100%;
}
td,
th {
  vertical-align: top;
}

/* Перенос длинных токенов внутри code */
td code,
th code {
  white-space: pre-wrap; /* уважает \n и позволяет переносы */
  overflow-wrap: anywhere; /* перенос любых длинных "слов" */
  word-break: break-word; /* подстраховка */
}

/* Мобильные корректировки */
@media (max-width: 992px) {
  table {
    font-size: 0.95rem;
  }
}
@media (max-width: 576px) {
  table {
    font-size: 0.9rem;
  }
}
```

### Рекомендации по содержимому

- Стараться, чтобы «Пример» оставался минимальным (лишние параметры переносить в «Описание»).
- Для сверхдлинных токенов допустим ручной разрыв через `<wbr>` внутри `code`.
- При необходимости можно задать доли ширины столбцов через `<colgroup>` для конкретной таблицы.

---

## CI/CD (GitHub Actions)

Файл `.github/workflows/build.yml` (пример):

```yaml
name: build-and-deploy
on:
  push:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: quarto-dev/quarto-actions/setup@v2
      - name: Render HOME (root)
        run: quarto render
      - name: Render EN
        run: quarto render --profile en
      - name: Render RU
        run: quarto render --profile ru
      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: _site

  deploy:
    needs: build
    permissions:
      pages: write
      id-token: write
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    steps:
      - id: deployment
        uses: actions/deploy-pages@v4
```

---

## Скрипт проверки локалей (`scripts/l10n_check.py`)

Задачи:

1. Собрать все плейсхолдеры `{{< var ... >}}` из шаблонов в `templates/`.
2. Смёрджить YAML из `metadata-files` профиля (`_quarto-*.yml`).
3. Проверить, что каждый ключ существует; иначе — вывести список пропусков и завершиться с ошибкой (для CI).

Псевдокод (упрощённый фрагмент):

```python
import re, sys, yaml, pathlib

VAR = re.compile(r"\{\{<\s*var\s+([^\s>]+)\s*>\}\}")

def load_yaml(paths):
    data = {}
    for p in paths:
        with open(p, 'r', encoding='utf-8') as f:
            d = yaml.safe_load(f) or {}
        # простое слияние словарей; при необходимости заменить на deep-merge
        for k, v in d.items():
            if isinstance(v, dict) and isinstance(data.get(k), dict):
                data[k].update(v)
            else:
                data[k] = v
    return data

def get(obj, dotted):
    cur = obj
    for part in dotted.split('.'):
        if isinstance(cur, dict) and part in cur:
            cur = cur[part]
        else:
            return None
    return cur

# 1) собрать ключи из всех шаблонов
keys = set()
for p in pathlib.Path('templates').glob('**/*.qmd'):
    txt = p.read_text(encoding='utf-8')
    keys.update(VAR.findall(txt))

# 2) определить профиль из аргумента (ru|en) и его metadata-files
lang = sys.argv[1] if len(sys.argv) > 1 else 'ru'
meta = {
    'ru': [
        'locales/ru/_site.yml',
        'locales/ru/linux.yml',
        'locales/ru/docker.yml',
        'locales/ru/git.yml',
        'locales/ru/kubernetes.yml',
    ],
    'en': [
        'locales/en/_site.yml',
        'locales/en/linux.yml',
        'locales/en/docker.yml',
        'locales/en/git.yml',
        'locales/en/kubernetes.yml',
    ],
}

data = load_yaml(meta[lang])

# 3) валидация
missing = sorted(k for k in keys if get(data, k) is None)
if missing:
    print('Missing keys ({}):'.format(len(missing)))
    for k in missing: print('  -', k)
    sys.exit(1)
else:
    print('All keys OK for', lang)
```

> В CI стоит вызывать проверку для каждого языка до рендера.

---

## Добавление нового языка — чек‑лист

1. Создать `locales/<lang>/`.
2. Скопировать `locales/en/_site.yml` → адаптировать.
3. Для каждой темы (`linux.yml`, `docker.yml`, …) создать YAML с **точно теми же ключами**, что и в EN/RU.
4. Создать профиль `_quarto-<lang>.yml` с нужными `metadata-files` и `output-dir: _site/<lang>`.
5. Добавить шаг рендера `<lang>` в CI.
6. Запустить `scripts/l10n_check.py <lang>` — убедиться, что нет пропусков.

---

## Добавление нового раздела (темы) — чек‑лист

1. Создать шаблон `templates/<filename>.qmd`.
2. Придерживаться конвенции ключей `filename.*` в плейсхолдерах.
3. Добавить включение в `templates/cheatsheet.qmd`.
4. Создать `locales/*/<filename>.yml` с полным набором ключей.
5. Запустить `l10n_check.py` для всех языков.

---

## Рекомендации по навигации

- Использовать автоматический TOC Quarto (`toc: true`, `toc-location: left`, `toc-depth: 3`).
- Не дублировать «Contents» вручную внутри страниц.
- Единые заголовки разделов и эмодзи — в локали.

---

## Частые ошибки и как их избежать

- **Отсутствующий ключ в локали** → `l10n_check.py` в CI останавливает сборку.
- **Переполнение таблицы** → применять правила из `styles.css`, при необходимости разрывы `<wbr>` в `code`.
- **Дублирование заголовков колонок** → использовать `common.table.columns.*`.
- **Случайные различия между языками** → все YAML зеркалируются; изменения в одной локали повторять во всех.

---

## Дальнейшие расширения (опционально)

- **Lua‑шорткоды** для генерации таблиц из массивов YAML (сокращают размер шаблонов, когда строк очень много).
- **Авто‑генератор болванок локали**: из EN формировать пустые файлы для нового языка по списку ключей.
- **Deep‑merge YAML**: заменить простое объединение на рекурсивное при необходимости.

---

## История версий

- **v1.0** — первичная фиксация структуры, конвенции ключей, правил сборки и стилей таблиц.

---

## Контакты

- Бренд: **Hackitect7**
- Автор: Алексей
