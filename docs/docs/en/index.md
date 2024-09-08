# Tribal Wars Planer Documentation

## Introduction

This is the documentation for the website [plemiona-planer.pl](https://plemiona-planer.pl) – an ambitious project for [plemiona.pl](https://plemiona.pl), which started in January 2020 after the game's update to version 8.192 in November 2019. The update introduced the ability for tribe administrators to collect data about players and their units.

- [1. Test World](./first_steps/index.md) - a section dedicated to exploring the site without the need to install anything or even have an active game account. It allows for planning actions in a specially prepared Test World.
- [2. Installing the necessary scripts](./scripts/army_and_defence_collection.md) - for use in the real world and planning actions for an actual tribe, a script is necessary to gather data from the tribe (optionally, a second script helps send messages to players).
- [3. Guides](./primary/write_outline_targets.md) - 6 extended articles on specific topics related to planning actions.
- [4. Advanced](./primary/write_outline_targets.md) - a description of all the tabs and options in the main "Planer" tab.

## Questions and Answers

### About the Site

> What is this site, and who is it for and not for?

This site is for **tribe administrators** and their offense coordinators who have access to player data. By using tribe data and inputting action targets and adjusting settings, a coordinator can generate an action outline and send targets to players (via a link to the site or directly in a game message). The mathematics used on the site and the many options allow for planning virtually any action at any stage of the game, saving the planner's time.

> What is plemiona-planer NOT?

It is NOT an illegal tool, a game bot, or any script that automates in-game actions. The site does NOT connect to the game for any purpose other than fetching publicly available world data. You will NEVER be asked for your game password!

### Payments

> Is plemiona-planer paid?

The site is free. However, you can purchase a premium account subscription, which allows for planning more than 40 targets in a single outline and grants access to unused data from previously planned actions (for use in future actions). There are no differences in functionality, algorithm quality, or speed. This model helps maintain the service, and the fee can be split among tribe members. There's no need for more than one account per tribe, except in cases of **obvious!** issues with account sharing. The site is not responsible for losses due to unauthorized access, account theft, or sharing passwords with opponents. The account owner should weigh the pros and cons before giving their password to a third party.

> How is it possible that the app code is open and available on GitHub? 
> 
> Why pay for a subscription if you can use the code for free?

I'm a proponent of [open-source software](https://opensource.com/resources/what-open-source)! It's true, you can choose not to pay and use the site’s code and the result of years of work by many dedicated users. For free, and it will stay that way :) It also reflects my confidence in the security and the mathematics used in the planning – there's nothing to hide. However, the convenience of planning from any location and online access to planning results for tribe members is invaluable. Setting up your own servers requires specialized knowledge, considerable costs, and ongoing maintenance, updates, etc. The subscription fee also covers the time needed to fix bugs, help users with issues, or write new features. All of this would not be possible without user support. Thanks to everyone supporting this project.

### Data

> Are my data safe?

The site has been online since mid-2020. During this time, there has been no security incident. The current business model sustains the servers. Data submitted by users is their responsibility and will never be sold or shared with third parties.

> Can I create outlines in your Planer without having access to tribe data?

No, providing data is required. You must be in tribe administration, and its members need to enable the appropriate settings to share data. There is a test world where you can try out the site without tribe data access.

### Outline

> Hi, why isn’t the Planer outlining all my offensive units? I think I’ve changed everything in the settings, but it keeps leaving 2.7k offensive troops unused…

There could be many reasons, mainly the action settings in the [1. Available Troops and table description](./advanced/1_available_troops_and_table.md) tab, like skipping some frontline villages or distant ones near the edge. Less often, it’s due to [3. Outline Parameters](./advanced/3_outline_parameters.md). The Planer doesn’t fully check for unthought-of parameters and **allows for mistakes**. For example, if the frontline settings indicate that the entire tribe is on the front, but the user sets offensive units only from the backline, the app will outline such an action, even though no offensive unit will be included.

### Night Bonus

> How does the algorithm work to avoid nighttime attacks as much as possible?

The range of natural numbers 0-23, with 0-7 having the worst score = 1, the edges of the range score = 2, and completely "safe" hours score = 3, all wrapped in modulo 24. [Code here](https://github.com/rafsaf/Tribal-Wars-Planer/blob/708b2677a3ee64d2fb8fc50eb8d7601811260dff/utils/write_ram_target.py#L297).

This must be done for each target individually through all allied villages, first calculating the distance in tiles.

### Scripts

> Hi, I don’t quite understand how the send target script works. After installing it on the toolbar, nothing happens in the tribes interface.

See [Script for sending messages](./scripts/sending_messages.md). It is a **browser script**, not for the in-game toolbar. It’s used in the new message view if there are specially added parameters in the URL. [Check point 11 in the results tab](./first_steps/step_7_results_tab.md).

### Legal & License

> Can I use the plemiona-planer code from GitHub?

Yes! You can do anything within the **Apache License 2.0** – set up the Planer locally, use forks, and deploy them yourself. You can use the code copied from the GitHub repo for your tools (under Apache License 2.0, meaning WITHOUT removing the license header). I do NOT agree to impersonation of the plemiona-planer.pl brand, using the rafsaf.pl logo, or my name in the privacy policy in products or projects based on plemiona-planer.pl.