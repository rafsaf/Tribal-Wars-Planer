---
title: "Ničivé osnovy - Průvodce"
date: 2026-02-28
---

V tomto průvodci se dozvíte, jak plánovat ničivé akce, konkrétně zaměřené na pozdější fáze světa. Poznámka: Předpokládá se plná znalost [Prvních kroků s Plánovačem](./../first_steps/index.md)! Doporučuje se také nejprve si přečíst dva krátké předchozí průvodce v této sekci, konkrétně [Jak zadávat a ukládat cíle akce](./two_regions_of_the_tribe.md) a [Dvě oblasti kmene, aneb Co je fronta a zázemí](./two_regions_of_the_tribe.md).

!!! hint

    Vždy začněte plánovat jakoukoli akci na této stránce spočítáním všech jednotek a jejich rozdělením na jednotky Fronty a Zázemí v souladu s povahou konkrétního plánu. K tomuto účelu použijte záložku 1. Dostupné jednotky a výsledky jsou uvedeny v tabulce pod cíli.

Akce se vytváří v poli **Obléhací jednotky** vedle cílů. Nastavení v záložce {==6. Obléhací jednotky==} určují pořadí budov k zničení a minimální počet katapultů, který musí vesnice mít, aby se kvalifikovala pro ničitelské útoky. Přesný průběh ničení vychází z vestavěných tabulek ničení, takže plánovač kontroluje zbylý level po každém útoku a posílá jen tolik katapultů, kolik je potřeba pro další přesný krok.

Příklad cílů ničení a výsledků v tabulce, s 3 off jednotkami a *50 obléhacími jednotkami:

![alt text](image-24.png){ width="600" }

Příklad nastavení ničivé akce, cílící na 3 viditelné budovy v tomto pořadí:

![alt text](image-25.png){ width="600" }

Počet dostupných obléhacích jednotek můžete odhadnout pomocí záložky {==1. Dostupné jednotky==} a jednoduché matematiky. Po každém obnovení naleznete celkový počet katapultů připravených k plánování v tabulce pod **Počet všech dostupných katapultů**. Stačí se rozhodnout, na kolik cílů budou stačit.

Příklad naplánované mini-akce s různým počtem katapultů od 200 do 50:

![alt text](image-26.png){ width="600" }

## Přesný výběr katapultů pro ničení

Vesnice s více dostupnými katapulty jsou přiřazeny první, ale plánovač nepoužívá samostatný maximální limit katapultů. Namísto toho vždy používá přesnou tabulku ničení pro vybraný typ vesnice. Stejná logika se používá pro pass ruin-off i pro ruin útoky, takže přesný zbylý level budovy po každém zásahu se porovnává s tabulkou a plánovač pokračuje, dokud není budova zničena na úroveň 0, pokud je to potřeba.

To znamená, že planner po každém zásahu zkontroluje přesný zbývající level budovy a pokračuje podle dalšího správného kroku v tabulce. Pokud je k dispozici více katapultů, než tabulka vyžaduje, budova se zničí na úroveň 0, pokud je to potřeba.

## Off jednotky před obléhacími jednotkami

Off jednotky plánované před útoky na ničení sdílejí stejný harmonogram poškození budov jako pozdější ruin útoky. Jejich objednávky zůstávají standardní OFF, ale jejich katapulty posouvají stav budovy cíle ničení.

## Pořadí ničení budov

V nastavení {==6. Ničení==} můžeme změnit pořadí budov k zničení. Je důležité si pamatovat, že budovy, které nejsou v tomto seznamu, budou přeskočeny, a algoritmus se zastaví ve dvou případech: buď už nejsou žádné katapulty k naplánování, nebo všechny uvedené budovy již byly zničeny. To znamená, že i když se rozhodneme napsat `000|000:0:1000`, 1000 obléhacích jednotek pravděpodobně nebude naplánováno – jakmile jsou uvedené budovy zničeny, Plánovač přejde k dalším krokům (např. k dalšímu cíli a podobně).

## Vidím 10 000 dostupných katapultů. Kolik je to cílů?

Odpověď zní: záleží. Hlavně na zvoleném pořadí budov. Předpokládejme, že je vybrána pouze jedna budova, **[ Kovárna ]**. V tomto případě stačí 200-250 katapultů (např. 200 a 50, nebo 100, 100, nebo 50, 50, 50, 50 atd.) k zničení jedné vesnice, takže můžete naplánovat 40-50 cílů. Pokud jsou vybrány dvě budovy, **[ Kovárna, Farma ]**, budete potřebovat 200-250 katapultů na Kovárnu a 500-700 katapultů na Farmu (např. 14x 50, nebo 5x 100, 4x 150, 3x 200 katapultů, nebo mnoho dalších kombinací), což znamená 700-950 katapultů na vesnici, neboli 10-14 cílů. Níže je jednoduchá tabulka pro 30-úrovňové budovy (jako jsou Farmy, Sklady, všechny eko-budovy) a 20-úrovňové budovy (Hlavní budova, Kovárna), která pomůže vypočítat, kolik cílů je možných.

|                    | Počet katapultů potřebných k úplnému zničení budovy |
| ------------------ | --------------------------------------------------- |
| 20-úrovňové budovy | 200-250                                             |
| 30-úrovňové budovy | 500-700                                             |

## Velikost vesnice a tabulka ničení

Přesná tabulka ničení se vybírá podle bodů vesnice. Vesnice nad 8 000 body používají rozpad budov pro velké vesnice, zatímco vesnice na 8 000 a méně používají průběh pro střední vesnice. Jinými slovy, vesnice není posuzována podle redundantního pole maximálního počtu katapultů; její bodová hodnota říká plánovači, kterou tabulku použít.

## Shrnutí

Pamatujte, že v jádru je plánování stále založeno na jednoduchém chamtivém algoritmu, a tak Plánovač **VŽDY** přiřazuje obléhací jednotky, fejky nebo off jednotky velmi podobným způsobem. Pokud chcete, aby off jednotky nebo obléhací jednotky byly nerozeznatelné od fejků, musíte naplánovat hodně fejků. Při plánování ničení stojí za to povolit možnost **Fejky ze všech vesnic** v {==Záložce 3. Výchozí nastavení akce==}, která na rozdíl od výchozího nastavení přiřazuje fejky ze všech zadních vesnic.

Důležitým posledním detailem je, že plánování ničení nyní vychází z přesných hodnot tabulky místo zjednodušených heuristik, takže chování je přesnější a snadněji předvídatelné. Zvažte počet katapultů a budov, které stojí za zničení, a naplánujte dostatek fejků. Užijte si demolici!

---

Dejte mi vědět, pokud potřebujete další podrobnosti nebo změny!
