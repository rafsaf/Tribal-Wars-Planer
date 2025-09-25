# Szkript üzenetek küldéséhez

| Szerver       | Klánháború Fórum                                                                                                                                                                         | Engedélyezett        | Kód                                                                                                                                   |
| ------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| plemiona.pl   | [https://forum.plemiona.pl/index.php?threads/auto-uzupe%C5%82nianie-wiadomo%C5%9Bci.128461/](https://forum.plemiona.pl/index.php?threads/auto-uzupe%C5%82nianie-wiadomo%C5%9Bci.128461/) | IGEN                 | [Kód a GitHubon (v2.0)](https://github.com/rafsaf/scripts_tribal_wars/blob/2024-09-01/public/GET_message_autocomplete.js)             |
| más szerverek | -                                                                                                                                                                                        | NEM (nem észlelhető) | [Kód a GitHubon (v2.2)](https://github.com/rafsaf/scripts_tribal_wars/blob/2025-09-22/public/GET_message_autocomplete_v2.2_global.js) |

!!! warning

    Más nyelvi verziókon való használat, **ahol a szkript nem engedélyezett**, saját felelősségre történik. A szkript a lengyel nyelvi verzión engedélyezett, és működése teljesen észrevehetetlen, de más nyelvi verziók (pl. cseh, globális) esetében mindig illegálisak.

=== "plemiona.pl"

    ```title="Automatikus üzenetkiegészítő szkript"
    --8<-- "sending_messages_script_plemiona_pl.txt"
    ```

=== "más szerverek"

    ```title="Automatikus üzenetkiegészítő szkript"
    --8<-- "sending_messages_script_global.txt"
    ```

## Telepítés

A szkriptek használatához először telepítenie kell a megfelelő böngészőbővítményt (monkey):

- [Tampermonkey](https://www.tampermonkey.net/) (Chrome, Opera, Microsoft Edge, Safari, Firefox)
- [Greasemonkey](https://addons.mozilla.org/pl/firefox/addon/greasemonkey/) (Firefox)

Ezután hozzon létre egy új felhasználói szkriptet, és illessze be az alábbi kódot.

A szkript Tampermonkey-ben való használatához engedélyeznie kell a "Felhasználói szkriptek engedélyezése" kapcsolót, vagy engedélyeznie kell a Fejlesztői módot.
Lásd [https://www.tampermonkey.net/faq.php#Q209](https://www.tampermonkey.net/faq.php#Q209).

## Hogyan ellenőrizhető, hogy a bővítmény működik-e

Menjen a "Levél" -> "Üzenet írása" menüpontba bármelyik világon.

Győződjön meg róla, hogy a Tampermonkey bővítmény engedélyezve van, és a "GET message autocomplete" bővítmény aktív.

![tampermonkey](image-4.png)

## Használati útmutató

1. Menjen a befejezett ütemterv Eredmények fülére, [lásd ezt a fejezetet az eredmények fülről](./../first_steps/step_7_results_tab.md)
2. Kattintson a {==Küldés==} gombra az új fülek megnyitásához a játékban
3. Küldje el az üzenetet a játékban
4. Az oldalon a szöveg "Elküldve!"-re változik, folytassa

## Leírás

Egy egyszerű és rövid böngésző szkript, amely kitölti a **"Címzett"**, **"Tárgy"** és **"Üzenet tartalma"** mezőket egy új üzenetben, ha azok a linkben meg vannak adva. Automatizálja az üzenetek küldését a játékosoknak az oldalon történő ütemezés után, a szkriptet és annak végrehajtását csak az új üzenet fülön érzékeli. Egy használati példa alább található.

- to - címzett
- subject - tárgy
- message - üzenet

Példa:

```
https://pl155.plemiona.pl/game.php?screen=mail&mode=new#to=Valaki&subject=Cím&message=Tartalom
```

![Példa üzenet](image.png)

![Tampermonkey irányítópult](image-1.png)
