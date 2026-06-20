import subprocess
import os
import sys
import shutil
from typing import Optional

from utils import log


def resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


def _find_ffmpeg() -> Optional[str]:
    candidates = [
        resource_path(os.path.join("ffmpeg", "ffmpeg.exe")),
        resource_path(os.path.join("ffmpeg", "bin", "ffmpeg.exe")),
        shutil.which("ffmpeg"),
    ]

    for candidate in candidates:
        if candidate and os.path.exists(candidate):
            return candidate

    return None


def remux(ts_path: str, mp4_path: str) -> bool:
    if not os.path.exists(ts_path) or os.path.getsize(ts_path) == 0:
        log("TS file missing or empty, skip remux")
        return False

    ffmpeg_path = _find_ffmpeg()
    if not ffmpeg_path:
        log("ffmpeg.exe not found, skip remux")
        return False

    output_dir = os.path.dirname(mp4_path)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    log("Remuxing TS to MP4")

    mp4_base, mp4_ext = os.path.splitext(mp4_path)
    temp_mp4_path = f"{mp4_base}.tmp{mp4_ext or '.mp4'}"
    if os.path.exists(temp_mp4_path):
        os.remove(temp_mp4_path)

    cmd = [
        ffmpeg_path,
        "-y",
        "-i", ts_path,
        "-c", "copy",
        "-f", "mp4",
        temp_mp4_path,
    ]

    try:
        subprocess.run(
            cmd,
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
            text=True,
        )
        if not os.path.exists(temp_mp4_path) or os.path.getsize(temp_mp4_path) == 0:
            log("Remux failed, MP4 output is empty")
            return False
        os.replace(temp_mp4_path, mp4_path)
        os.remove(ts_path)
        log("Remux success")
        return True
    except subprocess.CalledProcessError as e:
        if os.path.exists(temp_mp4_path):
            os.remove(temp_mp4_path)
        stderr = (e.stderr or "").strip().splitlines()
        detail = stderr[-1] if stderr else str(e)
        log(f"Remux failed, TS file preserved: {detail}")
        return False
    except OSError as e:
        if os.path.exists(temp_mp4_path):
            os.remove(temp_mp4_path)
        log(f"Remux failed, TS file preserved: {e}")
        return False
