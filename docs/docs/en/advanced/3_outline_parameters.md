# 3. Outline parameters

This tab is used to specify the details of where exactly the offensive troops should come from for an operation, as well as other general schedule settings. Buckle up.

The appearance of the tab with default settings:

![alt text](image-2.png){ width="600" }

In the article [The two regions of the tribe: what are the Frontline and Rearline](./../primary/two_regions_of_the_tribe.md), you learned how the Planer handles the division into Frontline, Rearline, and Outside. First, let's discuss points 1 and 2 in the image above.

Note, for all considerations below, we ignore all villages in the Outside region. They are completely skipped by the Planer, so we focus only on the Frontline and Rearline.

Settings 1-2:

![alt text](image-3.png){ width="600" }

You can define exactly which parts of the tribe the offensive troops and nobles should come from by default. The default is Rearline Random for offensive troops and Frontline Closest for nobles.

**Frontline Closest** means as close as possible. It doesn't even necessarily have to be from villages on the Frontline. If, for example, there are no frontline villages or when automatically scheduling, only rearline villages remain in a region (because frontline ones have been used), then simply the closest villages will be chosen.

**Rearline Close** must come from the Rearline, and among them, the closest possible ones are selected.

**Rearline Random** are villages from the Rearline, selected truly randomly (not pseudo-random) from all possible options. This is the default setting for offensive troops—usually, we don't want anything (distance, sending player) to indicate that it's an offense and could be distinguished from fakes.

**Rearline Far** are villages from the Rearline, sorted in the opposite order of Rearline Close, meaning the farthest ones possible.

!!! info

    For added fun, which the defenders of actions planned on this page will undoubtedly feel, all the above settings have a minimal degree of randomness. That means the closest and farthest possible have a slight fluctuation. This is because theoretically, Rearline Close and Rearline Far could be recognized by a defender, and this way it will be a bit harder to guess, depending on how many attacks are scheduled for a village. The more attacks, the greater the fluctuation.

Let’s move on to settings 3 through 6, which focus on the general settings of the schedule.

Settings 3-6:

![alt text](image-4.png){ width="600" }

**In point 3**, you decide how the nobles from one village should be divided. There are three usual options: Divide (each noble with the same escort), Do not divide (the first noble with the largest escort, the rest with minimal escort—note this doesn't work well with, for example, 5 nobles when they are split across several villages), and Separately, meaning all nobles have minimal escort, and the offenses go separately before them—only for specific actions and uses.

The most sensible option, especially for larger actions, is usually to divide, although the default is not to divide, as this is typically how it works for smaller schedules.

**In point 4**, you have three options. In the first, the Planer tries to take nobles for a village from different villages of our players (use case: nobles from far away). In the second option (default), it does this optimally, while in the third option, it tries to send a set of nobles from one player per village or, alternately, 3 nobles from one player and 1 noble from another, or 2 and 2, while likely there won’t be individual nobles from different villages. The third option is the least reliable and can generate strange results.

**In point 5**, you choose how the commands to the rally point should look for our players in the case of multiple nobles from one village. Suppose our player is to send 20k offense and 4 nobles to the village `500|500`.

In the first option, they will receive ONE rally point link with 20k offense and 4 nobles.

In the second, default option, they will receive FOUR consecutive rally point links for their targets, each noble treated as a separate order.

Which option in point 5 is better? As usual, it depends. For small actions, probably the second, default option. For very large, massive actions where offenses will always be split, the first option is more convenient for players. For other actions, choose what suits you best. The default option means more detail for the player (as they know exactly what escort each noble has), while the first option as a single order means fewer details and less occupied space.

**In point 6**, you choose how many fakes can be sent from one of our villages at most.