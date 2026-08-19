# Website und Meetup zeigen jetzt aufeinander

Wer einen Termin bei [Meetup](https://www.meetup.com/pycologne/) findet, soll
das ausführliche Programm hier lesen können, und wer hier landet, soll sich
dort anmelden können, ohne zu suchen. Seit dem 16. August verlinken beide
Seiten deshalb direkt aufeinander, und zwar auf das jeweilige einzelne Event
statt auf die Startseite der Gruppe.

Damit die Verknüpfung nicht bei jedem Termin von Hand hergestellt werden muss,
pflegt unser Kommandozeilenwerkzeug für Meetup die Zeile mit der Website-Adresse
jetzt bei jedem Aufruf selbst mit. Die Zuordnung entsteht also beiläufig beim
normalen Bearbeiten der Beschreibung und ist danach dauerhaft da.

Beim Bauen kam eine Einschränkung heraus, die für andere Gruppen nützlich sein
dürfte: **Meetup verweigert jede Änderung an einem Event, das bereits
vorbei ist.** Die Beschreibung eines vergangenen Termins lässt sich über die
Schnittstelle nicht mehr anfassen, unabhängig von den eigenen Rechten. Wir haben
das gegen alle vier vergangenen Termine geprüft, es ist keine Rechte-, sondern
eine Zustandsfrage.

Der Ausweg ist unspektakulär und funktioniert: bei vergangenen Terminen landet
der Link als öffentlicher Kommentar unter dem Event statt in der Beschreibung.
Damit sind auch die Treffen von Mai bis August rückwirkend verbunden. Die
Termine mit Programm stehen wie immer unter [Termine](/events).
