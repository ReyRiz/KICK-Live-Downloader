import os
import threading
from dataclasses import dataclass

from utils import log


@dataclass
class RecordingResult:
    success: bool
    bytes_written: int = 0
    error: str = ""


class Recorder:
    def __init__(self):
        self._stop_event = threading.Event()
        self._recording = False

    def start(self, channel_url: str, output_ts: str) -> RecordingResult:
        self._stop_event.clear()
        self._recording = True
        bytes_written = 0

        try:
            from streamlink import Streamlink
        except Exception as e:
            error = f"Streamlink import error: {e}"
            log(error)
            self._recording = False
            return RecordingResult(False, error=error)

        log("Recording started")

        try:
            session = Streamlink()
            streams = session.streams(channel_url)

            if not streams:
                error = "No streams found (offline or blocked)"
                log(error)
                return RecordingResult(False, error=error)

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
                    bytes_written += len(chunk)

            if not os.path.exists(output_ts) or os.path.getsize(output_ts) == 0:
                error = "Recording produced an empty TS file"
                log(error)
                return RecordingResult(False, bytes_written=bytes_written, error=error)

            return RecordingResult(True, bytes_written=bytes_written)
        except Exception as e:
            error = f"Recording error: {e}"
            log(error)
            return RecordingResult(False, bytes_written=bytes_written, error=error)
        finally:
            self._recording = False
            log("Recording ended")

    def stop(self):
        if self._recording:
            log("Recording force-stopped by user")
        self._stop_event.set()
