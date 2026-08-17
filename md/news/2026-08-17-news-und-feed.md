# Neu: News und ein Feed zum Abonnieren

Diese Seite konnte bisher nur Termine bekanntgeben. Für alles daneben gab es
keinen Ort, und daran hakte es regelmäßig: Neuigkeiten aus der Gruppe standen
dann in einem Chat, in dem sie ein halbes Jahr später niemand mehr findet.

Ab jetzt gibt es dafür diesen Bereich. Wer mitlesen möchte, ohne hier
vorbeizuschauen, kann den [Atom-Feed](/news.atom) abonnieren, in Thunderbird
oder einem Reader nach Wahl. Die Termine gibt es übrigens schon länger als
[Kalender-Abo](/events.ics), das ließ sich bisher nur schlecht finden.

Technisch ist es bewusst schlicht geblieben, passend zum Rest der Seite: ein
News-Eintrag ist eine Markdown-Datei im
[Content-Repository](https://github.com/Daniel-Steinberger/pycologne-content),
das Datum steht im Dateinamen, und veröffentlichen heißt committen. Es wird
dafür nichts gebaut und nichts neu gestartet, keine Minute nach dem Commit
steht der Eintrag hier. Der Feed selbst entsteht ohne zusätzliche Bibliothek
aus ein paar Zeilen Python, nachzulesen wie alles andere im
[Quellcode](https://github.com/Daniel-Steinberger/pycologne-app).

Was hier künftig stehen wird: Neues zu unseren Kanälen, Fundstücke aus der
Python-Welt, Rückblicke, die über ein Protokoll hinausgehen. Wer etwas
beizutragen hat, kann es als Pull Request schicken oder uns beim nächsten
[Treffen](/events) ansprechen.
