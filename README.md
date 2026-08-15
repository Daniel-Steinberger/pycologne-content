# PyCologne: Inhalte der Webseite

Die redaktionellen Inhalte von [pycologne.de](https://www.pycologne.de):
Termin-Ankündigungen, Protokolle vergangener Treffen, die festen Seiten und
die dazugehörigen Bilder. Der Programmcode der Webseite liegt getrennt davon
in [pycologne-app](https://github.com/Daniel-Steinberger/pycologne-app).

Der Sinn der Trennung: Eine Textänderung soll nichts weiter erfordern als
einen Commit hier. Es wird dafür nichts neu gebaut und nichts neu gestartet,
und niemand braucht dafür Zugang zum Server.

## Aufbau

```
md/events/JJJJ-MM-TT.md   Ein Treffen: vorher die Ankündigung, hinterher das Protokoll
md/about.md               Seite "Die User Group"
md/contact.md             Seite "Kontakt"
images/                   Logos
images/events/            Bilder zu einzelnen Terminen
```

Der Dateiname einer Termin-Datei ist ihr Datum, daraus zieht die Webseite die
Zuordnung. Termine finden am zweiten Mittwoch im Monat um 19:00 Uhr statt.
Eine Datei, deren Name kein Datum ist, taucht auf der Webseite nirgends auf,
weder in der Übersicht noch in der Suche noch im Kalender-Abo. Deshalb prüft
das die CI (s. u.).

Bilder werden aus dem Text heraus als `/static/images/...` angesprochen, also
etwa so:

```markdown
![Screenshot der Anwendung](/static/images/events/2026-09-09-klassifikation-demo.svg)
```

## Ändern

Ein Commit auf `main` genügt. Danach passiert Folgendes von selbst:

1. Die CI prüft die Inhalte (`check_content.py`).
2. Ist sie grün, zieht sie den Branch `live` auf diesen Stand vor.
3. Der Server holt sich `live` und liefert die neuen Inhalte aus.

Der Server folgt ausschließlich `live`, nie `main`. Ein Commit, der die
Prüfung nicht besteht, erreicht die Webseite also gar nicht erst.

**Etwas zurücknehmen**: `live` auf den letzten guten Commit zurücksetzen.
Dafür braucht es keinen Server-Zugriff und keine Kenntnis der Servertechnik.

## Vor dem Commit prüfen

```sh
python3 check_content.py
```

Braucht nichts weiter als Python, keine Installation. Geprüft wird, dass die
Dateinamen der Termine gültige Daten sind, dass jede Seite mit ihrer
Überschrift beginnt, dass Adressen im Text als Links ausgezeichnet sind und
dass verwendete Bilder auch wirklich im Repo liegen.

## Örtlich ansehen

Mit dem App-Repo daneben lässt sich die Seite lokal starten:

```sh
cd ..
git clone https://github.com/Daniel-Steinberger/pycologne-app
cd pycologne-app
make run
```

`make run` verlinkt die Inhalte aus diesem Repo automatisch in die
Anwendung und startet den Entwicklungsserver auf
[localhost:5014](http://localhost:5014). Änderungen an einer Markdown-Datei
sind nach einem Neuladen im Browser sichtbar, ohne Neustart.

## Wer hier schreiben darf

Schreibzugriff hat der Kreis der Maintainer, Beiträge von außen laufen über
Pull Requests. Das ist eine bewusste Entscheidung und keine Bequemlichkeit:
In den Markdown-Dateien ist eingebettetes HTML erlaubt, weil einzelne Seiten
es brauchen. Schreibzugriff hier bedeutet damit die Möglichkeit, beliebiges
Markup auf pycologne.de auszuliefern.

## Herkunft

Die Inhalte lagen bis August 2026 im App-Repo unter `templates/md/` und
`static/images/`. Die Historie ist beim Herauslösen erhalten geblieben, ein
`git log` reicht also weiter zurück als dieses Repo alt ist. Die Protokolle
der Jahre 2013 bis 2020 stammen aus dem früheren Etherpad-Archiv.

## Lizenz

GPL-3.0-or-later, wie das App-Repo.
