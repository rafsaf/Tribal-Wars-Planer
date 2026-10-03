---
title: "6. Zerstörung"
date: 2026-02-28
---

Diese Registerkarte enthält mehrere Einstellungen im Zusammenhang mit Zerstörungsaktionen.

Aussehen der Registerkarte:

![alt text](image-8.png){ width="600" }

In Option **1.** wird die Reihenfolge der zu zerstörenden Gebäude festgelegt. Der Planer plant Angriffe auf sie in der angegebenen Reihenfolge und ignoriert übersprungene Gebäude.

Unter **2.** legen wir die Mindestanzahl an Katapulten fest, die ein Dorf haben muss, um für einen Ruin-Angriff zu qualifizieren. Es gibt kein separates Feld für eine maximale Katapultzahl mehr. Der Planer folgt der exakten Ruin-Tabelle für den ausgewählten Dorftyp, sodass nur genau so viele Katapulte gesendet werden, wie für den nächsten exakten Schritt nötig sind oder zum Zerstören des Gebäudes auf Stufe 0, wenn mehr Katapulte verfügbar sind als in der Tabelle enthalten sind.

In **3.** wählen wir die Anzahl der Off-Einheiten für Ruin-Angriffe, die zusammen mit den Katapulten gesendet werden sollen.

Die Gebäudelevel werden anhand der Punkte des Quellendorfes bestimmt. Dörfer mit mehr als 8.000 Punkten verwenden die Ruin-Progression für große Dörfer, während Dörfer mit 8.000 Punkten oder weniger die Progression für mittlere Dörfer verwenden. Der genaue verbleibende Level nach jedem Ruin-Schritt kommt aus den eingebauten Ruin-Tabellen, und der Planer prüft diesen Wert nach jedem Treffer, um den nächsten richtigen Schritt zu wählen. Wenn mehr Katapulte verfügbar sind als die Tabelle benötigt, setzt er das Zerstören bis zum Level 0 fort, falls nötig.
