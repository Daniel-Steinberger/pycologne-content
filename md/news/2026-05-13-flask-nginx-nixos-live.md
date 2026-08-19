# Flask, nginx und NixOS live beim Treffen

Beim Maitreffen haben wir nicht über Deployment geredet, sondern eines gebaut,
live und mit offenem Ausgang: eine Flask-App unter NixOS in einen
nginx-Webserver einhängen, mit Passwortschutz, unter Zuhilfenahme eines
KI-Assistenten.

Interessant war weniger das Ergebnis als der Weg dorthin. NixOS beschreibt
seinen Zustand deklarativ, und genau daran scheiterte die Maschine zuerst: sie
schrieb nginx-Konfigurationssyntax mitten in die Nix-Datei, wo sie nichts zu
suchen hat. Zwei Welten, die ähnlich aussehen und sich nicht mischen lassen.
Danach lief die App, mit `uv` für die Abhängigkeiten und Gunicorn dahinter.

Drumherum ging es um genau die Fragen, die einem bei NixOS zuerst begegnen: was
passiert bei einem Update mit selbstgeschriebenen Rollen, wann braucht man
trotz Deklarativität ein imperatives Kochrezept, und warum die Hash-basierten
Pakete im `/nix/store` beim Verteilen auf viele Knoten so praktisch sind.

Reizvoll im Rückblick: die Seite, auf der Du das hier liest, läuft heute genau
in dieser Konstellation, Flask und Gunicorn hinter nginx auf einer
NixOS-Maschine. Das ganze Protokoll steht unter
[Treffen vom 13. Mai 2026](/events/2026-05-13).
