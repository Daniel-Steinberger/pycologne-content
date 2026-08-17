#!/usr/bin/env python3
"""Postet Termine und Rückblicke auf die Facebook-Page "pyCologne".

Bewusst ohne Abhängigkeiten (nur Standardbibliothek), wie check_content.py.
Aufgerufen vom GitHub-Workflow facebook.yml, funktioniert aber genauso von
Hand.

Modi:

    python3 facebook_post.py event 2026-09-09 [weitere Daten ...]
        Baut aus md/events/<Datum>.md einen Post. Liegt das Datum in der
        Zukunft, wird es eine Ankündigung (Datum, Ort, Programm-Teaser,
        Meetup-Link), sonst ein Rückblick (Themenliste aus den
        ###-Überschriften plus Link aufs Protokoll).

    python3 facebook_post.py text --file posts/beispiel.txt [--link URL]
        Postet den Inhalt der Datei wörtlich, optional mit Link-Vorschau.

    python3 facebook_post.py show [--post ID]
        Sieht nur nach, was auf der Page steht, und ändert nichts. Nötig,
        weil das Absetzen eines Posts lediglich eine ID zurückgibt: ob der
        Beitrag danach noch existiert, sagt allein ein Abruf.

Zugangsdaten kommen aus den Umgebungsvariablen FB_PAGE_ID und
FB_PAGE_TOKEN (im Repo als GitHub-Secrets hinterlegt, Einrichtung s.
README). Fehlen sie, läuft ein Probelauf: der fertige Post wird nur
ausgegeben, nichts wird gesendet. So lässt sich jeder Post gefahrlos
vorher ansehen.
"""

from __future__ import annotations

import argparse
import datetime
import json
import os
import pathlib
import re
import sys
import urllib.error
import urllib.parse
import urllib.request

ROOT = pathlib.Path(__file__).parent
GRAPH = "https://graph.facebook.com/v23.0"
WEBSITE = "https://www.pycologne.de"
MEETUP = "https://www.meetup.com/pycologne/"

# Überschriften, die in jedem Protokoll auftauchen und im Post nichts
# erzählen. Redaktionelle Heuristik, bei Bedarf ergänzen.
BOILERPLATE_TOPICS = (
    "einleitung",
    "rahmenbedingungen",
    "vorstellungsrunde",
    "weitere themen",
    "über den moderator",
)

_HEADING_NUMBER = re.compile(r"^\d+\.\s*")
_MD_LINK = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
_MD_MARKUP = re.compile(r"[*_`]+")
_META_LINE = re.compile(r"^\*\*(Datum|Ort|Dauer):\*\*\s*(.+?)\s*$")


def plain(text: str) -> str:
    """Markdown-Auszeichnung entfernen, Facebook rendert kein Markdown."""
    text = _MD_LINK.sub(r"\1", text)
    return _MD_MARKUP.sub("", text).strip()


def read_event(stem: str) -> dict:
    """Die Termin-Datei in ihre Bestandteile zerlegen."""
    path = ROOT / "md" / "events" / f"{stem}.md"
    lines = path.read_text(encoding="utf-8").splitlines()

    title = ""
    meta: dict[str, str] = {}
    topics: list[str] = []
    teaser: list[str] = []
    summary_intro: list[str] = []
    in_summary_intro = False
    seen_section = False  # ab der ersten ##/###-Überschrift kein Teaser mehr
    teaser_done = False

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("# ") and not title:
            title = stripped.removeprefix("# ").strip()
            continue
        match = _META_LINE.match(stripped)
        if match:
            meta[match.group(1)] = plain(match.group(2).split("([")[0])
            continue
        if stripped.startswith("## "):
            # Der Absatz direkt unter "## Zusammenfassung" (vor der ersten
            # ###-Überschrift) taugt als Einstiegstext des Rückblicks.
            in_summary_intro = stripped.removeprefix("## ").strip().lower() == "zusammenfassung"
            seen_section = True
            continue
        if stripped.startswith("### "):
            in_summary_intro = False
            seen_section = True
            topic = _HEADING_NUMBER.sub("", stripped.removeprefix("### ").strip())
            if not any(marker in topic.lower() for marker in BOILERPLATE_TOPICS):
                topics.append(plain(topic))
            continue
        if in_summary_intro and stripped:
            summary_intro.append(plain(stripped))
            continue
        # Teaser für Ankündigungen: erster Textabsatz im Kopfbereich, vor
        # der ersten Abschnitts-Überschrift und vor dem festen
        # "Wir suchen Themen!"-Block, ohne Metazeilen und Bilder.
        if seen_section or teaser_done or stripped.startswith("**Wir suchen Themen!**"):
            teaser_done = True
            continue
        if stripped and not stripped.startswith(("**", "![")):
            teaser.append(plain(stripped))
        elif teaser and not stripped:
            teaser_done = True

    return {
        "title": title or f"PyCologne Treffen {stem}",
        "meta": meta,
        "topics": topics,
        "teaser": " ".join(teaser),
        "summary_intro": " ".join(summary_intro),
        "url": f"{WEBSITE}/events/{stem}",
        "date": datetime.date.fromisoformat(stem),
    }


def event_message(stem: str) -> tuple[str, str]:
    """Post-Text und Link für einen Termin bauen."""
    event = read_event(stem)
    parts: list[str] = []
    if event["date"] >= datetime.date.today():
        parts.append(event["title"])
        if "Datum" in event["meta"]:
            parts.append("")
            parts.append(f"📅 {event['meta']['Datum']}")
        if "Ort" in event["meta"]:
            parts.append(f"📍 {event['meta']['Ort']}")
        if event["teaser"]:
            parts.append("")
            parts.append(event["teaser"])
        parts.append("")
        parts.append(f"Anmeldung, kostenlos und unverbindlich: {MEETUP}")
        parts.append(f"Alle Infos: {event['url']}")
    else:
        parts.append(f"Rückblick: {event['title']}")
        if event["summary_intro"]:
            parts.append("")
            parts.append(event["summary_intro"])
        if event["topics"]:
            parts.append("")
            parts.append("Themen des Abends:")
            parts.extend(f"• {topic}" for topic in event["topics"])
        parts.append("")
        parts.append(f"Das ganze Protokoll: {event['url']}")
    return "\n".join(parts), event["url"]


def publish(message: str, link: str | None) -> None:
    """Den Post absetzen, oder im Probelauf nur zeigen."""
    page_id = os.environ.get("FB_PAGE_ID", "")
    token = os.environ.get("FB_PAGE_TOKEN", "")
    print("=" * 62)
    print(message)
    if link:
        print(f"[Link-Vorschau: {link}]")
    print("=" * 62)
    if not page_id or not token:
        print("Probelauf: FB_PAGE_ID/FB_PAGE_TOKEN nicht gesetzt, nichts gesendet.")
        return
    payload = {"message": message, "access_token": token}
    if link:
        payload["link"] = link
    request = urllib.request.Request(
        f"{GRAPH}/{page_id}/feed",
        data=urllib.parse.urlencode(payload).encode("utf-8"),
        method="POST",
    )
    with urllib.request.urlopen(request) as response:
        result = json.load(response)
    print(f"Gepostet: {result.get('id', result)}")


def _get(path: str, **params: str) -> dict:
    """Eine lesende Graph-Abfrage, Antwort als Dictionary."""
    token = os.environ.get("FB_PAGE_TOKEN", "")
    if not token:
        raise SystemExit("FB_PAGE_TOKEN ist nicht gesetzt, ohne Token geht kein Abruf.")
    query = urllib.parse.urlencode({**params, "access_token": token})
    try:
        with urllib.request.urlopen(f"{GRAPH}/{path}?{query}") as response:
            return json.load(response)
    except urllib.error.HTTPError as error:
        # Der Fehlertext von Graph sagt, woran es liegt, und ist genau das,
        # was hier interessiert. Ohne ihn bleibt nur "HTTP 400".
        return {"fehler": json.loads(error.read().decode("utf-8", "replace"))}


def show(post_id: str | None) -> None:
    """Zeigen, was auf der Page steht, ohne etwas zu aendern.

    Gedacht zum Nachsehen, wenn ein Post nicht dort auftaucht, wo er
    erwartet wird: das Absetzen liefert nur eine ID zurueck, ob der Beitrag
    danach noch existiert, sagt allein ein Abruf.
    """
    page_id = os.environ.get("FB_PAGE_ID", "")
    if post_id:
        # Eine ID ohne Praefix gehoert zu dieser Page.
        full = post_id if "_" in post_id else f"{page_id}_{post_id}"
        print(f"--- Abruf des Beitrags {full} ---")
        print(json.dumps(_get(full, fields="id,created_time,message,permalink_url"), indent=2))
        return

    fields = "id,created_time,message,permalink_url,is_published,is_hidden"
    for edge in ("feed", "published_posts", "posts"):
        print(f"--- {edge} ---")
        print(json.dumps(_get(f"{page_id}/{edge}", fields=fields, limit="15"), indent=2))


def main() -> int:
    """Kommandozeile auswerten, s. Moduldocstring."""
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="mode", required=True)

    event_cmd = sub.add_parser("event", help="Termin-Datei(en) posten")
    event_cmd.add_argument("dates", nargs="+", metavar="JJJJ-MM-TT")

    text_cmd = sub.add_parser("text", help="Freitext aus Datei posten")
    text_cmd.add_argument("--file", required=True)
    text_cmd.add_argument("--link", default=None)

    show_cmd = sub.add_parser("show", help="Nachsehen, was auf der Page steht (nur lesend)")
    show_cmd.add_argument("--post", default=None, help="Eine einzelne Beitrags-ID abrufen")

    args = parser.parse_args()
    if args.mode == "event":
        for stem in args.dates:
            message, link = event_message(stem)
            publish(message, link)
    elif args.mode == "show":
        show(args.post)
    else:
        message = (ROOT / args.file).read_text(encoding="utf-8").strip()
        publish(message, args.link)
    return 0


if __name__ == "__main__":
    sys.exit(main())
