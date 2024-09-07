# 1. Available Troops and table description

This tab is used to divide our tribe’s villages into Frontline and Rearline. Since understanding this is fundamental to using the site, part of its description can be found in other tabs, including this article:
[The two regions of the tribe: what are the Frontline and Rearline](./../primary/two_regions_of_the_tribe.md).

![alt text](image.png)

- **Min. off units number** and **Max. off units number**

    Enter the size range of offenses (in terms of population in the farm) that should be planned.

    For example, if the range is 10,000-12,000, the planner will skip both offenses larger than 12,000 and smaller than 10,000. The maximum number of scouts considered is 200; any more will be ignored. The noblemen are counted as x6 units only if **there are more offensive units than defensive units**. The exact code can be found [here](https://github.com/rafsaf/Tribal-Wars-Planer/blob/ecc7ff31ed122928a7aea6199af4a0f9ce4718fd/utils/basic/army.py#L242-L250).

- **Minimum distance from front line**

    The value in tiles used to calculate the frontline, based on which frontline villages are determined. The exact code for dividing into Frontline/Rearline/Outside can be found [here](https://github.com/rafsaf/Tribal-Wars-Planer/blob/ecc7ff31ed122928a7aea6199af4a0f9ce4718fd/utils/basic/cdist_brute.py#L83-L99). The entire intuition behind this division can be found in the guide [The two regions of the tribe: what are the Frontline and Rearline](./../primary/two_regions_of_the_tribe.md).

- **Max Distance for nobles**

    By default, this is the maximum value of the distance in tiles for the specific world. It is not possible to set a higher value (such attacks could not be sent).

- **Max Distance for offs and ruins**

    The planner will not assign attacks from villages further away from the enemy than this value. It is also used to give an approximate number of villages in the "Outside" region, meaning those that will be skipped.

- **Excluded enemy villages coords (secluded villages)**

    Enter all enemy dead accounts within our tribe's territory. **It’s worth** doing this because with a **Minimum distance from front line** of, for example, 10 tiles, everything around 10 tiles from the enemy dead accounts will naturally be considered as the frontline, and offenses from this area will be skipped in the plan. However, sometimes it’s a better decision to keep offenses around islands for local use and not enter enemy dead accounts here.