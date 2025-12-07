# RadarSuite API Overview

## Architektura

- **core/** – warstwa wspólna (logowanie, konfiguracja, tłumaczenia) oraz rejestracja DI.
- **audio/** – nagrywanie, przetwarzanie bloków audio i podgląd RMS wykorzystywany przez UI.
- **ml/** – detekcja (YAMNet, klasyfikacja heurystyczna) oraz pipeline treningowy (`training/`).
- **widgets/** – komponenty PyQt5: panele konfiguracji, wizualizacje (spectrum, waterfall, waveform) i edytor treningu ML.
- **ui/builder.py** – kompozycja głównego okna i zakładek (Radar, Detection & Audio, ML Training itd.).

## Główne moduły

### core
- `core.logger.log(message, level)` – lekkie logowanie do konsoli oraz plików diagnostycznych.
- `core.translations.tr(key)` – tłumaczenia EN/PL dla tekstów UI.
- `core.config.AppConfig` – odczyt i zapis ustawień aplikacji.
- `core.export_import` – eksport/import konfiguracji w formacie JSON/ZIP.

### audio
- `audio.recorder.AudioRecorder` – przechwytywanie dźwięku z wybranego urządzenia (loopback / mikrofon).
- `audio.engine.AudioEngine` – miksowanie i przesyłanie bloków audio do widżetów podglądu.

### ml (detekcja)
- `ml.detector.MLDetector` – obsługa modelu ML (YAMNet) z trybem awaryjnym heurystycznym.
- `ml.yamnet.YAMNetDetector` – ładuje model TFLite i wykonuje klasyfikację dźwięku.

### ml/training (trening)
- `ml.training.SessionManager` – zarządza sesjami nagrań oraz metadanymi etykiet.
- `ml.training.LabeledRecorder` – nagrywa audio i dodaje etykiety w czasie rzeczywistym.
- `ml.training.ModelTrainer` – ekstrakcja cech i trenowanie modelu; statusy w `TrainingStatus`.
- `widgets.ml_training_panel.MLTrainingPanel` – UI do nagrywania, etykietowania i uruchamiania treningu.
- `widgets.waveform_timeline.WaveformTimelineWidget` – wizualizacja przebiegu, zoom/scroll, wybór segmentów.

### UI
- `widgets.detection_panel.DetectionPanel` – konfiguracja detekcji, czułości i statusów.
- `widgets.device_panel.DevicePanel` – wybór urządzeń audio i trybu pracy.
- `ui.builder.UIBuilder` – tworzy paski narzędzi, zakładki i przypina widżety do głównego okna.

## Przepływy pracy

### Nagrywanie i etykietowanie (ML Training)
1. Użytkownik otwiera zakładkę **Trening ML** (UIBuilder tworzy `MLTrainingPanel`).
2. `LabeledRecorder` startuje nagrywanie z wybranego źródła audio; bloki trafiają do `WaveformTimelineWidget`.
3. Użytkownik zaznacza fragmenty przebiegu i dodaje etykiety (przyciski lub hotkeys 1–8).
4. `SessionManager` zapisuje WAV + metadane etykiet; sesja staje się dostępna w tabeli zapisów.

### Trening modelu
1. Użytkownik wybiera sesje i uruchamia trening w `MLTrainingPanel`.
2. `ModelTrainer` aktualizuje postęp przez `TrainingStatus` (PREPARING → EXTRACTING_FEATURES → TRAINING → SAVING).
3. Po zakończeniu model jest zapisywany w katalogu profilu i rejestrowany w konfiguracji.

### Eksport/Import
- `core.export_import.export_package(path)` pakuje konfigurację (JSON) oraz modele/dane pomocnicze do ZIP.
- `core.export_import.import_package(path)` odtwarza ustawienia, profile gier i ścieżki modeli na innym stanowisku.

### Integracja z detekcją podczas gry
1. `audio.engine` przekazuje bloki audio do `ml.detector.MLDetector` oraz algorytmów heurystycznych.
2. Wyniki zasila `widgets.detection_panel`, aktualizując wskaźniki (chód/bieg/strzał) i HUD.
3. Jeśli ML jest wyłączone lub model brakujący, system pozostaje w trybie heurystycznym.
