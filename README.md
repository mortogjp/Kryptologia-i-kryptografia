# Permutation Cipher TUI

Projekt implementujący szyfr permutacyjny z interfejsem tekstowym (TUI), napisany w Pythonie. 

## Autorzy (Praca grupowa):
- Jan Paczuski (nr albumu: 166192)
- Maciej Polowczyk (nr albumu: 166480)

## Wymagania zrealizowane w projekcie:
- Szyfrowanie i deszyfrowanie na podstawie hardcodowanej permutacji (długość 6).
- Unikalny warunek: szyfrowanie uwzględnia przesunięcie kluczem, jeśli `(indeks_startowy + indeks_docelowy) % 3 == 2`.
- Obsługa dwóch typów klucza (liczba całkowita lub słowo min. 8 liter).
- W 100% bezpieczne wprowadzanie danych (odporność na znaki specjalne, puste wejścia i skróty klawiszowe).

## Jak uruchomić:
Uruchom aplikację z poziomu konsoli za pomocą polecenia:
`python 1.py`