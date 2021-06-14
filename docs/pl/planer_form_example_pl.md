<div class="p-3 mb-2 bg-light text-dark"><svg xmlns="http://www.w3.org/2000/svg" width="1.2em" height="1.2em" fill="currentColor" class="bi bi-info-square" viewBox="0 0 16 16"><path d="M14 1a1 1 0 0 1 1 1v12a1 1 0 0 1-1 1H2a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1h12zM2 0a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V2a2 2 0 0 0-2-2H2z"/><path d="M8.93 6.588l-2.29.287-.082.38.45.083c.294.07.352.176.288.469l-.738 3.468c-.194.897.105 1.319.808 1.319.545 0 1.178-.252 1.465-.598l.088-.416c-.2.176-.492.246-.686.246-.275 0-.375-.193-.304-.533L8.93 6.588zM9 4.5a1 1 0 1 1-2 0 1 1 0 0 1 2 0z"/></svg> Większość zagadnień wyjaśniają dokumentacje w <b>Info</b>. W razie problemów z wpisywaniem celów, niżej znajdziesz garść przykładów dla standardowych i rozszerzonych kodowań offów i szlachty.</div>

<pre class="md-pre">
<span class="md-correct2">Przykład 1 (Czyste kordy)</span>

500|499
500|498

<span class="md-correct2">Co odpowiada:</span>

500|499 - cel: 0 offów i 0 szlachcice
500|498 - cel: 0 offów i 0 szlachcice

</pre>
<pre class="md-pre">
<span class="md-correct2">Przykład 2 (Zdefiniowana ilość offów i szlachty)</span>

500|499:10:2
500|498:12:4

<span class="md-correct2">Co odpowiada:</span>

500|499 - cel: 10 offów i 2 szlachcice
500|498 - cel: 12 offów i 4 szlachcice

</pre>
<pre class="md-pre">
<span class="md-correct2">Przykład 3 (Dokładnie zdefiniowana ilość offów i grubych)</span>

500|499:5|0|2|3:2
500|498:0|2|2|8:4
500|497
500|495
500|444

<span class="md-correct2">Co odpowiada:</span>

500|499 - cel: OFFY: 5 z bliska(front), 0 z bliska(zaplecze), 2 losowo z zaplecza i 3 z daleka
500|499 - cel: SZLACHCIE: 2

500|498 - cel: OFFY: 0 z bliska(front), 2 z bliska(zaplecze), 2 losowo z zaplecza i 8 z daleka
500|498 - cel: SZLACHCIE: 4

500|497 - cel (było, ale warto pamiętać że można dowolnie mieszać szczegółowe cele nawet z pustymi)
500|495 - cel
500|444 - cel 

</pre>

<pre class="md-pre">
<span class="md-correct2">Przykład 4 (Dokładnie zdefiniowana ilość offów i grube jak poprzednio)</span>

500|499:5|0|2|3:5|0|2|3
500|498:0|2|2|8:5|0|2|3
500|497
500|495
500|444

<span class="md-correct2">Co odpowiada:</span>

500|499 - cel: OFFY: 5 z bliska(front), 0 z bliska(zaplecze), 2 losowo z zaplecza i 3 z daleka
500|499 - cel: SZLACHCIE: 5 z bliska(front), 0 z bliska(zaplecze), 2 losowo z zaplecza i 3 z daleka

500|498 - cel: OFFY: 0 z bliska(front), 2 z bliska(zaplecze), 2 losowo z zaplecza i 8 z daleka
500|498 - cel: SZLACHCIE: 5 z bliska(front), 0 z bliska(zaplecze), 2 losowo z zaplecza i 3 z daleka

500|497 - cel (było, ale warto pamiętać że można dowolnie mieszać szczegółowe cele nawet z pustymi)
500|495 - cel
500|444 - cel 

</pre>
