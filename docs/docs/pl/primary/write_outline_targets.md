# Jak wpisywać i zapisać cele akcji

Konwencja: kolejne cele akcji muszą być wpisywane w kolejnych linijkach Celów. Minimalnie wystarczą same koordy, wówczas przykładowa linijka `000|000` zostanie uzupełniona do `000|000:0:0`. W dalszej części nauczysz się kodowania ilości offów i szlachciców. Aby zapisać cele kliknij Zapisz cele.

<figure markdown="span">
  ![alt text](image.png){ width="600" }
  <figcaption>Przykład 1, offy i szlachta domyślnie kodowane</figcaption>
</figure>

`440|670:5:4` w pierszej linijce to przykład, jak domyślnie kodować ilość offów i szlachciców na dany cel. Pierwsza liczba oznacza Ilość offów, zaś druga Ilość szlachciców.

Planer obsługuje trzy rodzaje celów, prawdziwe, fejkowe oraz burzące. Cele prawdziwe zamieszaj w Cele, Cele fejkowe obok w Fejki, zaś Cele do burzenia w Burzaki. Dla Fejków kodujemy zamiast offów i szlachiców odpowiednio ilość fejków i fejk szlachciców, zaś w zakładce Burzaki odpowiednio ilość offów i ilość burzaków (które wchodzą za offami).

<figure markdown="span">
  ![alt text](image-1.png){ width="600" }
  <figcaption>Przykład 2, rozszerzone kodowanie offów i szlachty</figcaption>
</figure>

Domyślnie cele jak w Przykładzie 1, dziedziczą tryb wysyłania z zakładki 3. Parametry rozpiski, czyli np. offy losowo z zaplecza oraz szlachta z najbliższego frontu. W przypadku gdy chcemy na dany cel, np. linijkę numer 3 w Przykładzie 2, czyli `439|671` wysłać 5 offów losowo z zaplecza, 2 offów z bliskiego zaplecza, 1 szlachcica z daleka oraz ostatnie 3 szlachcice z bliska, można wykorzystać rozszerzoną składnię wpisując:

```
439|671:2|0|5|0:3|0|0|1
```

W takim przypadku zmiast jednej liczby offów wpisaliśmy 2|0|5|0 a zamiast jednej liczby szlachciców wpisaliśmy 3|0|0|1. Korzystamy z rozszerzonej składni wtedy gdy zależy nam na części rozkazów z daleka a innej części z bliska, do wyboru są 4 rejony naszegeo plemienia.

!!! info

    **A|B|C|D** tłumaczymy na: 
    A z bliska|B z bliskiego zaplecza|C losowo z zaplecza|D z daleka


Błędy pojawią się w standardowych przypadkach, czyli przede wszystkim gdy dana wioska nie istnieje na zadeklarowanym w rozpisce świecie lub gdy wioska jest barbarzyńska oraz gdy wpisywane po kordach znaki nie będą jednymi z podanych powyżej możliwości. Nie ma przeszkód by celami były wioski współplemieńców lub by te same wioski były wpisane wielokrotnie (choć w tym przypadku, u góry pojawi się informacja, że wykryto powtórzenia). Powtórzenia nie są zabronione, każdy wpisany cel, nawet jeśli pojawia się wielokrotnie, zostanie potraktowany oddzielnie, tym nie mniej może to spowodować chaos u graczy bo będzie np. kilka tych samych celów z różnymi rozkazami na nie (?). Powtórzenia w różnych zakładkach (Cele, Fejki, Burzaki) nie są zliczane.

<figure markdown="span">
  ![alt text](image-2.png){ width="600" }
  <figcaption>Przykład 3, błędy podczas zapisywania</figcaption>
</figure>