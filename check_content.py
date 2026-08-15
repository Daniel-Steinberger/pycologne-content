#!/usr/bin/env python3
"""Prüfungen für die Inhalte dieses Repos.

Bewusst ohne jede Abhängigkeit, damit ein Aufruf von

    python3 check_content.py

überall funktioniert, ohne vorher etwas zu installieren. Die CI ruft
genau dieses Skript auf, es gibt also keinen zweiten Satz Regeln, der
davon abweichen könnte.

Die Prüfungen stammen aus `_tests/test_protocols.py` der Webanwendung.
Dort waren sie fehl am Platz, denn sie prüfen den Inhalt, nicht den Code.
"""

from __future__ import annotations

import datetime
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).parent
EVENTS_DIR = ROOT / "md" / "events"
IMAGES_DIR = ROOT / "images"

# Adressen im Fließtext, die nicht als Link ausgezeichnet sind. Markdown-Links
# ``[text](url)``, Autolinks ``<url>`` und Codeblöcke sind ausgenommen.
BARE_URL = re.compile(r'(?<![(<"\w])https?://')
BARE_HOST = re.compile(r"(?<![/\w.>(])www\.[\w.-]+\.[a-z]{2,}", re.I)
MD_LINK = re.compile(r"\[[^\]]*\]\(([^)]*)\)")
AUTOLINK = re.compile(r"<https?://[^>]*>")
IMAGE_REF = re.compile(r"/static/images/([\w./-]+)")


def markdown_files() -> list[pathlib.Path]:
    """Alle Markdown-Dateien des Repos, nach Pfad sortiert."""
    return sorted((ROOT / "md").rglob("*.md"))


def text_lines(path: pathlib.Path):
    """Zeilen einer Datei ohne Codeblöcke und ohne fertige Links."""
    in_fence = False
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        yield number, AUTOLINK.sub("", MD_LINK.sub("", line))


def check_event_filenames() -> list[str]:
    """Termin-Dateien müssen nach ihrem Datum benannt sein.

    Die Anwendung liest das Datum aus dem Dateinamen. Ein Tippfehler dort
    lässt die Datei stillschweigend aus Übersicht, Suche und Kalender
    verschwinden, statt einen Fehler zu werfen.
    """
    problems = []
    for path in sorted(EVENTS_DIR.iterdir()):
        if path.suffix != ".md":
            problems.append(f"{path.name}: keine Markdown-Datei in md/events/")
            continue
        try:
            datetime.date.fromisoformat(path.stem)
        except ValueError:
            problems.append(f"{path.name}: Dateiname ist kein Datum im Format JJJJ-MM-TT")
    return problems


def check_headings() -> list[str]:
    """Jede Seite beginnt mit ihrer Überschrift."""
    problems = []
    for path in markdown_files():
        lines = path.read_text(encoding="utf-8").splitlines()
        if not lines or not lines[0].startswith("# "):
            first = lines[0] if lines else "(leere Datei)"
            problems.append(f"{path.relative_to(ROOT)}: erste Zeile ist keine Überschrift: {first}")
    return problems


def check_addresses_are_linked() -> list[str]:
    """Adressen im Text müssen klickbar sein.

    Ein Link braucht Markdown-Syntax. Die linkify-Option des Parsers greift
    nur, solange das Paket linkify-it-py installiert ist; eine nackte URL
    bliebe sonst schlichter Text.
    """
    problems = []
    for path in markdown_files():
        for number, stripped in text_lines(path):
            if BARE_URL.search(stripped) or BARE_HOST.search(stripped):
                problems.append(
                    f"{path.relative_to(ROOT)}:{number}: nicht verlinkte Adresse: "
                    f"{stripped.strip()[:80]}"
                )
    return problems


def check_referenced_images_exist() -> list[str]:
    """Bilder, auf die eine Seite verweist, müssen auch im Repo liegen.

    Die Anwendung liefert `images/` unter `/static/images/` aus. Ein
    Verweis auf eine fehlende Datei fällt sonst erst im Browser auf.
    """
    problems = []
    for path in markdown_files():
        for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            for reference in IMAGE_REF.findall(line):
                if not (IMAGES_DIR / reference).is_file():
                    problems.append(
                        f"{path.relative_to(ROOT)}:{number}: Bild fehlt: images/{reference}"
                    )
    return problems


CHECKS = (
    ("Dateinamen der Termine", check_event_filenames),
    ("Überschriften", check_headings),
    ("verlinkte Adressen", check_addresses_are_linked),
    ("vorhandene Bilder", check_referenced_images_exist),
)


def main() -> int:
    """Alle Prüfungen laufen lassen und die Funde ausgeben."""
    total = 0
    for label, check in CHECKS:
        problems = check()
        total += len(problems)
        if problems:
            print(f"\n{label}: {len(problems)} Beanstandung(en)")
            for problem in problems:
                print(f"  {problem}")
        else:
            print(f"{label}: in Ordnung")
    if total:
        print(f"\n{total} Beanstandung(en) insgesamt.")
        return 1
    print(f"\nAlles in Ordnung ({len(markdown_files())} Seiten geprüft).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
