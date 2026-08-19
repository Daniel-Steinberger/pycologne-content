# Code hinter der Kachel

Auf einer Seite, die von einer Programmier-Gruppe betrieben wird, sollte man den
Code sehen können, der sie erzeugt. Seit dem 17. August tragen vier Kacheln
deshalb einen kleinen `</>`-Griff. Ein Klick dreht die Kachel um, und auf der
Rückseite steht der Quelltext der Funktion, die den Inhalt der Vorderseite
gerade berechnet hat.

Vier Stellen haben echte Funktionen dahinter und deshalb einen Griff bekommen:
das nächste Treffen, das aus einer Terminregel entsteht, das Zen-Zitat, das bei
jedem Aufruf neu gelost wird, die [Suche](/suche), deren Rückseite die gerade
laufende Anfrage als FTS5-Ausdruck zeigt, und das Kalender-Abo mit der Funktion,
die iCalendar-Zeilen auf 75 Oktette faltet. Der Hero und die Aufzählung "Was wir
bieten" bleiben bewusst ohne, dort läuft kein Code.

Wichtig war uns, dass die Rückseite nicht lügt. Der Quelltext wird zur Laufzeit
per `inspect` aus dem laufenden Modul gelesen, nicht ins Template kopiert. Ändert
sich die Funktion, ändert sich die Anzeige. Dazu gehört eine REPL-Zeile am
unteren Rand, die den Aufruf und dessen tatsächliches Ergebnis von gerade eben
zeigt, im selben Zustand wie die Vorderseite.

Das ist übrigens das erste JavaScript auf dieser Seite, und es bleibt optional.
Ohne JavaScript ist der Griff schlicht ein Link auf die entsprechende Zeile im
[Quellcode bei GitHub](https://github.com/Daniel-Steinberger/pycologne-app),
mit Zeilenanker. Die Optik der Rückseiten ist ein Terminal in Phosphorgrün, was
kein Zufall ist, sondern der Versuch, den Wechsel von der Oberfläche zum Code
auch sichtbar zu machen.
