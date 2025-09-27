# Die Stämme Planer Dokumentation

## Einführung

Dies ist die Dokumentation für die Webseite [plemiona-planer.pl](https://plemiona-planer.pl) – ein ehrgeiziges Projekt für [die-staemme.de](https://die-staemme.de), das im Januar 2020 nach dem Update des Spiels auf Version 8.192 im November 2019 gestartet wurde. Das Update führte die Möglichkeit für Stammes-Admins ein, Daten über Spieler und ihre Einheiten zu sammeln.

- [1. Testwelt](./first_steps/index.md) - ein Abschnitt, der dem Erkunden der Seite gewidmet ist, ohne dass etwas installiert werden muss oder sogar ein aktives Spielkonto erforderlich ist. Er ermöglicht die Planung von Aktionen in einer speziell vorbereiteten Testwelt.
- [2. Installation der notwendigen Skripte](./scripts/army_and_defence_collection.md) - für den Einsatz in der realen Welt und die Planung von Aktionen für einen tatsächlichen Stamm ist ein Skript erforderlich, um Daten vom Stamm zu sammeln (optional hilft ein zweites Skript beim Senden von Nachrichten an Spieler).
- [3. Anleitungen](./primary/write_outline_targets.md) - 6 erweiterte Artikel zu spezifischen Themen im Zusammenhang mit der Aktionsplanung.
- [4. Erweitert](./primary/write_outline_targets.md) - eine Beschreibung aller Registerkarten und Optionen in der Hauptregisterkarte "Planer".

## Fragen und Antworten

### Über die Seite

> Was ist diese Seite, und für wen ist sie und für wen nicht?

Diese Seite ist für **Stammes-Admins** und ihre Offensiv-Koordinatoren, die Zugriff auf Spielerdaten haben. Durch die Nutzung von Stammesdaten und die Eingabe von Aktionszielen sowie die Anpassung von Einstellungen kann ein Koordinator einen Aktionsplan erstellen und Ziele an Spieler senden (über einen Link zur Seite oder direkt in einer Spielnachricht). Die auf der Seite verwendete Mathematik und die vielen Optionen ermöglichen die Planung von praktisch jeder Aktion in jeder Phase des Spiels und sparen dem Planer Zeit.

> Was ist plemiona-planer NICHT?

Es ist KEIN illegales Tool, kein Spiel-Bot oder irgendein Skript, das Aktionen im Spiel automatisiert. Die Seite verbindet sich NICHT mit dem Spiel, außer um öffentlich verfügbare Weltdaten abzurufen. Sie werden NIEMALS nach Ihrem Spielpasswort gefragt!

### Zahlungen

> Ist plemiona-planer kostenpflichtig?

Die Seite ist kostenlos. Sie können jedoch ein Premium-Account-Abonnement erwerben, das die Planung von mehr als 40 Zielen in einem einzigen Plan ermöglicht und den Zugriff auf ungenutzte Daten aus zuvor geplanten Aktionen gewährt (zur Verwendung in zukünftigen Aktionen). Es gibt keine Unterschiede in der Funktionalität, der Qualität des Algorithmus oder der Geschwindigkeit. Dieses Modell hilft, den Dienst aufrechtzuerhalten, und die Gebühr kann unter den Stammesmitgliedern aufgeteilt werden. Es ist nicht mehr als ein Account pro Stamm erforderlich, außer in Fällen von **offensichtlichen!** Problemen mit der Account-Freigabe. Die Seite ist nicht verantwortlich für Verluste aufgrund von unbefugtem Zugriff, Account-Diebstahl oder der Weitergabe von Passwörtern an Gegner. Der Account-Inhaber sollte die Vor- und Nachteile abwägen, bevor er sein Passwort an Dritte weitergibt.

> Wie ist es möglich, dass der App-Code offen und auf GitHub verfügbar ist?
>
> Warum für ein Abonnement bezahlen, wenn man den Code kostenlos nutzen kann?

Ich bin ein Befürworter von [Open-Source-Software](https://opensource.com/resources/what-open-source)! Es ist wahr, Sie können sich entscheiden, nicht zu bezahlen und den Code der Seite sowie das Ergebnis jahrelanger Arbeit vieler engagierter Benutzer kostenlos zu nutzen. Und das wird auch so bleiben :) Es spiegelt auch mein Vertrauen in die Sicherheit und die im Planer verwendete Mathematik wider – es gibt nichts zu verbergen. Die Bequemlichkeit, von jedem Ort aus zu planen und Online-Zugriff auf die Planungsergebnisse für Stammesmitglieder zu haben, ist jedoch von unschätzbarem Wert. Das Einrichten eigener Server erfordert Fachwissen, erhebliche Kosten und laufende Wartung, Updates usw. Die Abonnementgebühr deckt auch die Zeit ab, die für die Behebung von Fehlern, die Unterstützung von Benutzern bei Problemen oder das Schreiben neuer Funktionen benötigt wird. All dies wäre ohne die Unterstützung der Benutzer nicht möglich. Vielen Dank an alle, die dieses Projekt unterstützen.

### Daten

> Sind meine Daten sicher?

Die Seite ist seit Mitte 2020 online. In dieser Zeit gab es keinen Sicherheitsvorfall. Das aktuelle Geschäftsmodell trägt die Server. Die von den Benutzern übermittelten Daten liegen in ihrer Verantwortung und werden niemals an Dritte verkauft oder weitergegeben.

> Kann ich in Ihrem Planer Pläne erstellen, ohne Zugriff auf Stammesdaten zu haben?

Nein, die Bereitstellung von Daten ist erforderlich. Sie müssen in der Stammesverwaltung sein, und deren Mitglieder müssen die entsprechenden Einstellungen aktivieren, um Daten zu teilen. Es gibt eine Testwelt, in der Sie die Seite ohne Zugriff auf Stammesdaten ausprobieren können.

### Angriffsplan

> Hallo, warum plant der Planer nicht alle meine Offensiv-Einheiten ein? Ich glaube, ich habe alles in den Einstellungen geändert, aber er lässt immer 2.7k Offensiv-Truppen ungenutzt…

Dafür kann es viele Gründe geben, hauptsächlich die Aktionseinstellungen in der Registerkarte [1. Verfügbare Truppen und Tabellenbeschreibung](./advanced/1_available_troops_and_table.md), wie das Überspringen einiger Frontdörfer oder entfernter Dörfer am Rand. Seltener liegt es an den [3. Plan-Parametern](./advanced/3_outline_parameters.md). Der Planer prüft nicht vollständig auf undurchdachte Parameter und **erlaubt Fehler**. Wenn beispielsweise die Fronteinstellungen angeben, dass der gesamte Stamm an der Front ist, der Benutzer aber Offensiv-Einheiten nur aus der zweiten Reihe einstellt, wird die App eine solche Aktion planen, obwohl keine Offensiv-Einheit berücksichtigt wird.

### Nachtbonus

> Wie funktioniert der Algorithmus, um nächtliche Angriffe so weit wie möglich zu vermeiden?

Der Bereich der natürlichen Zahlen 0-23, wobei 0-7 die schlechteste Bewertung = 1 haben, die Ränder des Bereichs die Bewertung = 2 und vollständig "sichere" Stunden die Bewertung = 3, alles verpackt in Modulo 24. [Code hier](https://github.com/rafsaf/Tribal-Wars-Planer/blob/708b2677a3ee64d2fb8fc50eb8d7601811260dff/utils/write_ram_target.py#L297).

Dies muss für jedes Ziel einzeln durch alle verbündeten Dörfer erfolgen, wobei zuerst die Entfernung in Feldern berechnet wird.

### Skripte

> Hallo, ich verstehe nicht ganz, wie das Skript zum Senden von Zielen funktioniert. Nach der Installation in der Symbolleiste passiert nichts in der Stammesoberfläche.

Siehe [Skript zum Senden von Nachrichten](./scripts/sending_messages.md). Es ist ein **Browser-Skript**, nicht für die In-Game-Symbolleiste. Es wird in der neuen Nachrichtenansicht verwendet, wenn speziell hinzugefügte Parameter in der URL vorhanden sind. [Siehe Punkt 11 in der Ergebnis-Registerkarte](./first_steps/step_7_results_tab.md).

### Rechtliches & Lizenz

> Kann ich den plemiona-planer-Code von GitHub verwenden?

Ja! Sie können alles im Rahmen der **Apache License 2.0** tun – den Planer lokal einrichten, Forks verwenden und diese selbst bereitstellen. Sie können den aus dem GitHub-Repo kopierten Code für Ihre Tools verwenden (unter der Apache License 2.0, was bedeutet, OHNE den Lizenz-Header zu entfernen). Ich stimme NICHT der Nachahmung der Marke plemiona-planer.pl, der Verwendung des rafsaf.pl-Logos oder meines Namens in der Datenschutzrichtlinie in Produkten oder Projekten zu, die auf plemiona-planer.pl basieren.
