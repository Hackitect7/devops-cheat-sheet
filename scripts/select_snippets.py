# filename: scripts/select_snippets.py
import os
import shutil
import sys

# Профиль из окружения (Quarto передаёт QUARTO_PROFILE)
PROFILE_RAW = os.environ.get("QUARTO_PROFILE", "").strip()
profile = PROFILE_RAW.replace("_", "-").lower()  # en_US -> en-us, RU_RU -> ru-ru, etc.

# База путей для сниппетов
base = os.path.join("assets", "snippets", "linux")
target = os.path.join(base, "tldr-install.sh")

# Карта источников (КЛЮЧИ — нижний регистр, ЗНАЧЕНИЯ — реальный путь к файлу)
# Папки у тебя: US, ES, RU
src_map = {
    "us": os.path.join(base, "US", "tldr-install.sh"),
    "es": os.path.join(base, "ES", "tldr-install.sh"),
    "ru": os.path.join(base, "RU", "tldr-install.sh"),
    "cn": os.path.join(base, "CN", "tldr-install.sh"),
    "sa": os.path.join(base, "SA", "tldr-install.sh"),
    "in": os.path.join(base, "IN", "tldr-install.sh"),
    "fr": os.path.join(base, "FR", "tldr-install.sh"),
    "br": os.path.join(base, "BR", "tldr-install.sh"),
    "de": os.path.join(base, "DE", "tldr-install.sh"),
    "bd": os.path.join(base, "BD", "tldr-install.sh"),
    "la": os.path.join(base, "la", "tldr-install.sh"),
    "mx": os.path.join(base, "MX", "tldr-install.sh"),
    "ir": os.path.join(base, "IR", "tldr-install.sh"),
    "id": os.path.join(base, "ID", "tldr-install.sh"),
    "it": os.path.join(base, "IT", "tldr-install.sh"),
    "jp": os.path.join(base, "JP", "tldr-install.sh"),
    "kr": os.path.join(base, "KR", "tldr-install.sh"),
    "pl": os.path.join(base, "PL", "tldr-install.sh"),
    "pt": os.path.join(base, "PT", "tldr-install.sh"),
    "ke": os.path.join(base, "KE", "tldr-install.sh"),
    "th": os.path.join(base, "TH", "tldr-install.sh"),
    "tr": os.path.join(base, "TR", "tldr-install.sh"),
    "ua": os.path.join(base, "UA", "tldr-install.sh"),
    "vn": os.path.join(base, "VN", "tldr-install.sh"),
    "hk": os.path.join(base, "HK", "tldr-install.sh"),
    "tw": os.path.join(base, "TW", "tldr-install.sh"),
}

# Алиасы профилей → ключи src_map
aliases = {
    # английский (US)
    "en-us": "us",
    "en": "us",
    "us": "us",

    # английский (GB)
    "en-gb": "gb",
    "en": "gb",
    "gb": "gb",

    # испанский (Испания)
    "es-es": "es",
    "es-mx": "es",
    "es": "es",

    # русский
    "ru-ru": "ru",
    "ru": "ru",

    # китайский упрощенный
    "zh-cn": "cn",
    "zh": "cn",
    "cn": "cn",

    # арабский
    "ar-sa": "sa",
    "ar": "sa",
    "sa": "sa",

    # хинди
    "hi-in": "in",
    "hi": "in",
    "in": "in",

    # французский
    "fr-fr": "fr",
    "fr": "fr",

    # португальский (Бразилия)
    "pt-br": "br",
    "pt": "br",
    "br": "br",

    # немецкий
    "de-de": "de",
    "de": "de",

    # бенгальский (Бангладеш)
    "bn-bd": "bd",
    "bn": "bd",
    "bd": "bd",

    # испанский (Латинская Америка)
    "es-la": "la",
    "es": "la",
    "la": "la",

    # испанский (Мексика)
    "es-mx": "mx",
    "es": "mx",
    "mx": "mx",

    # фарси (Иордания)
    "fa-ir": "ir",
    "fa": "ir",
    "ir": "ir",

    # индонезийский (Индонезия)
    "id-id": "id",
    "id": "id",

    # итальянский (Италия)
    "it-it": "it",
    "it": "it",

    # японский (Япония)
    "ja-jp": "jp",
    "ja": "jp",
    "jp": "jp",

    # корейский (Республика Корея)
    "ko-kr": "kr",
    "ko": "kr",
    "kr": "kr",

    # польский (Польша)
    "pl-pl": "pl",
    "pl": "pl",

    # португальский (Португалия)
    "pt-pt": "pt",
    "pt": "pt",

    # суахили (Восточная Африка: Кения, Танзания и др.)
    "sw-ke": "ke",
    "sw": "ke",
    "ke": "ke",

    # тайский (Таиланд)
    "th-th": "th",
    "th": "th",

    # турецкий (Турция)
    "tr-tr": "tr",
    "tr": "tr",

    # украинский (Украина)
    "uk-ua": "ua",
    "uk": "ua",
    "ua": "ua",

    # вьетнамский (Вьетнам)
    "vi-vn": "vn",
    "vi": "vn",
    "vn": "vn",

    # китайский традиционный (Гонконг)
    "zh-hk": "hk",
    "zh": "hk",
    "hk": "hk",

    # китайский традиционный (Тайвань)
    "zh-tw": "tw",
    "zh": "tw",
    "tw": "tw",
}

def pick_source(profile_key: str) -> str:
    """
    Выбираем подходящий исходник по профилю с fallback'ами:
    1) точный ключ после нормализации и алиасов
    2) язык без региона (если был регион)
    3) финальный fallback: 'us'
    """
    candidates = []

    # 0) исходный нормализованный ключ
    k = profile_key

    # 1) алиас, если есть
    k = aliases.get(k, k)
    if k:
        candidates.append(k)

    # 2) язык без региона (например, en-us -> en) и его алиас
    if "-" in profile_key:
        lang = profile_key.split("-", 1)[0]
        lang = aliases.get(lang, lang)
        candidates.append(lang)

    # 3) универсальный fallback
    candidates.append("us")

    # Ищем первый существующий файл
    for c in candidates:
        path = src_map.get(c)
        if path and os.path.isfile(path):
            return path

    return ""  # не нашли

def main():
    src = pick_source(profile)
    if not src:
        sys.stderr.write(
            "[select_snippets] ERROR: no snippet found. "
            f"QUARTO_PROFILE='{PROFILE_RAW}', normalized='{profile}'. "
            f"Checked keys: {list(src_map.keys())}\n"
        )
        sys.exit(1)

    os.makedirs(os.path.dirname(target), exist_ok=True)
    shutil.copyfile(src, target)
    print(f"[select_snippets] {src} -> {target}  (QUARTO_PROFILE='{PROFILE_RAW}', normalized='{profile}')")

if __name__ == "__main__":
    main()
