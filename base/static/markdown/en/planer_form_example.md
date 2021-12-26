<div class="p-3 mb-2 bg-light text-dark"><i class="bi bi-info-square"></i> Most things are explained in the <b> Info </b> documentation. If you have trouble typing targets, below are a handful of examples for standard and extended off and nobility encodings.</div>

<pre class="md-pre">
<span class="md-correct2">Example 1 (Clean cords)</span>

500|499
500|498

<span class="md-correct2">What corresponds to:</span>

500|499 - target: 0 offs and 0 nobles
500|498 - target: 0 offs and 0 nobles

</pre>
<pre class="md-pre">
<span class="md-correct2">Example 2 (Defined amount of offs and nobles)</span>

500|499:10:2
500|498:12:4

<span class="md-correct2">What corresponds to:</span>

500|499 - target: 10 offs and 2 nobles
500|498 - target: 12 offs and 4 nobles

</pre>
<pre class="md-pre">
<span class="md-correct2">Example 3 (Exactly defined number of offs and nobles)</span>

500|499:5|0|2|3:2
500|498:0|2|2|8:4
500|497
500|495
500|444

<span class="md-correct2">What corresponds to:</span>

500|499 - target: OFFS: 5 up close(front), 0 up close(back), 2 random from back and 3 from afar
500|499 - target: NOBLES: 2

500|498 - target: OFFY: 0 up close(front), 2 up close(back), 2 random from back and 8 from afar
500|498 - target: NOBLES: 4

500|497 - target (it was mentioned, but it is worth remembering that you can freely mix specific goals, even with empty ones)
500|495 - target
500|444 - target 

</pre>

<pre class="md-pre">
<span class="md-correct2">Example 4 (Exactly defined number of offs and nobles as before)</span>

500|499:5|0|2|3:5|0|2|3
500|498:0|2|2|8:5|0|2|3
500|497
500|495
500|444

<span class="md-correct2">What corresponds to:</span>

500|499 - target: OFFS: 5 up close(front), 0 up close(back), 2 random from back and 3 from afar
500|499 - target: NOBLES: 5 up close(front), 0 up close(back), 2 random from back and 3 from afar

500|498 - target: OFFS: 0 up close(front), 2 up close(back), 2 random from back and 8 from afar
500|498 - target: NOBLES: 5 up close(front), 0 up close(back), 2 random from back and 3 from afar


</pre>
