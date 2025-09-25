# 7. lépés - Eredmények fül

<figure markdown="span">
  ![alt text](image-11.png)
  <figcaption>Eredmények fül.</figcaption>
</figure>

| Szám | Leírás                                                                                                                          |
| ---- | ------------------------------------------------------------------------------------------------------------------------------- |
| 1    | Táblázat a játékosok célpontjaihoz és a küldési linkekhez, valamint egy űrlap a küldött üzenetek tartalmának megváltoztatásához |
| 2    | Rövid szöveges összefoglaló a becenevekről és a célpontokról                                                                    |
| 3    | Szövegmező linkekkel, amelyeket manuálisan lehet elküldeni a játékosoknak                                                       |
| 4    | Terv eredményei teljes szövegként (minden játékos)                                                                              |
| 5    | Fel nem használt csapatok a következő tervhez (PRÉMIUM)                                                                         |
| 6    | A VÉDELEM GYŰJTÉSE fülről származó védelemgyűjtés eredményei                                                                    |
| 7    | Űrlap a küldött üzenet tartalmához és más játékosok parancsainak elrejtéséhez                                                   |
| 8    | Táblázat a ehhez a tervhez elérhető régi linkekkel                                                                              |
| 9    | Ez a link egy egyedi oldalra visz a játékos célpontjaival                                                                       |
| 10   | Manuális lehetőség más játékosok parancsainak láthatóságának megváltoztatására                                                  |
| 11   | Link üzenet küldéséhez a játékban, ehhez szükséges a [Szkript üzenetek küldéséhez](./../scripts/sending_messages.md)            |

!!! info

    Minden játékos számára létrehoztunk egy {==EGYEDI URL-t==}, ahol csak az ő célpontjaik jelennek meg, a jegyzetekbe illeszthető szöveggel és a parancsaik grafikus bemutatásával együtt. Ezeket a 9-es gombra kattintva érheti el a fenti képen. A linkjükre kattintva a játékos mindent megkap, amire szüksége van a tervben szereplő csapatok elküldéséhez.

A {==Cím, szöveg beállítása és rejtett érték megjelenítése==} kibontásával, ami a 7-es szám, megadhatja a játékosoknak küldött üzenet tartalmát, és azt, hogy a játékosok lássák-e más játékosok parancsait az egyéni célpontjaik részleteiben. Alapértelmezés szerint a Rejtett megjelenítése - Hamis azt jelenti, hogy csak a saját parancsaikat látják, és mások parancsait csak akkor, ha közeli nemesekkel támadják azt a falut. A Rejtett megjelenítése - Igaz beállítás lehetővé teszi a játékosok számára, hogy mindenki más parancsát lássák. A 8-as szám alatt található egy táblázat az összes létrehozott linkkel; minden terv megerősítése után újak jönnek létre, míg a régiek ebbe a fülbe kerülnek (de aktívak maradnak!).

Megjegyzés! Az idő múlásával és az alkalmazás fejlődésével az eltávolítható linkeket (és maradnak is) nem eltávolítható linkekre cseréltük, amelyeket a felhasználó nem tud megváltoztatni vagy letiltani, például rossz személynek való küldés után. Ez a konvenció biztosítja, hogy az ütemező ne törölje véletlenül a már elküldött linkeket, ami nagy félreértéseket okozna. A linkek 30 napig aktívak, függetlenül attól, hogy a terv még létezik-e vagy törölték.
