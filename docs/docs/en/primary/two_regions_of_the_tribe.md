# Two regions of the Tribe - front and rear

!!! hint

    Always start writing down any action on this page by counting all the offs and dividing them into Front, Rear, and Beyond according to the spirit of the given list. For this purpose, use the tab 1. Available units, and the results are presented in the table under the goals.

## Intuition

The answer to not assigning front offs to frontmen who should keep them for close-range finishing (or use them in any other way) during action planning is to divide our villages into two main groups: Front, which includes offs and nobility close to the enemy, and Rear, which includes offs and nobility far from the enemy. From version 2.1.0, another region called Beyond was added, intuitively indicating very distant villages (but there are more examples of applications), solving the problem of offs from very far away, which are not desired, but also allowing for action with offs in the range of, for example, 20 tiles - 80 tiles. How exactly this happens and how to control it will be explained shortly.

The entire intuition related to the division can be summarized in the following pictures:

<figure markdown="span">
  ![alt text](image-3.png)
  <figcaption>Example 1. Division into front and rear, green for front and yellow for rear</figcaption>
</figure>

<figure markdown="span">
  ![alt text](image-4.png)
  <figcaption>Example 2. Division into front and rear, red for the enemy and around it our tribe, green for front and yellow for rear</figcaption>
</figure>

Our tribes (in blue) surround the enemy (in red), the left picture shows the state BEFORE the algorithm is applied, and the right one AFTER its application. We divided all our villages into "sectors" depending on the distance from the enemy: closest to the red - Front, a bit further but not too far - Rear, and very distant villages remained blue and indicate Beyond.

How our offs and nobility will be divided depends on the settings in tab 1. Available units, let's consider a few popular possibilities.

!!! info

    Offs close to targets and nobility close to targets work identically to Offs and Nobility, except that instead of considering "all" enemies and dividing into regions based on that, they only consider the targets entered by the User in Goals. This is a much more accurate result because it is known how many units we have available near the targets (this can vary greatly from what we have in the entire tribe).

## Example 1

Example result for min. 0 tiles and max. 500 tiles - meaning we don't want ANY "Fronts" and no "Beyond", everything is rear and everything can be written down.

<figure markdown="span">
  ![alt text](image-5.png){ width="600" }
  <figcaption>0 tiles front and max. 500 tiles rear</figcaption>
</figure>

<figure markdown="span">
  ![alt text](image-6.png){ width="600" }
  <figcaption>0 tiles front and max. 500 tiles rear</figcaption>
</figure>

## Example 2

Example result for min. 15 tiles and max. 100 tiles - meaning we want players who are less than 15 tiles from the enemy to keep offs as frontmen and we don't want any off to be further from the target than 100 tiles (meaning it would fly longer than 2 days etc).

<figure markdown="span">
  ![alt text](image-7.png){ width="600" }
  <figcaption>15 tiles front and max. 100 tiles rear</figcaption>
</figure>

<figure markdown="span">
  ![alt text](image-8.png){ width="600" }
  <figcaption>15 tiles front and max. 100 tiles rear</figcaption>
</figure>

## Example 3

Example result for min. 60 tiles and max. 120 tiles - when we want the rear to be above 60 tiles from the enemy and below 120, e.g., for action or demolition from afar (and we do a separate one from close).

<figure markdown="span">
  ![alt text](image-9.png){ width="600" }
  <figcaption>60 tiles front and max. 120 tiles rear</figcaption>
</figure>

<figure markdown="span">
  ![alt text](image-10.png){ width="600" }
  <figcaption>60 tiles front and max. 120 tiles rear</figcaption>
</figure>

Only offs larger than the selected minimum number of units in the off will be shown. In the current version, ck from offs will also be recognized and distinguished from ck from defensive villages and counted. The result mainly depends on the Opposing tribes that were selected at the very beginning when creating the list. The algorithm is very simple, around each enemy village, a region is calculated at the distance given as the distance from the front line. Taking the sum of all these regions as a whole, we can indicate for each allied village whether it is near these enemy villages (then it is front), or not (then it is rear). Therefore, in the field Not considered when counting front offs, we paste all enemy diodes so as not to disturb the result.

The two bottom rows also take into account the given maximum distance for nobility, where from less than the indicated number of tiles, no nobleman will be written down. Additionally, they count the number of offs and nobility AROUND the entered goals, so if no goals are entered yet, we will get 0 there.

!!! hint

    It is always worth selecting all our nearby enemy tribes for the list, not just the one we are planning the action on. If our tribe has two fronts with tribes A and B, and we want to plan an action on A, we still want to keep front offs at B for the use of the frontmen there, so we add both tribes to the enemy tribes (otherwise, if only tribe A is there, it may turn out that front offs from B are written down for the action).