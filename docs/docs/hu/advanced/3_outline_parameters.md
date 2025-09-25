# 3. Terv Paraméterei

Ez a fül arra szolgál, hogy meghatározzuk a részleteket, hogy pontosan honnan származzanak a támadó csapatok egy hadművelethez, valamint egyéb általános ütemezési beállításokat. Kapcsolódjatok be!

A fül megjelenése alapértelmezett beállításokkal:

![alt text](image-2.png){ width="600" }

A [A klán két régiója: mi a Frontvonal és a Hátország](./../primary/two_regions_of_the_tribe.md) című cikkben megtanultad, hogyan kezeli a Tervező a Frontvonal, Hátország és Külső területekre való felosztást. Először is, beszéljük meg az 1. és 2. pontot a fenti képen.

Megjegyzés, az alábbi összes megfontolásnál figyelmen kívül hagyjuk a Külső régió összes faluját. Ezeket a Tervező teljesen kihagyja, tehát csak a Frontvonalra és a Hátországra koncentrálunk.

1-2. beállítások:

![alt text](image-3.png){ width="600" }

Pontosan meghatározhatja, hogy a klán mely részeiről származzanak alapértelmezés szerint a támadó csapatok és a nemesek. Az alapértelmezés a Hátország Véletlenszerű a támadó csapatoknak és a Frontvonal Legközelebbi a nemeseknek.

**Frontvonal Legközelebbi** a lehető legközelebbit jelenti. Nem is feltétlenül kell, hogy a Frontvonal falvaiból származzon. Ha például nincsenek frontvonalbeli falvak, vagy az automatikus ütemezés során csak hátországi falvak maradnak egy régióban (mert a frontvonalbelieket már felhasználták), akkor egyszerűen a legközelebbi falvakat választja ki.

**Hátország Közel** a Hátországból kell származnia, és közülük a lehető legközelebbieket választja ki.

**Hátország Véletlenszerű** a Hátországból származó falvak, valóban véletlenszerűen (nem pszeudo-véletlenszerűen) kiválasztva az összes lehetséges opció közül. Ez az alapértelmezett beállítás a támadó csapatok számára – általában nem akarjuk, hogy bármi (távolság, küldő játékos) jelezze, hogy ez egy támadás, és megkülönböztethető legyen a hamis támadásoktól.

**Hátország Távol** a Hátországból származó falvak, a Hátország Közel ellentétes sorrendjében rendezve, vagyis a lehető legtávolabbiak.

!!! info

    A további szórakozás kedvéért, amit a ezen az oldalon tervezett támadások védői kétségtelenül érezni fognak, az összes fenti beállítás minimális mértékű véletlenszerűséget tartalmaz. Ez azt jelenti, hogy a legközelebbi és a legtávolabbi lehetségesnek van egy kis ingadozása. Ez azért van, mert elméletileg a Hátország Közel és a Hátország Távol felismerhető lenne egy védő által, és így egy kicsit nehezebb lesz kitalálni, attól függően, hogy hány támadást ütemeznek egy falura. Minél több a támadás, annál nagyobb az ingadozás.

Térjünk át a 3-tól 6-ig terjedő beállításokra, amelyek az ütemezés általános beállításaira összpontosítanak.

3-6. beállítások:

![alt text](image-4.png){ width="600" }

**A 3. pontban** eldöntheti, hogyan osszák fel az egy faluból származó nemeseket. Három szokásos lehetőség van: Felosztás (minden nemes azonos kísérettel), Ne ossza fel (az első nemes a legnagyobb kísérettel, a többi minimális kísérettel – vegye figyelembe, hogy ez nem működik jól például 5 nemes esetén, ha több falura vannak felosztva), és Külön, ami azt jelenti, hogy minden nemes minimális kísérettel rendelkezik, és a támadások külön mennek előttük – csak speciális támadásokhoz és felhasználásokhoz.

A legésszerűbb lehetőség, különösen nagyobb támadások esetén, általában a felosztás, bár az alapértelmezés a nem felosztás, mivel ez általában így működik a kisebb ütemezéseknél.

**A 4. pontban** három lehetőség közül választhat. Az elsőben a Tervező megpróbál nemeseket venni egy faluhoz a játékosaink különböző falvaiból (felhasználási eset: távoli nemesek). A második opcióban (alapértelmezett) ezt optimálisan teszi, míg a harmadik opcióban megpróbál egy játékostól egy falura egy sor nemest küldeni, vagy felváltva 3 nemest egy játékostól és 1 nemest egy másiktól, vagy 2 és 2, miközben valószínűleg nem lesznek egyedi nemesek különböző falvakból. A harmadik opció a legkevésbé megbízható, és furcsa eredményeket generálhat.

**Az 5. pontban** kiválaszthatja, hogyan nézzenek ki a gyülekezőhelyre küldött parancsok a játékosaink számára, ha egy faluból több nemes is indul. Tegyük fel, hogy a játékosunknak 20 ezer támadót és 4 nemest kell küldenie a `500|500` faluba.

Az első opcióban EGY gyülekezőhelyi linket kapnak 20 ezer támadóval és 4 nemessel.

A második, alapértelmezett opcióban NÉGY egymást követő gyülekezőhelyi linket kapnak a célpontjaikhoz, minden nemest külön parancsként kezelve.

Melyik opció jobb az 5. pontban? Mint általában, ez attól függ. Kisebb támadásoknál valószínűleg a második, alapértelmezett opció. Nagyon nagy, masszív támadásoknál, ahol a támadásokat mindig felosztják, az első opció kényelmesebb a játékosok számára. Más támadásoknál válassza azt, ami a legjobban megfelel. Az alapértelmezett opció több részletet jelent a játékos számára (mivel pontosan tudja, milyen kísérete van minden nemesnek), míg az első opció egyetlen parancsként kevesebb részletet és kevesebb elfoglalt helyet jelent.

**A 6. pontban** kiválaszthatja, hogy legfeljebb hány hamis támadást lehet küldeni egy falunkból.
