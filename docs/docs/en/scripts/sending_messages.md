# Script for sending messages

| Server        | Tribal Wars Forum                                                                                                                                                                        | Allowed                 | Code                                                                                                                                  |
| ------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| plemiona.pl   | [https://forum.plemiona.pl/index.php?threads/auto-uzupe%C5%82nianie-wiadomo%C5%9Bci.128461/](https://forum.plemiona.pl/index.php?threads/auto-uzupe%C5%82nianie-wiadomo%C5%9Bci.128461/) | YES                     | [Code on GitHub (v2.0)](https://github.com/rafsaf/scripts_tribal_wars/blob/2024-09-01/public/GET_message_autocomplete.js)             |
| other servers | -                                                                                                                                                                                        | NO (cannot be detected) | [Code on GitHub (v2.2)](https://github.com/rafsaf/scripts_tribal_wars/blob/2025-09-22/public/GET_message_autocomplete_v2.2_global.js) |

!!! warning

    Using on other language versions of the game **where the script is not allowed** is at your own risk. The script is allowed on the Polish language version and its operation is completely undetectable, but for other language versions of the game (e.g., Czech, global), they are always illegal.

=== "plemiona.pl"

    ```title="Auto Message Completion Script"
    --8<-- "sending_messages_script_plemiona_pl.txt"
    ```

=== "other servers"

    ```title="Auto Message Completion Script"
    --8<-- "sending_messages_script_global.txt"
    ```

## Installation

To use the scripts, you must first install the appropriate browser extension (monkey):

- [Tampermonkey](https://www.tampermonkey.net/) (Chrome, Opera, Microsoft Edge, Safari, Firefox)
- [Greasemonkey](https://addons.mozilla.org/pl/firefox/addon/greasemonkey/) (Firefox)

Then create a new user script and paste the code below.

To use script in Tampermonkey, you must enable "Allow User Scripts" toggle for it or enable Devloper Mode.
See [https://www.tampermonkey.net/faq.php#Q209](https://www.tampermonkey.net/faq.php#Q209).

## How to check if the extension is working

Go to "Mail" -> "Write Message" on any world.

Make sure that the Tampermonkey extension is enabled, and the "GET message autocomplete" extension is active.

![tampermonkey](image-4.png)

## Usage Instructions

1. Go to the Results tab of the completed schedule, [see this chapter on the results tab](./../first_steps/step_7_results_tab.md)
2. Click on {==Send==} to open new tabs in the game
3. Send the message in the game
4. On the page, the text will change to "Sent!", continue

## Description

A simple and short browser script that fills in the **"To"**, **"Subject"**, and **"Message content"** fields in a new message if they are provided in the link. It automates sending messages to players after scheduling on the site, detecting the script and its execution only in the new message tab. An example of usage can be found below.

- to - recipient
- subject - subject
- message - message

Example:

```
https://pl155.plemiona.pl/game.php?screen=mail&mode=new#to=JakisGracz&subject=Tytul&message=Zawartosc
```

![Example message](image.png)

![Tampermonkey dashboard](image-1.png)
