# -*- coding: utf-8 -*-
"""
Копирует ВСЕ файлы из assets/snippets/<section>/<yy>/ → assets/snippets/<section> для текущего профиля Quarto.
Локаль берётся из QUARTO_PROFILE: en-US→us, ru-RU→ru, us→us; иначе fallback us.

Поведение:
- Для каждого раздела (любая папка в assets/snippets/*):
  - копируем содержимое <section>/<yy>/ в <section>/ (перезаписываем одноимённые файлы);
  - если нет/пусто — fallback из <section>/us/;
- Подробные логи в стиле: "[select_snippets] src -> dst  (QUARTO_PROFILE='...', normalized='...')".
- Не падает (exit 0) — только предупреждения. Можно STRICT=1, чтобы падать при пропусках.
- CLEAN_ROOT=1 — перед копированием чистит файлы в корне раздела.
"""

import os
import sys
import shutil
from typing import Iterable, List

def log(msg: str) -> None:
    print(f"[select_snippets] {msg}")

def warn(msg: str) -> None:
    sys.stderr.write(f"[select_snippets][WARN] {msg}\n")

def repo_root() -> str:
    # .../<repo>/scripts/select_snippets.py -> <repo>
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(os.path.join(here, os.pardir))

def norm_profile(raw: str) -> str:
    return (raw or "").strip().replace("_", "-").lower()

def profile_to_yy(profile_norm: str) -> str:
    # 'en-US' -> 'us'; 'ru-RU' -> 'ru'; 'us' -> 'us'; иное -> 'us'
    if "-" in profile_norm:
        tail = profile_norm.rsplit("-", 1)[-1].strip().lower()
        return tail if len(tail) == 2 and tail.isalpha() else "us"
    return profile_norm if len(profile_norm) == 2 and profile_norm.isalpha() else "us"

def iter_sections(root: str) -> Iterable[str]:
    if not os.path.isdir(root):
        return
    for e in os.scandir(root):
        if e.is_dir() and not e.name.startswith("."):
            yield e.path

def list_files(d: str) -> List[str]:
    try:
        return [os.path.join(d, f) for f in os.listdir(d) if os.path.isfile(os.path.join(d, f))]
    except FileNotFoundError:
        return []

def clean_root(section_dir: str) -> int:
    removed = 0
    try:
        for name in os.listdir(section_dir):
            p = os.path.join(section_dir, name)
            if os.path.isfile(p):
                os.remove(p); removed += 1
    except FileNotFoundError:
        pass
    return removed

def copy_all(src_dir: str, dst_dir: str, profile_raw: str, profile_norm: str) -> int:
    files = list_files(src_dir)
    if not files:
        return 0
    os.makedirs(dst_dir, exist_ok=True)
    copied = 0
    for src in files:
        dst = os.path.join(dst_dir, os.path.basename(src))
        shutil.copy2(src, dst)
        log(f"{src} -> {dst}  (QUARTO_PROFILE='{profile_raw}', normalized='{profile_norm}')")
        copied += 1
    return copied

def main() -> None:
    # Работать всегда из корня репозитория — чтобы относительные пути были корректны
    os.chdir(repo_root())

    SNIPPETS_ROOT = os.environ.get("SNIPPETS_DIR", os.path.join("assets", "snippets"))
    CLEAN = os.environ.get("CLEAN_ROOT", "0") == "1"
    STRICT = os.environ.get("STRICT", "0") == "1"

    PROFILE_RAW = os.environ.get("QUARTO_PROFILE", "")
    profile_norm = norm_profile(PROFILE_RAW)
    yy = profile_to_yy(profile_norm)
    if not PROFILE_RAW:
        warn("QUARTO_PROFILE is not set. Using the 'us' fallback.")
        yy = "us"

    log(f"cwd={os.getcwd()}")
    log(f"Profile: raw='{PROFILE_RAW}', norm='{profile_norm}', locale folder='{yy}'")

    if not os.path.isdir(SNIPPETS_ROOT):
        warn(f"Directory not found: {SNIPPETS_ROOT}.")
        sys.exit(0 if not STRICT else 1)

    sections = 0
    total_copied = 0
    had_misses = False

    for section_dir in iter_sections(SNIPPETS_ROOT):
        sections += 1
        section = os.path.basename(section_dir)

        src_dir = os.path.join(section_dir, yy)
        if not list_files(src_dir):
            if yy != "us":
                fb = os.path.join(section_dir, "us")
                if list_files(fb):
                    warn(f"[{section}] No files in '{yy}'. Using the 'us' fallback.")
                    src_dir = fb
                else:
                    warn(f"[{section}] No files in either '{yy}' or 'us'. Skipping.")
                    had_misses = True
                    continue
            else:
                warn(f"[{section}] No files in 'us'. Skipping.")
                had_misses = True
                continue

        if CLEAN:
            removed = clean_root(section_dir)
            log(f"[{section}] Root cleanup: files deleted: {removed}")

        copied = copy_all(src_dir, section_dir, PROFILE_RAW, profile_norm)
        log(f"[{section}] Copied: {copied}")
        total_copied += copied

    log(f"Done. Sections: {sections}. Total copied: {total_copied}.")
    if STRICT and had_misses:
        sys.exit(1)

if __name__ == "__main__":
    main()
