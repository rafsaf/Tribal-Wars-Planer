---
title: "Rombolási tervek - Útmutató"
date: 2026-02-28
---

Ebben az útmutatóban megtanulhatja, hogyan tervezzen rombolási akciókat, kifejezetten a világ későbbi szakaszaira. Megjegyzés: Ez feltételezi a [Kezdő lépések a Tervezővel](./../first_steps/index.md) teljes ismeretét! Ajánlott továbbá először elolvasni a két rövid korábbi útmutatót ebben a szakaszban, nevezetesen [Hogyan adjuk meg és mentsük el az akció céljait](./write_outline_targets.md) és [A klán két régiója, azaz mi a front és a hátország](./two_regions_of_the_tribe.md).

!!! hint

    Mindig kezdje bármely akció tervezését ezen az oldalon az összes csapat megszámolásával és a Front és Hátország csapatokra való felosztásával az adott terv jellegének megfelelően. Ehhez használja az 1. Elérhető egységek fület, és az eredmények a célok alatti táblázatban jelennek meg.

Az akció a **Ostromgépek** mezőben jön létre a célok mellett. A {==6. Ostromgépek==} fül beállításai határozzák meg a lerombolandó épületek sorrendjét és a minimum katapultmennyiséget, amely szükséges ahhoz, hogy egy falu részt vehessen a rombolási támadásokban. A pontos rombolási folyamat a beépített rombolási táblázatokból származik, ezért a tervező minden támadás után ellenőrzi a megmaradt szintet, és csak annyi katapultot küld, amennyi a következő pontos lépéshez szükséges.

Példa a rombolási célokra és a táblázat eredményeire, 3 támadó egységgel és \*50 ostromgéppel:

![alt text](image-24.png){ width="600" }

Példa a rombolási akció beállításaira, 3 látható épületet célozva ebben a sorrendben:

![alt text](image-25.png){ width="600" }

Az elérhető ostromgépek számát a {==1. Elérhető egységek==} fül és egyszerű matematika segítségével becsülheti meg. Minden frissítés után a táblázatban megtalálhatja a tervezésre kész katapultok teljes számát a **Minden elérhető katapult száma** alatt. Csak el kell döntenie, hogy hány célpontra lesznek elegendőek.

Példa egy megtervezett mini-akcióra, különböző számú katapulttal 200-tól 50-ig:

![alt text](image-26.png){ width="600" }

## A rombolás pontos katapultválasztása

A több elérhető katapulttal rendelkező falvak kapnak először prioritást, de a tervező nem használ külön max katapultkorlátot. Ehelyett mindig a kiválasztott falutípus pontos rombolási táblázatát követi. Ugyanez a logika érvényes a rombolási OFF és a rombolási támadás esetén is, ezért minden találat után ellenőrzi a megmaradt épületszintet a táblázattal, és folytatja, amíg az épület szükség esetén 0 szintre nem semmisül meg.

Ez azt jelenti, hogy a tervező minden találat után ellenőrzi az épület pontos maradék szintjét, és a táblázat következő megfelelő lépésével folytatja. Ha több katapult áll rendelkezésre, mint amennyire a táblázat szüksége van, az épületet 0 szintre is lerombolhatja, ha ez szükséges.

## Támadó egységek az ostromgépek előtt

A rombolási támadások előtt beütemezett off egységek ugyanazt az épületkárosító ütemezést követik, mint a későbbi rombolási támadások. Az ő rendelések továbbra is normál OFF-ek maradnak, de a katapultjaik előreviszik a rombolási cél épületállapotát.

## Épületrombolási sorrend

A {==6. Rombolás==} beállításokban megváltoztathatjuk a lerombolandó épületek sorrendjét. Fontos megjegyezni, hogy a listán nem szereplő épületek kimaradnak, és az algoritmus két esetben áll le: vagy nincs több tervezhető katapult, vagy az összes felsorolt épület már megsemmisült. Ez azt jelenti, hogy még ha úgy is döntünk, hogy `000|000:0:1000`-et írunk, 1000 ostromgép valószínűleg nem lesz beütemezve – amint a felsorolt épületek megsemmisülnek, a Tervező a következő lépésekre lép (pl. a következő cél, stb.).

## 10 000 elérhető katapultot látok. Ez hány célpontot jelent?

A válasz: attól függ. Főleg a választott épületsorrendtől. Tegyük fel, hogy csak egy épület van kiválasztva, **[ Kovácsműhely ]**. Ebben az esetben 200-250 katapult (pl. 200 és 50, vagy 100, 100, vagy 50, 50, 50, 50, stb.) elegendő egy falu lerombolásához, tehát 40-50 célpontot tervezhet. Ha két épület van kiválasztva, **[ Kovácsműhely, Tanya ]**, akkor 200-250 katapultra lesz szüksége a Kovácsműhelyhez, és 500-700 katapultra a Tanyához (pl. 14x 50, vagy 5x 100, 4x 150, 3x 200 katapult vagy sok más kombináció), ami 700-950 katapultot jelent falunként, vagy 10-14 célpontot. Az alábbiakban egy egyszerű táblázat található a 30 szintes épületekhez (mint a Tanyák, Raktárak, minden gazdasági épület) és a 20 szintes épületekhez (Főhadiszállás, Kovácsműhely), hogy segítsen kiszámítani, hány célpont lehetséges.

|                     | A teljes épületromboláshoz szükséges katapultok száma |
| ------------------- | ----------------------------------------------------- |
| 20 szintes épületek | 200-250                                               |
| 30 szintes épületek | 500-700                                               |

## A falu mérete és a rombolási táblázat

A pontos rombolási táblázat a falu pontjai alapján kerül kiválasztásra. A 8 000 pont feletti falvak a nagy falvak rombolási progresszióját használják, míg a 8 000 pont vagy alatti falvak a közepes falvak progresszióját. Más szóval: a falu nem egy redundáns maximális katapultmező alapján kerül értékelésre; a pontértéke mondja meg a tervezőnek, hogy melyik táblázatot kell használni.

## Összefoglalás

Ne feledje, hogy a tervezés alapja továbbra is egy egyszerű mohó algoritmus, és a Tervező **MINDIG** nagyon hasonló módon rendeli hozzá az ostromgépeket, hamis támadásokat vagy off egységeket. Ha azt szeretné, hogy a támadó egységek vagy az ostromgépek megkülönböztethetetlenek legyenek a hamis támadásoktól, sok hamis támadást kell terveznie. Rombolás tervezésekor érdemes engedélyezni a **Hamis támadások minden faluból** opciót a {==3. fülön. Alapértelmezett akcióbeállítások==}, amely az alapértelmezett beállítással ellentétben minden hátsó faluból hozzárendel hamis támadásokat.

A fontos utolsó részlet, hogy a rombolási tervezés már a pontos táblázatértékek alapján működik a leegyszerűsített heurisztikák helyett, ezért a viselkedés pontosabb és könnyebben előrejelezhető. Vegye figyelembe a katapultok számát és azokat az épületeket, amelyek megérik a lerombolást, és tervezzen sok hamis támadást. Jó rombolást!
