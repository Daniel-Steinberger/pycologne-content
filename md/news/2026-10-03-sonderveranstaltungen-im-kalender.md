# Große Abende jetzt auch im Kalender

PyCologne #6 am 19. November steht jetzt dort, wo man nach Terminen sucht: in
der [Terminvorschau](/events) und im [Kalender-Abo](/events.ics), mit der
richtigen Startzeit um 18 Uhr. Bisher kannte die Seite dort nur die
monatlichen Treffen am zweiten Mittwoch, alles andere fand man nur über einen
direkten Link.

Woran die Seite eine Sonderveranstaltung erkennt, kann man sich direkt
ansehen: Die Kachel "Die nächsten Termine" auf der [Terminseite](/events)
lässt sich über den Griff `</>` umdrehen. Dahinter steckt
[`upcoming_events()`](https://github.com/Daniel-Steinberger/pycologne-app/blob/1f184f0f4e5b5c5a038b60e8f9e5457845edb306/pycgnweb/webapp.py#L528),
und die letzte Zeile wertet live aus, welche Sonderveranstaltungen sie gerade
gefunden hat. Die Regel ist schlicht: Jede Termin-Datei, die auf keinen
regulären Mittwoch fällt, ist eine. Titel, Uhrzeit und Ort stehen ohnehin in
der Datei, ein zusätzliches Register braucht es nicht.

Wer den Kalender schon abonniert hat, muss nichts tun, der neue Termin taucht
beim nächsten Abgleich von selbst auf.
