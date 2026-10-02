# Thomas Reh

Persönliche Website von Thomas Reh.

Themen: Camper, Camperausbau, Fahrradwohnwagen (FaWoWa), Liegerad, Boot, Reisen, Piaggio MP3, Fahrrad, Drohne, Technik, Videoschnitt, Livestreams und YouTube.

YouTube-Kanal: Kreher Imperial 2.0
https://www.youtube.com/user/furbybln

## Automatisches Hauptvideo

Der Workflow `.github/workflows/youtube-pages.yml` veröffentlicht die bestehende
statische Seite bei Änderungen an `main`, manuell und stündlich (Minute 17 UTC).
GitHub kann geplante Läufe verzögern. Er wählt für Kanal
`UCqP7ZH3SxoWeOIZENSGul5g` zuerst einen laufenden öffentlichen Livestream,
sonst den geplanten Stream mit dem frühesten Start, sonst das neueste öffentliche
normale Video nach Veröffentlichungsdatum. Beendete Livestreams werden nicht als
normale Videos verwendet. Ausgewählt werden nur Videos, die Einbettung erlauben.

Voraussetzungen: YouTube Data API v3 aktivieren; API-Schlüssel als Repository
Actions Secret `YOUTUBE_API_KEY` speichern (API-Einschränkung auf YouTube Data
API v3, keine Browser-Referrer-Einschränkung). Unter Settings → Pages muss die
Source auf **GitHub Actions** stehen. Ein OAuth-Zugang ist nicht erforderlich.

Der Schlüssel wird nur im Build verwendet. Die veröffentlichte Seite enthält
weder ihn noch API-Abfragen. Das Skript ersetzt nur die Hero-Video-ID und zwei
Beschriftungen in der Kopie unter `_site/index.html`; die feste ID in der
Repository-Datei bleibt als Ausgangswert bestehen. Player-Optionen, JavaScript,
Unterseiten und übriges Design bleiben erhalten. Bei Fehlern wird nicht
veröffentlicht und die bisherige Seite bleibt online. Die Auswahl eines bereits
geplanten Streams wechselt beim Streambeginn automatisch in die Live-Wiedergabe
des YouTube-Players. Weitere Wechsel erscheinen nach dem nächsten erfolgreichen
Workflow und Neuladen der Seite.

Tests: `python3 -m unittest discover -s tests -v`.
Das dezente Badge über dem Hauptvideo animiert nur seinen Punkt auf größeren
Bildschirmen; mobil und bei reduzierter Bewegung bleibt es unbewegt.
