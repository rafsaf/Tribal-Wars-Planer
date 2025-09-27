# Krok 7 - Záložka s výsledky

<figure markdown="span">
  ![alt text](image-11.png)
  <figcaption>Záložka s výsledky.</figcaption>
</figure>

| Číslo | Popis                                                                                                        |
| ----- | ------------------------------------------------------------------------------------------------------------ |
| 1     | Tabulka s odkazy na cíle hráčů a odkazy pro odeslání, stejně jako formulář pro změnu obsahu odeslaných zpráv |
| 2     | Krátké textové shrnutí přezdívek a cílů                                                                      |
| 3     | Textové pole s odkazy, které lze ručně poslat hráčům                                                         |
| 4     | Výsledky osnovy jako plný text k odeslání (všichni hráči)                                                    |
| 5     | Nevyužité jednotky pro další osnovu (PREMIUM)                                                                |
| 6     | Výsledky sběru obrany ze záložky SBĚR OBRANY                                                                 |
| 7     | Formulář pro obsah odeslané zprávy a skrytí příkazů ostatních hráčů                                          |
| 8     | Tabulka se starými odkazy dostupnými pro tuto osnovu                                                         |
| 9     | Tento odkaz vás zavede na jedinečnou stránku s cíli hráče                                                    |
| 10    | Ruční možnost změny viditelnosti příkazů ostatních hráčů                                                     |
| 11    | Odkaz pro odeslání zprávy ve hře, vyžaduje [Skript pro odesílání zpráv](./../scripts/sending_messages.md)    |


!!! info

    Pro každého hráče byla vytvořena {==UNIKÁTNÍ URL==}, kde jsou prezentovány pouze jeho cíle spolu s textem k vložení do poznámek a grafickou prezentací jeho příkazů. Můžete se k nim dostat kliknutím na tlačítko 9 na výše uvedeném obrázku. Po zadání svého odkazu má hráč vše, co potřebuje k odeslání jednotek naplánovaných v osnově.


Rozbalením {==Nastavit název, text a zobrazit skrytou hodnotu==}, což je číslo 7, určíte obsah zprávy odeslané hráčům a zda mají hráči vidět příkazy ostatních hráčů v detailech svých jednotlivých cílů. Ve výchozím nastavení Zobrazit skryté - Nepravda znamená, že vidí pouze své příkazy a příkazy ostatních pouze v případě, že útočí na danou vesnici se šlechtici zblízka. Nastavení Zobrazit skryté - Pravda umožňuje hráčům vidět všechny příkazy ostatních. Pod číslem 8 naleznete tabulku se všemi vytvořenými odkazy; po každém potvrzení osnovy se vytvoří nové, zatímco staré přejdou do této záložky (ale zůstávají aktivní!).

Pozor! Postupem času a s vývojem aplikace byly odstranitelné odkazy změněny (a zůstanou) na neodstranitelné odkazy, které uživatel nemůže změnit ani zablokovat přístup k nim, například po odeslání nesprávné osobě. Tato konvence zajišťuje, že plánovač omylem nesmaže již odeslané odkazy, což by způsobilo velké nedorozumění. Odkazy jsou aktivní 30 dní, bez ohledu na to, zda osnova stále existuje nebo byla smazána.
