### Dokumentacja:
  * #### [Skrypty](#Skrypty)
    1. [Skrypt zbiórka obrona](#Skrypt-zbiorka-obrona)
    2. [Skrypt zbiórka wojska](#Skrypt-zbiorka-wojska)

  * #### [Tworzenie nowej rozpiski](#Tworzenie-nowej-rozpiski)
  * #### [Opis funkcjonalności rozpiski](#Opis-funkcjonalnosci-rozpiski)
    1. [Wyniki](#Wyniki)
    2. [Zbierz deff](#Zbierz-deff)
  * #### [Błędy](#bledy)

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

      * [Skrypt zbiórka obrona](#Skrypt-zbiorka-obrona)
      * [Skrypt zbiórka wojska](#Skrypt-zbiorka-wojska)

  * Użycie

    W zakładce plemię -> członkowie -> wojsko/obrona znajdują się przyciski uruchamiające skrypty.

    <img class="img-fluid"  src="/static/images/zbiorkawojsko.png" alt="Example1">  

    <img class="img-fluid"  src="/static/images/zbiorkaobrona.png" alt="Example2">

  * Wyniki

    Wyniki prezentowane są w czerownym okienku dialogowym, wystarczy skopiować (ctrl+c) zawartość i wkleić ją na stronie.

    <img class="img-fluid"  src="/static/images/resultwojsko.png" alt="Example3">  

    <img class="img-fluid"  src="/static/images/resultobrona.png" alt="Example4">

---

#### 1. Skrypt zbiórka obrona {#Skrypt-zbiorka-obrona}  

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

#### 2. Skrypt zbiórka wojska {#Skrypt-zbiorka-wojska}

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

### Tworzenie nowej rozpiski {#Tworzenie-nowej-rozpiski}
...

---

### Opis funkcjonalności rozpiski {#Opis-funkcjonalnosci-rozpiski}
...

---

### Błędy {#bledy}  

  * Gdzie

    Komunikaty o błędach pojawiają się po wprowadzeniu danych przez użytkownika, świadomie bądź też nieświadomie nieprawdidłowych.  

  * Dlaczego

    "Ciche" usuwanie błędnych informacji lub zmienianie ich nie jest działaniem pożądanym. Ponieważ nie ma możliwości korzystania z nieistniejących w grze wiosek czy graczy, użytkownik w skrajnym przypadku zostanie zasypany błędami. Uniemożliwia to również omyłkowe skorzystanie z nieaktualnych danych zebranych ze skryptów.

---

#### 1. Błędy w zbiórce wojska i obrony {#bledy-zbiorka}

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

- [Niepoprawne kordy](#bledy-wioska)


---

#### 2. Błąd - Niepoprawne kordy {#bledy-wioska}

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



