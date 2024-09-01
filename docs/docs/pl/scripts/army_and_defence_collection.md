# Skrypt Zbiórka Wojska i Obrony

| Serwer             | Forum plemion                                                                                                                                                        | Dozwolony | Kod                                                                                                   |
| ------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------- | ----------------------------------------------------------------------------------------------------- |
| plemiona-planer.pl | [https://forum.plemiona.pl/index.php?threads/zbi%C3%B3rka-wojska-i-obrony.128630/](https://forum.plemiona.pl/index.php?threads/zbi%C3%B3rka-wojska-i-obrony.128630/) | TAK       | [Kod na GitHubie](https://github.com/rafsaf/scripts_tribal_wars/blob/master/src/collect_troops_v2.ts) |

!!! warning

    Użycie na innych wersjach językowych gry **gdzie skrypt jest niedozwolony** przez obsługę może spowodować zablokowanie konta. Użycie na własne ryzyko.

=== "plemiona.pl"

    ```title="Skrypt Zbiórka Wojska i Obrony"
    --8<-- "army_script_plemiona_pl_pl.txt"
    ```

## Instalacja

Przebiega identycznie jak w przypadku wszystkich skryptów do paska, należy przekleić zawartość do nowo utworzonego skryptu do paska w grze.

## Instrukcja użycia

1. Utwórz skrypt do paska, kliknij go
2. Poczekaj na wynik
3. Przejdź do wybranej rozpiski
4. Wklej dane i potwierdź


## Opis

Po kliknięciu na środku ekranu pojawia się "licznik" z postępem, potem wynik w okienku. Działa w obu zakładkach Wojska i Obrony. Domyślne ustawienia do skopiowania mają ustawione cache na true a cacheTime na 5 min, przez ten czas skrypt wypluwa wynik zapisany w przeglądarce zamiast od nowa latać po wszystkich członkach i zbierać dane. W razie wątpliwości czy mamy do czynienia z nowym czy starym wynikiem na dole pojawia się data zebrania.

Dane generowane w wyniku uruchomienia skryptu należy wklejać w rozpiskę na stronie.

Opcje:

Konfiguracja odbywa się za pomocą obiektu **COLLECT_TROOPS_DATA_V2**. Uwaga każdy parametr JEST OPCJONALNY, jeśli obie zmienne są niezdefiniowane lub zdefiniowane, ale nie ma tam kluczy, sensowne wartości domyślne zostaną użyte.

- **cache**: <boolean> (domyślnie: `true`) odpowiada za przechowywanie wyniku w przeglądarce, aby przypadkowo nie kliknąć kilka razy z rzędu i niepotrzebnie obciążać serwery gry, gdy damy na false, skrypt nie będzie zapisywać wyniku w przeglądarce (użyteczne np. gdy zamierzamy zebrać dane od dwóch plemion skaczących od razu do drugiego). Uwaga: jeśli plemię ma ogromną liczbę wiosek, może to zająć miejsce zbyt dużo miejsca w localStorage (~max 5MB), z tego powodu limit wynosi 1MB, jeśli dane wyjściowe są > 1 MB, zapis do localStorage zostanie pominięty.

- **cacheTime**: <number> (domyślnie: `5`) to czas przechowywania wygenerowanego wyniku w przeglądarce, w minutach.

- **removedPlayers**: <string> (domyślnie: `""`) tutaj wpisujemy nicki graczy od których nie chcemy zbierać przeglądów, oddzielając średnikiem jak przy wiadomościach np. "Rafsaf;kmic;ktoś jeszcze".

- **allowedPlayers**: <string> (domyślnie: `""`) tutaj wpisujemy nicki graczy od których JEDYNIE chcemy zbierać przegląd, pozostali zostaną pominięci, oddzielając nicki średnikiem jak przy wiadomościach np. "Rafsaf;kmic;ktoś jeszcze". Uwaga, wartość domyslna "" ma specjalne znaczenie i oznacza że chcemy zbierać przegląd od wszystkich graczy.

- **language**: <string> (domyślnie: `"pl"`) język skryptu, wsparcie dla "pl" i "en", jeśli damy coś innego, skrypt użyje angielskiego, choć domyślna wartość to "pl" by zachować kompatybilność z pierwszą wersją skryptu.

- **showNicknamesTroops**: <boolean> (domyślnie: `false`) gdy wartość to true, do wyniku zbiórki Wojska w każdej linijce zostanie dodany nick gracza, parametr podobny do showNicknamesDeff, który działa dla zakładki Obrony

- **showFirstLineTroops**: <boolean> (domyślnie: `false`) gdy wartość to true, do wyniku zbiórki Wojska zostanie dodany nagłówek (pierwsza linijka u góry wyniku) której wartość ustalamy w kolejnym parametrze firstLineTroops.

- **firstLineTroops**: <string> (domyślnie: `""`) wartość jaka zostanie dodana w nagłówku w wyniku zbiórki Wojska jeśli showFirstLineTroops jest na true.

- **showNicknamesDeff**: <boolean> (domyślnie: `false`) gdy wartość to true, do wyniku zbiórki Obrony w każdej linijce zostanie dodany nick gracza, parametr podobny do showNicknamesTroops, który działa dla zakładki Wojska

- **showFirstLineDeff**: <boolean> (domyślnie: `false`) gdy wartość to true, do wyniku zbiórki Obrony zostanie dodany nagłówek (pierwsza linijka u góry wyniku) której wartość ustalamy w kolejnym parametrze firstLineTroops.

- **firstLineDeff**: <string> (domyślnie: `""`) wartość jaka zostanie dodana w nagłówku w wyniku zbiórki Wojska jeśli showFirstLineDeff jest na true.