# Skript pro sběr armády a obrany

| Server          | Fórum Tribal Wars                                                                                                                                                    | Povoleno | Kód                                                                                                                  |
| --------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------- | -------------------------------------------------------------------------------------------------------------------- |
| tribalwars.net  | [https://forum.tribalwars.net/index.php?threads/collect-troops-script.292893/](https://forum.tribalwars.net/index.php?threads/collect-troops-script.292893/)         | ANO      | [Kód na GitHubu (v2.1)](https://github.com/rafsaf/scripts_tribal_wars/blob/2024-09-09-2/src/collect_troops_v2.1.ts)  |
| plemiona.pl     | [https://forum.plemiona.pl/index.php?threads/zbi%C3%B3rka-wojska-i-obrony.128630/](https://forum.plemiona.pl/index.php?threads/zbi%C3%B3rka-wojska-i-obrony.128630/) | ANO      | [Kód na GitHubu (v2)](https://github.com/rafsaf/scripts_tribal_wars/blob/2024-09-01/public/collect_troops_v2.js)     |
| ostatní servery | -                                                                                                                                                                    | NE       | [Kód na GitHubu (v2.3)](https://github.com/rafsaf/scripts_tribal_wars/blob/2025-09-22/public/collect_troops_v2.3.js) |

!!! warning

    Používání na jiných jazykových verzích hry, **kde skript není povolen** podporou, může vést k zablokování účtu. Používejte na vlastní nebezpečí.

=== "tribalwars.net"

    ```title="Skript pro sběr armády a obrany"
    --8<-- "army_script_tribalwars_net_en.txt"
    ```

=== "plemiona.pl"

    ```title="Skript pro sběr armády a obrany"
    --8<-- "army_script_plemiona_pl_en.txt"
    ```

=== "ostatní servery"

    ```title="Skript pro sběr armády a obrany"
    --8<-- "army_script_latest.txt"
    ```

## Instalace

Postupuje se stejně jako u všech skriptů pro lištu; je třeba vložit obsah do nově vytvořeného skriptu pro lištu ve hře.

## Návod k použití

1. Vytvořte skript pro lištu, klikněte na něj
2. Počkejte na výsledek
3. Přejděte na vybraný plán
4. Vložte data a potvrďte

![Příklad výstupu skriptu](image-2.png)

## Popis

Po kliknutí se uprostřed obrazovky objeví "čítač" s postupem, poté výsledek v okně. Funguje jak v záložce Armáda, tak v záložce Obrana. Výchozí nastavení pro kopírování má cache nastaveno na true a cacheTime na 5 minut. Během této doby skript vypíše výsledek uložený v prohlížeči, místo aby znovu procházel všechny členy a sbíral data. V případě pochybností, zda se jedná o nový nebo starý výsledek, se dole zobrazí datum sběru.

Data vygenerovaná spuštěním skriptu by měla být vložena do plánu na webu.

Možnosti:

Konfigurace probíhá pomocí objektu **COLLECT_TROOPS_DATA_V2**. Všimněte si, že každý parametr JE VOLITELNÝ, pokud jsou obě proměnné
nedefinované nebo jsou definované, ale neobsahují žádné klíče, budou použity
rozumné výchozí hodnoty.

- **cache**: <boolean> (výchozí: `true`) je zodpovědný za ukládání výsledku
  v prohlížeči, aby se náhodou nekliklo několikrát za sebou a
  nezatěžovaly se herní servery, nastavení cache: false způsobí, že se výsledek neuloží
  (např. když máme v úmyslu sbírat data ze dvou kmenů a okamžitě přejít
  na druhý). Poznámka: pokud má kmen obrovské množství vesnic, může to zabrat příliš
  mnoho místa v localStorage (~max 5MB), kvůli tomu je limit 1MB,
  pokud je výstup > 1MB, uložení do localStorage bude přeskočeno.

- **cacheTime**: <number> (výchozí: `5`) je doba uložení výsledku v
  prohlížeči, v minutách.

- **removedPlayers**: <string> (výchozí: `""`) zde zadáváme přezdívky hráčů,
  od kterých nechceme sbírat informace o jednotkách, oddělené středníky jako v
  zprávách ve hře, např. "Rafsaf;kmic;někdojiný"

- **allowedPlayers**: <string> (výchozí: `""`) zde zadáváme přezdívky hráčů,
  od kterých POUZE! (pokud je prázdné, budou použiti všichni hráči v kmeni) chceme
  sbírat informace o jednotkách, oddělené středníky jako v zprávách ve hře,
  např. "Rafsaf;kmic;někdojiný"

- **language**: <string> (výchozí: `"pl"`) toto by mělo být `"en"` nebo `"pl"`, pokud je
  použito něco jiného, skript použije angličtinu

- **showNicknamesTroops**: <boolean> (výchozí: `false`) pokud je nastaveno na true, způsobí, že
  na každém řádku se na jeho začátku navíc objeví přezdívka hráče,
  platí pouze v záložce Jednotky, podobně jako showNicknamesDeff

- **showFirstLineTroops**: <boolean> (výchozí: `false`) pokud je nastaveno na true, způsobí, že
  k výsledku bude přidán další řádek nahoře, který je specifikován
  proměnnou firstLineDeff, platí pouze v záložce Jednotky, podobně jako showFirstLineDeff

- **firstLineTroops**: <string> (výchozí: `""`) řádek, který se zobrazí nahoře ve výsledku,
  když je showFirstLineTroops true, platí pouze v záložce Jednotky, podobně jako
  showNicknamesDeff

- **showNicknamesDeff**: <boolean> (výchozí: `false`) pokud je nastaveno na true, způsobí, že
  na každém řádku se na jeho začátku navíc objeví přezdívka hráče,
  platí pouze v záložce Obrana, podobně jako showNicknamesTroops

- **showFirstLineDeff**: <boolean> (výchozí: `false`) pokud je nastaveno na true, způsobí, že
  k výsledku bude přidán další řádek nahoře, který je specifikován
  proměnnou firstLineDeff, platí pouze v záložce Obrana, podobně jako showFirstLineTroops

- **firstLineDeff**: <string> (výchozí: `""`) řádek, který se zobrazí nahoře ve výsledku,
  když je showFirstLineTroops true, platí pouze v záložce Obrana, podobně
  jako firstLineTroops
