### Dokumentacja:
  * #### [Skrypty](#Skrypty)
    1. [Skrypt zbiórka obrona](#deff-script)
    2. [Skrypt zbiórka wojska](#army-script)

  * #### [Świat Testowy](#test)

  * #### [Błędy](#errors)

---

### Skrypty {#Skrypty}

  * Opis

    Korzystanie ze skryptów jest <strong>konieczne</strong> by korzystać z planera. Zbierają one jednym kliknięciem cały stan wojsk od wszystkich członków plemienia, co pozwala rozpisać akcję lub zebrać deff plemienny mając <strong>faktyczny</strong> stan wszystkich wojsk.

  * Problemy

    Skrypty zbierają aktualny! stan wojsk, nie uwzględniają np. szlachciców jeszcze nie zbudowanych, jednym z możliwych obejść jest ręczna zmiana uzyskanych ze skryptu danych

  * Instalacja

    Aby korzystać ze skryptów należy zainstalować najpierw dodatek do przeglądarki:  

      * [Pomocny dział w skryptotece Plemion](https://forum.plemiona.pl/index.php?forums/skrypty-do-przegl%C4%85darek.974/){:target="_blank"}
      * [Tampermonkey (Chrome)](https://chrome.google.com/webstore/detail/tampermonkey/dhdgffkkebhmkfjojejmpbldmpobfkfo?hl=en){:target="_blank"}
      * [Greasmonkey (Firefox)](https://addons.mozilla.org/pl/firefox/addon/greasemonkey/){:target="_blank"}  
      <br>

    Następnie trzeba dodać poniższe skrypty do własnych skryptów(Kopiuj-wklej):

      * [Skrypt zbiórka obrona](#deff-script)
      * [Skrypt zbiórka wojska](#army-script)

  * Użycie

    W zakładce plemię -> członkowie -> wojsko/obrona znajdują się przyciski uruchamiające skrypty.

    <img class="img-fluid"  src="/static/images/zbiorkawojsko.png" alt="Example1">  

    <img class="img-fluid"  src="/static/images/zbiorkaobrona.png" alt="Example2">

  * Wyniki

    Wyniki prezentowane są w czerownym okienku dialogowym, wystarczy skopiować (ctrl+c) zawartość i wkleić ją na stronie.

    <img class="img-fluid"  src="/static/images/resultwojsko.png" alt="Example3">  

    <img class="img-fluid"  src="/static/images/resultobrona.png" alt="Example4">

---

#### 1. Skrypt zbiórka obrona {#deff-script}  

  * [Instalacja, opis i użycie](#Skrypty)  

  * Kopiowanie

    <button onclick="updateClipboard('copy-button-1')" class="btn btn-secondary my-2">    Kopiuj do schowka
    </button>  

  * Kod skryptu 

    <pre id="copy-button-1" class="prettyprint md-pre">
    // ==UserScript==
    // @name     Zbiórka przegląd Obrona.
    // @version  3
    // @match    &ast;://&ast;.plemiona.pl/game.php&ast;screen=ally&ast;&mode=members_defense
    // ==/UserScript==
    // By Rafsaf
    var output = "";
    var players = [];
    // Adds players from current html to get array with players nicknames and ids
    function get_all_players_list(){
      Array.from(document.querySelector('#ally_content .input-nicer').options).forEach(function(option_element) {
        var option_text = option_element.text.trim();
        var option_value = option_element.value;
        if (option_text != 'Wybierz członka') {
          players.push({
            id: option_value,
            nick: option_text
          });
        }
      });
    }
    // Uses some methods to get all stuff from table with units from current html site
    function add_current_player_info_to_output(doc){
      var trs = doc.querySelectorAll('.table-responsive .vis tr');
      var attacks;
      var coordinates;
      for (var i = 1; i < trs.length; i++) {
        output += "&lt;br&gt;";
        var tds = trs[i].querySelectorAll('td');
        if (i % 2 == 1){
          for (var j = 0; j < tds.length; j++) {
          var value = String(tds[j].innerHTML).trim();
          if (j == 0) {
            value = value.slice(-17,-10);
            coordinates = value;
          }
          if (j == 12){
            attacks = value;
          }
          output += value+",";
          }
        } else {
          output += coordinates+",";
          for (j = 0; j < tds.length; j++) {
          value = String(tds[j].innerHTML).trim();
          output += value + ",";
          }
          output += attacks+",";
          }
      }
    }
    // To add player_id to current path
    function getURL(id){
      var params = new URLSearchParams(window.location.search);
      params.set('player_id', id);
      return "".concat(window.location.origin).concat(window.location.pathname, "?").concat(params.toString());
    }
    // Used to parse string from fetch func to html
    function convertToHTML(str) {
      var parser = new DOMParser();
      var doc = parser.parseFromString(str, 'text/html');
      return doc.body;
    }
    // Most important async function, after confirmation waits 2s then uses get_all_players_list.
    // Then starts to fetch response from first player's page, then converts it.
    // Then uses 'add current player info to output' on it, and so on, in the end prints some dialog with results.
    async function renderPlayerTroops() {
      var con = window.confirm("Czy chcesz zebrać wojska?(może to chwilkę potrwać ;) )");
      if (con == false){
        return;
      }
      var today = (new Date()).getTime();
      var after_5_hours = today + 1800000;
      var storage_date = localStorage.getItem('storage_date_obrona');
      var now = (new Date()).getTime();
      if (now < storage_date) {
        output = localStorage.getItem('output_obrona');
      } else {
      get_all_players_list();
      for (var i = 0; i < players.length; i++){
        if (i == 0){
          await new Promise(function (resolve) {
            return setTimeout(resolve, 2000);
          });
      }
        var id = players[i].id;
        var response = await fetch(getURL(id));
        var html = await response.text();
        var doc = convertToHTML(html);
        add_current_player_info_to_output(doc);
        }
        localStorage.setItem('storage_date_obrona', after_5_hours);
        localStorage.setItem('output_obrona', output);
      }
      var div = document.createElement("div");
      div.contentEditable = "true";
      div.style.width = "600px";
      div.style.height = "auto";
      div.style.border = "2px solid black";
      div.style.left = "25%";
      div.style.top = "40%";
      div.style.position = "absolute";
      div.style.background = "red";
      div.style.margin = "0px 0px 100px 0px";
      div.style.color = "white";
      div.innerHTML = output;
      document.body.appendChild(div);
    }
    function create_button(){
      var td_place = document.querySelector('#menu_row2');
      var td = document.createElement('td');
      td.setAttribute('id', 'new_button');
      td_place.appendChild(td);
      var button_place = document.querySelector('#new_button');
      var btn = document.createElement('btn');
      btn.setAttribute('class', 'btn btn-default');
      btn.innerHTML = 'Zbierz Obronę';
      button_place.appendChild(btn);
      btn.addEventListener ("click", function() {
        renderPlayerTroops();
      });
    }
    create_button();
    </pre>

---

#### 2. Skrypt zbiórka wojska {#army-script}

  * [Instalacja, opis i użycie](#Skrypty)

  * Kopiowanie


    <button onclick="updateClipboard('copy-button-2')" class="btn btn-secondary my-2">    Kopiuj do schowka
    </button>  

  * Kod skryptu

    <pre id="copy-button-2" class="prettyprint md-pre">
    // ==UserScript==
    // @name     Zbiórka przegląd Wojska.
    // @version  3
    // @match    &ast;://&ast;.plemiona.pl/game.php&ast;screen=ally&ast;&mode=members_troops
    // ==/UserScript==
    // By Rafsaf
    var output = "";
    var players = [];
    // Adds players from current html to get array with players nicknames and ids
    function get_all_players_list(){
      Array.from(document.querySelector('#ally_content .input-nicer').options).forEach(function(option_element) {
        var option_text = option_element.text.trim();
        var option_value = option_element.value;
        if (option_text != 'Wybierz członka') {
          players.push({
            id: option_value,
            nick: option_text
          });
        }
      });
    }
    // Uses some methods to get all stuff from table with units from current html site
    function add_current_player_info_to_output(doc){
      var trs = doc.querySelectorAll('.table-responsive .vis tr');
      for (var i = 1; i < trs.length; i++) {
        output += "&lt;br&gt;";
        var tds = trs[i].querySelectorAll('td');
        for (var j = 0; j < tds.length; j++) {
          var value = String(tds[j].innerHTML).trim();
          if (j == 0) {
          value = value.slice(-17,-10);
          }
          output += value+",";
        }
      }
    }
    // To add player_id to current path
    function getURL(id){
      var params = new URLSearchParams(window.location.search);
      params.set('player_id', id);
      return "".concat(window.location.origin).concat(window.location.pathname, "?").concat(params.toString());
    }
    // Used to parse string from fetch func to html
    function convertToHTML(str) {
      var parser = new DOMParser();
      var doc = parser.parseFromString(str, 'text/html');
      return doc.body;
    }
    // Most important async function, after confirmation waits 2s then uses get_all_players_list.
    // Then starts to fetch response from first player's page, then converts it.
    // Then uses 'add current player info to output' on it, and so on, in the end prints some dialog with results.
    async function renderPlayerTroops() {
      var con = window.confirm("Czy chcesz zebrać wojska?(może to chwilkę potrwać ;) )");
      if (con == false){
        return;
      }
      // added today + 5h and output to local storage, in this term function uses 'ouput' from local storage
      var today = (new Date()).getTime();
      var after_5_hours = today + 1800000;
      var storage_date = localStorage.getItem('storage_date');
      var now = (new Date()).getTime();
      if (now < storage_date) {
        output = localStorage.getItem('output');
      } else {
        get_all_players_list();
        for (var i = 0; i < players.length; i++){
          if (i == 0){
            await new Promise(function (resolve) {
              return setTimeout(resolve, 2000);
            });
          }
          var id = players[i].id;
          var response = await fetch(getURL(id));
          var html = await response.text();
          var doc = convertToHTML(html);
          add_current_player_info_to_output(doc);
        }
        localStorage.setItem('storage_date', after_5_hours);
        localStorage.setItem('output', output);
      }
      var div = document.createElement("div");
      div.contentEditable = "true";
      div.style.width = "600px";
      div.style.height = "auto";
      div.style.border = "2px solid black";
      div.style.left = "25%";
      div.style.top = "40%";
      div.style.position = "absolute";
      div.style.background = "red";
      div.style.margin = "0px 0px 100px 0px";
      div.style.color = "white";
      div.innerHTML = output;
      document.body.appendChild(div);
    }
    // creates button
    function create_button(){
      var td_place = document.querySelector('#menu_row2');
      var td = document.createElement('td');
      td.setAttribute('id', 'new_button');
      td_place.appendChild(td);
      var button_place = document.querySelector('#new_button');
      var btn = document.createElement('btn');
      btn.setAttribute('class', 'btn btn-default');
      btn.innerHTML = 'Zbierz wojska';
      button_place.appendChild(btn);
      btn.addEventListener ("click", function() {
        renderPlayerTroops();
      });
    }
    create_button();
    </pre>

---

### Świat Testowy: Świat 0 {#test}
  * Pierwsze kroki...

    Świat z specjalnym numerem 0 jest stworzony do testowania planera szczególnie dla nowych użytkowników, pozwala na szybkie zapoznanie się z możliwościami strony bez konieczności wcześniejszego instalowania i korzystania ze skryptów. Wszelkie informacje co, gdzie, jak i po co wpisywać, znajdują się w dalszej części rozdziału.

  * Krok 1 - Utworzenie Rozpiski

    Należy utworzyć nową rozpiskę w zakładce <span class="md-error">Stwórz nową rozpiskę</span> pamiętając by wybranym światem gry był <span class="md-correct2">Świat 0</span>.
  
  * Krok 2 - Wybieranie plemion

    W każdej rozpisce należy wybrać dokładne plemię nasze (atakujące) i przeciwne (atakowane). W przypadku kilku takich, wybieramy kilka. Na testowym świecie 0 istnieją dokładnie dwa plemiona, <span class="md-correct2">ALLY</span> i <span class="md-error">ENEMY</span>, ustawiamy nasze plemię jako <span class="md-correct2">ALLY</span> zaś przeciwne jako <span class="md-error">ENEMY</span>, pamiętając o kliknięciu "DODAJ". Potwierdzmy.

  * Krok 3 - Uzupełnianie Zbiórki Wojska

    Wynik skryptu Zbiórki Wojska musi zostać wklejony w pole "Zbiórka Wojska", dla celów świata testowego wklej poniższe dane:

    <pre class="md-pre">
    <div class="md-correct2">
100|100,100,100,7000,0,100,2800,0,0,350,100,0,0,0,0,0,
101|101,100,100,7001,0,100,2801,0,0,350,100,0,0,0,0,0,
102|102,100,100,7002,0,100,2802,0,0,350,100,0,0,0,0,0,
103|103,100,100,7003,0,100,2803,0,0,350,100,0,0,0,0,0,
104|104,100,100,7004,0,100,2804,0,0,350,100,0,0,0,0,0,
105|105,100,100,7005,0,100,2805,0,0,350,100,0,0,0,0,0,
106|106,100,100,7006,0,100,2806,0,0,350,100,0,0,0,0,0,
107|107,100,100,7007,0,100,2807,0,0,350,100,0,0,0,0,0,
108|108,100,100,7008,0,100,2808,0,0,350,100,0,0,0,0,0,
109|109,100,100,7009,0,100,2809,0,0,350,100,0,0,0,0,0,
110|110,100,100,7010,0,100,2810,0,0,350,100,0,0,0,0,0,
111|111,100,100,7011,0,100,2811,0,0,350,100,0,0,0,0,0,
112|112,100,100,7012,0,100,2812,0,0,350,100,0,0,0,0,0,
113|113,100,100,7013,0,100,2813,0,0,350,100,0,0,0,0,0,
114|114,100,100,7014,0,100,2814,0,0,350,100,0,0,0,0,0,
115|115,100,100,7015,0,100,2815,0,0,350,100,0,0,0,0,0,
116|116,100,100,7016,0,100,2816,0,0,350,100,0,0,0,0,0,
117|117,100,100,7017,0,100,2817,0,0,350,100,0,0,0,0,0,
118|118,100,100,7018,0,100,2818,0,0,350,100,0,0,0,0,0,
119|119,100,100,7019,0,100,2819,0,0,350,100,0,0,0,0,0,
120|120,100,100,7020,0,100,2820,0,0,350,100,0,0,0,0,0,
121|121,100,100,7021,0,100,2821,0,0,350,100,0,0,0,0,0,
122|122,100,100,7022,0,100,2822,0,0,350,100,0,0,0,0,0,
123|123,100,100,7023,0,100,2823,0,0,350,100,0,0,0,0,0,
124|124,100,100,7024,0,100,2824,0,0,350,100,0,0,0,0,0,
125|125,100,100,7025,0,100,2825,0,0,350,100,0,0,0,0,0,
126|126,100,100,7026,0,100,2826,0,0,350,100,0,0,0,0,0,
127|127,100,100,7027,0,100,2827,0,0,350,100,0,0,0,0,0,
128|128,100,100,7028,0,100,2828,0,0,350,100,0,0,0,0,0,
129|129,100,100,7029,0,100,2829,0,0,350,100,0,0,0,0,0,
130|130,100,100,7030,0,100,2830,0,0,350,100,0,2,0,0,0,
131|131,100,100,7031,0,100,2831,0,0,350,100,0,2,0,0,0,
132|132,100,100,7032,0,100,2832,0,0,350,100,0,2,0,0,0,
133|133,100,100,7033,0,100,2833,0,0,350,100,0,2,0,0,0,
134|134,100,100,7034,0,100,2834,0,0,350,100,0,2,0,0,0,
135|135,100,100,7035,0,100,2835,0,0,350,100,0,2,0,0,0,
136|136,100,100,7036,0,100,2836,0,0,350,100,0,2,0,0,0,
137|137,100,100,7037,0,100,2837,0,0,350,100,0,2,0,0,0,
138|138,100,100,7038,0,100,2838,0,0,350,100,0,2,0,0,0,
139|139,100,100,7039,0,100,2839,0,0,350,100,0,2,0,0,0,
140|140,100,100,7040,0,100,2840,0,0,350,100,0,4,0,0,0,
141|141,100,100,7041,0,100,2841,0,0,350,100,0,4,0,0,0,
142|142,100,100,7042,0,100,2842,0,0,350,100,0,4,0,0,0,
143|143,100,100,7043,0,100,2843,0,0,350,100,0,4,0,0,0,
144|144,100,100,7044,0,100,2844,0,0,350,100,0,4,0,0,0,
145|145,100,100,7045,0,100,2845,0,0,350,100,0,4,0,0,0,
146|146,100,100,7046,0,100,2846,0,0,350,100,0,4,0,0,0,
147|147,100,100,7047,0,100,2847,0,0,350,100,0,4,0,0,0,
148|148,100,100,7048,0,100,2848,0,0,350,100,0,4,0,0,0,
149|149,100,100,7049,0,100,2849,0,0,350,100,0,4,0,0,0,
    </div>
    </pre>

    Do dyspozycji w powyższych danych masz:

    <pre class="md-pre">
    <div class="md-error">
30x pełnych offów z 0 szlachciami 
10x pełnych offów z 2 szlachciami 
10x pełnych offów z 4 szlachciami 
    </div>
    </pre>

  * Krok 4 - Rozpisanie akcji

    W zakładce <span class="md-error">Planer</span> należy umieszczać cele akcji zgodnie z opisem w zakładce, pamiętając że offy poniżej 19k jednostek domyślnie nie zostaną rozpisane. Na świecie testowym można umieścić poniższe cele, zmieniając ilość offów i szlachty na dowolnie wybraną lub pozostawiając przykładowe niżej:

    <pre class="md-pre">
    <div class="md-error">
200|200:4:4
205|205:2:2
210|210:4:4
215|215:5:2
220|220:4:4
225|225:4:2
230|230:4:4
\-\-\-
235|235:6:3
    </div>
    </pre>

  * Krok 5 - Szczegóły rozpiski

    Cele są podzielone po 12 na jedną stronę. Przy każdym z nich znajduje się przycisk <span class="md-correct2">Edytuj</span> pozwalający dopracować każdy cel z osobna.

    Wspierane operacje to:
     
     - Zamiana atakujących wiosek miejscami.

     - Zmiana ilości wojsk w ataku.

     - Podział ataku na 2,3,4 równe części.

     - Dodawanie nowej atakującej wioski (z tych które pozostały 'wolne') na początek lub koniec.

     - Sortowanie pozostałych wiosek na kilka sposobów.

     - Usuwanie ataku

    Warto wspomnieć, że nie istnieje wymóg 1 Cel - 1 Wioska, nie ma przeszkód by jedna wioska 'atakowała' wiele różnych celów.

  * Krok 6 - Ustawienie czasów wejścia

    Na stronie rozpiski domyślna zakładka to Menu, klikając na ikonę zegara przechodzimy do zakładki Time, by ustalić czas wejścia poszczególnych rozkazów.

    Użytkownik ma możliwość tworzenia wielu objektów w zakładce, w praktyce jednak wystarczyć może nawet jeden lub kilka. Wybieramy przedziały czasowe dla rozkazu, jednostkę oraz tryb spośród 3 możliwych. Przykładowy czas mógłby wyglądać tak:

    <img class="img-fluid"  src="/static/images/time1.png" alt="TimeExample1"> 
    
    Co oznacza tyle co:

     1. Rozpisać losową liczbę offów pomiędzy 0 a 5 między 7:00 a 8:00 (lub mniej jeśli zostały wykorzystane)

     2. Rozpisać dokładnie 3 offy pomiędzy 8:00 a 8:10 (lub mniej jeśli zostały wykorzystane)

     3. Rozpisać dokładnie 4 szlachcie na 8:10 (lub mniej etc j.w.)

     4. Rozpisać *wszystkie pozostałe tarany o ile jeszcze są* między 12:00 a 12:30

     5. Rozpisać *pozostałe szlachcice* na 12:30

    Następnie na każdej stronie należy wybrać czas wejścia każdemu celowi i kliknąć potwierdzić zakończenie rozpisywania.

  * Krok 7 - Wyniki

    - Zakładka pierwsza

        Domyślnie został stworzony <span class="md-correct2">unikalny adres url</span> dla każdego gracza gdzie prezentowane są <span class="md-correct2">tylko i wyłącznie jego cele</span> wraz z tekstem do wklejenia w notatkach, oraz graficznym zaprezentowaniem jego rozkazów.

        <span class="md-error">JEŚLI</span> atakuje on wioskę w odległości poniżej ok. 8h dla szalchcica (14 kratek) na jego stronie będą widoczne wszystkie rozkazy innych współplemieńców na ten cel, w innym wypadku - tylko jego rozkazy.

        Korzystanie z skrpytu auto-uzupełniania wiadomości pozwala przyspieszyć rozsyłanie celów

    - Zakładka druga

        W przypadku nie korzstania z auto uzupełniania wiadomości w grze, można ręcznie przekopiować członkom plemienia linki do strony z ich celami.

    - Zakładka trzecia

        W razie konieczności dostępna jest także forma wszystkich celów w plemieniu w postaci tekstu, wystarczy ręcznie przekopiować je członkom plemienia.


---


### Błędy {#errors}  

  * Gdzie

    Komunikaty o błędach pojawiają się po wprowadzeniu danych przez użytkownika, świadomie bądź też nieświadomie nieprawdidłowych.  

  * Dlaczego

    "Ciche" usuwanie błędnych informacji lub zmienianie ich nie jest działaniem pożądanym. Ponieważ nie ma możliwości korzystania z nieistniejących w grze wiosek czy graczy, użytkownik w skrajnym przypadku zostanie zasypany błędami. Uniemożliwia to również omyłkowe skorzystanie z nieaktualnych danych zebranych ze skryptów.

---

#### 1. Błędy w zbiórce wojska i obrony {#errors-zbiorka}

Rodzaje błędów podczas potwierdzania formularza:

- Nieprawidłowa długość linii (Dla różnych światów może się różnić, rycerz/brak rycerza etc.)

    <pre class="md-pre">
    <div class="md-correct">  Poprawna</div>
    500|500,1000,1000,0,10,0,10,0,0,0,0,0,0,0,
    </pre>

    <pre class="md-pre">
    <div class="md-error">  Niepoprawna, dodatkowy element 5</div>
    500|500,1000,1000,5,0,10,0,10,0,0,0,0,0,0,0,
    </pre>

    <pre class="md-pre">
    <div class="md-error">  Niepoprawna, usunięte elementy </div>
    500|500,0,10,0,10,0,0,0,0,0,0,0,
    </pre>

---  

- Nieistniejąca wioska

    <pre class="md-pre">
    <div class="md-correct">  Poprawna gdy 500|500 istnieje w grze</div>
    500|500,1000,1000,0,10,0,10,0,0,0,0,0,0,0,
    </pre>

    <pre class="md-pre">
    <div class="md-error">  Niepoprawna gdy 500|500 nie istnieje w grze</div>
    500|500,1000,1000,0,10,0,10,0,0,0,0,0,0,0,  
    Uwaga, istnieje możliwość wystąpienia tego błędu z powodu niezaktualizowanej bazy.
    </pre>

---

- Gracz spoza plemion rozpiski

    <pre class="md-pre">
    <div class="md-correct">  Poprawna gdy właściciel wioski jest w plemionach rozpiski</div>
    500|500,1000,1000,0,10,0,10,0,0,0,0,0,0,0,
    </pre>

    <pre class="md-pre">
    <div class="md-error">  Niepoprawna gdy właściciel wioski jest spoza plemion rozpiski</div>
    500|500,1000,1000,0,10,0,10,0,0,0,0,0,0,0,  
    Uwaga, istnieje możliwość wystąpienia tego błędu z powodu niezaktualizowanej bazy.
    </pre>

---

- Litery wewnątrz linii

    <pre class="md-pre">
    <div class="md-correct">  Poprawna</div>
    500|500,1000,1000,0,10,0,10,0,0,0,0,0,0,0,
    </pre>

    <pre class="md-pre">
    <div class="md-error">  Niepoprawna</div>
    500|500,1000,1000,5,0,10,0,10,0,0,0,0,0,0,0,x
    </pre>

    <pre class="md-pre">
    <div class="md-error">  Niepoprawna </div>
    500|500,0,jeden,10,0,10,0,0,0,0,0,0,0,
    </pre>

---  

- [Niepoprawne kordy](#errors-wioska)


---

#### 2. Błąd - Niepoprawne kordy {#errors-wioska}

  <pre class="md-pre">
  <div class="md-correct">  Poprawna</div>
  500|500,1000,1000,0,10,0,10,0,0,0,0,0,0,0,
  </pre>

  <pre class="md-pre">
  <div class="md-error">  Niepoprawna</div>
  500|500:),1000,1000,0,10,0,10,0,0,0,0,0,0,0,  
  </pre>

  <pre class="md-pre">
  <div class="md-error">  Niepoprawna</div>
  5000|500,1000,1000,0,10,0,10,0,0,0,0,0,0,0,  
  </pre>

---



