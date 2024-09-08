# Skrypt Auto uzupełnianie wiadomości

| Serwer             | Forum plemion                                                                                                                                                                            | Dozwolony                      | Kod                                                                                                                                    |
| ------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------- |
| plemiona-planer.pl | [https://forum.plemiona.pl/index.php?threads/auto-uzupe%C5%82nianie-wiadomo%C5%9Bci.128461/](https://forum.plemiona.pl/index.php?threads/auto-uzupe%C5%82nianie-wiadomo%C5%9Bci.128461/) | TAK                            | [Kod na GitHubie (v2.0)](https://github.com/rafsaf/scripts_tribal_wars/blob/2024-09-01/public/GET_message_autocomplete.js)             |
| inne serwery       | -                                                                                                                                                                                        | NIE (brak możliwości wykrycia) | [Kod na GitHubie (v2.1)](https://github.com/rafsaf/scripts_tribal_wars/blob/2024-09-01/public/GET_message_autocomplete_v2.1_global.js) |

!!! warning

    Użycie na innych wersjach językowych gry **gdzie skrypt jest niedozwolony** na własne ryzyko. Skrypt jest dozwolony na polskiej wersji językowej a jego działanie zupełnie niewykrywalne, ale dla wersji językowych gry (np. czeska, globalna) są one zawsze nielegalne.

=== "plemiona.pl"

    ```title="Skrypt Auto uzupełnianie wiadomości"
    --8<-- "sending_messages_script_plemiona_pl.txt"
    ```
=== "inne serwery"

    ```title="Skrypt Auto uzupełnianie wiadomości"
    --8<-- "sending_messages_script_global.txt"
    ```

## Instalacja

Aby korzystać ze skryptów należy zainstalować najpierw odpowiedni dodatek do przeglądarki (małpka):

- [Tampermonkey](https://www.tampermonkey.net/) (Chrome, Opera, Microsoft Edge, Safari, Firefox)
- [Greasmonkey](https://addons.mozilla.org/pl/firefox/addon/greasemonkey/) (Firefox)

Następnie utworzyć nowy skrypt użytkownika i wkleić poniższy kod.

## Instrukcja użycia

1. Przejdź do zakładki Wyników ukończonej rozpiski, [zobacz ten rozdział o zakładce wyników](./../first_steps/step_7_results_tab.md)
2. Klikaj na {==Wyślij==}, aby przejść do nowych kart w grze
3. Wyślij wiadomość w grze
4. Na stronie napis zmieni się na "Wysłano!", kontynuuj


## Opis

Prosty i krótki skrypt do przeglądarki który uzupełnia pola **"Do"**, **"Temat"** i **Treść w nowej wiadomości** jeśli są podane w linku. Automatyzuje wysyłanie wiadomości graczom po rozpisaniu rozpiski na stronie, wykrycie skryptu i jego wykonanie tylko w karcie nowej wiadomości. Przykład użycia znajdziesz poniżej.

- to - do kogo
- subject - temat
- message - wiadomość

Przykład:

```
https://pl155.plemiona.pl/game.php?screen=mail&mode=new#to=JakisGracz&subject=Tytul&message=Zawartosc
```

![Przykładowa wiadomość](image.png)

![Menu tampermonkey](image-1.png)