---
title: "Skript pro sběr armády a obrany"
date: 2026-09-09
---

## Instalace

V současné době je jedinou podporovanou možností instalace použití **oficiální knihovny skriptů** (Nastavení -> Knihovna skriptů). Hledejte ho podle autora – Rafsaf nebo podle názvu.

![Pohled do knihovny skriptů](image-5.png)

| Server             | Název v knihovně skriptů       | Autor  | Kód                                                                                                                            |
| ------------------ | ------------------------------ | ------ | ------------------------------------------------------------------------------------------------------------------------------ |
| plemiona.pl        | Zbiórka Wojska i Obrony        | Rafsaf | [Kód na GitHubu (v20260218)](https://github.com/rafsaf/scripts_tribal_wars/blob/2026-02-18/public/collect_troops_v20260218.js) |
| tribalwars.net     | Collect troops script          | Rafsaf | [Kód na GitHubu (v20260218)](https://github.com/rafsaf/scripts_tribal_wars/blob/2026-02-18/public/collect_troops_v20260218.js) |
| guerretribale.fr   | Script de collecte des troupes | Rafsaf | [Kód na GitHubu (v20260218)](https://github.com/rafsaf/scripts_tribal_wars/blob/2026-02-18/public/collect_troops_v20260218.js) |
| tribals.it         | Raccolta delle truppe          | Rafsaf | [Kód na GitHubu (v20260218)](https://github.com/rafsaf/scripts_tribal_wars/blob/2026-02-18/public/collect_troops_v20260218.js) |
| guerrastribales.es | Script de colector de tropas   | Rafsaf | [Kód na GitHubu (v20260218)](https://github.com/rafsaf/scripts_tribal_wars/blob/2026-02-18/public/collect_troops_v20260218.js) |
| ostatní servery    | -                              | -      | [Kód na GitHubu (v20260218)](https://github.com/rafsaf/scripts_tribal_wars/blob/2026-02-18/public/collect_troops_v20260218.js) |

!!! warning

    Skript je dostupný na mnoha jazykových verzích – nahlaste problém přes podporu na svém serveru, aby byl přidán, pokud není výše uveden. Používání na jiných jazykových verzích hry, **kde skript není povolen** podporou, může vést k zablokování účtu. Používejte na vlastní nebezpečí.

=== "Podporované servery"

    Instalace pouze přes knihovnu skriptů!

=== "Ostatní servery"

    ```title="Skript pro sběr armády a obrany"
    --8<-- "army_script_latest.txt"
    ```

## Návod k použití

1. Vytvořte skript pro lištu, přejděte do pohledu kmene a klikněte na něj
2. Změňte nastavení (volitelně) a stiskněte Spustit
3. Počkejte na výsledek
4. Přejděte na vybraný plán
5. Vložte data a potvrďte

Nastavení:

![Pohled nastavení](image-6.png)

Výsledek:

![Příklad výstupu skriptu](image-2.png)

## Popis

Po kliknutí se uprostřed obrazovky objeví "čítač" s postupem a poté výsledek v okně. Funguje jak v záložce Armáda, tak v záložce Obrana. Výchozí nastavení pro kopírování má `Mezipaměť` zapnutou a `Doba cache` nastavenou na 5 minut. Během této doby skript vypíše výsledek uložený v prohlížeči, místo aby znovu procházel všechny členy a sbíral data. V případě pochybností, zda se jedná o nový nebo starý výsledek, se dole zobrazí datum sběru.

Data vygenerovaná spuštěním skriptu by měla být vložena do plánu na webu.

Možnosti:

- **Mezipaměť**: <boolean> (výchozí: `true`) je zodpovědná za ukládání výsledku v prohlížeči, aby se náhodou neklikalo několikrát za sebou a nezatěžovaly se herní servery. Pokud nastavíte `false`, skript nebude ukládat výsledek do prohlížeče (užitečné například když chcete sbírat data ze dvou kmenů a okamžitě přejít na druhý). Poznámka: pokud má kmen obrovské množství vesnic, může to zabrat příliš mnoho místa v `localStorage` (~max 5MB), kvůli tomu je limit 1MB. Pokud je výstup > 1MB, uložení do `localStorage` bude přeskočeno.

- **Doba cache**: <number> (výchozí: `5`) je doba uložení výsledku v prohlížeči, v minutách.

- **Vynechaní hráči**: <string> (výchozí: `""`) zde zadáváte přezdívky hráčů, od kterých nechcete sbírat informace o přehledu, oddělené středníky jako v zprávách ve hře, např. "Rafsaf;kmic;někdo jiný".

- **Povolení hráči**: <string> (výchozí: `""`) zde zadáváte přezdívky hráčů, od kterých chcete sbírat informace o přehledu JENOM! Ostatní budou přeskočeni, přezdívky jsou oddělené středníky jako v zprávách ve hře, např. "Rafsaf;kmic;někdo jiný". Poznámka: výchozí hodnota `""` má speciální význam a znamená, že chcete sbírat přehled od všech hráčů.

- **Zobrazit přezdívky**: <boolean> (výchozí: `false`) pokud je hodnota `true`, přidá se do výsledku sběru Armády na začátek každé řádky přezdívka hráče, podobně jako pro záložku Obrana.

- **Zobrazit první řádek**: <boolean> (výchozí: `false`) pokud je hodnota `true`, přidá se k výsledku sběru Armády hlavička (první řádek nahoře), jejíž hodnota je nastavena v dalším parametru `Text prvního řádku`.

- **Text prvního řádku**: <string> (výchozí: `""`) hodnota, která se přidá do hlavičky ve výsledku sběru Armády, pokud je `Zobrazit první řádek` nastaveno na `true`.

- **Zobrazit přezdívky**: <boolean> (výchozí: `false`) pokud je hodnota `true`, přidá se do výsledku sběru Obrany na začátek každé řádky přezdívka hráče, podobně jako pro záložku Armáda.

- **Zobrazit první řádek**: <boolean> (výchozí: `false`) pokud je hodnota `true`, přidá se k výsledku sběru Obrany hlavička (první řádek nahoře), jejíž hodnota je nastavena v dalším parametru `Text prvního řádku`.

- **Text prvního řádku**: <string> (výchozí: `""`) hodnota, která se přidá do hlavičky ve výsledku sběru Obrany, pokud je `Zobrazit první řádek` nastaveno na `true`.
