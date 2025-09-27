# 4. Morálka

Karta slouží k ovládání hodnot morálky při plánování akcí.

Nastavení:

![alt text](image-5.png){ width="600" }

Poznámka: Ve výchozím nastavení je tato možnost v každé akci zakázána, ale toto chování můžete změnit v Menu -> Můj účet.

První pole "Použít pouze útočníky NAD touto hodnotou morálky" slouží k rozhodnutí, jaká je nejnižší přijatelná hodnota morálky pro akci. Často to bude hodnota mezi 90-100, v závislosti na fázi světa, cílech akcí atd. Dopad na výsledek akce je takový, že pro daný cíl (každý jednotlivě!) je seznam všech přípustných vesnic, ze kterých by mohly být naplánovány útoky, filtrován a vyloučeny jsou všechny, které nesplňují naše požadavky na morálku.

Takže teoreticky, pokud máme mezi mnoha cíli několik hráčů s malým počtem bodů, útoky na ně budou naplánovány od hráčů v kmeni také s menším počtem bodů.

V extrémních situacích můžete odškrtnout druhou možnost "Zohlednit morálku v tomto přehledu", což má za následek, že morálka nebude brána v úvahu.

Všimněte si, že v kmenech existují tři nastavení morálky v pořadí popularity: bodová, bodová a časová a žádná morálka:

1. Bodová morálka

    Pro nejoblíbenější nastavení je morálka založena pouze na bodech útočícího a bránícího hráče, což Plánovač přesně implementuje, i když počáteční ochrany přítomné na některých světech nejsou zohledněny (ačkoli plánování akcí s Plánovačem na vesnice hráčů, kteří jsou na světě méně než například 2 týdny, se zdá nepravděpodobné).

2. Bodová a časová morálka

    V tomto případě se kromě bodů morálka zvyšuje úměrně k času obránce na světě, až do maximální hodnoty 50 %. Hra tento typ dat neposkytuje. Plánovač však sbírá data ze všech světů na všech herních serverech po mnoho let, proto jsou data týkající se času hráčů na světě brána (z interní databáze udržované v rámci stránky). Výsledek by měl být přesný a v souladu s hrou.

3. Žádná morálka

    V tomto případě je karta neaktivní a otázka morálky je ignorována.
