# 3. Parametry rozpiski

Zakładka służy do ustalenia szczegółow skąd dokładnie powinny lecieć offy na akcję oraz innych, ogólnych ustawień rozpiski. Zapnij pasy.

Wygląd zakładki z domyślnymi ustawieniami:


![alt text](image-2.png){ width="600" }

W artykule [Dwa rejony plemienia czyli co to front i zaplecze](./../primary/two_regions_of_the_tribe.md) dowidziałeś/aś się jak Planer radzi sobie z podziałem na Front, Zaplecze i Poza. Najpierw omówimy punkty 1. i 2. na powyższym zdjęciu.

Uwaga, dla całości rozważań poniżej, ignorujemy wszystkie wioski z rejonu Poza. Są one całkowicie pomijane przez Planer, stąd skupiamy się jedynie na froncie i zapleczu.

Ustawienia 1-2:

![alt text](image-3.png){ width="600" }

Możesz zdefiniować z których dokładnie części plemienia powinny domyślnie polecieć offy i szlachta. Domyślnie jest to Zaplecze Losowo dla offów oraz Front Najbliżej dla szlachty.

**Front Najbliżej** oznacza tyle co Jak najbliżej się da, niekoniecznie nawet musi być to z wiosek z Frontu, jeśli np. nie ma frontowych wiosek lub podczas automatycznego rozpisywania, w danym rejonie już zostaną same wioski z zaplecza (bo frontowe zostaną wykorzystane), wówczas zwyczajnie zostaną wzięte jak najbliższe wioski.

**Zaplecze Blisko** to już musowo wioski z Zaplecza, a wśród nich wzięte są najbliższe możliwe.

**Zaplecze Losowo** to wioski z Zaplecza, wzięte prawdziwie (a nie pseudo) losowo spośród wszystkich możliwych, domyślne ustawienie dla offów - przeważnie nie chcemy by cokolwiek (odległość, wysyłający gracz) świadczyło, że to off i dało się go odróżnić od fejków.

**Zaplecze Daleko** to wioski z Zaplecza, posortowane odwrotnie niż te z Zaplecze Blisko, to znaczy od najdalszych jakie są tylko możliwe.

!!! info

    Dla dodatkowej frajdy, którą niewątpliwie będą czuć obrońcy akcji pisanych na tej stronie, wszystkie powyższe ustawienia mają minimalny stopień losowości, tzn najbliższe i najdalsze możliwe, mają pewne malutkie wahanie, ponieważ teoretycznie Zaplecze Blisko i Zaplecze Daleko są możliwe do rozpoznania dla obrońcy, a w ten sposób będzie to troszkę cięższe do odgadnięcia, w zależności ile ataków jest rozpisanych na daną wioskę, wahanie będzie większe.

Przejdźmy do ustawień 3. do 6. , które skupiają się na ogólnych ustawieniach rozpiski.

Ustawienia 3-6:

![alt text](image-4.png){ width="600" }

**W punkcie 3**. decydujemy jak powinna być dzielona szlachta z jednej wioski. Do wyboru są trzy zwyczajowe możliwości, czyli Dzielić (każdy szlachcic z tą samą obstawą), Nie dzielić (pierwszy szlachcic z największą obstawą, pozostałe z minimalną obstawą, uwaga słabo to wypada w przypadku np. 5 szlachciców, zawsze wtedy gdy rozdzielone zostaną na kilka wiosek) oraz Osobno, czyli wszystkie szlachcice są z minimalną obstawą, a offy lecą osobno przed nimi, tylko do szczególnych akcji i zastosowań.

Najbardziej sensowna opcja szczególnie dla większych akcji to raczej dzielenie, choć domyślne jest nie dzielenie, bo tak raczej to wygląda dla mniejszych rozpisek.

**W punkcie 4**. mamy do wyboru 3 opcje, przy pierwszej Planer stara się brać szlachtę na daną wioskę możliwie z różnych wiosek naszych graczy (zastosowanie to na przykład offoszlachty z daleka), w drugiej opcji (domyślnej) robi to optymalnie zaś w trzeciej stara się puścić na każdą wioskę karetę od jednego gracza lub następnie 3 szlachcice od jednego gracz i 1 szlachcica od drugiego bądź też po 2, zaś prawdopodobnie nigdzie nie będzie pojedynczych szlachciców z różnych wiosek. Opcja trzecia jest najmniej pewna i może generować różne dziwne wyniki.

**W punkcie 5**. wybieramy jak powinny wyglądać rozkazy do placu dla naszych graczy w przypadku wielu szlachciców z jednej wioski. Załóżmy że nasz dany gracz ma puścić 20k offa i 4 szlachcice na wioskę `500|500`.

W przypadku pierwszej opcji, dostanie JEDEN link do placu z 20k offa i 4 szlachcicami.

W przypadku drugiej, domyślnej opcji, dostanie CZTERY linki do placu pod rząd w swoich celach, każdy szalchcic zostanie innymi słowy potraktowany jako osobny rozkaz.

Która opcja w punkcie 5 jest lepsza? Odpowiedź jak zwykle: to zależy. Dla małych akcji zapewne druga, domyślna. Dla bardzo dużych, ogromnych akcji gdzie offy i tak zawsze będą dzielone, wygodniejsza dla graczy będzie opcja pierwsza. Dla reszty akcji dobieramy tak jak nam pasuje, domyślna opcja oznacza więcej szczegółów dla gracza (bo wie dokładnie jak wygląda obstawa dla każdego szlachcica), zaś opcja pierwsza jako jeden rozkaz oznacza mniej szczegółów i mniej zajętego miejsca.

**W punkcie 6**. wybieramy ile maksymalnie fejków z jednej naszej wioski może zostać wysłane.