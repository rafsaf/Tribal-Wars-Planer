---
title: "6. Burzenie"
date: 2026-02-28
---

Zakładka zawiera kilka ustawień dotyczących akcji burzących.

Wygląd zakładki:

![alt text](image-8.png){ width="600" }

W opcji pod numerem **1.** ustalana jest kolejność burzonych budynków. Planer rozpisze na nie ataki w podanej kolejności, ignorując pominięte budynki.

Pod numerem **2.** ustawiamy minimalną liczbę katapultów, jaką wioska musi mieć, aby kwalifikować się do ataku burzącego. Nie ma już osobnego pola maksymalnej liczby katapultów. Planer używa dokładnej tabeli burzenia dla wybranego typu wioski, więc wysyła tylko tyle katapultów, ile potrzeba do kolejnego dokładnego kroku lub do zniszczenia budynku do poziomu 0, jeśli dostępnych jest więcej katapultów niż wynika z tabeli.

W **3.** wybieramy liczbę offów w atakach burzących, które mają być wysłane razem z katapultami.

Poziomy budynków są wyliczane na podstawie punktów wioski źródłowej. Wioski powyżej 8 000 punktów używają progresji burzenia dla dużych wiosek, a wioski na 8 000 punktów lub mniej używają progresji dla średnich wiosek. Dokładny pozostały poziom po każdym kroku burzenia pobierany jest z wbudowanych tabel, a algorytm po każdym uderzeniu sprawdza ten wynik, aby wybrać właściwy następny krok. Jeśli dostępnych jest więcej katapultów niż tabela wymaga, kontynuuje niszczenie aż do poziomu 0, gdy jest to potrzebne.
