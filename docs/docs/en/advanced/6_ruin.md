---
title: "6. Ruining"
date: 2026-02-28
---

This tab contains several settings related to demolition actions.

Tab appearance:

![alt text](image-8.png){ width="600" }

In option **1.**, the order of buildings to be demolished is set. The Planer schedules attacks on them in the specified order, ignoring any skipped buildings.

Under **2.**, we set the minimum number of catapults a village must have to qualify for a ruin attack. There is no separate maximum-catapult setting anymore. The planner follows the exact ruin table for the selected source village type, so it sends only the catapults needed to reach the next exact step or to destroy the building to level 0 when available catapults exceed the table.

In **3.**, we choose the number of off units in ruin attacks that should be sent along with the catapults.

The building levels are inferred from the source village points. Villages above 8,000 points use the large-village ruin progression, while villages at or below 8,000 points use the medium-village progression. The exact remaining level after each ruin step comes from the built-in ruin tables, and the planner checks that value after every hit to choose the next correct step. If the available catapults exceed the table, it keeps going until the building is reduced to level 0 when needed.