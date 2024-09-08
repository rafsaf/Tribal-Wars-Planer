# 1. Dostępne jednostki i opis Tabeli

Zakładka służy do dzielenia wiosek naszego plemienia na Front i Zaplecze. Ponieważ jej znajomość jest podstawą obsługi strony, część jej opisu znajdziesz w innych zakładkach, między innymi w tym artykule
[Dwa rejony plemienia czyli co to front i zaplecze](./../primary/two_regions_of_the_tribe.md).

![alt text](image.png)

- **Minimalna liczba jednostek w offie** oraz **Maksymalna liczba jednostek w offie**

    Wpisujemy zakres wielkości offów (w liczebności zagrody), które należy rozpisać.

    Jeśli będzie to np. 10000-12000, planer pominie zarówno offy większe niż 12000 jak i mniejsze niż 10000. Maksymalna ilość zwiadowców która jest brana pod uwagę to 200, jeśli jest ich więcej, zostaną zignorowani. CK do offów jest doliczane jako x6 jednostek tylko w przypadku gdy **jest więcej ofensywnych jednostek niż defensywnych**. Dokładny kod znajduje się [tutaj](https://github.com/rafsaf/Tribal-Wars-Planer/blob/ecc7ff31ed122928a7aea6199af4a0f9ce4718fd/utils/basic/army.py#L242-L250).

- **Minimalna odległość od linii frontu**

    Wartość w kratkach do obliczania linii frontowej, na podstawie której liczone są wioski frontowe. Dokładny kod podziału na Front/Zaplecze/Poza znajduje się [tutaj](https://github.com/rafsaf/Tribal-Wars-Planer/blob/ecc7ff31ed122928a7aea6199af4a0f9ce4718fd/utils/basic/cdist_brute.py#L83-L99). Całość intuicji związanej z podziałem można znaleźć w poradniku [Dwa rejony plemienia czyli co to Front i Zaplecze](./../primary/two_regions_of_the_tribe.md).

- **Maksymalna odległość dla szlachciców**

    Domyślnie jest to maksymalna wartość odległości w kratkach dla danego świata. Nie da się ustawić wyższej wartości (takich ataków nie dałoby się wysłać).

- **Maksymalna odległość dla offów (i burzaków)**

    Planer nie rozpisze ataków z wiosek dalszych od wroga niż ta wartość. Używana jest też do szacunkowego pokazania ilości wiosek w rejonie "Poza" czyli tych które zostaną pominięte.

- **Nieuwzględniane przy liczeniu frontowych offów wioski wroga (diody itp.)**

    Wpisujemy wszystkie diody wroga na terenie naszego plemienia. **Warto** to zrobić, ponieważ dla **Minimalna odległość od linii frontu** równej np 10 kratek, wszystko wokół 10 kratek od diód przeciwnika, zostanie naturalnie uznane jako front, zaś offy z tego rejonu pominięte w rozpisce. Czasem jednak lepszą decyzją jest pozostawienie offów wokół wysp na lokalny użytek i nie wpisywanie tu diód wroga.