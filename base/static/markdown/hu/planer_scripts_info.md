### Játékadatokkal való feltöltés

<div class="p-3 mb-2 bg-light text-dark"><i class="bi bi-info-square"></i> A <b><a target="_blank" href="/hu/documentation/scripts/army_and_defence_collection/">játékban lévő bar script</a></b> használatával, miután összegyűjtötte az adatokat egy klán (vagy több klán) játékosairól, illessze be ide az eredményeiket.</div>

<div class="p-3 mb-2 bg-light text-dark"><i class="bi bi-info-square"></i> A <span class="md-error">Tervező</span> fülre lépéshez és egy terv beállításához csak a <b>Csapatösszesítő</b> kitöltése szükséges. Ezenkívül a <span class="md-error">Védelem összesítő</span> fülhöz a <b>Védelem összesítő</b> adatai szükségesek.</div>

### Előforduló hibák

Először is, tegyük fel, hogy ez nem a <b>Tervező</b> oldali probléma és a weboldal kódjában lévő hiba <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-emoji-smile-upside-down" viewBox="0 0 16 16"><path d="M8 1a7 7 0 1 0 0 14A7 7 0 0 0 8 1zm0-1a8 8 0 1 1 0 16A8 8 0 0 1 8 0z"/><path d="M4.285 6.433a.5.5 0 0 0 .683-.183A3.498 3.498 0 0 1 8 4.5c1.295 0 2.426.703 3.032 1.75a.5.5 0 0 0 .866-.5A4.498 4.498 0 0 0 8 3.5a4.5 4.5 0 0 0-3.898 2.25.5.5 0 0 0 .183.683zM7 9.5C7 8.672 6.552 8 6 8s-1 .672-1 1.5.448 1.5 1 1.5 1-.672 1-1.5zm4 0c0-.828-.448-1.5-1-1.5s-1 .672-1 1.5.448 1.5 1 1.5 1-.672 1-1.5z"/></svg>

A leggyakoribb hibák:

<p class = "my-2"> <span class = "md-error"> 1. </span> Ha minden, amit beírt, rossz, valószínű, hogy a beillesztett falvak nem tartoznak azokhoz a klánokhoz és/vagy világhoz, amelyeket a listák létrehozásakor megadott. </p>
<p class = "my-2"> <span class = "md-error"> 2. </span> Néha a falvak tulajdonost vagy a játékosok klánt válthatnak. Az adatfrissítés néhány percenként fut, DE a Klánháború csak <b>1 óránként</b> kínál friss adatokat. Az infrastruktúrájukban lévő hiba miatt ez <b><span class = "md-error"> gyakran </span></b> lehet rövidebb időszak, mindig nézze meg a <u>Utolsó világfrissítés: X perccel ezelőtt.</u> üzenetet a bal felső sarokban. </p>
<p class = "my-2"> <span class = "md-error"> 3. </span> Ha egy nagy rész rossz, a többi pedig helyes, talán egy duplikált szkript kimenetet illesztettek be, a duplikált sorok rosszként jelennek meg. </p>

<div class="p-3 mb-2 bg-light text-dark"><i class="bi bi-info-square"></i> Ha a fentiek egyike sem, egy kis információ arról, hogy mi mást ellenőriznek, valamint egy példa a beillesztett szövegre, itt is megtalálható <b><a target="_blank" href="/hu/documentation/first_steps/step_3_fill_data/">itt</a></b>. Ha úgy érzi, hogy ez egyértelműen egy oldali hiba, jelentse a <b>Discordon</b>.</div>
