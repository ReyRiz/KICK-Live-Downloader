import os
import re
import datetime
import locale
import time

def sanitize_filename(text: str) -> str:
    text = re.sub(r'[\\/:*?"<>|]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text[:180]  # aman untuk Windows

def format_date_id(include_time: bool = False) -> str:
    try:
        locale.setlocale(locale.LC_TIME, "id_ID")
    except Exception:
        pass
    now = datetime.datetime.now()
    if include_time:
        # aman untuk nama file Windows (tanpa ':')
        return now.strftime("%d %B %Y %H-%M-%S")
    return now.strftime("%d %B %Y")

def make_unique_path(path: str) -> str:
    if not os.path.exists(path):
        return path

    base, ext = os.path.splitext(path)
    counter = 2
    while True:
        candidate = f"{base} ({counter}){ext}"
        if not os.path.exists(candidate):
            return candidate
        counter += 1

def make_numbered_stem(stem_path: str, exts: list[str]) -> str:
    """Return a unique stem by appending ' #N' (starting at 1).

    Example: make_numbered_stem('output/Foo - 13 Maret 2026', ['.mp4', '.ts'])
    might return 'output/Foo - 13 Maret 2026 #2'.
    """
    n = 1
    while True:
        candidate_stem = f"{stem_path} #{n}"
        if all(not os.path.exists(candidate_stem + ext) for ext in exts):
            return candidate_stem
        n += 1

def ensure_dir(path: str):
    os.makedirs(path, exist_ok=True)

def log(msg: str):
    ensure_dir("logs")
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] {msg}"
    print(line)
    with open("logs/app.log", "a", encoding="utf-8") as f:
        f.write(line + "\n")

def sleep_safe(seconds: int, stop_flag):
    for _ in range(seconds):
        if stop_flag():
            return
        time.sleep(1)
