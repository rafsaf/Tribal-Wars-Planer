# Akcja burząca - poradnik

W tym poradniku zobaczysz jak rozpisywać akcje burzące, docelowo w późniejszym etapie świata. Uwaga, zakładana jest już cała wiedza z [Pierwszych kroków z planerem](./../first_steps/index.md)! oraz zalecane przeczytanie najpierw dwóch krótkich poprzednich poradników w tym dziale, czyli [Jak wpisywać i zapisać cele akcji](./two_regions_of_the_tribe.md) i [Dwa rejony plemienia czyli co to front i zaplecze](./two_regions_of_the_tribe.md).

!!! hint

    Zawsze rozpoczynaj rozpisywanie dowolnej akcji na tej stronie od policzenia wszystkich offów i podzieleniu ich na Frontowe i Zapleczowe zgodnie z duchem danej rozpiski. Do tego celu służy zakładka 1. Dostępne jednostki, zaś wyniki prezentowane są w tabeli pod celami.


Akcja będzie całkowicie tworzona w polu **Burzaki** obok Celów. Ustawienia w zakładce {==6. Burzaki==} są bardzo proste, ustalamy tam przede wszystkim kolejność burzonych budynków oraz max ilość katapult w atakach burzących (minimalna to 50).

Przykład celów burzących i wyników tabeli, po 3 offy i *50 burzaków:

![alt text](image-24.png){ width="600" }

Przykład ustawień akcji burzącej, celujemy w 3 widoczne budynki w tej kolejności:

![alt text](image-25.png){ width="600" }

(Uwaga, 50 burzaków nie oznacza że tyle koniecznie zostanie rozpisane!)

Szacunkową liczbę dostępnych burzaków możesz uzyskać korzystając z poznanej zakładki {==1. Dostępne jednostki==} przy użyciu prostej matematyki. Po każdym odświeżeniu, w tabeli pod nazwą **Liczba wszystkich dostępnych katapult** znaleźć można całkowitą liczbę katapult gotowych do rozpisania, wystarczy zdecydować na ile celów tyle "wystarczy".

Przykład rozpisanej mini akcji, różne ilości katapult od 200 do 50:

![alt text](image-26.png){ width="600" }

## Optymalny wybów katapult do burzenia

Zwróćmy uwagę jak dla MAX katapult ustawionych na 200, zachowuje się Planer. Jeśli są tego typu wioski z taką ilością, zostaną one wzięte w pierwszej kolejności (powyżej 100 katapult), natomiast gdy się skończą, cała reszta zostaje wypełniona mniejszymi ilościami - 150, 100, 75, 50. Dodatkowo, co ważne, w przypadku gdy po kilku atakach zostaje np. 10 poziom budynku, Planer rozpisze tam ostatni atak 50 katapult zamiast większej ilości (choćby była dostępna), aby oszczędzać katapulty.

## Offy przed burzakami

Jeśli chodzi o offy, których liczbę można określić wchodzących przed atakami burzącymi, ich rola ogranicza się jedynie jak w przypadku standardowych offów, nie są one częścią algorytmu, który przypisuje im konkretną ilość katapult oraz budynek do burzenia - choć teoretycznie może dojść do sytuacji, gdzie z tej samej wioski zostanie wzięty off przed burzakami oraz sam burzak wśród rozpisanych ataków. Są to oddzielne procesy i w obecnej wersji nie ma możliwości, aby offy "działały" jak jedne z burzaków.

## Kolejność burzenia bydynków

W ustawieniach {==6. Burzenie==} dokonujemy zmian w kolejności burzonych budynków. Trzeba pamiętać, że budynki nieuwzględnione w tym spisie, zostaną pominięte, a algorytm zatrzymuje się w dwóch przypadkach - albo zabrakło katapult do rozpisania, albo zostały już zburzone wszystkie wymienione budynki. To oznacza, że nawet jeśli zdecydujemy się napisać `000|000:0:1000`, to prawdopodobnie nie zostanie rozpisane 1000 burzaków - po prostu po zburzeniu wymienionych budynków, Planer przejdzie do kolejnych etapów rozpisywania (np. do kolejnego celu itp.).

## Mam pokazane 10000 dostępnych katapult, ile to celów?

Odpowiedź brzmi: to zależy. Głównie od wybranej kolejności budynków. Załóżmy że wybrano jedynie jeden budynek, **[ kuźnia ]**. Wówczas wystarczy 200-250 katapult (np. 200 i 50 lub 100, 100 lub 50, 50, 50, 50 itp.) na zburzenie jednej wioski więc można rozpisać 40-50 celów. Gdyby to były dwa budynki, **[ kuźnia, zagroda]**, trzeba znowu 200-250 katapult na kuźnię, ale też 500-700 katapult na zniszczenie zagrody (np. 14x 50, ale też 5x 100, 4x 150, 3x 200 katapult lub wiele, wiele innych kombinacji) czyli 700-950 katapult na wioskę, czyli 10-14 celów. Poniżej zamieszczam prostą tabelę dla budynków 30 poziomowych (czyli zagród, spichlerzy, wszystkich eko) i 20 poziomowych (ratusz, kuźnia) co wystarczy na policzenie ile to celów.

|                | Ilość katapult wymaganych do pełnego zburzenia budynku |
| -------------- | ------------------------------------------------------ |
| Budynki 20 lvl | 200-250                                                |
| Budynki 30lvl  | 500-700                                                |

## Podsumowanie

Pamiętaj, że u podstaw rozpisywania leży prosty algrytm zachłanny i stąd Planer **ZAWSZE** rozpisuje czy burzaki, czy fejki czy offy **LOSOWO** w bardzo podobny sposób, więc jeśli chcesz by offy czy burzaki były zupełnie nieodróżnialne od fejków, musisz rozpisać mnóstwo fejków. W przypadku burzenia warto zaznaczyć opcję **Fejki ze wszystkich wiosek** z {==Zakładki 3. Domyślne ustawienia akcji==}, która w przeciwieństwie do domyślnego ustawienia, fejki rozpisuje z wszystkich zapleczowych wiosek.

Podsumowując warto zastanowić się nad ilością katapult (i ile budynków warto w ogóle zburzyć, być może wystarczy tylko zagroda + ratusz + kuźnia?) i rozpisać mnóstwo fejków. Miłego gruzowania.