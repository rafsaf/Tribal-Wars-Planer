# Armee- und Verteidigungssammelskript

| Server         | Die Stämme Forum                                                                                                                                                                 | Erlaubt | Code                                                                                                                  |
| -------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------- | --------------------------------------------------------------------------------------------------------------------- |
| die-staemme.de | [https://forum.die-staemme.de/index.php?threads/truppen-und-deff-sammeln-skript.197153/](https://forum.die-staemme.de/index.php?threads/truppen-und-deff-sammeln-skript.197153/) | JA      | [Code auf GitHub (v2.1)](https://github.com/rafsaf/scripts_tribal_wars/blob/2024-09-09-2/src/collect_troops_v2.1.ts)  |
| plemiona.pl    | [https://forum.plemiona.pl/index.php?threads/zbi%C3%B3rka-wojska-i-obrony.128630/](https://forum.plemiona.pl/index.php?threads/zbi%C3%B3rka-wojska-i-obrony.128630/)             | JA      | [Code auf GitHub (v2)](https://github.com/rafsaf/scripts_tribal_wars/blob/2024-09-01/public/collect_troops_v2.js)     |
| andere Server  | -                                                                                                                                                                                | NEIN    | [Code auf GitHub (v2.3)](https://github.com/rafsaf/scripts_tribal_wars/blob/2025-09-22/public/collect_troops_v2.3.js) |

!!! warning

    Die Verwendung auf anderen Sprachversionen des Spiels, **wo das Skript nicht erlaubt ist**, kann zur Sperrung des Kontos führen. Benutzung auf eigene Gefahr.

=== "die-staemme.de"

    ```title="Armee- und Verteidigungssammelskript"
    --8<-- "army_script_tribalwars_net_en.txt"
    ```

=== "plemiona.pl"

    ```title="Armee- und Verteidigungssammelskript"
    --8<-- "army_script_plemiona_pl_en.txt"
    ```

=== "andere Server"

    ```title="Armee- und Verteidigungssammelskript"
    --8<-- "army_script_latest.txt"
    ```

## Installation

Die Installation erfolgt identisch wie bei allen Skripten für die Leiste; Sie müssen den Inhalt in ein neu erstelltes Skript für die Leiste im Spiel einfügen.

## Gebrauchsanweisung

1. Erstellen Sie ein Skript für die Leiste, klicken Sie darauf
2. Warten Sie auf das Ergebnis
3. Gehen Sie zum ausgewählten Zeitplan
4. Fügen Sie die Daten ein und bestätigen Sie

![Beispielausgabe des Skripts](image-2.png)

## Beschreibung

Nach dem Klicken erscheint ein "Zähler" mit Fortschritt in der Mitte des Bildschirms, dann das Ergebnis in einem Fenster. Es funktioniert sowohl in den Registerkarten Armee als auch Verteidigung. Die Standardeinstellungen für das Kopieren haben Cache auf true und cacheTime auf 5 Minuten gesetzt. Während dieser Zeit gibt das Skript das im Browser gespeicherte Ergebnis aus, anstatt alle Mitglieder erneut zu durchlaufen und Daten neu zu sammeln. Im Zweifelsfall, ob es sich um ein neues oder altes Ergebnis handelt, erscheint das Sammeldatum unten.

Die durch Ausführen des Skripts generierten Daten sollten in den Zeitplan auf der Website eingefügt werden.

Optionen:

Die Konfiguration erfolgt über das Objekt **COLLECT_TROOPS_DATA_V2**. Beachten Sie, dass jeder Parameter OPTIONAL ist. Wenn beide Variablen
undefiniert sind oder definiert sind, aber keine Schlüssel enthalten, werden sinnvolle
Standardwerte verwendet.

- **cache**: `<boolean>` (Standard: `true`) ist für das Speichern des Ergebnisses
  im Browser verantwortlich, um nicht versehentlich mehrmals hintereinander zu klicken und
  die Spieleserver zu belasten. Das Setzen von cache: false bewirkt, dass das Ergebnis nicht gespeichert wird
  (z.B. wenn wir beabsichtigen, Daten von zwei Stämmen zu sammeln und sofort
  zum anderen zu springen). Beachten Sie, dass bei einer riesigen Anzahl von Dörfern im Stamm
  der Speicherplatz im localStorage (~max 5MB) überschritten werden kann. Aus diesem Grund beträgt das Limit 1MB.
  Wenn die Ausgabe > 1MB ist, wird das Speichern im localStorage übersprungen.

- **cacheTime**: `<number>` (Standard: `5`) ist die Zeit, für die das Ergebnis im
  Browser gespeichert wird, in Minuten.

- **removedPlayers**: `<string>` (Standard: `""`) hier geben wir die Spitznamen der Spieler ein,
  von denen wir keine Truppeninformationen sammeln möchten, getrennt durch Semikolons wie in
  den Nachrichten im Spiel, z.B. "Rafsaf;kmic;someoneelse"

- **allowedPlayers**: `<string>` (Standard: `""`) hier geben wir die Spitznamen der Spieler ein,
  von denen NUR! (wenn es leer ist, werden alle Spieler im Stamm verwendet) wir
  Truppeninformationen sammeln möchten, getrennt durch Semikolons wie in den Nachrichten im Spiel,
  z.B. "Rafsaf;kmic;someoneelse"

- **language**: `<string>` (Standard: `"pl"`) dies sollte `"en"` oder `"pl"` sein, wenn etwas
  anderes verwendet wird, verwendet das Skript Englisch

- **showNicknamesTroops**: `<boolean>` (Standard: `false`) wenn auf true gesetzt, erscheint
  am Anfang jeder Zeile zusätzlich der Spitzname des Spielers,
  gilt nur in der Registerkarte Truppen, ähnlich wie showNicknamesDeff

- **showFirstLineTroops**: `<boolean>` (Standard: `false`) wenn auf true gesetzt, wird
  am Ergebnis eine zusätzliche Zeile oben hinzugefügt, die durch die
  Variable firstLineDeff angegeben wird, gilt nur in der Registerkarte Truppen, ähnlich wie showFirstLineDeff

- **firstLineTroops**: `<string>` (Standard: `""`) Zeile, die oben im Ergebnis angezeigt wird,
  wenn showFirstLineTroops auf true gesetzt ist, gilt nur in der Registerkarte Truppen, ähnlich wie
  showNicknamesDeff

- **showNicknamesDeff**: `<boolean>` (Standard: `false`) wenn auf true gesetzt, erscheint
  am Anfang jeder Zeile zusätzlich der Spitzname des Spielers,
  gilt nur in der Registerkarte Verteidigung, ähnlich wie showNicknamesTroops

- **showFirstLineDeff**: `<boolean>` (Standard: `false`) wenn auf true gesetzt, wird
  am Ergebnis eine zusätzliche Zeile oben hinzugefügt, die durch die
  Variable firstLineDeff angegeben wird, gilt nur in der Registerkarte Verteidigung, ähnlich wie showFirstLineTroops

- **firstLineDeff**: `<string>` (Standard: `""`) Zeile, die oben im Ergebnis angezeigt wird,
  wenn showFirstLineTroops auf true gesetzt ist, gilt nur in der Registerkarte Verteidigung, ähnlich
  wie firstLineTroops
