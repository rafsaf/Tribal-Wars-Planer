<div class="p-3 mb-2 bg-light text-dark"><i class="bi bi-info-square"></i> A maioria das coisas é explicada na documentação de <b> Informações </b>. Se você tiver problemas para digitar os alvos, abaixo estão alguns exemplos para codificações padrão e estendidas de ataque e nobreza.</div>

<pre class="md-pre">
<span class="md-correct2">Exemplo 1 (Coordenadas limpas)</span>

500|499
500|498

<span class="md-correct2">O que corresponde a:</span>

500|499 - alvo: 0 ataques e 0 nobres
500|498 - alvo: 0 ataques e 0 nobres

</pre>
<pre class="md-pre">
<span class="md-correct2">Exemplo 2 (Quantidade definida de ataques e nobres)</span>

500|499:10:2
500|498:12:4

<span class="md-correct2">O que corresponde a:</span>

500|499 - alvo: 10 ataques e 2 nobres
500|498 - alvo: 12 ataques e 4 nobres

</pre>
<pre class="md-pre">
<span class="md-correct2">Exemplo 3 (Número exatamente definido de ataques e nobres)</span>

500|499:5|0|2|3:2
500|498:0|2|2|8:4
500|497
500|495
500|444

<span class="md-correct2">O que corresponde a:</span>

500|499 - alvo: ATAQUES: 5 de perto (frente), 0 de perto (retaguarda), 2 aleatórios da retaguarda e 3 de longe
500|499 - alvo: NOBRES: 2

500|498 - alvo: ATAQUES: 0 de perto (frente), 2 de perto (retaguarda), 2 aleatórios da retaguarda e 8 de longe
500|498 - alvo: NOBRES: 4

500|497 - alvo (foi mencionado, mas vale lembrar que você pode misturar livremente alvos específicos, mesmo com os vazios)
500|495 - alvo
500|444 - alvo 

</pre>

<pre class="md-pre">
<span class="md-correct2">Exemplo 4 (Número exatamente definido de ataques e nobres como antes)</span>

500|499:5|0|2|3:5|0|2|3
500|498:0|2|2|8:5|0|2|3
500|497
500|495
500|444

<span class="md-correct2">O que corresponde a:</span>

500|499 - alvo: ATAQUES: 5 de perto (frente), 0 de perto (retaguarda), 2 aleatórios da retaguarda e 3 de longe
500|499 - alvo: NOBRES: 5 de perto (frente), 0 de perto (retaguarda), 2 aleatórios da retaguarda e 3 de longe

500|498 - alvo: ATAQUES: 0 de perto (frente), 2 de perto (retaguarda), 2 aleatórios da retaguarda e 8 de longe
500|498 - alvo: NOBRES: 5 de perto (frente), 0 de perto (retaguarda), 2 aleatórios da retaguarda e 3 de longe


</pre>
