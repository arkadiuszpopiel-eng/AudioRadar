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
        # Application
        'app_title': 'RadarSuite Final',
        'language': 'Language:',

        # Main Tabs
        'tab_radar_view': 'Radar View',
        'tab_detection_audio': 'Detection & Audio',
        'tab_game_detection': 'Game Detection',
        'tab_analysis': 'Analysis',
        'tab_ml_training': 'ML Training',

        # Toolbar Buttons
        'start': 'START',
        'stop': 'STOP',
        'rec': 'REC',
        'export': 'Export',
        'import': 'Import',

        # Radar Tab
        'radar': 'Radar',
        'military_hud': 'Military HUD',
        '3d_wallhack': '3D Wallhack',
        'detach_radar': 'Detach Radar',
        'detach_led': 'Detach LED',
        'frameless_mode': 'Frameless',
        'opacity': 'Opacity:',
        'radar_alpha': 'Radar Alpha:',
        'led_alpha': 'LED Alpha:',

        # Detection Panel
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
        'human_footstep_analysis': 'Human Footstep Analysis',
        'human_voice_analysis': 'Human Voice Analysis',

        # Device Panel
        'audio_device': 'Audio Device',
        'select_device': 'Select Device:',
        'refresh_devices': 'Refresh Devices',
        'audio_settings': 'Audio Settings',
        'sample_rate': 'Sample Rate:',
        'block_size': 'Block Size:',
        'channels': 'Channels:',
        'mode': 'Mode',
        'test_mode': 'Synthetic Test Mode',
        'loopback_mode': 'Loopback (soundcard)',
        'audio_enhancements': 'Audio Enhancements',
        'presets': 'Presets',
        'sb_preset': 'SB Z SE + Cloud II',
        'game_detection': 'Game Detection',

        # Analysis Tab
        'spectrum': 'Spectrum',
        'waterfall': 'Waterfall',
        'waveform': 'Waveform',
        'live_spectrum': 'LIVE SPECTRUM',
        'led_alert': 'LED Edge Alert',

        # ML Training Tab
        'ml_training': 'ML Training',
        'ml_training_studio': 'ML Training Studio',
        'recording': 'Recording',
        'training': 'Training',
        'models': 'Models',

        # Status
        'status': 'Status',
        'ready': 'Ready',
        'running': 'Running',
        'stopped': 'Stopped',
        'rms': 'RMS:',
        'backend': 'Backend:',

        # Radar HUD
        'targets': 'TARGETS',
        'tactical': 'TACTICAL',
        'range': 'RANGE',
        'lock': 'LOCK',
        'statistics': 'STATISTICS',

        # Messages
        'no_device_selected': 'No device selected',
        'device_active': 'Device active',
        'scanning': 'Scanning...',
        'stopped_ready': 'Stopped - Ready to start',
    },
    'pl': {
        # Application
        'app_title': 'RadarSuite Final',
        'language': 'Język:',

        # Main Tabs
        'tab_radar_view': 'Widok Radaru',
        'tab_detection_audio': 'Detekcja i Audio',
        'tab_game_detection': 'Wykrywanie Gry',
        'tab_analysis': 'Analiza',
        'tab_ml_training': 'Trening ML',

        # Toolbar Buttons
        'start': 'START',
        'stop': 'STOP',
        'rec': 'NAGRAJ',
        'export': 'Eksportuj',
        'import': 'Importuj',

        # Radar Tab
        'radar': 'Radar',
        'military_hud': 'HUD Militarny',
        '3d_wallhack': 'Wallhack 3D',
        'detach_radar': 'Odłącz Radar',
        'detach_led': 'Odłącz LED',
        'frameless_mode': 'Bez Ramek',
        'opacity': 'Przeźroczystość:',
        'radar_alpha': 'Przeźroczystość Radaru:',
        'led_alpha': 'Przeźroczystość LED:',

        # Detection Panel
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
        'human_footstep_analysis': 'Analiza Kroków Człowieka',
        'human_voice_analysis': 'Analiza Głosu Człowieka',

        # Device Panel
        'audio_device': 'Urządzenie Audio',
        'select_device': 'Wybierz Urządzenie:',
        'refresh_devices': 'Odśwież Urządzenia',
        'audio_settings': 'Ustawienia Audio',
        'sample_rate': 'Częstotliwość Próbkowania:',
        'block_size': 'Rozmiar Bloku:',
        'channels': 'Kanały:',
        'mode': 'Tryb',
        'test_mode': 'Tryb Testowy (Syntetyczny)',
        'loopback_mode': 'Loopback (karta dźwiękowa)',
        'audio_enhancements': 'Ulepszenia Audio',
        'presets': 'Presety',
        'sb_preset': 'SB Z SE + Cloud II',
        'game_detection': 'Wykrywanie Gry',

        # Analysis Tab
        'spectrum': 'Widmo',
        'waterfall': 'Wodospad',
        'waveform': 'Przebieg Fali',
        'live_spectrum': 'WIDMO NA ŻYWO',
        'led_alert': 'Alarm LED',

        # ML Training Tab
        'ml_training': 'Trening ML',
        'ml_training_studio': 'Studio Treningu ML',
        'recording': 'Nagrywanie',
        'training': 'Trening',
        'models': 'Modele',

        # Status
        'status': 'Status',
        'ready': 'Gotowy',
        'running': 'Działa',
        'stopped': 'Zatrzymany',
        'rms': 'RMS:',
        'backend': 'Backend:',

        # Radar HUD
        'targets': 'CELE',
        'tactical': 'TAKTYKA',
        'range': 'ZASIĘG',
        'lock': 'NAMIAR',
        'statistics': 'STATYSTYKI',

        # Messages
        'no_device_selected': 'Nie wybrano urządzenia',
        'device_active': 'Urządzenie aktywne',
        'scanning': 'Skanowanie...',
        'stopped_ready': 'Zatrzymano - Gotowy do startu',
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
