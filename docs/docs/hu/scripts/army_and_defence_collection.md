# Sereg és Védelem Gyűjtő Szkript

| Szerver        | Klánháború Fórum                                                                                                                                                     | Engedélyezett | Kód                                                                                                                  |
| -------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------- | -------------------------------------------------------------------------------------------------------------------- |
| tribalwars.net | [https://forum.tribalwars.net/index.php?threads/collect-troops-script.292893/](https://forum.tribalwars.net/index.php?threads/collect-troops-script.292893/)         | IGEN          | [Kód a GitHubon (v2.1)](https://github.com/rafsaf/scripts_tribal_wars/blob/2024-09-09-2/src/collect_troops_v2.1.ts)  |
| plemiona.pl    | [https://forum.plemiona.pl/index.php?threads/zbi%C3%B3rka-wojska-i-obrony.128630/](https://forum.plemiona.pl/index.php?threads/zbi%C3%B3rka-wojska-i-obrony.128630/) | IGEN          | [Kód a GitHubon (v2)](https://github.com/rafsaf/scripts_tribal_wars/blob/2024-09-01/public/collect_troops_v2.js)     |
| más szerverek  | -                                                                                                                                                                    | NEM           | [Kód a GitHubon (v2.3)](https://github.com/rafsaf/scripts_tribal_wars/blob/2025-09-22/public/collect_troops_v2.3.js) |

!!! warning

    Más nyelvi verziókon való használat, **ahol a szkript nem engedélyezett** a támogatás által, fiókfelfüggesztést vonhat maga után. Használata saját felelősségre.

=== "tribalwars.net"

    ```title="Sereg és Védelem Gyűjtő Szkript"
    --8<-- "army_script_tribalwars_net_en.txt"
    ```

=== "plemiona.pl"

    ```title="Sereg és Védelem Gyűjtő Szkript"
    --8<-- "army_script_plemiona_pl_en.txt"
    ```

=== "más szerverek"

    ```title="Sereg és Védelem Gyűjtő Szkript"
    --8<-- "army_script_latest.txt"
    ```

## Telepítés

A telepítés ugyanúgy történik, mint az összes sávszkript esetében; a tartalmat be kell illeszteni egy újonnan létrehozott sávszkriptbe a játékban.

## Használati útmutató

1. Hozzon létre egy sávszkriptet, kattintson rá
2. Várja meg az eredményt
3. Menjen a kiválasztott ütemtervhez
4. Illessze be az adatokat és erősítse meg

![Példa a szkript kimenetére](image-2.png)

## Leírás

Kattintás után egy "számláló" jelenik meg a képernyő közepén, majd az eredmény egy ablakban. Működik mind a Sereg, mind a Védelem fülön. A másolás alapértelmezett beállításai a gyorsítótár `true`-ra és a cacheTime 5 percre vannak állítva. Ez idő alatt a szkript a böngészőben mentett eredményt adja ki, ahelyett, hogy újra körbejárná az összes tagot és új adatokat gyűjtene. Kétség esetén, hogy új vagy régi eredménnyel van-e dolgunk, a gyűjtés dátuma alul jelenik meg.

A szkript futtatásával generált adatokat be kell illeszteni az oldal ütemtervébe.

Opciók:

A konfiguráció a **COLLECT_TROOPS_DATA_V2** objektum használatával történik. Megjegyzés: minden paraméter OPCIONÁLIS, ha mindkét változó
nincs definiálva, vagy definiálva van, de nincsenek benne kulcsok, ésszerű
alapértelmezések lesznek használva.

- **cache**: <boolean> (alapértelmezett: `true`) felelős az eredmény tárolásáért
  a böngészőben, hogy ne kattintsunk véletlenül néhányszor egymás után és
  ne terheljük a játék szervereit, a cache: false beállítása azt eredményezi, hogy nem tárolja az eredményt
  (pl. amikor két klánból szándékozunk adatokat gyűjteni, azonnal
  a másikra ugorva). Megjegyzés: ha a klánnak hatalmas mennyiségű faluja van, túl
  sok tárhelyet foglalhat el a localStorage-ban (~max 5MB), ezért a korlát 1MB,
  ha a kimenet > 1MB, a localStorage-ba mentés kihagyásra kerül.

- **cacheTime**: <number> (alapértelmezett: `5`) az eredmény tárolásának ideje
  a böngészőben, percekben.

- **removedPlayers**: <string> (alapértelmezett: `""`) ide írjuk be azoknak a játékosoknak a beceneveit,
  akiktől nem akarunk csapatinformációkat gyűjteni, pontosvesszővel elválasztva, mint
  a játékbeli üzenetekben, pl. "Rafsaf;kmic;valakimás"

- **allowedPlayers**: <string> (alapértelmezett: `""`) ide írjuk be azoknak a játékosoknak a beceneveit,
  akiktől CSAK! (ha üres, a klán összes játékosa használva lesz) csapatinformációkat akarunk
  gyűjteni, pontosvesszővel elválasztva, mint a játékbeli üzenetekben,
  pl. "Rafsaf;kmic;valakimás"

- **language**: <string> (alapértelmezett: `"pl"`) ennek `"en"`-nek vagy `"pl"`-nek kell lennie, ha bármi
  mást használunk, a szkript angolt fog használni

- **showNicknamesTroops**: <boolean> (alapértelmezett: `false`) ha true-ra van állítva, akkor
  minden sor elején megjelenik a játékos beceneve is,
  csak a Csapatok fülön érvényes, hasonlóan a showNicknamesDeff-hez

- **showFirstLineTroops**: <boolean> (alapértelmezett: `false`) ha true-ra van állítva, akkor
  az eredmény tetején egy további sor jelenik meg, amelyet a
  firstLineDeff változó határoz meg, csak a Csapatok fülön érvényes, hasonlóan a showFirstLineDeff-hez

- **firstLineTroops**: <string> (alapértelmezett: `""`) sor, amely az eredmény tetején jelenik meg,
  ha a showFirstLineTroops true, csak a Csapatok fülön érvényes, hasonlóan a
  showNicknamesDeff-hez

- **showNicknamesDeff**: <boolean> (alapértelmezett: `false`) ha true-ra van állítva, akkor
  minden sor elején megjelenik a játékos beceneve is,
  csak a Védelem fülön érvényes, hasonlóan a showNicknamesTroops-hoz

- **showFirstLineDeff**: <boolean> (alapértelmezett: `false`) ha true-ra van állítva, akkor
  az eredmény tetején egy további sor jelenik meg, amelyet a
  firstLineDeff változó határoz meg, csak a Védelem fülön érvényes, hasonlóan a showFirstLineTroops-hoz

- **firstLineDeff**: <string> (alapértelmezett: `""`) sor, amely az eredmény tetején jelenik meg,
  ha a showFirstLineTroops true, csak a Védelem fülön érvényes, hasonlóan
  a firstLineTroops-hoz
