---
title: "Csapat- és védelemgyűjtő szkript"
date: 2026-09-09
---

## Telepítés

Jelenleg az egyetlen támogatott telepítési lehetőség a **hivatalos Szkriptkönyvtár** használata (Beállítások -> Szkriptkönyvtár). Keresse meg a szerző szerint – Rafsaf vagy név szerint.

![A szkriptkönyvtár nézete](image-5.png)

| Szerver            | Név a szkriptkönyvtárban       | Szerző | Kód                                                                                                                            |
| ------------------ | ------------------------------ | ------ | ------------------------------------------------------------------------------------------------------------------------------ |
| plemiona.pl        | Zbiórka Wojska i Obrony        | Rafsaf | [Kód a GitHubon (v20260218)](https://github.com/rafsaf/scripts_tribal_wars/blob/2026-02-18/public/collect_troops_v20260218.js) |
| tribalwars.net     | Collect troops script          | Rafsaf | [Kód a GitHubon (v20260218)](https://github.com/rafsaf/scripts_tribal_wars/blob/2026-02-18/public/collect_troops_v20260218.js) |
| guerretribale.fr   | Script de collecte des troupes | Rafsaf | [Kód a GitHubon (v20260218)](https://github.com/rafsaf/scripts_tribal_wars/blob/2026-02-18/public/collect_troops_v20260218.js) |
| tribals.it         | Raccolta delle truppe          | Rafsaf | [Kód a GitHubon (v20260218)](https://github.com/rafsaf/scripts_tribal_wars/blob/2026-02-18/public/collect_troops_v20260218.js) |
| guerrastribales.es | Script de colector de tropas   | Rafsaf | [Kód a GitHubon (v20260218)](https://github.com/rafsaf/scripts_tribal_wars/blob/2026-02-18/public/collect_troops_v20260218.js) |
| más szerverek      | -                              | -      | [Kód a GitHubon (v20260218)](https://github.com/rafsaf/scripts_tribal_wars/blob/2026-02-18/public/collect_troops_v20260218.js) |

!!! warning

    A szkript sok nyelvi verzióban elérhető – jelentsd a problémát a szerver támogatásán keresztül, hogy ott is hozzáadhassák, ha nincs fent felsorolva. Más nyelvi verziókon való használat, **ahol a szkript nem engedélyezett** a támogatás által, fiókfelfüggesztést vonhat maga után. Használata saját felelősségre.

=== "Támogatott szerverek"

    Telepítés csak a szkriptkönyvtáron keresztül!

=== "Más szerverek"

    ```title="Csapat- és védelemgyűjtő szkript"
    --8<-- "army_script_latest.txt"
    ```

## Használati útmutató

1. Hozzon létre egy sávszkriptet, menjen a klánnézetre és kattintson rá
2. Módosítsa a beállításokat (opcionálisan) és nyomja meg az Indítás gombot
3. Várja meg az eredményt
4. Menjen a kiválasztott ütemtervhez
5. Illessze be az adatokat és erősítse meg

Beállítások:

![A beállítások képernyője](image-6.png)

Eredmény:

![Példa a szkript kimenetére](image-2.png)

## Leírás

Kattintás után a képernyő közepén megjelenik egy "számláló" a folyamatjelzéssel, majd az eredmény egy ablakban. Működik mind a Csapatok, mind a Védelem fülön. A másolás alapértelmezett beállításai a `Gyorsítótár` bekapcsolva vannak, a `Gyorsítótár idő` pedig 5 perc. Ezen az idő alatt a szkript a böngészőben mentett eredményt adja ki, ahelyett, hogy újra körbejárná az összes tagot és új adatokat gyűjtene. Kétség esetén, hogy új vagy régi eredménnyel van-e dolgunk, az összegyűjtés dátuma alul jelenik meg.

A szkript futtatásával generált adatokat be kell illeszteni az oldal ütemtervébe.

Opciók:

- **Gyorsítótár**: <boolean> (alapértelmezett: `true`) felelős az eredmény tárolásáért a böngészőben, hogy ne kattintsunk véletlenül több alkalommal egymás után és ne terheljük a játék szervereit. Ha `false` értékre állítjuk, a szkript nem menti el az eredményt a böngészőben (hasznos például akkor, ha két klánból szeretnénk adatokat gyűjteni, és azonnal a másikra ugrunk). Megjegyzés: ha a klánnak nagyon sok faluja van, ez túl sok helyet foglalhat el a `localStorage`-ban (~max 5MB), ezért a korlát 1MB. Ha a kimenet > 1MB, a mentés a `localStorage`-ba kihagyásra kerül.

- **Gyorsítótár idő**: <number> (alapértelmezett: `5`) az eredmény tárolásának ideje a böngészőben, percekben.

- **Kizárt játékosok**: <string> (alapértelmezett: `""`) ide írjuk be azoknak a játékosoknak a beceneveit, akiktől nem szeretnénk a teljes körű áttekintés adatait gyűjteni, pontosvesszővel elválasztva, mint a játékbeli üzenetekben, például "Rafsaf;kmic;valaki más".

- **Engedélyezett játékosok**: <string> (alapértelmezett: `""`) ide írjuk be azoknak a játékosoknak a beceneveit, akiktől CSAK a teljes körű áttekintés adatait szeretnénk gyűjteni. A többi játékost kihagyjuk, a beceneveket pontosvesszővel elválasztva, mint a játékbeli üzenetekben, például "Rafsaf;kmic;valaki más". Megjegyzés: az alapértelmezett `""` érték különleges jelentéssel bír, és azt jelenti, hogy az összes játékostól szeretnénk gyűjteni az áttekintést.

- **Becenév megjelenítése**: <boolean> (alapértelmezett: `false`) ha az érték `true`, akkor a Csapatok gyűjtésének minden sorában megjelenik a játékos beceneve, hasonlóan a Védelem fülön használt beállításhoz.

- **Első sor megjelenítése**: <boolean> (alapértelmezett: `false`) ha az érték `true`, akkor a Csapatok gyűjtésének eredményéhez hozzáadódik egy fejléc (az első sor a tetején), amelynek értékét a következő paraméterben, a `Első sor szövege` mezőben adjuk meg.

- **Első sor szövege**: <string> (alapértelmezett: `""`) az az érték, amely a Csapatok gyűjtésének eredményéhez kerül a fejlécbe, ha az `Első sor megjelenítése` értéke `true`.

- **Becenév megjelenítése**: <boolean> (alapértelmezett: `false`) ha az érték `true`, akkor a Védelem gyűjtésének minden sorában megjelenik a játékos beceneve, hasonlóan a Csapatok fülön használt beállításhoz.

- **Első sor megjelenítése**: <boolean> (alapértelmezett: `false`) ha az érték `true`, akkor a Védelem gyűjtésének eredményéhez hozzáadódik egy fejléc (az első sor a tetején), amelynek értékét a következő paraméterben, a `Első sor szövege` mezőben adjuk meg.

- **Első sor szövege**: <string> (alapértelmezett: `""`) az az érték, amely a Védelem gyűjtésének eredményéhez kerül a fejlécbe, ha az `Első sor megjelenítése` értéke `true`.
