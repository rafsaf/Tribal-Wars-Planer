### Uzupełnianie danymi z gry

<div class="p-3 mb-2 bg-light text-dark"><i class="bi bi-info-square"></i> Korzystając z <b><a target="_blank" href="/pl/documentation/scripts/army_and_defence_collection/">skryptu do paska</a></b>, po zebraniu danych o graczach z plemienia (lub wielu plemion), wklej tutaj ich wyniki.</div>

<div class="p-3 mb-2 bg-light text-dark"><i class="bi bi-info-square"></i> By przejść do programu <span class="md-error">Planer</span> i rozpisać akcję, wymagane jest jedynie uzupełnienie wybranego formularza: <b>Zbiórki Wojska</b> lub <b>Zbiórka Obrona</b>. Należy wkleić tam dane zebrane skryptem z widoku plemienia w grze, z odpowiadającej im nazwy zakładki. Można ustalić które dane powinien wykorzystywać Planer.

Dla programu <span class="md-error">Raport deffa</span> wymagana są dane z obu zakładek.
</div>

### \<span\> w wyniku skryptu

Np. zamiast `12345` \[kolumna punktów\], skrypt pokaże `12<span class="grey">.</span>345`. 

Wklej wynik bez modyfikacji, strona poprawnie go odczytuje.

### Pojawiające się błędy

Przede wszystkim załóż, że nie jest to problem po stronie <b>Planera</b> i błąd w kodzie strony <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-emoji-smile-upside-down" viewBox="0 0 16 16"><path d="M8 1a7 7 0 1 0 0 14A7 7 0 0 0 8 1zm0-1a8 8 0 1 1 0 16A8 8 0 0 1 8 0z"/><path d="M4.285 6.433a.5.5 0 0 0 .683-.183A3.498 3.498 0 0 1 8 4.5c1.295 0 2.426.703 3.032 1.75a.5.5 0 0 0 .866-.5A4.498 4.498 0 0 0 8 3.5a4.5 4.5 0 0 0-3.898 2.25.5.5 0 0 0 .183.683zM7 9.5C7 8.672 6.552 8 6 8s-1 .672-1 1.5.448 1.5 1 1.5 1-.672 1-1.5zm4 0c0-.828-.448-1.5-1-1.5s-1 .672-1 1.5.448 1.5 1 1.5 1-.672 1-1.5z"/></svg>

Najczęstsze błędy to przede wszystkim:

<p class="my-2"><span class="md-error">1.</span> Jeśli wszystko co wpisałeś jest błędne, prawdopodobnie wklejone wioski nie należą do plemion i/lub świata, które zadeklarowałeś przy tworzeniu tej rozpiski.</p>
<p class="my-2"><span class="md-error">2.</span> Czasem wioski zmieniają właściciela lub gracze człon. Dane na stronie synchronizują się co kilka minut, ALE Plemiona aktualizują wystawiane dane jedynie <b>co 1 godzinę</b>. Ponieważ w swojej infrastrukturze mają buga, <b><span class = "md-error"> często </span></b> czas ten jest o wiele krótszy, zawsze patrz na wiadomość <u>Ostatnia aktualizacja świata: X minut temu.</u> w lewym górnym rogu strony, jest to dokładny czas ostatniej synchronizacji z grą.</p>
<p class="my-2"><span class="md-error">3.</span> Jeśli spora część jest błędna a reszta poprawna, być może został wklejony powtórzony wynik skryptu, podwojone linijki są pokazywane jako błędne.</p>

<div class="p-3 mb-2 bg-light text-dark"><i class="bi bi-info-square"></i> Jeśli to żadne z powyższych, trochę informacji na temat tego, co jeszcze jest sprawdzane wraz z przykładem wklejanego tekstu, możesz znaleźć też <b><a target="_blank" href="/pl/documentation/first_steps/step_3_fill_data/">tutaj</a></b>. Jeśli zaś czujesz, że to na pewno błąd strony, powinieneś zgłosić to na <b>Discordzie</b>.</div>
