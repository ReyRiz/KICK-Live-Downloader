from utils import log
from urllib.parse import urlparse


def _is_live_via_streamlink(channel_url: str) -> bool:
    try:
        from streamlink import Streamlink
    except Exception as e:
        log(f"Streamlink import error: {e}")
        return False

    try:
        session = Streamlink()
        streams = session.streams(channel_url)
        return bool(streams)
    except Exception as e:
        log(f"Streamlink probe error: {e}")
        return False

def check_live(channel_url: str) -> dict:
    parsed = urlparse(channel_url.strip())
    path = parsed.path if parsed.scheme else channel_url.strip()
    username = path.strip("/").split("/")[-1] or "channel"

    if _is_live_via_streamlink(channel_url):
        return {
            "live": True,
            "title": "Live Stream",
            "username": username,
        }

    return {"live": False, "title": "", "username": username}
