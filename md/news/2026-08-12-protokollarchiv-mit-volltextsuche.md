# 78 Protokolle von 2013 bis 2020 sind zurück, mit Volltextsuche

Sieben Jahre PyCologne stehen wieder im Netz: 78 Protokolle der Treffen von
August 2013 bis Mai 2020, nach Jahrgang gruppiert unter
[Termine](/events), und durchsuchbar unter [Suche](/suche). Wer wissen will,
wann wir das erste Mal über MicroPython gesprochen haben oder wie oft pandas
vorkam, findet es dort in einem Suchfeld.

Dass es diese Texte noch gibt, ist knapper als es aussieht. Geschrieben wurden
sie gemeinsam während der Treffen in einem Etherpad, damals unter
`yourpart.eu`. Diese Adresse leitet heute weiter, der Export-Endpunkt antwortet
nur noch mit 404, und die Pads selbst sind nicht mehr abrufbar. Auch die
[Wayback Machine](https://web.archive.org/) hat sie nie archiviert. Die
Exporte, die 2020 mit eigenen Skripten gezogen wurden, sind damit die einzige
bekannte Kopie dieser sieben Jahre.

Von 81 Pads tragen 78 ein echtes Protokoll, drei enthielten nur Notizen ohne
Inhalt. Jeder Export lag doppelt vor, und alle Paare wurden per SHA-256 als
byte-identisch geprüft, bevor daraus die veröffentlichten Fassungen entstanden.
Anwesenheitslisten haben wir beim Redigieren entfernt, Zählungen wie "ca. 20
Personen" sind geblieben. Und weil eine Kopie auf einem einzelnen Rechner
keine Sicherheit ist, liegen die Dateien jetzt in Git.

Technisch steckt hinter der Suche kein Suchserver, sondern
[SQLite mit FTS5](https://www.sqlite.org/fts5.html). Der Index entsteht beim
ersten Suchaufruf im Speicher und baut sich neu, sobald sich an den Dateien
etwas ändert. Bei rund hundert Protokollen dauert das wenige Millisekunden,
deshalb braucht es dafür keine Datei auf der Platte und keinen Schritt beim
Deployment.
