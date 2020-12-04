#### Zbieraj deff z zaplecza
* Program jest używany do zbierania jednostek obronnych z wiosek w odległości większej niż promień od wrogiego plemiona jako zaplecze zaś w odległości mniejszej jako front.
* Odległość jest liczona w kratkach.
* Wartość domyślna 30 odpowiada około 17 godzinom drogi dla szlachcica na większości światów, z powodów optymalizacyjnych maksymalny możliwy promień to 100.
* Uwaga, przy dużej wielkości promienia i liczbie wiosek w naszych i wrogich plemionach, (np. kilka wrogów po 5k+ wiosek i nasze plemiona 5k+ wiosek) może to chwile potrwać, jeśli chcesz upewnić się, że to nie błąd, spróbuj zmniejszyć promień do małej wartości i sprawdź rezultat. Jeśli wszystko jest w porządku, to powodem jest rozmiar wprowadzonych danych i musisz albo dłuższą chwilę poczekać (ponad minutę), albo zmniejszyć promień. Chyba że przypadkowo jesteś milionerem i zapłacisz za przeniesienie na mocniejszy host :)
#### Upewnij się, że ...
* Uwzględniono wszystkie plemiona własne i wrogie.
* Wybrany promień jest odpowiedni do potrzeb.
#### Pamiętaj, że ...
* Pozostałe opcje są opcjonalne.
* Więcej szczegółów można znaleźć w pozostałych zakładkach
#### Przykładowy wynik dla 1 gracza
<pre class="md-pre">
Przetestowane. LEGENDA:
CK liczone jako x4 a nie x6, zwiad NIE jest liczony.
W WIOSKACH = swój w wiosce + cudzy z stałych.
CAŁY SWÓJ = swój w wiosce + swój poza wioską.


Gracz1
Na froncie 2 wsi, 30000 deffa W WIOSKACH, zaś 25000 CAŁEGO SWOJEGO.
Na zapleczu 4 wsi, 5400 deffa W WIOSKACH, zaś 65000 CAŁEGO SWOJEGO.

Gracz1
---------FRONT---------
100|100- W wiosce- 20000  (CAŁY własny deff [ 5000 ])
101|101- W wiosce- 10000  (CAŁY własny deff [ 20000 ])
---------ZAPLECZE---------
105|105- W wiosce- 100  (CAŁY własny deff [ 10000 ])
106|106- W wiosce- 100  (CAŁY własny deff [ 15000 ])
107|107- W wiosce- 5000 (CAŁY własny deff [ 20000 ])
108|108- W wiosce- 200  (CAŁY własny deff [ 20000 ])
</pre>