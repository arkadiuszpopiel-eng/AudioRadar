# Testowanie RadarSuite

## Zewnętrzne testy automatyczne (pytest)

1. Zainstaluj zależności deweloperskie:

```bash
pip install -r requirements.txt pytest
```

2. Uruchom testy:

```bash
pytest
```

Domyślnie testy oczekują dostępu do katalogu `app/` (ustawiane w `tests/conftest.py`).

## Wewnętrzny SELF-TEST w aplikacji

1. Uruchom RadarSuite.
2. Na pasku narzędzi kliknij przycisk **TEST** (opis "Self-test systemu").
3. Aplikacja wykona szybki zestaw kontroli (importy, logika nagrywania, opcjonalnie mini-overlay).
4. Podsumowanie pojawi się w oknie dialogowym, a pełny raport znajdziesz w `logs/selftest_YYYYMMDD_HHMMSS.log`.

Self-test działa w trybie bezpiecznym – używa katalogów tymczasowych i nie modyfikuje danych użytkownika.
