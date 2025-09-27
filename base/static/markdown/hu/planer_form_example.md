<div class="p-3 mb-2 bg-light text-dark"><i class="bi bi-info-square"></i> A legtöbb dolgot az <b> Információ </b> dokumentáció magyarázza. Ha problémái vannak a célpontok beírásával, alább talál néhány példát a standard és kiterjesztett támadósereg és nemes kódolásokra.</div>

<pre class="md-pre">
<span class="md-correct2">1. példa (Tiszta koordináták)</span>

500|499
500|498

<span class="md-correct2">Ami megfelel:</span>

500|499 - célpont: 0 támadósereg és 0 nemes
500|498 - célpont: 0 támadósereg és 0 nemes

</pre>
<pre class="md-pre">
<span class="md-correct2">2. példa (Meghatározott számú támadósereg és nemes)</span>

500|499:10:2
500|498:12:4

<span class="md-correct2">Ami megfelel:</span>

500|499 - célpont: 10 támadósereg és 2 nemes
500|498 - célpont: 12 támadósereg és 4 nemes

</pre>
<pre class="md-pre">
<span class="md-correct2">3. példa (Pontosan meghatározott számú támadósereg és nemes)</span>

500|499:5|0|2|3:2
500|498:0|2|2|8:4
500|497
500|495
500|444

<span class="md-correct2">Ami megfelel:</span>

500|499 - célpont: TÁMADÓSEREGEK: 5 közelről (front), 0 közelről (hátország), 2 véletlenszerűen a hátországból és 3 távolról
500|499 - célpont: NEMESEK: 2

500|498 - célpont: TÁMADÓSEREGEK: 0 közelről (front), 2 közelről (hátország), 2 véletlenszerűen a hátországból és 8 távolról
500|498 - célpont: NEMESEK: 4

500|497 - célpont (említve volt, de érdemes megjegyezni, hogy szabadon keverheti a konkrét célokat, akár üresekkel is)
500|495 - célpont
500|444 - célpont 

</pre>

<pre class="md-pre">
<span class="md-correct2">4. példa (Pontosan meghatározott számú támadósereg és nemes, mint korábban)</span>

500|499:5|0|2|3:5|0|2|3
500|498:0|2|2|8:5|0|2|3
500|497
500|495
500|444

<span class="md-correct2">Ami megfelel:</span>

500|499 - célpont: TÁMADÓSEREGEK: 5 közelről (front), 0 közelről (hátország), 2 véletlenszerűen a hátországból és 3 távolról
500|499 - célpont: NEMESEK: 5 közelről (front), 0 közelről (hátország), 2 véletlenszerűen a hátországból és 3 távolról

500|498 - célpont: TÁMADÓSEREGEK: 0 közelről (front), 2 közelről (hátország), 2 véletlenszerűen a hátországból és 8 távolról
500|498 - célpont: NEMESEK: 5 közelről (front), 0 közelről (hátország), 2 véletlenszerűen a hátországból és 3 távolról


</pre>
