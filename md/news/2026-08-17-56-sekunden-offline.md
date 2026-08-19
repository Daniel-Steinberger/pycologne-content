# Wie wir die Seite für 56 Sekunden abgeschossen haben

In der Nacht zum 17. August war diese Seite 56 Sekunden lang nicht erreichbar.
Jede Anfrage bekam einen Fehler, von 23:57:37 bis 23:58:33, dann war sie per
Rollback zurück. Die Geschichte dahinter ist zu lehrreich, um sie zu
verschweigen, denn der Fehlschlag hat einen älteren Fehler aufgedeckt, den wir
sonst nicht gefunden hätten.

Angefangen hat es harmlos. Im Protokoll standen seit Tagen Serverfehler, alle
ausgelöst von Scannern mit absichtlich kaputten Host-Headern, etwa einer offenen
eckigen Klammer. Unsere Fehlerseite setzte mit `request.url` die vollständige
angefragte Adresse in ihren Text, und dafür braucht Flask den Host-Header: bei
einem kaputten warf die Bibliothek darunter einen `ValueError`, und aus einem
harmlosen 404 wurde ein 500.

Der Fix ist eine einzige Zeile, `request.path` statt `request.url`, denn für den
Text der Fehlerseite genügt der Pfad. Nachlesen kann man das im
[Commit dazu](https://github.com/Daniel-Steinberger/pycologne-app/commit/32214e7c4520414d5ac30a7d065dfcebc9ccf11b),
der auch gleich den Test mitbringt, der so einen Header nachstellt. Denn ein
Fehler, den man behebt, ohne ihn festzuhalten, kommt wieder.

Damit solche Anfragen künftig gleich am Eingang abgewiesen werden, haben wir
danach eine Liste erlaubter Hostnamen aktiviert. Und da fiel die Seite um. Alle
Anfragen wurden abgelehnt, auch die legitimen, weil der Host, der ankam, nicht
der war, den wir erwarteten.

Der Grund war ein Fehler, der von der ersten Fassung unserer Serverkonfiguration
an bestanden hatte: wir setzten Weiterleitungs-Header, die die Plattform ohnehin
schon setzt. nginx schickte den Hostnamen deshalb **zweimal**, und was in der
Anwendung ankam, war beides aneinandergehängt.

Solange niemand hinsah, war das unauffällig, denn im Alltag baut die Seite ihre
Adressen relativ. Nur eine Stelle brauchte den Host wirklich und hat es die
ganze Zeit sichtbar verraten: unser Kalender-Feed. Der setzt die Adresse jedes
Termins mit
[`url_for(..., _external=True)`](https://github.com/Daniel-Steinberger/pycologne-app/blob/cd7f4382032d61a33d16d8c58a100f3f30307971/pycgnweb/webapp.py#L1040),
also aus genau dem Host, der angekommen ist. Heraus kam eine Adresse mit einem
Komma und dem doppelten Hostnamen mitten darin. Wer den Kalender abonniert
hatte, konnte den Link zum Termin nicht anklicken.

Die überflüssigen Zeilen sind weg, die Liste erlaubter Hosts ist aktiv, und die
Adressen im [Kalender-Abo](/events.ics) sind erstmals korrekt. Bleibt die
unangenehme Erkenntnis: der doppelte Header hat monatelang niemandem
wehgetan, außer den Leuten, die unseren Kalender abonniert hatten, und gefunden
haben wir ihn nur, weil ein anderer Versuch spektakulär gescheitert ist.
