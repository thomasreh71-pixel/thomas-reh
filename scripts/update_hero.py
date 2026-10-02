"""Select the public YouTube hero at build time; never expose credentials."""
import html
import json
import os
from pathlib import Path
import re
import sys
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

CHANNEL_ID = "UCqP7ZH3SxoWeOIZENSGul5g"


class YouTube:
    def __init__(self, key):
        self.key = key

    def get(self, resource, **params):
        # Credentials are not included in exception messages or output files.
        url = "https://www.googleapis.com/youtube/v3/" + resource
        request = Request(url + "?" + urlencode(params),
                          headers={"X-Goog-Api-Key": self.key})
        try:
            with urlopen(request, timeout=30) as response:
                return json.load(response)
        except HTTPError as error:
            raise RuntimeError(f"YouTube API: HTTP {error.code}. Check API activation, key restrictions and quota.") from None
        except (URLError, TimeoutError, ValueError):
            raise RuntimeError("YouTube API unavailable or invalid response; deployment cancelled.") from None

    def pages(self, resource, **params):
        token = None
        while True:
            result = self.get(resource, **params, **({"pageToken": token} if token else {}))
            yield from result.get("items", [])
            token = result.get("nextPageToken")
            if not token:
                return

    def videos(self, ids):
        ids = list(dict.fromkeys(ids))
        result = []
        for offset in range(0, len(ids), 50):
            result.extend(self.get("videos", part="snippet,status,liveStreamingDetails",
                                   id=",".join(ids[offset:offset + 50])).get("items", []))
        return result


def playable(video):
    return (re.fullmatch(r"[A-Za-z0-9_-]{11}", video.get("id", "")) is not None
            and video.get("snippet", {}).get("channelId") == CHANNEL_ID
            and video.get("status", {}).get("privacyStatus") == "public"
            and video.get("status", {}).get("embeddable") is True)


def select_stream(videos, kind):
    eligible = [v for v in videos if playable(v)
                and v["snippet"].get("liveBroadcastContent") == kind
                and not v.get("liveStreamingDetails", {}).get("actualEndTime")]
    if not eligible:
        return None
    return min(eligible, key=lambda v: (
        v.get("liveStreamingDetails", {}).get("scheduledStartTime", "9999"), v["id"]))


def select_upload(videos):
    eligible = [v for v in videos if playable(v)
                and v["snippet"].get("liveBroadcastContent", "none") == "none"
                and not v.get("liveStreamingDetails")]
    return max(eligible, key=lambda v: (v["snippet"]["publishedAt"], v["id"]), default=None)


def resolve(api):
    for kind in ("live", "upcoming"):
        results = api.pages("search", part="snippet", channelId=CHANNEL_ID,
                            type="video", eventType=kind, maxResults=50, safeSearch="none")
        stream = select_stream(api.videos(r["id"]["videoId"] for r in results), kind)
        if stream:
            return stream, kind
    channels = api.get("channels", part="contentDetails", id=CHANNEL_ID).get("items", [])
    if len(channels) != 1:
        raise RuntimeError("Expected YouTube channel not found; deployment cancelled.")
    playlist = channels[0]["contentDetails"]["relatedPlaylists"]["uploads"]
    items = api.pages("playlistItems", part="contentDetails", playlistId=playlist, maxResults=50)
    video = select_upload(api.videos(item["contentDetails"]["videoId"] for item in items))
    if video is None:
        raise RuntimeError("No public embeddable normal video found; deployment cancelled.")
    return video, "video"


def update_html(source, video, kind):
    # Patch the existing tag, preserving all player options and layout attributes.
    match = list(re.finditer(r'<iframe\b[^>]*\bid="hero-latest-player"[^>]*>', source))
    if len(match) != 1:
        raise RuntimeError("Expected exactly one hero-latest-player iframe.")
    tag = match[0].group()
    if len(re.findall(r'src="https://www\.youtube\.com/embed/[A-Za-z0-9_-]{11}\?', tag)) != 1:
        raise RuntimeError("Unexpected hero embed URL; deployment cancelled.")
    label = {"live": "Livestream läuft", "upcoming": "Geplanter Livestream", "video": "Neuestes Video"}[kind]
    title = html.escape(label + ": " + video["snippet"]["title"], quote=True)
    tag = re.sub(r'(src="https://www\.youtube\.com/embed/)[A-Za-z0-9_-]{11}(\?)',
                 lambda m: m[1] + video["id"] + m[2], tag)
    tag, count = re.subn(r'\btitle="[^"]*"', lambda _: 'title="' + title + '"', tag)
    if count != 1:
        raise RuntimeError("Unexpected hero title attribute.")
    source = source[:match[0].start()] + tag + source[match[0].end():]
    pattern = r'(<div\b[^>]*\bclass="[^"]*\bhero-latest-video\b[^"]*"[^>]*\baria-label=")[^"]*(")'
    source, count = re.subn(pattern, lambda m: m[1] + title + m[2], source)
    if count != 1:
        raise RuntimeError("Unexpected hero container; deployment cancelled.")
    return source


def main():
    key = os.environ.get("YOUTUBE_API_KEY", "").strip()
    if not key:
        raise RuntimeError("Missing repository Actions secret YOUTUBE_API_KEY.")
    video, kind = resolve(YouTube(key))
    path = Path(sys.argv[1] if len(sys.argv) > 1 else "index.html")
    updated = update_html(path.read_text(encoding="utf-8"), video, kind)
    path.write_text(updated, encoding="utf-8")
    print(f"Hero updated: {kind} / {video['id']}")


if __name__ == "__main__":
    try:
        main()
    except (RuntimeError, KeyError) as error:
        print(f"Update failed: {error}", file=sys.stderr)
        sys.exit(1)
