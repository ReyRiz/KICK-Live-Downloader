import subprocess
import os
import sys
from utils import log


def resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


def remux(ts_path: str, mp4_path: str) -> bool:
    if not os.path.exists(ts_path):
        log("TS file missing, skip remux")
        return False

    ffmpeg_path = resource_path(os.path.join("ffmpeg", "ffmpeg.exe"))

    log("Remuxing TS to MP4")

    cmd = [
        ffmpeg_path,
        "-y",
        "-i", ts_path,
        "-c", "copy",
        mp4_path,
    ]

    try:
        subprocess.run(cmd, check=True)
        os.remove(ts_path)
        log("Remux success")
        return True
    except subprocess.CalledProcessError:
        log("Remux failed, TS file preserved")
        return False
