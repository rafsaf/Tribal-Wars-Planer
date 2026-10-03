---
title: "Ruin Outlines - Guide"
date: 2026-02-28
---

In this guide, you will learn how to plan destruction actions, specifically aimed at the later stages of the world. Note: This assumes full knowledge of [First Steps with the Planer](./../first_steps/index.md)! It is also recommended to first read the two short previous guides in this section, namely [How to Input and Save Action Goals](./two_regions_of_the_tribe.md) and [The Two Regions of the Tribe, i.e., What is the Front and the Rear](./two_regions_of_the_tribe.md).

!!! hint

    Always start planning any action on this page by counting all the troops and dividing them into Front and Rear troops in accordance with the nature of the specific plan. For this purpose, use tab 1. Available Units, and the results are presented in a table below the goals.

The action is created in the **Siege Units** field next to the goals. The settings in tab {==6. Siege Units==} determine the order of buildings to be destroyed and the minimum catapult count required for a village to qualify for ruin attacks. The exact ruin progression comes from the built-in ruin tables, so the planner checks the remaining level after each attack and only sends the catapults needed for the next exact step.

Example of destruction goals and table results, with 3 off units and *50 siege units:

![alt text](image-24.png){ width="600" }

Example of destruction action settings, targeting 3 visible buildings in this order:

![alt text](image-25.png){ width="600" }

You can estimate the number of available siege units by using tab {==1. Available Units==} and simple math. After each refresh, you can find the total number of catapults ready for planning in the table under **Number of All Available Catapults**. You only need to decide how many targets they will be sufficient for.

Example of a planned mini-action with different numbers of catapults from 200 to 50:

![alt text](image-26.png){ width="600" }

## Exact Catapult Selection for Destruction

Villages with more available catapults are assigned first, but the planner does not use a separate maximum catapult limit. Instead, it always follows the exact ruin table for the selected village type. The same logic is used for the ruin-off pass and the ruin attack pass, so the exact remaining building level after each hit is checked against the table and the planner continues until the building is destroyed to level 0 when required.

This means the planner checks the exact remaining building level after each hit and follows the next correct step in the ruin table. If the available catapults exceed what the table needs, it continues until the building is destroyed to level 0 when required.

## Off Units Before Siege Units

Off units scheduled before the destruction attacks share the same building-damage schedule as the later ruin attacks. Their orders remain standard OFFs, but their catapults advance the ruin target's building state.

## Building Destruction Order

In settings {==6. Destruction==}, we can change the order of buildings to be destroyed. It is important to remember that buildings not included in this list are skipped, and the algorithm stops in two cases: either there are no more catapults to plan, or all listed buildings have already been destroyed. This means that even if we decide to write `000|000:0:1000`, 1000 siege units will likely not be planned—once the listed buildings are destroyed, the Planer moves on to the next steps (for example, the next goal, and so on).

## I See 10,000 Available Catapults. How Many Targets Is That?

The answer is: it depends. Mainly on the chosen building order. Let’s assume only one building is chosen, **[ Smithy ]**. In this case, 200-250 catapults (for example, 200 and 50, or 100, 100, or 50, 50, 50, 50, and so on) are enough to destroy one village, so you can plan 40-50 targets. If two buildings are chosen, **[ Smithy, Farm ]**, you will need 200-250 catapults for the Smithy and 500-700 catapults for the Farm (for example, 14x 50, or 5x 100, 4x 150, 3x 200 catapults, or many other combinations), which means 700-950 catapults per village, or 10-14 targets. Below is a simple table for 30-level buildings (such as Farms, Warehouses, all eco-buildings) and 20-level buildings (Headquarters, Smithy) to help calculate how many targets are possible.

|                    | Number of Catapults Required for Complete Building Destruction |
| ------------------ | -------------------------------------------------------------- |
| 20-level Buildings | 200-250                                                        |
| 30-level Buildings | 500-700                                                        |

## Village Size and the Ruin Table

The exact ruin table is selected from the village points. Sources above 8,000 points use the large-village ruin progression, while villages at or below 8,000 points use the medium-village progression. In other words, a source village is not judged by a redundant maximum-catapult field; its point value tells the planner which table to use.

## Summary

Remember that the core of the planning is still a simple greedy algorithm, and the Planer **ALWAYS** assigns siege units, fakes, or off units in a very similar way. If you want off units or siege units to be indistinguishable from fakes, you need to plan a lot of fakes. When planning destruction, it is worth enabling the **Fakes from All Villages** option in {==Tab 3. Default Action Settings==}, which, unlike the default setting, assigns fakes from all rear villages.

The important final detail is that ruin planning now follows the exact table values instead of simplified heuristics, so the behavior is more accurate and easier to predict. Consider the number of catapults and the buildings worth destroying, and plan plenty of fakes. Enjoy the demolishing!

---

Let me know if you need any other details or changes!