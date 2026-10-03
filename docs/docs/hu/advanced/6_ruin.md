---
title: "6. Rombolás"
date: 2026-02-28
---

Ez a fül számos, a rombolási műveletekkel kapcsolatos beállítást tartalmaz.

A fül megjelenése:

![alt text](image-8.png){ width="600" }

Az **1.** opcióban a lerombolandó épületek sorrendje állítható be. A Tervező a megadott sorrendben ütemezi a támadásokat, figyelmen kívül hagyva a kihagyott épületeket.

A **2.** alatt beállítjuk a minimum katapultmennyiséget, amelyet egy falu legalább rendelkezésre kell bocsátson a rombolási támadáshoz. Nincs külön max katapultmező. A tervező a kiválasztott falu típusának pontos rombolási táblázatát követi, ezért csak annyi katapultot küld, amennyi a következő pontos lépéshez szükséges, vagy amennyire szükség van az épület 0 szintre való lerombolásához, ha több katapult áll rendelkezésre, mint a táblázat tartalmaz.

A **3.** pontban kiválaszthatjuk a rombolási támadásokban a katapultokkal együtt küldendő OFF egységek számát.

Az épületszintek a forrásfalu pontjaiból származnak. A 8 000 pont feletti falvak a nagy falvak rombolási progresszióját használják, míg a 8 000 pont vagy alatti falvak a közepes falvak progresszióját. A rombolás minden lépése után megmaradó pontos szintet a beépített rombolási táblázatok adják, és a tervező minden találat után ellenőrzi ezt az értéket, hogy kiválassza a következő helyes lépést. Ha több katapult áll rendelkezésre, mint amennyire a táblázat szüksége van, folytatja a rombolást addig, amíg az épület 0 szintre nem csökken, ha ez szükséges.
