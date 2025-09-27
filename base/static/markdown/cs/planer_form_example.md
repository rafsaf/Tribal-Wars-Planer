<div class="p-3 mb-2 bg-light text-dark"><i class="bi bi-info-square"></i> Většina věcí je vysvětlena v dokumentaci <b> Info </b>. Pokud máte potíže se zadáváním cílů, níže je několik příkladů pro standardní a rozšířené kódování offů a šlechticů.</div>

<pre class="md-pre">
<span class="md-correct2">Příklad 1 (Čisté souřadnice)</span>

500|499
500|498

<span class="md-correct2">Což odpovídá:</span>

500|499 - cíl: 0 offů a 0 šlechticů
500|498 - cíl: 0 offů a 0 šlechticů

</pre>
<pre class="md-pre">
<span class="md-correct2">Příklad 2 (Definované množství offů a šlechticů)</span>

500|499:10:2
500|498:12:4

<span class="md-correct2">Což odpovídá:</span>

500|499 - cíl: 10 offů a 2 šlechtici
500|498 - cíl: 12 offů a 4 šlechtici

</pre>
<pre class="md-pre">
<span class="md-correct2">Příklad 3 (Přesně definovaný počet offů a šlechticů)</span>

500|499:5|0|2|3:2
500|498:0|2|2|8:4
500|497
500|495
500|444

<span class="md-correct2">Což odpovídá:</span>

500|499 - cíl: OFFY: 5 zblízka(fronta), 0 zblízka(zázemí), 2 náhodné ze zázemí a 3 z dálky
500|499 - cíl: ŠLECHTICI: 2

500|498 - cíl: OFFY: 0 zblízka(fronta), 2 zblízka(zázemí), 2 náhodné ze zázemí a 8 z dálky
500|498 - cíl: ŠLECHTICI: 4

500|497 - cíl (bylo to zmíněno, ale stojí za to si pamatovat, že můžete volně míchat konkrétní cíle, dokonce i s prázdnými)
500|495 - cíl
500|444 - cíl 

</pre>

<pre class="md-pre">
<span class="md-correct2">Příklad 4 (Přesně definovaný počet offů a šlechticů jako předtím)</span>

500|499:5|0|2|3:5|0|2|3
500|498:0|2|2|8:5|0|2|3
500|497
500|495
500|444

<span class="md-correct2">Což odpovídá:</span>

500|499 - cíl: OFFY: 5 zblízka(fronta), 0 zblízka(zázemí), 2 náhodné ze zázemí a 3 z dálky
500|499 - cíl: ŠLECHTICI: 5 zblízka(fronta), 0 zblízka(zázemí), 2 náhodné ze zázemí a 3 z dálky

500|498 - cíl: OFFY: 0 zblízka(fronta), 2 zblízka(zázemí), 2 náhodné ze zázemí a 8 z dálky
500|498 - cíl: ŠLECHTICI: 5 zblízka(fronta), 0 zblízka(zázemí), 2 náhodné ze zázemí a 3 z dálky


</pre>
