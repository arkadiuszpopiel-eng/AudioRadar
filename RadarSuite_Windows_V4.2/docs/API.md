# RadarSuite API Overview (v4.2.1)

## Architektura
- **app/main.py** – główne okno PyQt5, łączy audio, detekcję, ML i UI Builder.
- **core/** – konfiguracja, logowanie, tłumaczenia, eksport/import ustawień (ExportImportManager).
- **utils/** – monitorowanie wydajności/pamięci (PerformanceMonitor, MemoryOptimizer), skanowanie urządzeń audio, wykrywanie gier i launcherów.
- **audio/** – strumieniowanie i nagrywanie (AudioEngine, AudioRecorder), klasyfikacja (SoundClassifier), przetwarzanie sygnału (AudioProcessor, AudioProcessingCache).
- **detection/** – algorytmy wykrywania kroków/głosów/zdarzeń (DetectionWorker, HumanFootstepDetector).
- **tracking/** – obiekty i logika śledzenia celów (Target, TargetTracker, ThreatPrioritySystem).
- **widgets/** – komponenty UI: radar (MilitaryHUDRadar), panele urządzeń/detekcji, widżety widma/wodospadu/przebiegu fali, panel treningu ML (MLTrainingPanel).
- **ml/** – trenowanie modeli: SessionManager (zarządzanie sesjami/etykietami), LabeledRecorder (nagrywanie z etykietami), ModelTrainer (uczenie modeli), TrainingConfig/TrainingStatus.
- **ui/builder.py** – tworzenie zakładek, toolbaru, statusbaru; integracja paneli.

## Typowy przepływ danych
1. **Wejście audio** – AudioEngine wybiera urządzenie z DevicePanel i buforuje dane w AudioProcessingCache.
2. **Analiza w czasie rzeczywistym** – DetectionWorker/HumanFootstepDetector przetwarzają bufory, wyniki trafiają do radarów i paneli statusu.
3. **Nagrywanie i etykietowanie** – MLTrainingPanel używa LabeledRecorder do zapisu WAV + metadanych; WaveformTimelineWidget pozwala zoomować, przewijać i zaznaczać segmenty.
4. **Trening modelu** – ModelTrainer ładuje zapisane sesje, generuje cechy (ml.feature_extractor) i uczy model (ml.detector/ml.yamnet); status raportowany w panelu.
5. **Integracja z grami** – GameProcessDetector/PlatformLauncherDetector śledzą aktywne gry; profile audio i modele są wiązane z wykrytym tytułem.
6. **Eksport/Import** – ExportImportManager pakuje konfigurację, profile i modele do archiwum (ZIP+JSON) i odtwarza je na innej instalacji.

## Kluczowe klasy i metody
- **AudioRecorder.start/stop** – rozpoczyna/zatrzymuje zapis WAV; zwalnia bufory po zakończeniu.
- **DetectionPanel.update_status** – wyświetla stany wykrywania (CHÓD/BIEG/STRZAŁ) z progami czułości.
- **MilitaryHUDRadar.paintEvent** – rysuje cele, panele TAKTYKA/CELE i pasek statusu z tłumaczeniami.
- **MLTrainingPanel._on_recording_state_change** – reaguje na start/stop nagrania, aktualizuje timer i kolor statusu.
- **WaveformTimelineWidget.set_audio_data / zoom** – ładuje przebieg fali, umożliwia powiększanie i przesuwanie osi czasu z markerami etykiet.
- **ExportImportManager.export_all / import_all** – serializuje ustawienia, profile gier i modele; waliduje wersję formatu.
- **MemoryOptimizer.cleanup_buffers** – usuwa przestarzałe bufory audio, ogranicza użycie pamięci w długich sesjach.

## Konwencje API
- Wszystkie widżety UI przyjmują `parent=None`, używają sygnałów Qt do aktualizacji.
- Funkcja tłumaczeń `tr(key)` powinna być stosowana zamiast hard-coded stringów.
- Modele i sesje ML są identyfikowane przez nazwę gry/profilu; metadane przechowywane w JSON obok plików WAV.

