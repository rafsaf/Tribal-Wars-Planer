---
title: "Zerstörungspläne - Anleitung"
date: 2026-02-28
---

In dieser Anleitung erfahren Sie, wie Sie Zerstörungsaktionen planen, die speziell auf die späteren Phasen der Welt abzielen. Hinweis: Dies setzt vollständige Kenntnisse von [Erste Schritte mit dem Planer](./../first_steps/index.md) voraus! Es wird auch empfohlen, zuerst die beiden kurzen vorherigen Anleitungen in diesem Abschnitt zu lesen, nämlich [Wie man Aktionsziele eingibt und speichert](./two_regions_of_the_tribe.md) und [Die zwei Regionen des Stammes, d.h. was ist die Front und das Hinterland](./two_regions_of_the_tribe.md).

!!! hint

    Beginnen Sie die Planung jeder Aktion auf dieser Seite immer damit, alle Truppen zu zählen und sie gemäß der Art des jeweiligen Plans in Front- und Hinterlandtruppen zu unterteilen. Verwenden Sie dazu die Registerkarte 1. Verfügbare Einheiten, und die Ergebnisse werden in einer Tabelle unter den Zielen dargestellt.

Die Aktion wird im Feld **Belagerungseinheiten** neben den Zielen erstellt. Die Einstellungen in Registerkarte {==6. Belagerungseinheiten==} bestimmen die Reihenfolge der zu zerstörenden Gebäude und die Mindestanzahl an Katapulten, die ein Dorf haben muss, um für Zerstörungsangriffe in Frage zu kommen. Der genaue Verlauf der Zerstörung kommt aus den eingebauten Ruin-Tabellen, sodass der Planer nach jedem Treffer prüft, wie viele Stufen noch verbleiben und nur genau so viele Katapulte sendet, wie für den nächsten exakten Schritt nötig sind.

Beispiel für Zerstörungsziele und Tabellenergebnisse mit 3 Off-Einheiten und *50 Belagerungseinheiten:

![alt text](image-24.png){ width="600" }

Beispiel für die Einstellungen einer Zerstörungsaktion, die auf 3 sichtbare Gebäude in dieser Reihenfolge abzielt:

![alt text](image-25.png){ width="600" }

Sie können die Anzahl der verfügbaren Belagerungseinheiten schätzen, indem Sie die Registerkarte {==1. Verfügbare Einheiten==} und einfache Mathematik verwenden. Nach jeder Aktualisierung finden Sie die Gesamtzahl der zur Planung bereiten Katapulte in der Tabelle unter **Anzahl aller verfügbaren Katapulte**. Sie müssen nur entscheiden, für wie viele Ziele sie ausreichen werden.

Beispiel für eine geplante Mini-Aktion mit verschiedenen Anzahlen von Katapulten von 200 bis 50:

![alt text](image-26.png){ width="600" }

## Exakte Katapultauswahl zur Zerstörung

Dörfer mit mehr verfügbaren Katapulten werden zuerst zugewiesen, aber der Planer verwendet keine separate Obergrenze für Katapulte. Stattdessen folgt er immer der exakten Zerstörungstabelle für den ausgewählten Dorftyp. Dieselbe Logik gilt für den ruin-off-Lauf und für den ruin-Angriffslauf, sodass der genaue verbleibende Gebäudestufenwert nach jedem Treffer mit der Tabelle abgeglichen wird und der Planer fortfährt, bis das Gebäude bei Bedarf auf Stufe 0 zerstört ist.

Das bedeutet, der Planer prüft nach jedem Treffer den genauen verbleibenden Gebäudewert und fährt mit dem nächsten richtigen Schritt in der Ruin-Tabelle fort. Wenn mehr Katapulte verfügbar sind als die Tabelle benötigt, wird das Gebäude auf 0 zerstört, falls dies erforderlich ist.

## Off-Einheiten vor Belagerungseinheiten

Off-Einheiten, die vor den Zerstörungsangriffen eingeplant werden, teilen denselben Schadensplan für Gebäude wie die späteren Ruin-Angriffe. Ihre Befehle bleiben normale OFFs, aber ihre Katapulte verbessern den Zustand des Zielgebäudes.

## Reihenfolge der Gebäudezerstörung

In den Einstellungen {==6. Zerstörung==} können wir die Reihenfolge der zu zerstörenden Gebäude ändern. Es ist wichtig zu bedenken, dass Gebäude, die nicht in dieser Liste enthalten sind, übersprungen werden und der Algorithmus in zwei Fällen stoppt: Entweder gibt es keine Katapulte mehr zu planen oder alle aufgelisteten Gebäude wurden bereits zerstört. Das bedeutet, dass selbst wenn wir uns entscheiden, `000|000:0:1000` zu schreiben, 1000 Belagerungseinheiten wahrscheinlich nicht geplant werden – sobald die aufgelisteten Gebäude zerstört sind, geht der Planer zu den nächsten Schritten über (z. B. zum nächsten Ziel usw.).

## Ich sehe 10.000 verfügbare Katapulte. Wie viele Ziele sind das?

Die Antwort lautet: Es kommt darauf an. Hauptsächlich auf die gewählte Gebäudereihenfolge. Nehmen wir an, es wird nur ein Gebäude gewählt, **[ Schmiede ]**. In diesem Fall reichen 200-250 Katapulte (zum Beispiel 200 und 50, oder 100, 100, oder 50, 50, 50, 50 usw.) aus, um ein Dorf zu zerstören, sodass Sie 40-50 Ziele planen können. Wenn zwei Gebäude gewählt werden, **[ Schmiede, Bauernhof ]**, benötigen Sie 200-250 Katapulte für die Schmiede und 500-700 Katapulte für den Bauernhof (zum Beispiel 14x 50 oder 5x 100, 4x 150, 3x 200 Katapulte oder viele andere Kombinationen), was 700-950 Katapulte pro Dorf oder 10-14 Ziele bedeutet. Unten finden Sie eine einfache Tabelle für 30-stufige Gebäude (wie Bauernhöfe, Speicher, alle Öko-Gebäude) und 20-stufige Gebäude (Hauptgebäude, Schmiede), um zu berechnen, wie viele Ziele möglich sind.

|                    | Anzahl der für die vollständige Zerstörung des Gebäudes erforderlichen Katapulte |
| ------------------ | -------------------------------------------------------------------------------- |
| 20-stufige Gebäude | 200-250                                                                          |
| 30-stufige Gebäude | 500-700                                                                          |

## Dorfgröße und Zerstörungstabelle

Die genaue Zerstörungstabelle wird anhand der Dorfpunkte ausgewählt. Dörfer mit mehr als 8.000 Punkten verwenden die Ruin-Progression für große Dörfer, während Dörfer mit 8.000 Punkten oder weniger die Progression für mittlere Dörfer verwenden. Mit anderen Worten: Ein Dorf wird nicht anhand eines redundanten Feldes für die maximale Katapultzahl bewertet; sein Punktwert sagt dem Planer, welche Tabelle verwendet werden muss.

## Zusammenfassung

Denken Sie daran, dass die Planung im Kern immer noch auf einem einfachen gierigen Algorithmus basiert, und der Planer **VERTEILT** Belagerungseinheiten, Fälschungen oder Off-Einheiten auf sehr ähnliche Weise. Wenn Sie möchten, dass Off-Einheiten oder Belagerungseinheiten nicht von Fälschungen zu unterscheiden sind, müssen Sie viele Fälschungen planen. Bei der Planung von Zerstörungen lohnt es sich, die Option **Fälschungen aus allen Dörfern** in {==Registerkarte 3. Standard-Aktionseinstellungen==} zu aktivieren, die im Gegensatz zur Standardeinstellung Fälschungen aus allen hinteren Dörfern zuweist.

Der wichtigste letzte Punkt ist, dass die Zerstörungsplanung nun den exakten Tabellenwerten folgt statt vereinfachten Heuristiken. Dadurch ist das Verhalten genauer und leichter vorhersehbar. Berücksichtigen Sie die Anzahl der Katapulte und die Gebäude, die es wert sind, zerstört zu werden, und planen Sie genügend Fälschungen. Viel Spaß beim Zerstören!

---

Lassen Sie mich wissen, wenn Sie weitere Details oder Änderungen benötigen!
