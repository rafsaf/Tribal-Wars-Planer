# Formularbeispiel

> Die meisten Dinge werden in der **Info**-Dokumentation erklärt. Wenn Sie Probleme beim Eingeben von Zielen haben, finden Sie unten eine Handvoll Beispiele für Standard- und erweiterte Off- und Adels-Kodierungen.

## Beispiele

### Beispiel 1 (Reine Koordinaten)

```text
500|499
500|498
```

**Was entspricht:**

```text
500|499 - Ziel: 0 Offs und 0 Adlige
500|498 - Ziel: 0 Offs und 0 Adlige
```

### Beispiel 2 (Definierte Anzahl von Offs und Adligen)

```text
500|499:10:2
500|498:12:4
```

**Was entspricht:**

```text
500|499 - Ziel: 10 Offs und 2 Adlige
500|498 - Ziel: 12 Offs und 4 Adlige
```

### Beispiel 3 (Genau definierte Anzahl von Offs und Adligen)

```text
500|499:5|0|2|3:2
500|498:0|2|2|8:4
500|497
500|495
500|444
```

**Was entspricht:**

```text
500|499 - Ziel: OFFS: 5 aus der Nähe (Front), 0 aus der Nähe (Hinterland), 2 zufällig aus dem Hinterland und 3 von weitem
500|499 - Ziel: ADLIGE: 2

500|498 - Ziel: OFFS: 0 aus der Nähe (Front), 2 aus der Nähe (Hinterland), 2 zufällig aus dem Hinterland und 8 von weitem
500|498 - Ziel: ADLIGE: 4

500|497 - Ziel (es wurde erwähnt, aber es ist erwähnenswert, dass Sie bestimmte Ziele frei mischen können, sogar mit leeren)
500|495 - Ziel
500|444 - Ziel
```

### Beispiel 4 (Genau definierte Anzahl von Offs und Adligen wie zuvor)

```text
500|499:5|0|2|3:5|0|2|3
500|498:0|2|2|8:5|0|2|3
500|497
500|495
500|444
```

**Was entspricht:**

```text
500|499 - Ziel: OFFS: 5 aus der Nähe (Front), 0 aus der Nähe (Hinterland), 2 zufällig aus dem Hinterland und 3 von weitem
500|499 - Ziel: ADLIGE: 5 aus der Nähe (Front), 0 aus der Nähe (Hinterland), 2 zufällig aus dem Hinterland und 3 von weitem

500|498 - Ziel: OFFS: 0 aus der Nähe (Front), 2 aus der Nähe (Hinterland), 2 zufällig aus dem Hinterland und 8 von weitem
500|498 - Ziel: ADLIGE: 5 aus der Nähe (Front), 0 aus der Nähe (Hinterland), 2 zufällig aus dem Hinterland und 3 von weitem
```
