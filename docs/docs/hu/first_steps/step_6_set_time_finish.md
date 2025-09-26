# 6. lépés - Érkezési idők beállítása és a terv befejezése

!!! info

    Miután áttekintette az összes fület és esetleg végrehajtott műveleteket az egyes célpontok szerkesztésében, végül a terv befejezéséhez lépjen az utolsó, időpontokat tartalmazó fülre.

<figure markdown="span">
  ![alt text](image-8.png)
  <figcaption>Idők fül, használhatja a fenti nagyon egyszerű időt és kattintson a "Létrehozás" gombra</figcaption>
</figure>

A felhasználónak lehetősége van több érkezési idő objektumot létrehozni a fülön, de a gyakorlatban akár egy vagy néhány is elegendő lehet. Kiválasztjuk a támadások időintervallumait, az egységet és a módot 3 lehetséges opció közül. Egy összetett idő példája így nézhet ki:

<figure markdown="span">
  ![alt text](image-9.png)
  <figcaption>1. példa</figcaption>
</figure>

Ami azt jelenti:

- Ütemezzen egy véletlenszerű számú támadást 0 és 5 között 7:00 és 8:00 között (vagy kevesebbet, ha már felhasználták őket)

- Ütemezzen pontosan 3 támadást 8:00 és 8:10 között (vagy kevesebbet, ha már felhasználták őket)

- Ütemezzen pontosan 4 nemest 8:10-kor (vagy kevesebbet, stb. mint fent)

- Ütemezze az összes megmaradt faltörő kost, ha van még, 12:00 és 12:30 között

- Ütemezze az összes megmaradt nemest 12:30-kor

Az is támogatott, hogy a {==Minden fennmaradó==} korábban legyen, mint a többi mód. Az alábbi példában a célpont mindig 2 támadást és 2 nemest kap a nap végén, és az összes többit (az összeg különböző falvaknál eltérően állítható be) reggel. A megadott időknek értelmesnek kell lenniük; a maximális érkezési időnek későbbinek vagy azonosnak kell lennie a minimális érkezési idővel. A Minden fennmaradó módnak pontosan kétszer kell megjelennie: a Faltörő kos és a Nemes egységeknél, és a legalacsonyabb prioritással rendelkezik.

<figure markdown="span">
  ![alt text](image-10.png)
  <figcaption>2. példa</figcaption>
</figure>

A tesztvilág céljaira létrehozhat egy egyszerű időt az első képről, és beállíthatja az összes célpontra a fül tetején. Ezután fejezze be a tervet a {==Terv befejezése==} gombra kattintva.

Automatikusan a következő, eredményeket tartalmazó fülre lép.
