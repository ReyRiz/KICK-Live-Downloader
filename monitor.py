from utils import log


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
    username = channel_url.rstrip("/").split("/")[-1]

    if _is_live_via_streamlink(channel_url):
        return {
            "live": True,
            "title": "Live Stream",
            "username": username,
        }

    return {"live": False, "title": "", "username": username}
