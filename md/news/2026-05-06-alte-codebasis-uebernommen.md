# Eine alte Codebasis wieder in Gang gebracht

Diese Seite ist kein Neubau. Ihr Quellcode reicht bis in den November 2013
zurück, lag aber jahrelang still. Im Mai 2026 haben wir ihn übernommen und
wieder lauffähig gemacht, statt von vorn anzufangen.

Der erste Tag bestand fast nur aus Aufräumen, und die Fundstücke erzählen die
Geschichte des Projekts von selbst: eine `.hgignore` als Rest aus der Zeit vor
Git, ein `tox.ini`, das niemand mehr brauchte, und eine Konfiguration, die noch
auf Bitbucket zeigte. Dazu der Umzug von Poetry auf
[uv](https://docs.astral.sh/uv/), eine `pyproject.toml` nach PEP 621 und ein
Makefile, das jetzt uv und [ruff](https://docs.astral.sh/ruff/) aufruft.

Am Code selbst haben wir dabei bewusst wenig angefasst. Das Interessante beim
Übernehmen fremder Software ist ohnehin nicht, was man wegwirft, sondern was
man behält: die Terminberechnung für den zweiten Mittwoch im Monat etwa läuft
in ihren Grundzügen noch so, wie sie einmal geschrieben wurde.

Der ganze Verlauf ist offen einzusehen, inklusive der Beiträge derjenigen, die
die Seite in den Jahren zuvor gebaut haben. Sie stehen alle noch in der
Historie: [pycologne-app auf
GitHub](https://github.com/Daniel-Steinberger/pycologne-app).
