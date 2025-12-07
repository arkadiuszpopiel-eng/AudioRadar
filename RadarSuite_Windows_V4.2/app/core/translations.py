"""
RadarSuite V4.2.1 - Translations Module
Multi-language support (EN/PL)

FIXED v4.2.1: Comprehensive translations for all UI elements
- All hardcoded strings moved to translation keys
- Full Polish translation support
- Extensible structure for future languages
"""

# ============================================================================
# TRANSLATIONS
# ============================================================================

TRANSLATIONS = {
    'en': {
        # ===== Application =====
        'app_title': 'RadarSuite Final',
        'app_version': 'Version',

        # ===== Main Tabs =====
        'tab_radar': '🎯 Radar View',
        'tab_detection_audio': '🔊 Detection & Audio',
        'tab_game_detection': '🎮 Game Detection',
        'tab_analysis': '📊 Analysis',
        'tab_ml_training': '🧠 ML Training',

        # ===== Radar Tab =====
        'radar': 'Radar',
        'military_hud': '🎯 Military HUD',
        '3d_wallhack': '🌐 3D Wallhack',
        'detach_window': '⬜ Detach Window',
        'frameless': 'Frameless',
        'opacity': 'Opacity:',

        # ===== Spectrum/Analysis =====
        'spectrum': 'Spectrum',
        'waterfall': 'Waterfall',
        'waveform': 'Waveform',
        'live_spectrum': '📡 LIVE SPECTRUM',
        'waterfall_view': '🌊 WATERFALL',
        'waveform_view': '〰️ WAVEFORM',

        # ===== LED Alert =====
        'led_alert': '⚡ LED Edge Alert',
        'detach_led': '⬜ Detach LED',

        # ===== Device Settings =====
        'device_settings': 'Device & Settings',
        'audio_device': 'Audio Device',
        'select_device': 'Select Device:',
        'refresh_devices': 'Refresh Devices',
        'audio_settings': 'Audio Settings',
        'sample_rate': 'Sample Rate:',
        'block_size': 'Block Size:',
        'channels': 'Channels:',
        'apply_settings': 'Apply Settings',

        # ===== Mode =====
        'mode': 'Mode',
        'test_mode': 'Synthetic Test Mode',
        'loopback_mode': 'Loopback (soundcard)',

        # ===== Audio Enhancement =====
        'audio_enhancement': 'Audio Enhancement',
        'auto_gain': 'Auto-Gain',
        'manual_gain': 'Manual Gain:',
        'noise_gate': 'Noise Gate:',
        'noise_gate_tooltip': 'Block audio below this level (reduces noise)',

        # ===== Presets =====
        'presets': 'Presets',
        'sb_preset': '🎧 SB Z SE + Cloud II',
        'laptop_preset': '💻 Laptop (Realtek)',

        # ===== Status =====
        'status': 'Status',
        'rms': 'RMS:',
        'backend': 'Backend:',
        'ready': 'Ready',
        'running': 'Running',
        'stopped': 'Stopped',

        # ===== Detection Panel =====
        'detection': 'Detection',
        'detection_profile': 'Detection Profile',
        'enable_detection': 'Enable Detection',
        'detect_walk': 'Detect WALK',
        'detect_run': 'Detect RUN',
        'detect_shot': 'Detect SHOT',
        'ml_detection': '🧠 ML Detection (YAMNet)',

        # ===== Sensitivity =====
        'sensitivity': 'Sensitivity',
        'walk': 'Walk:',
        'run': 'Run:',
        'shot': 'Shot:',

        # ===== Detection Status =====
        'detection_status': 'Detection Status',
        'walk_detected': 'WALK: DETECTED',
        'run_detected': 'RUN: DETECTED',
        'shot_detected': 'SHOT: DETECTED',
        'walk_none': 'WALK: —',
        'run_none': 'RUN: —',
        'shot_none': 'SHOT: —',

        # ===== Human Footstep Analysis =====
        'footstep_analysis': 'Human Footstep Analysis',
        'confidence': 'Confidence:',
        'cadence': 'Cadence:',
        'foot': 'Foot:',
        'surface': 'Surface:',
        'distance': 'Distance:',
        'gait': 'Gait:',

        # ===== Human Voice Analysis =====
        'voice_analysis': 'Human Voice Analysis',
        'voice_type': 'Voice Type:',
        'pitch': 'Pitch:',
        'intensity': 'Intensity:',
        'communication': 'Communication:',
        'breathing': 'Breathing:',

        # ===== Game Detection Tab =====
        'active_games': '🎮 Active Games & Engines',
        'scanning_games': 'Scanning for games...',
        'no_engines': 'No engines detected',
        'quick_setup': '⚡ QUICK SETUP - Enable Game Audio Capture',
        'platform_launchers': '🚀 Gaming Platform Launchers',
        'scanning_launchers': 'Scanning for launchers...',
        'audio_sources': '🔊 Audio Sources Monitor',
        'active_sources': 'ACTIVE SOURCES:',
        'inactive_sources': 'INACTIVE SOURCES:',

        # ===== ML Training Tab =====
        'ml_training': 'ML Training',
        'ml_not_available': '🧠 ML Training module not available.\n\nPlease ensure all dependencies are installed.',
        'recording_session': 'Recording Session',
        'start_recording': '⏺ Start Recording',
        'stop_recording': '⏹ Stop Recording',
        'session_name': 'Session Name:',
        'game_profile': 'Game Profile:',
        'labeling': 'Labeling',
        'label_walk': 'Walk',
        'label_run': 'Run',
        'label_shot': 'Shot',
        'label_other': 'Other',
        'training': 'Training',
        'start_training': '🚀 Start Training',
        'training_progress': 'Training Progress:',

        # ===== Toolbar =====
        'start': '▶ START',
        'stop': '⏹ STOP',
        'rec': '⏺ REC',
        'language': '🌍',
        'targets': 'Targets:',
        'fps': 'FPS:',

        # ===== Statusbar =====
        'status_ready': '✓ Ready - All systems operational',

        # ===== Misc =====
        'radar_alpha': 'Radar Alpha:',
        'led_alpha': 'LED Alpha:',
        'detach_radar': 'Detach Radar',

        # ===== Export/Import =====
        'export_config': 'Export Configuration',
        'import_config': 'Import Configuration',
        'export_model': 'Export Model',
        'import_model': 'Import Model',

        # ===== Errors/Messages =====
        'error': 'Error',
        'warning': 'Warning',
        'success': 'Success',
        'loading': 'Loading...',
        'saving': 'Saving...',
        'processing': 'Processing...',

        # ===== Waveform Timeline (v4.2.1) =====
        'waveform_timeline': 'Waveform Timeline',
        'no_selection': 'No selection',
        'zoom_in': 'Zoom In',
        'zoom_out': 'Zoom Out',
        'segment_editor': 'Segment Editor',
        'add_label_to_selection': 'Add Label to Selection',
        'clear_selection': 'Clear Selection',
        'audio_overview': 'Audio Overview',
        'session_timeline': 'Session Timeline',

        # ===== Export/Import (v4.2.1) =====
        'export': 'Export',
        'import': 'Import',
        'export_config_file': 'Export Configuration File',
        'import_config_file': 'Import Configuration File',
        'export_ml_model': 'Export ML Model',
        'import_ml_model': 'Import ML Model',
        'export_session': 'Export Session',
        'import_session': 'Import Session',
        'export_success': 'Export successful',
        'import_success': 'Import successful',
        'export_failed': 'Export failed',
        'import_failed': 'Import failed',
        'select_file': 'Select File',
        'save_file_as': 'Save File As',
    },

    'pl': {
        # ===== Aplikacja =====
        'app_title': 'RadarSuite Final',
        'app_version': 'Wersja',

        # ===== Główne Zakładki =====
        'tab_radar': '🎯 Widok Radaru',
        'tab_detection_audio': '🔊 Detekcja i Audio',
        'tab_game_detection': '🎮 Wykrywanie Gier',
        'tab_analysis': '📊 Analiza',
        'tab_ml_training': '🧠 Trening ML',

        # ===== Zakładka Radaru =====
        'radar': 'Radar',
        'military_hud': '🎯 Wojskowy HUD',
        '3d_wallhack': '🌐 Wallhack 3D',
        'detach_window': '⬜ Odłącz Okno',
        'frameless': 'Bez ramek',
        'opacity': 'Przezroczystość:',

        # ===== Spektrum/Analiza =====
        'spectrum': 'Widmo',
        'waterfall': 'Wodospad',
        'waveform': 'Przebieg',
        'live_spectrum': '📡 WIDMO NA ŻYWO',
        'waterfall_view': '🌊 WODOSPAD',
        'waveform_view': '〰️ PRZEBIEG',

        # ===== Alert LED =====
        'led_alert': '⚡ Alert Krawędziowy LED',
        'detach_led': '⬜ Odłącz LED',

        # ===== Ustawienia Urządzenia =====
        'device_settings': 'Urządzenie i Ustawienia',
        'audio_device': 'Urządzenie Audio',
        'select_device': 'Wybierz Urządzenie:',
        'refresh_devices': 'Odśwież Urządzenia',
        'audio_settings': 'Ustawienia Audio',
        'sample_rate': 'Częstotliwość Próbkowania:',
        'block_size': 'Rozmiar Bloku:',
        'channels': 'Kanały:',
        'apply_settings': 'Zastosuj Ustawienia',

        # ===== Tryb =====
        'mode': 'Tryb',
        'test_mode': 'Tryb Testowy (Syntetyczny)',
        'loopback_mode': 'Loopback (karta dźwiękowa)',

        # ===== Ulepszenia Audio =====
        'audio_enhancement': 'Ulepszenia Audio',
        'auto_gain': 'Auto-Wzmocnienie',
        'manual_gain': 'Ręczne Wzmocnienie:',
        'noise_gate': 'Bramka Szumów:',
        'noise_gate_tooltip': 'Blokuj dźwięk poniżej tego poziomu (redukuje szumy)',

        # ===== Presety =====
        'presets': 'Presety',
        'sb_preset': '🎧 SB Z SE + Cloud II',
        'laptop_preset': '💻 Laptop (Realtek)',

        # ===== Status =====
        'status': 'Status',
        'rms': 'RMS:',
        'backend': 'Backend:',
        'ready': 'Gotowy',
        'running': 'Działa',
        'stopped': 'Zatrzymany',

        # ===== Panel Detekcji =====
        'detection': 'Detekcja',
        'detection_profile': 'Profil Detekcji',
        'enable_detection': 'Włącz Detekcję',
        'detect_walk': 'Wykrywaj CHÓD',
        'detect_run': 'Wykrywaj BIEG',
        'detect_shot': 'Wykrywaj STRZAŁY',
        'ml_detection': '🧠 Detekcja ML (YAMNet)',

        # ===== Czułość =====
        'sensitivity': 'Czułość',
        'walk': 'Chód:',
        'run': 'Bieg:',
        'shot': 'Strzały:',

        # ===== Status Detekcji =====
        'detection_status': 'Status Detekcji',
        'walk_detected': 'CHÓD: WYKRYTO',
        'run_detected': 'BIEG: WYKRYTO',
        'shot_detected': 'STRZAŁ: WYKRYTO',
        'walk_none': 'CHÓD: —',
        'run_none': 'BIEG: —',
        'shot_none': 'STRZAŁ: —',

        # ===== Analiza Kroków =====
        'footstep_analysis': 'Analiza Kroków Człowieka',
        'confidence': 'Pewność:',
        'cadence': 'Kadencja:',
        'foot': 'Stopa:',
        'surface': 'Powierzchnia:',
        'distance': 'Odległość:',
        'gait': 'Chód:',

        # ===== Analiza Głosu =====
        'voice_analysis': 'Analiza Głosu Człowieka',
        'voice_type': 'Typ Głosu:',
        'pitch': 'Wysokość:',
        'intensity': 'Intensywność:',
        'communication': 'Komunikacja:',
        'breathing': 'Oddychanie:',

        # ===== Zakładka Wykrywania Gier =====
        'active_games': '🎮 Aktywne Gry i Silniki',
        'scanning_games': 'Skanowanie gier...',
        'no_engines': 'Nie wykryto silników',
        'quick_setup': '⚡ SZYBKA KONFIGURACJA - Włącz Przechwytywanie Audio z Gry',
        'platform_launchers': '🚀 Platformy Gier',
        'scanning_launchers': 'Skanowanie platform...',
        'audio_sources': '🔊 Monitor Źródeł Audio',
        'active_sources': 'AKTYWNE ŹRÓDŁA:',
        'inactive_sources': 'NIEAKTYWNE ŹRÓDŁA:',

        # ===== Zakładka Treningu ML =====
        'ml_training': 'Trening ML',
        'ml_not_available': '🧠 Moduł treningu ML niedostępny.\n\nUpewnij się, że wszystkie zależności są zainstalowane.',
        'recording_session': 'Sesja Nagrywania',
        'start_recording': '⏺ Rozpocznij Nagrywanie',
        'stop_recording': '⏹ Zatrzymaj Nagrywanie',
        'session_name': 'Nazwa Sesji:',
        'game_profile': 'Profil Gry:',
        'labeling': 'Etykietowanie',
        'label_walk': 'Chód',
        'label_run': 'Bieg',
        'label_shot': 'Strzał',
        'label_other': 'Inne',
        'training': 'Trening',
        'start_training': '🚀 Rozpocznij Trening',
        'training_progress': 'Postęp Treningu:',

        # ===== Pasek Narzędzi =====
        'start': '▶ START',
        'stop': '⏹ STOP',
        'rec': '⏺ NAGR',
        'language': '🌍',
        'targets': 'Cele:',
        'fps': 'FPS:',

        # ===== Pasek Statusu =====
        'status_ready': '✓ Gotowy - Wszystkie systemy operacyjne',

        # ===== Różne =====
        'radar_alpha': 'Przezroczystość Radaru:',
        'led_alpha': 'Przezroczystość LED:',
        'detach_radar': 'Odłącz Radar',

        # ===== Eksport/Import =====
        'export_config': 'Eksportuj Konfigurację',
        'import_config': 'Importuj Konfigurację',
        'export_model': 'Eksportuj Model',
        'import_model': 'Importuj Model',

        # ===== Błędy/Komunikaty =====
        'error': 'Błąd',
        'warning': 'Ostrzeżenie',
        'success': 'Sukces',
        'loading': 'Ładowanie...',
        'saving': 'Zapisywanie...',
        'processing': 'Przetwarzanie...',

        # ===== Oś Czasu Fali (v4.2.1) =====
        'waveform_timeline': 'Oś Czasu Fali',
        'no_selection': 'Brak zaznaczenia',
        'zoom_in': 'Przybliż',
        'zoom_out': 'Oddal',
        'segment_editor': 'Edytor Segmentów',
        'add_label_to_selection': 'Dodaj Etykietę do Zaznaczenia',
        'clear_selection': 'Wyczyść Zaznaczenie',
        'audio_overview': 'Przegląd Audio',
        'session_timeline': 'Oś Czasu Sesji',

        # ===== Eksport/Import (v4.2.1) =====
        'export': 'Eksportuj',
        'import': 'Importuj',
        'export_config_file': 'Eksportuj Plik Konfiguracji',
        'import_config_file': 'Importuj Plik Konfiguracji',
        'export_ml_model': 'Eksportuj Model ML',
        'import_ml_model': 'Importuj Model ML',
        'export_session': 'Eksportuj Sesję',
        'import_session': 'Importuj Sesję',
        'export_success': 'Eksport zakończony pomyślnie',
        'import_success': 'Import zakończony pomyślnie',
        'export_failed': 'Eksport nie powiódł się',
        'import_failed': 'Import nie powiódł się',
        'select_file': 'Wybierz Plik',
        'save_file_as': 'Zapisz Plik Jako',
    }
}

# Global current language
current_language = 'en'


def tr(key: str) -> str:
    """
    Translate key to current language.

    Args:
        key: Translation key (e.g., 'app_title', 'detection_status')

    Returns:
        Translated string, or the key itself if not found

    Example:
        >>> tr('app_title')
        'RadarSuite Final'
    """
    return TRANSLATIONS.get(current_language, TRANSLATIONS['en']).get(key, key)


def set_language(lang_code: str) -> bool:
    """
    Set current language.

    Args:
        lang_code: Language code ('en' or 'pl')

    Returns:
        True if language was set, False if invalid code

    Example:
        >>> set_language('pl')
        True
    """
    global current_language
    if lang_code in TRANSLATIONS:
        current_language = lang_code
        return True
    return False


def get_language() -> str:
    """
    Get current language code.

    Returns:
        Current language code ('en' or 'pl')
    """
    return current_language


def get_available_languages() -> list:
    """
    Get list of available language codes.

    Returns:
        List of language codes (e.g., ['en', 'pl'])
    """
    return list(TRANSLATIONS.keys())


def get_language_name(lang_code: str) -> str:
    """
    Get human-readable language name.

    Args:
        lang_code: Language code

    Returns:
        Language name (e.g., 'English', 'Polski')
    """
    names = {
        'en': 'English',
        'pl': 'Polski',
    }
    return names.get(lang_code, lang_code)
