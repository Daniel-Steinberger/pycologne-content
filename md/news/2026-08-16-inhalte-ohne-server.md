# Textänderungen brauchen keinen Server mehr

Bis Mitte August löste jede Änderung an dieser Seite denselben schweren Ablauf
aus, egal ob Programmcode oder ein Tippfehler in einer Termin-Ankündigung: neuen
Commit anpinnen, komplette System-Closure bauen, aktivieren. Für einen
korrigierten Satz war das offensichtlich zu viel.

Seit dem 16. August liegen die Inhalte deshalb in einem eigenen Repository,
getrennt vom Anwendungscode. Eine Textänderung ist damit ein Commit und sonst
nichts. Danach läuft es von selbst: eine Prüfung sieht sich die Inhalte an, bei
grünem Ergebnis wird der Branch `live` vorgezogen, ein Webhook stößt den
Abgleich auf dem Server an. Gemessen dauert es vom Commit bis zur Seite unter
einer Minute, ohne Build und ohne Neustart.

Zwei Dinge daran waren die eigentliche Arbeit. Erstens musste die Anwendung
aufhören, in ihren eigenen Inhaltsordner zu schreiben, denn der ist jetzt ein
Git-Checkout, in den der Abgleich hineinschreibt. Der Platzhalter für einen
Termin ohne eigene Datei entsteht seitdem beim Rendern und nicht mehr als Datei.
Zweitens folgt der Server ausschließlich `live` und nie `main`: ein Commit, der
die Prüfung nicht besteht, erreicht die Seite gar nicht erst, und etwas
zurücknehmen heißt, `live` zurückzusetzen, ohne Server-Zugriff.

Der angenehme Nebeneffekt: Inhalte pflegen und Code schreiben sind jetzt zwei
verschiedene Tätigkeiten, und für die erste braucht niemand mehr Kenntnis der
Servertechnik. Wer mag, findet beides offen:
[Inhalte](https://github.com/Daniel-Steinberger/pycologne-content) und
[Anwendung](https://github.com/Daniel-Steinberger/pycologne-app).
