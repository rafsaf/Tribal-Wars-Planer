# Klánháború Tervező Dokumentáció

## Bevezetés

Ez a [plemiona-planer.pl](https://plemiona-planer.pl) weboldal dokumentációja – egy ambiciózus projekt a [klanhaboru.hu](https://klanhaboru.hu) számára, amely 2020 januárjában indult a játék 2019 novemberi 8.192-es verziófrissítése után. A frissítés bevezette a lehetőséget a klán adminisztrátorai számára, hogy adatokat gyűjtsenek a játékosokról és egységeikről.

- [1. Teszt Világ](./first_steps/index.md) - egy szekció, amely a weboldal felfedezésére szolgál anélkül, hogy bármit telepíteni kellene, vagy akár aktív játékfiókkal kellene rendelkezni. Lehetővé teszi az akciók tervezését egy speciálisan előkészített Teszt Világban.
- [2. A szükséges szkriptek telepítése](./scripts/army_and_defence_collection.md) - a valós világban való használathoz és egy tényleges klán akcióinak tervezéséhez szükség van egy szkriptre, amely adatokat gyűjt a klánból (opcionálisan egy második szkript segít üzeneteket küldeni a játékosoknak).
- [3. Útmutatók](./primary/write_outline_targets.md) - 6 bővített cikk az akciók tervezésével kapcsolatos konkrét témákról.
- [4. Haladó](./primary/write_outline_targets.md) - a fő "Tervező" fül összes lapjának és opciójának leírása.

## Kérdések és válaszok

### Az oldalról

> Mi ez az oldal, és kinek szól, illetve kinek nem?

Ez az oldal a **klán adminisztrátorainak** és támadásszervezőiknek szól, akik hozzáférnek a játékosok adataihoz. A klánadatok felhasználásával, a támadási célpontok megadásával és a beállítások módosításával a szervező létrehozhat egy támadási tervet, és elküldheti a célpontokat a játékosoknak (egy link segítségével az oldalra, vagy közvetlenül egy játékbeli üzenetben). Az oldalon használt matematika és a számos lehetőség lehetővé teszi gyakorlatilag bármilyen akció megtervezését a játék bármely szakaszában, időt takarítva meg a tervezőnek.

> Mi NEM a plemiona-planer?

NEM illegális eszköz, játékbot, vagy bármilyen szkript, amely automatizálja a játékon belüli műveleteket. Az oldal NEM csatlakozik a játékhoz semmilyen más célból, mint a nyilvánosan elérhető világi adatok lekérése. SOHA nem fogjuk kérni a játékjelszavát!

### Fizetések

> Fizetős a plemiona-planer?

Az oldal ingyenes. Azonban vásárolhat prémium fiók előfizetést, amely lehetővé teszi több mint 40 célpont tervezését egyetlen tervben, és hozzáférést biztosít a korábban tervezett akciókból származó fel nem használt adatokhoz (jövőbeli akciókhoz való felhasználásra). Nincs különbség a funkcionalitásban, az algoritmus minőségében vagy a sebességben. Ez a modell segít fenntartani a szolgáltatást, és a díjat meg lehet osztani a klántagok között. Nincs szükség több fiókra egy klánonként, kivéve **nyilvánvaló!** fiókmegosztási problémák esetén. Az oldal nem felelős az illetéktelen hozzáférésből, fióklopásból vagy a jelszavak ellenfelekkel való megosztásából eredő veszteségekért. A fiók tulajdonosának mérlegelnie kell az előnyöket és hátrányokat, mielőtt átadja a jelszavát egy harmadik félnek.

> Hogyan lehetséges, hogy az alkalmazás kódja nyílt és elérhető a GitHubon?
>
> Miért fizetnék előfizetésért, ha ingyen használhatom a kódot?

A [nyílt forráskódú szoftver](https://opensource.com/resources/what-open-source) híve vagyok! Igaz, dönthet úgy, hogy nem fizet, és használja az oldal kódját és a sok elkötelezett felhasználó többéves munkájának eredményét. Ingyen, és ez így is marad :) Ez tükrözi a biztonságba és a tervezésben használt matematikába vetett bizalmamat is – nincs mit rejtegetni. Azonban a tervezés kényelme bármely helyről és a tervezési eredmények online elérhetősége a klántagok számára felbecsülhetetlen. Saját szerverek beállítása speciális tudást, jelentős költségeket és folyamatos karbantartást, frissítéseket stb. igényel. Az előfizetési díj fedezi a hibajavításra, a felhasználói problémák megoldására vagy új funkciók írására fordított időt is. Mindez nem lenne lehetséges a felhasználói támogatás nélkül. Köszönet mindenkinek, aki támogatja ezt a projektet.

### Adatok

> Biztonságban vannak az adataim?

Az oldal 2020 közepe óta online van. Ez idő alatt nem történt biztonsági incidens. A jelenlegi üzleti modell fenntartja a szervereket. A felhasználók által beküldött adatokért ők felelnek, és soha nem kerülnek eladásra vagy megosztásra harmadik felekkel.

> Létrehozhatok terveket a Tervezőben anélkül, hogy hozzáférnék a klán adataihoz?

Nem, az adatok megadása kötelező. A klán adminisztrációjában kell lennie, és a tagoknak engedélyezniük kell a megfelelő beállításokat az adatok megosztásához. Van egy tesztvilág, ahol kipróbálhatja az oldalt klánadatokhoz való hozzáférés nélkül.

### Terv

> Szia, miért nem tervezi be a Tervező az összes támadó egységemet? Azt hiszem, mindent megváltoztattam a beállításokban, de folyamatosan 2,7 ezer támadó csapatot hagy fel nem használva…

Ennek számos oka lehet, főként a [1. Elérhető csapatok és táblázat leírása](./advanced/1_available_troops_and_table.md) fülön található beállítások, például néhány frontfalu vagy a szélén lévő távoli falvak kihagyása. Ritkábban a [3. Terv paraméterei](./advanced/3_outline_parameters.md) miatt. A Tervező nem ellenőrzi teljes mértékben az átgondolatlan paramétereket, és **lehetővé teszi a hibákat**. Például, ha a frontbeállítások azt jelzik, hogy az egész klán a fronton van, de a felhasználó csak a hátországból állít be támadó egységeket, az alkalmazás beütemezi ezt az akciót, annak ellenére, hogy egyetlen támadó egység sem kerül bele.

### Éjszakai bónusz

> Hogyan működik az algoritmus, hogy a lehető legjobban elkerülje az éjszakai támadásokat?

A 0-23 természetes számok tartománya, ahol a 0-7 a legrosszabb pontszámot = 1, a tartomány szélei = 2, és a teljesen "biztonságos" órák = 3 pontot kapnak, mindezt modulo 24-gyel körbevéve. [Kód itt](https://github.com/rafsaf/Tribal-Wars-Planer/blob/708b2677a3ee64d2fb8fc50eb8d7601811260dff/utils/write_ram_target.py#L297).

Ezt minden célpontra külön-külön el kell végezni az összes szövetséges falun keresztül, először kiszámítva a távolságot mezőkben.

### Szkriptek

> Szia, nem egészen értem, hogyan működik a célpontküldő szkript. Miután telepítettem az eszköztárra, semmi sem történik a klánok felületén.

Lásd [Szkript üzenetek küldéséhez](./scripts/sending_messages.md). Ez egy **böngésző szkript**, nem a játékon belüli gyorsmenühöz való. Az új üzenet nézetben használatos, ha speciálisan hozzáadott paraméterek vannak az URL-ben. [Ellenőrizze a 11. pontot az eredmények fülön](./first_steps/step_7_results_tab.md).

### Jogi és licenc

> Használhatom a plemiona-planer kódját a GitHubról?

Igen! Bármit megtehet az **Apache License 2.0** keretein belül – beállíthatja a Tervezőt helyileg, használhat forráskód-elágazásokat (forkokat), és telepítheti őket saját maga. Használhatja a GitHub repóból másolt kódot az eszközeihez (Apache License 2.0 alatt, ami azt jelenti, hogy a licenc fejléc eltávolítása NÉLKÜL). NEM járulok hozzá a plemiona-planer.pl márka megszemélyesítéséhez, a rafsaf.pl logó használatához, vagy a nevem használatához az adatvédelmi irányelvekben a plemiona-planer.pl alapú termékekben vagy projektekben.
