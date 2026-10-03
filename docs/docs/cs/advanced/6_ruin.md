---
title: "6. Ničení"
date: 2026-02-28
---

Tato karta obsahuje několik nastavení souvisejících s demoličními akcemi.

Vzhled karty:

![alt text](image-8.png){ width="600" }

V možnosti **1.** se nastavuje pořadí budov, které mají být zničeny. Plánovač naplánuje útoky na ně v zadaném pořadí a ignoruje všechny přeskočené budovy.

Pod **2.** nastavíme minimální počet katapultů, které musí vesnice mít, aby se kvalifikovala pro ničitelský útok. Neexistuje samostatné pole pro maximální počet katapultů. Plánovač používá přesnou tabulku ničení pro vybraný typ vesnice, takže posílá pouze tolik katapultů, kolik je potřeba pro další přesný krok nebo pro zničení budovy na úroveň 0, pokud je k dispozici více katapultů než tabulka obsahuje.

V **3.** vybereme počet off jednotek v ničitelských útocích, které mají být poslané spolu s katapulty.

Úrovně budov se odvozují od bodů zdrojové vesnice. Vesnice nad 8 000 bodů používají průběh ničení pro velké vesnice, zatímco vesnice na 8 000 a méně používají průběh pro střední vesnice. Přesný zbylý level po každém kroku ničení se bere z vestavěných tabulek ničení a plánovač po každém zásahu zkontroluje tento výsledek, aby určil správný další krok. Pokud je k dispozici více katapultů než tabulka vyžaduje, pokračuje v ničení až do úrovně 0, pokud je to potřeba.
