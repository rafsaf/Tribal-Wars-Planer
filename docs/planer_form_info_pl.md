#### Najprostsze przykłady
Uważaj by nie pojawiły się żadne dodatkowe spacje w wierszach (będzie błąd w tej linijce).
<div class="row">

<div class="col-6" id="left">
<p class="md-error">Pusta (potem można dodać cele)</p>
<pre class="md-pre">
---
</pre>
<p class="md-error">Tylko cele na fejki</p>
<pre class="md-pre">
---
500|499
500|498
</pre>
<p class="md-error">5 offów i 2 szlachty z daleka i 3 offy z bliska i 2 grube z bliska</p>
<pre class="md-pre">
500|499:3|0|0|5:2|0|0|2
---
</pre>

</div>

<div class="col-6" id="right" >
<p class="md-error">Tylko 1 prawdziwy cel </p>
<pre class="md-pre">
500|499
---
</pre>
<p class="md-error">Cele prawdziwe i fejki z określoną liczbą ataków</p>
<pre class="md-pre">
500|499:10:2
500|498:12:4
---
500|496:4:4
</pre>

</div>


</div>

#### Cele
* Wpisuj tutaj swoje cele oraz liczbę offów i szlachciców dla nich.
* Jest kilka poprawnych form, najprostsza to <span class="md-error">000|000</span> (symbolizuje dowolne kordy) w każdej nowej lini, wszystkie możliwe przypadki można znaleźć w zakładce Przykłady

* Dodawaj cele na fejki identycznie jak prawdziwe, ale poniżej oddzielającego cele od fejków separatora <span class="md-error">**---**</span>

#### 1. Tabela aktualnych jednostek i Dostępne jednostki
* <span class="md-error">FRONTEM nazwamy każdą wioskę w odległości w kratkach bliższej niż zdefiniowana wielkość OD DOWOLNEJ wioski wszystkich wrogów</span>
* Znajdziesz tutaj wszystkie dostępne aktualne wojska
* Możesz zaktualizować nowy promień frontu by zobaczyć ich ilość dla innych wartości, dla dużych wartości może to chwilę potrwać

#### 2. Zmiana daty
* Możesz zmienić datę określoną na początku tworzenia rozpiski

#### 3. Ustawienia trybów akcji

* Domyślnie każdy cel będzie miał identyczny tryb z domyślnym trybem (po każdym zapisaniu Celi każdy cel dostaje znowu domyślny tryb). Możemy wybierać pomiędzy najbliższymi frontowymi offami/grubymi, bliskimi (ale już z zaplecza), losowo z zaplecza albo dalekich z zaplecza. W przypadku szlachty nawet te najdalsze będą wzięte te których odległość od celu jest mniejsza niż maksymalna odległość dla szlachty, np. ustawiając ją na 50 kratek, planer nigdy nie rozpisze na jakiś cel szlachcica z wioski dalszej niż 50 kratek. 

* Dodatkowo są 3 opcje dotyczące dzielenia offów (dzielić, nie dzielić- to znaczy np. off + szlachcie z małą obstawą oraz zupełnie oddzielnie offy oraz szlachcice, zatem szlachta bez obstawy) oraz 3 opcje dotyczące preferencji wyboru wiosek rozpisując szlachtę, mianowicie "możliwie na jedną wioskę" oznacza że jeśli będzie taka możliwość to wszystkie grube polecą tylko na jeden cel. Optymalnie tzn. "na jedną lub wiele wiosek" oznacza że zostaną one dobrane tak, by było dobrze i by wszystkie zostały możliwie wykorzystane. Ostatni tryb to pojedyncze szlachcice z różnych wiosek, korzystne w przypadku np. offoszlach z daleka (lub fejków z daleka imitujących offoszlachty.

* Warto zauważyć, że mieszając ostatnie 3 tryby dzielenia z 3 trybami wyboru sposobu rozpisywania, można uzyskać ciekawe i różne połączenia, planer domyślnie ustawia większe offy z szlachtą przed mniejszymi (jeśli są z różnych wiosek) oraz dalsze offy przed bliższymi (tak by padały te z dalsza jako pierwsze)

#### Istnieje opcja połączenia offów i grubych z daleka, bliska i losowych. 

W tym celu (dla przykładu offów) zamiast 

<pre class="md-pre">
000|000:10:0
</pre>

Wpisz
<pre class="md-pre">
000|000:2|2|5|5:0
</pre>

Aby uzyskać kolejno 2 offy z bliskiego frontu, 2 offy z bliskiego zaplecza. 5 losowych offów z zaplecza, 5 dalekich offów z zaplecza

Identycznie sprawa się ma dla szlachciców.

#### 4. Wybór dla celów z osobna

* Tryby akcji dla każdego celu z osobna, ustaw i zapisz. Pamiętaj, że zmieniając później cele i zapisując je, musisz ustawić tryby od nowa.