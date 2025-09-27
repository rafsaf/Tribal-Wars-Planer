# Schritt 7 - Ergebnis-Registerkarte

<figure markdown="span">
  ![alt text](image-11.png)
  <figcaption>Ergebnis-Registerkarte.</figcaption>
</figure>

| Nummer | Beschreibung                                                                                                              |
| ------ | ------------------------------------------------------------------------------------------------------------------------- |
| 1      | Tabelle mit Links zu Spielerzielen und Links zum Senden sowie ein Formular zum Ändern des Inhalts gesendeter Nachrichten  |
| 2      | Kurze Textzusammenfassung von Spitznamen und Zielen                                                                       |
| 3      | Textfeld mit Links, die manuell an Spieler gesendet werden können                                                         |
| 4      | Planergebnisse als vollständiger Text zum Senden (alle Spieler)                                                           |
| 5      | Ungenutzte Truppen für den nächsten Plan (PREMIUM)                                                                        |
| 6      | Ergebnisse der Verteidigungssammlung aus der Registerkarte VERTEIDIGUNGSSAMMLUNG                                          |
| 7      | Formular für den Inhalt der gesendeten Nachricht und zum Ausblenden von Befehlen anderer Spieler                          |
| 8      | Tabelle mit alten Links, die für diesen Plan verfügbar sind                                                               |
| 9      | Dieser Link führt Sie zu einer einzigartigen Seite mit den Zielen des Spielers                                            |
| 10     | Manuelle Option zum Ändern der Sichtbarkeit der Befehle anderer Spieler                                                   |
| 11     | Link zum Senden einer Nachricht im Spiel, erfordert [Skript zum Senden von Nachrichten](./../scripts/sending_messages.md) |


!!! info

    Für jeden Spieler wurde eine {==EINZIGARTIGE URL==} erstellt, auf der nur seine Ziele zusammen mit dem Text zum Einfügen in Notizen und einer grafischen Darstellung seiner Befehle präsentiert werden. Sie können darauf zugreifen, indem Sie auf die Schaltfläche 9 im obigen Bild klicken. Nach Eingabe seines Links hat der Spieler alles, was er zum Senden der im Plan geplanten Truppen benötigt.


Durch Erweitern von {==Titel, Text festlegen und versteckten Wert anzeigen==}, was Nummer 7 ist, geben Sie den Inhalt der an die Spieler gesendeten Nachricht an und ob die Spieler die Befehle anderer Spieler in den Details ihrer einzelnen Ziele sehen sollen. Standardmäßig bedeutet "Versteckt anzeigen - Falsch", dass sie nur ihre eigenen Befehle und die Befehle anderer nur dann sehen, wenn sie dieses Dorf mit Adelsgeschlechtern aus der Nähe angreifen. Die Einstellung "Versteckt anzeigen - Wahr" ermöglicht es den Spielern, alle Befehle anderer zu sehen. Unter Nummer 8 finden Sie eine Tabelle mit allen erstellten Links; nach jeder Planbestätigung werden neue erstellt, während die alten in diese Registerkarte verschoben werden (sie bleiben jedoch aktiv!).

Hinweis! Im Laufe der Zeit und mit der Entwicklung der Anwendung wurden entfernbare Links in nicht entfernbare Links geändert (und werden es auch bleiben), die der Benutzer nicht ändern oder den Zugriff darauf blockieren kann, z.B. nach dem Senden an die falsche Person. Diese Konvention stellt sicher, dass der Planer nicht versehentlich bereits gesendete Links löscht, was zu großen Missverständnissen führen würde. Links sind 30 Tage lang aktiv, unabhängig davon, ob der Plan noch existiert oder gelöscht wurde.
