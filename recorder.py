import threading
from utils import log

class Recorder:
    def __init__(self):
        self._stop_event = threading.Event()
        self._recording = False

    def start(self, channel_url: str, output_ts: str):
        self._stop_event.clear()
        self._recording = True

        try:
            from streamlink import Streamlink
        except Exception as e:
            log(f"Streamlink import error: {e}")
            self._recording = False
            return

        log("Recording started")

        try:
            session = Streamlink()
            streams = session.streams(channel_url)

            if not streams:
                log("No streams found (offline or blocked)")
                return

            stream = streams.get("best")
            if stream is None:
                # Fallback: pick the first available stream
                stream = next(iter(streams.values()))

            with stream.open() as stream_fd, open(output_ts, "wb") as out_fd:
                while not self._stop_event.is_set():
                    chunk = stream_fd.read(1024 * 1024)
                    if not chunk:
                        break
                    out_fd.write(chunk)
        except Exception as e:
            log(f"Recording error: {e}")
        finally:
            self._recording = False
            log("Recording ended")

    def stop(self):
        if self._recording:
            log("Recording force-stopped by user")
        self._stop_event.set()
