<pre class="md-pre">
<span class="md-correct2">Przykład 1 (Czyste kordy)</span>

500|499
500|498
---
500|496

<span class="md-correct2">Co odpowiada:</span>

500|499 - cel: 0 offów i 0 szlachcice
500|498 - cel: 0 offów i 0 szlachcice

500|496 - fejk cel: 0 fejk offów i 0 fejk szlachcice

</pre>
<pre class="md-pre">
<span class="md-correct2">Przykład 2 (Zdefiniowana ilość offów i szlachty)</span>

500|499:10:2
500|498:12:4
---
500|496:4:4

<span class="md-correct2">Co odpowiada:</span>

500|499 - cel: 10 offów i 2 szlachcice
500|498 - cel: 12 offów i 4 szlachcice

500|496 - fejk cel: 4 fejk offów i 4 fejk szlachcice

</pre>
<pre class="md-pre">
<span class="md-correct2">Przykład 3 (Dokładnie zdefiniowana ilość offów i grubych)</span>

500|499:5|0|2|3:2
500|498:0|2|2|8:4
500|497
500|495
500|444
---
500|496:0|4|0|0:4

<span class="md-correct2">Co odpowiada:</span>

500|499 - cel: OFFY: 5 z bliska(front), 0 z bliska(zaplecze), 2 losowo z zaplecza i 3 z daleka
500|499 - cel: SZLACHCIE: 2

500|498 - cel: OFFY: 0 z bliska(front), 2 z bliska(zaplecze), 2 losowo z zaplecza i 8 z daleka
500|498 - cel: SZLACHCIE: 4

500|497 - cel (było, ale warto pamiętać że można dowolnie mieszać szczegółowe cele nawet z pustymi)
500|495 - cel
500|444 - cel 

500|496 - fejk cel: FEJKI: 0 z bliska(front), 4 z bliska(zaplecze), 0 losowo z zaplecza i 0 z daleka
500|496 - cel: FEJK SZLACHTA: 4

</pre>

<pre class="md-pre">
<span class="md-correct2">Przykład 4 (Dokładnie zdefiniowana ilość offów i grube jak poprzednio)</span>

500|499:5|0|2|3:5|0|2|3
500|498:0|2|2|8:5|0|2|3
500|497
500|495
500|444
---
500|496:0|4|0|0:5|0|2|3

<span class="md-correct2">Co odpowiada:</span>

500|499 - cel: OFFY: 5 z bliska(front), 0 z bliska(zaplecze), 2 losowo z zaplecza i 3 z daleka
500|499 - cel: SZLACHCIE: 5 z bliska(front), 0 z bliska(zaplecze), 2 losowo z zaplecza i 3 z daleka

500|498 - cel: OFFY: 0 z bliska(front), 2 z bliska(zaplecze), 2 losowo z zaplecza i 8 z daleka
500|498 - cel: SZLACHCIE: 5 z bliska(front), 0 z bliska(zaplecze), 2 losowo z zaplecza i 3 z daleka

500|497 - cel (było, ale warto pamiętać że można dowolnie mieszać szczegółowe cele nawet z pustymi)
500|495 - cel
500|444 - cel 

500|496 - fejk cel: FEJKI: 0 z bliska(front), 4 z bliska(zaplecze), 0 losowo z zaplecza i 0 z daleka
500|496 - cel: FEJK SZLACHTA: 5 z bliska(front), 0 z bliska(zaplecze), 2 losowo z zaplecza i 3 z daleka

</pre>