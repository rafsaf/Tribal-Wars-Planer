# Write the outline targets

Convention: subsequent action targets must be entered in consecutive lines of Targets. At a minimum, coordinates alone are sufficient, in which case an example line `000|000` will be completed to `000|000:0:0`. Later, you will learn how to encode the number of offenses and nobles. To save the targets, click Save targets.

<figure markdown="span">
  ![alt text](image.png){ width="600" }
  <figcaption>Example 1, offenses and nobles encoded by default</figcaption>
</figure>

`440|670:5:4` in the first line is an example of how to encode the number of offenses and nobles for a given target by default. The first number indicates the number of offenses, and the second number indicates the number of nobles.

The Planner supports three types of targets: real, fake, and demolition. Place real targets in Targets, fake targets in Fakes, and demolition targets in Demolitions. For Fakes, instead of offenses and nobles, encode the number of fakes and fake nobles, and in the Demolitions tab, encode the number of offenses and the number of demolitions (which follow the offenses).

<figure markdown="span">
  ![alt text](image-1.png){ width="600" }
  <figcaption>Example 2, extended encoding of offenses and nobles</figcaption>
</figure>

By default, targets as in Example 1 inherit the sending mode from tab 3. Schedule parameters, such as offenses randomly from the rear and nobles from the nearest front. If we want to send, for example, 5 offenses randomly from the rear, 2 offenses from the near rear, 1 noble from afar, and the last 3 nobles from nearby to a given target, e.g., line number 3 in Example 2, which is `439|671`, we can use the extended syntax by entering:

```
439|671:2|0|5|0:3|0|0|1
```


In this case, instead of a single number of offenses, we entered 2|0|5|0, and instead of a single number of nobles, we entered 3|0|0|1. We use the extended syntax when we want some orders from afar and others from nearby; there are 4 regions of our tribe to choose from.

!!! info

    **A|B|C|D** translates to: 
    A from nearby|B from the near rear|C randomly from the rear|D from afar

Errors will appear in standard cases, primarily when the given village does not exist in the declared world in the schedule, or when the village is barbarian, and when the characters entered after the coordinates are not among the possibilities listed above. There are no obstacles for targets to be villages of tribe members or for the same villages to be entered multiple times (although in this case, a message will appear at the top indicating that duplicates were detected). Duplicates are not prohibited; each entered target, even if it appears multiple times, will be treated separately. However, this may cause chaos among players because there will be, for example, several of the same targets with different orders for them (?). Duplicates in different tabs (Targets, Fakes, Demolitions) are not counted.

<figure markdown="span">
  ![alt text](image-2.png){ width="600" }
  <figcaption>Example 3, errors during saving</figcaption>
</figure>