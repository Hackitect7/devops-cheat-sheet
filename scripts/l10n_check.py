#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Validate that all {{< var ... >}} keys used in templates exist in the metadata,
and (optionally) trace each key to the source YAML file(s).

Usage:
  python scripts/l10n_check.py en
  python scripts/l10n_check.py en --trace
  python scripts/l10n_check.py _quarto-en.yml --trace
"""

import argparse
import pathlib
import re
import sys
from typing import Any, Dict, Iterable, List, Optional, Tuple

try:
    import yaml
except ImportError:
    print("PyYAML is required. Install: python -m pip install pyyaml", file=sys.stderr)
    sys.exit(2)

ROOT = pathlib.Path(__file__).resolve().parents[1]
VAR = re.compile(r"\{\{<\s*var\s+([^\s>]+)\s*>\}\}")

# ---------------- helpers ----------------

def deep_merge(a: Dict[str, Any], b: Dict[str, Any]) -> Dict[str, Any]:
    out = dict(a)
    for k, v in (b or {}).items():
        if k in out and isinstance(out[k], dict) and isinstance(v, dict):
            out[k] = deep_merge(out[k], v)
        else:
            out[k] = v
    return out

def load_yaml_file(path: pathlib.Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    if not isinstance(data, dict):
        return {}
    return data

def load_yaml_files(paths: Iterable[pathlib.Path]) -> Dict[str, Any]:
    data: Dict[str, Any] = {}
    for p in paths:
        data = deep_merge(data, load_yaml_file(p))
    return data

def get_by_dotted(obj: Any, dotted: str) -> Any:
    cur = obj
    for part in dotted.split("."):
        if isinstance(cur, dict) and part in cur:
            cur = cur[part]
        else:
            return None
    return cur

def collect_template_keys(templates_dir: pathlib.Path) -> List[str]:
    keys = set()
    for p in templates_dir.rglob("*.qmd"):
        txt = p.read_text(encoding="utf-8")
        keys.update(VAR.findall(txt))
    return sorted(keys)

def read_profile_metadata_files(profile_yaml: pathlib.Path) -> List[pathlib.Path]:
    cfg = load_yaml_file(profile_yaml)
    files = cfg.get("metadata-files") or []
    if not isinstance(files, list):
        files = []
    result: List[pathlib.Path] = []
    for f in files:
        p = ROOT.joinpath(pathlib.Path(f))
        result.append(p)
    return result

def default_meta_files_for_lang(lang: str) -> List[pathlib.Path]:
    """Fallback if _quarto-<lang>.yml is missing."""
    base = ROOT / "locales" / lang
    candidates = [
        base / "_site.yml",
        base / "linux.yml",
        base / "docker.yml",
        base / "git.yml",
        base / "kubernetes.yml",
    ]
    return [p for p in candidates if p.exists()]

def find_key_in_files(meta_files: List[pathlib.Path], dotted: str) -> Tuple[Optional[pathlib.Path], List[pathlib.Path]]:
    """Return (first_source, overrides_list)."""
    parts = dotted.split(".")
    source: Optional[pathlib.Path] = None
    overrides: List[pathlib.Path] = []
    for path in meta_files:
        doc = load_yaml_file(path)
        cur: Any = doc
        ok = True
        for p in parts:
            if isinstance(cur, dict) and p in cur:
                cur = cur[p]
            else:
                ok = False
                break
        if ok:
            if source is None:
                source = path
            else:
                overrides.append(path)
    return source, overrides

def flatten_meta_keys(d: Dict[str, Any], prefix: str = "") -> List[str]:
    items: List[str] = []
    for k, v in d.items():
        key = f"{prefix}.{k}" if prefix else k
        if isinstance(v, dict):
            items.extend(flatten_meta_keys(v, key))
        else:
            items.append(key)
    return items

# ---------------- main ----------------

def main() -> int:
    ap = argparse.ArgumentParser(
        description="Validate {{< var ... >}} keys against profile metadata files."
    )
    ap.add_argument("profile", help="Profile name (e.g., en, ru) OR path to _quarto-<lang>.yml")
    ap.add_argument("--templates", default="templates", help="Templates directory (default: templates)")
    ap.add_argument("--trace", action="store_true", help="Trace each key to the source YAML file(s)")
    args = ap.parse_args()

    templates_dir = ROOT.joinpath(args.templates)
    if not templates_dir.exists():
        print(f"ERROR: templates dir not found: {templates_dir}", file=sys.stderr)
        return 2

    # Resolve profile
    profile_arg = args.profile
    profile_path = ROOT.joinpath(profile_arg)
    meta_paths: List[pathlib.Path] = []

    if profile_path.exists():
        # Treat as explicit profile file
        meta_paths = read_profile_metadata_files(profile_path)
        if not meta_paths:
            print(f"WARNING: No metadata-files in {profile_path.name}. Falling back by lang guess...", file=sys.stderr)
            # try to guess lang from filename _quarto-xx.yml
            m = re.match(r"_quarto-(\w+)\.yml$", profile_path.name)
            if m:
                meta_paths = default_meta_files_for_lang(m.group(1))
    else:
        # Treat as short lang name
        guess_profile = ROOT / f"_quarto-{profile_arg}.yml"
        if guess_profile.exists():
            meta_paths = read_profile_metadata_files(guess_profile)
        if not meta_paths:
            # Fallback to default locales list
            meta_paths = default_meta_files_for_lang(profile_arg)

    if not meta_paths:
        print("ERROR: Could not resolve any metadata-files for the given profile/lang.", file=sys.stderr)
        return 2

    # Warn for missing files in list (keep order)
    resolved = []
    for p in meta_paths:
        if not p.exists():
            print(f"NOTE: metadata file not found (skipped): {p}", file=sys.stderr)
        else:
            resolved.append(p)
    meta_paths = resolved
    if not meta_paths:
        print("ERROR: All metadata files are missing.", file=sys.stderr)
        return 2

    # Load metadata and collect keys
    meta_data = load_yaml_files(meta_paths)
    used_keys = collect_template_keys(templates_dir)

    # Validation
    missing = sorted(k for k in used_keys if get_by_dotted(meta_data, k) is None)
    if missing:
        print(f"Missing keys ({len(missing)}):")
        for k in missing:
            print("  -", k)
    else:
        print(f"All keys OK ({len(used_keys)} keys)")  # no missing

    # Optional: trace
    if args.trace:
        print("\nTRACE (key -> source [overrides...]):")
        for k in used_keys:
            src, ov = find_key_in_files(meta_paths, k)
            if src is None:
                print(f"  {k}  ->  MISSING")
            elif ov:
                ov_s = ", ".join(str(p) for p in ov)
                print(f"  {k}  ->  {src}  (overridden by: {ov_s})")
            else:
                print(f"  {k}  ->  {src}")

        # Bonus: report unused meta keys (info only)
        all_meta_keys = set(flatten_meta_keys(meta_data))
        unused = sorted(k for k in all_meta_keys if k not in set(used_keys) and not k.startswith("quarto"))
        if unused:
            print(f"\nNote: {len(unused)} metadata keys are currently unused.")

    return 0 if not missing else 1


if __name__ == "__main__":
    sys.exit(main())
