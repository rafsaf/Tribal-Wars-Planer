# 1. Dostupné jednotky a popis tabulky

Tato karta slouží k rozdělení vesnic našeho kmene na Frontové a Týlové. Jelikož je pochopení tohoto zásadní pro používání stránky, část jejího popisu naleznete v jiných kartách, včetně tohoto článku:
[Dvě oblasti kmene: co jsou Frontová a Týlová linie](./../primary/two_regions_of_the_tribe.md).

![alt text](image.png)

- **Min. počet off jednotek** a **Max. počet off jednotek**

    Zadejte rozsah velikosti útoků (vzhledem k populaci na farmě), které by měly být naplánovány.

    Například, pokud je rozsah 10 000-12 000, Plánovač přeskočí jak útoky větší než 12 000, tak menší než 10 000. Maximální počet zohledněných zvědů je 200; jakýkoli vyšší počet bude ignorován. Šlechtici se počítají jako x6 jednotek pouze v případě, že **je více útočných jednotek než obranných**. Přesný kód naleznete [zde](https://github.com/rafsaf/Tribal-Wars-Planer/blob/ecc7ff31ed122928a7aea6199af4a0f9ce4718fd/utils/basic/army.py#L242-L250).

- **Minimální vzdálenost od frontové linie**

    Hodnota v polích použitá k výpočtu frontové linie, na základě které jsou určeny frontové vesnice. Přesný kód pro rozdělení na Frontovou/Týlovou/Vnější linii naleznete [zde](https://github.com/rafsaf/Tribal-Wars-Planer/blob/ecc7ff31ed122928a7aea6199af4a0f9ce4718fd/utils/basic/cdist_brute.py#L83-L99). Celou intuici za tímto rozdělením naleznete v průvodci [Dvě oblasti kmene: co jsou Frontová a Týlová linie](./../primary/two_regions_of_the_tribe.md).

- **Max. vzdálenost pro šlechtice**

    Ve výchozím nastavení je to maximální hodnota vzdálenosti v polích pro daný svět. Není možné nastavit vyšší hodnotu (takové útoky by nebylo možné poslat).

- **Max. vzdálenost pro offy a ruiny**

    Plánovač nepřiřadí útoky z vesnic, které jsou od nepřítele dál než tato hodnota. Používá se také k přibližnému určení počtu vesnic v oblasti "Vnější", tedy těch, které budou přeskočeny.

- **Vyloučené souřadnice nepřátelských vesnic (osamocené vesnice)**

    Zadejte všechny nepřátelské mrtvé účty na území našeho kmene. **Stojí za to** to udělat, protože s **Minimální vzdáleností od frontové linie** například 10 polí bude všechno v okruhu 10 polí od nepřátelských mrtvých účtů přirozeně považováno za frontovou linii a útoky z této oblasti budou v plánu přeskočeny. Někdy je však lepším rozhodnutím ponechat útoky kolem ostrovů pro místní použití a nezadávat sem nepřátelské mrtvé účty.
