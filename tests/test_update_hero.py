from pathlib import Path
import unittest

from scripts.update_hero import CHANNEL_ID, resolve, select_stream, select_upload, update_html


def video(id="abcdefghijk", kind="none", published="2026-09-29T10:00:00Z", **extra):
    return {"id": id, "snippet": {"channelId": CHANNEL_ID, "title": 'Titel & "Test"',
            "liveBroadcastContent": kind, "publishedAt": published},
            "status": {"privacyStatus": "public", "embeddable": True}, **extra}


class HeroTests(unittest.TestCase):
    def test_stream_priority_and_next_scheduled(self):
        later = video("abcdefghij1", "upcoming", liveStreamingDetails={"scheduledStartTime": "2026-10-03T13:00:00Z"})
        sooner = video("abcdefghij2", "upcoming", liveStreamingDetails={"scheduledStartTime": "2026-10-02T13:00:00Z"})
        self.assertEqual(select_stream([later, sooner], "upcoming"), sooner)
        self.assertIsNone(select_stream([later], "live"))

    def test_public_embeddable_channel_only(self):
        for field, value in [("privacyStatus", "private"), ("privacyStatus", "unlisted"), ("embeddable", False)]:
            item = video(kind="live")
            item["status"][field] = value
            self.assertIsNone(select_stream([item], "live"))
        item = video(kind="live")
        item["snippet"]["channelId"] = "another-channel"
        self.assertIsNone(select_stream([item], "live"))

    def test_upload_ignores_streams_and_uses_publication_date(self):
        old = video()
        new = video("abcdefghij2", published="2026-10-01T10:00:00Z")
        archived = video("abcdefghij3", published="2026-10-02T10:00:00Z", liveStreamingDetails={"actualEndTime": "2026-10-02T11:00:00Z"})
        upcoming = video("abcdefghij4", "upcoming")
        self.assertEqual(select_upload([new, archived, old, upcoming]), new)

    def test_ended_stream_not_selected(self):
        ended = video(kind="live", liveStreamingDetails={"actualEndTime": "2026-10-02T11:00:00Z"})
        self.assertIsNone(select_stream([ended], "live"))

    def test_exact_layout_and_player_options_preserved(self):
        source = Path("index.html").read_text()
        updated = update_html(source, video(), "upcoming")
        # Only video IDs and associated labels may change, including HTML escaping.
        expected = source.replace("/embed/ac0qW1LdM8Q?", "/embed/abcdefghijk?").replace(
            "Neuestes Video: Neuer Controller", "Geplanter Livestream: Titel &amp; &quot;Test&quot;")
        expected = expected.replace("/embed/i9wItnbXH6Y?", "/embed/abcdefghijk?").replace(
            "Kreher Imperial 2.0 – neuestes Video", "Geplanter Livestream: Titel &amp; &quot;Test&quot;")
        self.assertEqual(updated, expected)
        self.assertIn("mute=1", updated)
        self.assertIn("enablejsapi=1", updated)

    def test_unexpected_markup_fails_instead_of_corrupting_page(self):
        with self.assertRaises(RuntimeError):
            update_html("<html></html>", video(), "video")

    def test_resolution_stops_at_running_stream(self):
        class FakeAPI:
            def pages(self, resource, **params):
                self.kind = params["eventType"]
                return [{"id": {"videoId": "abcdefghijk"}}]

            def videos(self, ids):
                list(ids)
                return [video(kind=self.kind)]

            def get(self, *args, **kwargs):
                raise AssertionError("Uploads must not be queried when live")
        selected, kind = resolve(FakeAPI())
        self.assertEqual(kind, "live")

    def test_resolution_upcoming_and_normal_fallback(self):
        for stream_kind in ("upcoming", None):
            class FakeAPI:
                def pages(self, resource, **params):
                    if resource == "search":
                        self.kind = params["eventType"]
                        return [{"id": {"videoId": "abcdefghijk"}}] if self.kind == stream_kind else []
                    return [{"contentDetails": {"videoId": "abcdefghijk"}}]

                def videos(self, ids):
                    return [video(kind=stream_kind or "none")] if list(ids) else []

                def get(self, *args, **kwargs):
                    return {"items": [{"contentDetails": {"relatedPlaylists": {"uploads": "uploads-id"}}}]}
            self.assertEqual(resolve(FakeAPI())[1], stream_kind or "video")


if __name__ == "__main__":
    unittest.main()
