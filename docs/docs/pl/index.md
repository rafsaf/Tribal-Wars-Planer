# Dokumentacja Plemiona Planer

## Wstęp

Dokumentacja strony [plemiona-planer.pl](https://plemiona-planer.pl) – ambitnego projektu dla [plemiona.pl](https://plemiona.pl) rozpoczętego w styczniu 2020 roku po aktualizacji gry do wersji 8.192 w listopadzie 2019. Wprowadziła ona możliwość zbierania danych o graczach i ich jednostkach administratorom poszczególnych plemion.

- [1. Świat testowy](./first_steps/index.md) - sekcja poświęcona poznaniu strony bez potrzeby instalowania czegokolwiek ani nawet posiadania aktywnego konta w grze. Umożliwia rozpisanie akcji na specjalnie przygotowanym do tego celu Świecie Testowym.
- [2. Instalacja niezbędnych skryptów](./scripts/army_and_defence_collection.md) - w przypadku użycia na prawdziwym świecie i rozpisywania akcji dla prawdziwego plemienia, niezbędne jest skorzystanie z skryptu do pobierania danych z plemienia (oraz opcjonalnie drugiego skryptu, który ułatwia rozsyłanie wiadomości graczom).
- [3. Poradniki](./primary/write_outline_targets.md) - 6 dłuższych artykułów z konkretną tematyką dotyczącą rozpisywania akcji.
- [4. Zaawansowane](./primary/write_outline_targets.md) - Opis wszystkich zakładek i opcji w głównej zakładce "Planer".

## Pytanie - odpowiedź

### O stronie

> Czym jest ta strona i dla kogo jest a dla kogo nie jest?

Jest to strona dla **administratorów** plemion, ich koordynatorów offa z dostępem do danych graczy. Koordynator korzystając z danych plemienia oraz wpisując cele akcji oraz dopasowując ustawienia, generuje wynik rozpiski i rozsyła graczom cele (linkiem do strony lub bezpośrednio w wiadomości w grze). Matematyka użyta na stronie i wiele opcji pozwala na rozpisanie praktycznie dowolnej akcji na dowolnym etapie gry, oszczędzając czas osoby rozpisującej.

> Czym NIE jest plemiona-planer?

NIE jest nielegalnym narzędziem, botem do gry czy innym skryptem który automatyzuje akcje wykonywane w grze. Strona NIE łączy się z grą w celu innym niż pobieranie danych o światach co jest dostępne publicznie. NIGDY nie zostaniesz poproszony też o hasło z gry!

### Płatności

> Czy plemiona-planer jest płatny?

Strona jest bezpłatna. Istnieje możliwość zakupienia abonamentu na konto premium, które pozwala na rozpisywanie więcej niż 40 celów w ramach jednej rozpiski oraz udostępnia niewykorzystane dane z już rozpisanych akcji (do użycia w kolejnej akcji). Nie ma różnic w postaci innych funkcjonalności, jakości algorytmów czy szybkości. Model ten pozwala na utrzymanie serwisu, zaś opłata może być podzielona na członków plemienia. Nie ma potrzeby posiadania więcej niż 1 konta dla 1 plemienia, z wyjątkiem **oczywistych!** problemów z dzieleniem konta - strona nie ponosi odpowiedzialności za straty wynikłe z nieuprawnionego dostępu, kradzieży konta czy np. udostępniania hasła przeciwnikowi. Właściciel konta powinien sam rozważyć za i przeciw przed podaniem hasła osobie trzeciej.

> Jak to możliwe, że kod aplikacji jest otwarty i dostępny na GitHubie? 
> 
> Po co płacić abonament jeśli można korzystać z kodu za darmo?

Jestem zwolennikiem [oprogramowania otwartego](https://opensource.com/resources/what-open-source)! To prawda, można nie płacić i korzystać z kodu strony i efektów wieloletniej pracy bardzo wielu zaangażowanych użytkowników. Za darmo, i tak pozostanie :) Jest to też wyraz mojej pewności siebie dotyczącej bezpieczeństwa i użytej w rozpiskach matematyki - nie ma nic do ukrycia. Natomiast wygoda i możliwość rozpisywania z dowolnego miejsca oraz dostęp online do wyników rozpisek dla graczy plemienia jest nieoceniona. Postawienie serwerów samemu zaś wymaga specjalistycznej wiedzy i sporego nakładu kosztów, wymaga także ciągłego utrzymywania, aktualizacji itd. W ramach kosztu abonamentu wliczany jest także czas potrzebny na poprawianie błędów, pomoc osobom, które mają problemy lub pisanie nowych funkcjonalności. To wszystko nie będzie możliwe bez pomocy użytkowników. Podziękowania dla wszystkich którzy wspierają ten projekt.

### Dane

> Czy moje dane są bezpieczne?

Strona istnieje i jest dostępna w internecie od połowy 2020 roku. Przez ten czas nie nastąpił żaden incydent bezpieczeństwa. Obecny model biznesowy pozwala na utrzymanie serwerów. Dane wrzucane przez poszczególnych użytkowników to ich sprawa, nie są i nigdy nie będą sprzedwane lub w jakikolwiek sposób udostępniane osobom trzecim.

> Czy w Twoim planerze mogę tworzyć rozpiski nie mając dostępu do danych z plemienia?

Nie, podanie danych jest wymagane. Należy być w administracji plemienia, zaś jego członkowie muszą odznaczyć odpowiednie opcje w ustawieniach, aby udostępnić dane. Istnieje świat testowy, gdzie można przetestować stronę bez potrzeby dostępu do danych z plemienia.

### Rozpiska

> Siema, czemu planer nie rozpisuje mi wszystkich offow? Chyba wszystko już zmieniałem w tych opcjach, a cały czas 2,7k offa zostawia..

Powodów może być wiele, głównie ustawienia akcji w zakładce [1. Dostępne jednostki](./advanced/1_available_troops_and_table.md) i np. pomijanie tam części wiosek frontowych lub dalekich lub obok diód. Rzadziej winne są [3. Parametry rozpiski](./advanced/3_outline_parameters.md). Planer nie weryfikuje w pełni wszystkich nieprzemyślanych parametrów, **pozwala na błędy**. Np. jeśli ustawienia frontu będą takie że całe plemię jest frontem, a użytkownik ustawi offy tylko z zaplecza, aplikacja spełni życzenie rozpisania takiej akcji, choć w rezultacie żaden off nie zostanie rozpisany.


### Bonus nocny

> Jak działa algorytm, który próbuje jak najbardziej omijać noc, aby nie dawać wysyłek nocnych?

Przedział liczb naturalnych 0-23, 0-7 ma najgorszy score=1, brzegi przedziału score=2 a całkowicie "bezpieczne" godziny mają score=3, to wszystko opakowane w modulo 24. [Kod tutaj](https://github.com/rafsaf/Tribal-Wars-Planer/blob/708b2677a3ee64d2fb8fc50eb8d7601811260dff/utils/write_ram_target.py#L297).

I tak trzeba zrobić dla każdego celu z osobna przez wszystkie sojusznicze wioski, najpierw przeliczając dystans w kratkach.

### Skrypty

> Hej, nie bardzo rozumiem jak ma działać skrypt wysyłka celi, po zainstalowaniu go na pasku nic się nie dzieje z poziomu plemion.

Por. [Skrypt Auto uzupełnianie wiadomości](./scripts/sending_messages.md). Jest to skrypt **do przeglądarki**, nie zaś do paska skrótu w grze. Użycie następuje w widoku nowej wiadomości, jeśli są tam specjalnie dodane parametry do adresu URL. [Zobacz pkt. 11 w zakładce wyników](./first_steps/step_7_results_tab.md).

### Licencja

> Czy mogę używać kodu plemiona-planer z GitHuba?

Tak! Możesz robić wszystko w ramach **Apache License 2.0** - stawiać planer lokalnie i korzystać z niego, robić forki i stawiać je samodzielnie. Używać kodu skopiowanego z repo na GitHubie do własnych narzędzi (w ramach Apache License 2.0 czyli BEZ usuwania nagłówka o licencji). NIE zgadzam się na podszywanie się pod markę plemiona-planer.pl, używanie znaku rafsaf.pl, loga, pliku polityki prywatności z moim imieniem i nazwiskiem w produktach czy projektach bazujących na plemiona-planer.pl.