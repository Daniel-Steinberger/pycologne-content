# info@pycologne.de kommt wieder an

Wer uns in den letzten Jahren an `info@pycologne.de` geschrieben hat, hat
niemanden erreicht. Nicht "wir haben es übersehen", sondern buchstäblich
niemanden: der Mailserver hinter der Domain hat jede Nachricht an diese Adresse
abgelehnt. Seit heute gibt es dahinter ein echtes Postfach, und die Adresse
steht wieder auf unserer [Kontaktseite](/contact).

Aufgefallen ist es beim Aufräumen unserer alten Kanäle. In unserem GitHub-Profil
und auf unserer Facebook-Seite stand `info@pycologne.de` als offizieller
Kontakt, also haben wir das Naheliegende getan und einmal selbst hingeschrieben.
Zurück kam kein Postfach, sondern eine Fehlermeldung:

```
554 5.7.1 <info@pycologne.de>: Relay access denied
```

Das ist die Antwort eines Mailservers, der für eine Domain zwar zuständig
gemeldet ist, für die angefragte Adresse aber kein Ziel kennt. Die MX-Einträge
der Domain zeigten auf Server, die niemand aus der heutigen Orga kennt und auf
die niemand von uns Zugriff hat, freundlich betreut von jemandem, der irgendwann
in der Vergangenheit einmal geholfen hat. Damit war die Adresse jahrelang eine
Attrappe. Wie viele Anfragen von Vortragswilligen, Sponsoren oder
Interessierten dort verpufft sind, wissen wir nicht und werden es auch nie
erfahren.

Der Weg heraus war der gleiche wie bei der Website: nicht mehr an einer
Einzelperson hängen, sondern an einer Organisation. Die Website läuft seit Mai beim
[Python Software Verband](https://python-verband.org/), der uns das Hosting
sponsort, und dort liegt jetzt auch die Mail. Betrieben wird sie von
[Flying Circus](https://flyingcircus.io/), gehostet in Deutschland, mit einem
Webmail-Zugang, damit sich von der Adresse auch antworten lässt und nicht bloß
weiterleiten.

Der interessante Teil steckt danach im Kleingedruckten. Eine Mail zu empfangen
ist einfach, eine Mail so zu versenden, dass die Gegenseite sie nicht für
Fälschung hält, ist es nicht. Drei Einträge im DNS regeln das:

- **SPF** sagt, welche Server im Namen der Domain senden dürfen.
- **DKIM** hängt jeder Mail eine Signatur an, die zu einem Schlüssel im DNS
  passen muss.
- **DMARC** sagt, was mit Mail passieren soll, die daran scheitert. Unser Eintrag
  steht auf `p=reject`, also: wegwerfen.

Das ist die scharfe Einstellung, und wer sie setzt, kann sich damit auch selbst
aussperren. Deshalb war die letzte Prüfung nicht "ist die Mail angekommen",
sondern ein Blick in die Kopfzeilen der angekommenen Mail:

```
dkim=pass  spf=pass  dmarc=pass
```

Diese drei Wörter kann man in jedem Mail-Programm selbst nachsehen, meist unter
"Original anzeigen" oder "Quelltext". Sie stehen in der Zeile
`Authentication-Results`, und sie sind das Urteil des empfangenden Servers
darüber, ob er die Absenderadresse glaubt. Bei uns steht dort jetzt dreimal
`pass`, auch für eine Nachricht, die über die Weiterleitung gelaufen ist.

Was noch fehlt: die weiteren Postfächer für die Orga, damit nicht wieder alles an
einer Person hängt. Genau dieser Fehler hat uns die Adresse gekostet.
