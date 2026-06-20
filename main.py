import atexit
import json
import os
import sys
import threading
from concurrent.futures import ThreadPoolExecutor

from monitor import check_live
from recorder import Recorder
from remux import remux
from ui import AppUI
from utils import (
    ensure_dir,
    format_date_id,
    make_numbered_stem,
    sanitize_filename,
    sleep_safe,
)


def resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


def load_config(path):
    defaults = {
        "check_interval": 5,
        "output_dir": "output",
        "auto_remux": True,
    }

    try:
        with open(path, "r", encoding="utf-8") as f:
            loaded = json.load(f)
    except (OSError, json.JSONDecodeError) as e:
        print(f"Config load failed, using defaults: {e}")
        return defaults

    if not isinstance(loaded, dict):
        print("Config is not an object, using defaults")
        return defaults

    config = defaults.copy()
    config.update(loaded)

    try:
        config["check_interval"] = max(1, int(config["check_interval"]))
    except (TypeError, ValueError):
        config["check_interval"] = defaults["check_interval"]

    output_dir = str(config.get("output_dir") or defaults["output_dir"]).strip()
    config["output_dir"] = output_dir or defaults["output_dir"]

    auto_remux = config.get("auto_remux", defaults["auto_remux"])
    if isinstance(auto_remux, str):
        config["auto_remux"] = auto_remux.strip().lower() not in {"0", "false", "no", "off"}
    else:
        config["auto_remux"] = bool(auto_remux)

    return config


# ===== LOAD CONFIG =====
config_path = resource_path("config.json")
CONFIG = load_config(config_path)

monitoring = False
recorder = Recorder()
archive_executor = ThreadPoolExecutor(max_workers=1, thread_name_prefix="archive")


def finalize_archive(ts_path, mp4_path, ui):
    ts_name = os.path.basename(ts_path)
    archive_name = os.path.basename(mp4_path)

    try:
        if not os.path.exists(ts_path) or os.path.getsize(ts_path) == 0:
            ui.add_log(f"Archive skipped, TS missing or empty: {ts_name}")
            return

        if CONFIG.get("auto_remux", True):
            ui.add_log(f"Finalizing MP4 in background: {archive_name}")
            success = remux(ts_path, mp4_path)
            if success:
                ui.add_log(f"Archive completed: {archive_name}")
            else:
                ui.add_log(f"Archive failed, TS preserved: {os.path.basename(ts_path)}")
        else:
            ui.add_log(f"Archive completed as TS: {os.path.basename(ts_path)}")
    except Exception as e:
        ui.add_log(f"Archive error, TS preserved: {e}")


def queue_archive(ts_path, mp4_path, ui):
    archive_executor.submit(finalize_archive, ts_path, mp4_path, ui)


atexit.register(lambda: archive_executor.shutdown(wait=False, cancel_futures=True))


# ===== MONITOR LOOP =====
def monitor_loop(url, ui):
    global monitoring
    recording = False

    while monitoring:
        try:
            status = check_live(url)
        except Exception as e:
            ui.add_log(f"Monitor error: {e}")
            sleep_safe(CONFIG["check_interval"], lambda: not monitoring)
            continue

        # ===== LIVE DETECTED =====
        if status.get("live") and not recording:
            recording = True
            try:
                ui.set_status("LIVE")
                ui.add_log("LIVE detected")

                title = sanitize_filename(status.get("title") or "Live Stream") or "Live Stream"
                username = sanitize_filename(status.get("username") or "channel") or "channel"
                date_str = format_date_id()

                base_dir = os.path.join(CONFIG["output_dir"], username)
                ensure_dir(base_dir)

                stem = os.path.join(base_dir, f"{title} - {date_str}")
                stem = make_numbered_stem(stem, exts=[".mp4", ".ts"])
                ts_path = stem + ".ts"
                mp4_path = stem + ".mp4"

                # ===== START RECORDING =====
                ui.set_status("RECORDING")
                ui.add_log("Recording started")

                result = recorder.start(url, ts_path)

                # ===== RECORDING FINISHED =====
                if result.success:
                    ui.add_log(f"Recording ended ({result.bytes_written:,} bytes)")
                    queue_archive(ts_path, mp4_path, ui)
                    ui.add_log("Archive queued; monitoring continues")
                else:
                    if os.path.exists(ts_path) and os.path.getsize(ts_path) == 0:
                        os.remove(ts_path)
                    ui.add_log(f"Recording failed: {result.error}")
                    ui.add_log("Archive skipped; monitoring continues")
            except Exception as e:
                ui.add_log(f"Recording workflow error: {e}")
            finally:
                ui.set_status("MONITORING" if monitoring else "OFFLINE")
                recording = False

        # ===== WAIT (RESPONSIVE STOP) =====
        sleep_safe(CONFIG["check_interval"], lambda: not monitoring)


# ===== UI CALLBACKS =====
def start_monitoring(url):
    global monitoring
    url = url.strip()

    if monitoring:
        return False

    if not url:
        app.add_log("Please enter a Kick channel URL")
        return False

    monitoring = True
    app.add_log("Monitoring started")
    app.set_status("MONITORING")

    threading.Thread(
        target=monitor_loop,
        args=(url, app),
        daemon=True,
    ).start()

    return True


def stop_monitoring():
    global monitoring

    if not monitoring:
        return

    monitoring = False
    recorder.stop()
    app.set_status("OFFLINE")
    app.add_log("Monitoring stopped")


# ===== START UI =====
app = AppUI(start_monitoring, stop_monitoring)
app.mainloop()
