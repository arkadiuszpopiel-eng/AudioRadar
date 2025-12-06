"""
RadarSuite V4.2.1 - Translations Module
Multi-language support (EN/PL)
"""

# ============================================================================
# TRANSLATIONS
# ============================================================================

TRANSLATIONS = {
    'en': {
        'app_title': 'RadarSuite Final',
        'radar': 'Radar',
        'spectrum': 'Spectrum',
        'waterfall': 'Waterfall',
        'device_settings': 'Device & Settings',
        'detection': 'Detection',
        'led_alert': 'LED Edge Alert',
        'start': 'Start',
        'stop': 'Stop',
        'radar_alpha': 'Radar Alpha:',
        'led_alpha': 'LED Alpha:',
        'detach_radar': 'Detach Radar',
        'detach_led': 'Detach LED',
        'frameless_mode': 'Frameless Mode',
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
        'presets': 'Presets',
        'sb_preset': 'SB Z SE + Cloud II',
        'status': 'Status',
        'rms': 'RMS:',
        'backend': 'Backend:',
        'detection_profile': 'Detection Profile',
        'enable_detection': 'Enable Detection',
        'detect_walk': 'Detect WALK',
        'detect_run': 'Detect RUN',
        'detect_shot': 'Detect SHOT',
        'sensitivity': 'Sensitivity',
        'walk': 'Walk:',
        'run': 'Run:',
        'shot': 'Shot:',
        'detection_status': 'Detection Status',
        'walk_detected': 'WALK: DETECTED',
        'run_detected': 'RUN: DETECTED',
        'shot_detected': 'SHOT: DETECTED',
        'walk_none': 'WALK: —',
        'run_none': 'RUN: —',
        'shot_none': 'SHOT: —',
        'ready': 'Ready',
        'running': 'Running',
        'stopped': 'Stopped',
        'language': 'Language:',
    },
    'pl': {
        'app_title': 'RadarSuite Final',
        'radar': 'Radar',
        'spectrum': 'Widmo',
        'waterfall': 'Wodospad',
        'device_settings': 'Urządzenie i Ustawienia',
        'detection': 'Detekcja',
        'led_alert': 'Alarm LED',
        'start': 'Start',
        'stop': 'Stop',
        'radar_alpha': 'Przezroczystość Radaru:',
        'led_alpha': 'Przezroczystość LED:',
        'detach_radar': 'Odłącz Radar',
        'detach_led': 'Odłącz LED',
        'frameless_mode': 'Tryb Bez Ramek',
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
        'presets': 'Presety',
        'sb_preset': 'SB Z SE + Cloud II',
        'status': 'Status',
        'rms': 'RMS:',
        'backend': 'Backend:',
        'detection_profile': 'Profil Detekcji',
        'enable_detection': 'Włącz Detekcję',
        'detect_walk': 'Wykrywaj CHÓD',
        'detect_run': 'Wykrywaj BIEG',
        'detect_shot': 'Wykrywaj STRZAŁY',
        'sensitivity': 'Czułość',
        'walk': 'Chód:',
        'run': 'Bieg:',
        'shot': 'Strzały:',
        'detection_status': 'Status Detekcji',
        'walk_detected': 'CHÓD: WYKRYTO',
        'run_detected': 'BIEG: WYKRYTO',
        'shot_detected': 'STRZAŁ: WYKRYTO',
        'walk_none': 'CHÓD: —',
        'run_none': 'BIEG: —',
        'shot_none': 'STRZAŁ: —',
        'ready': 'Gotowy',
        'running': 'Działa',
        'stopped': 'Zatrzymany',
        'language': 'Język:',
    }
}

# Global current language
current_language = 'en'


def tr(key):
    """Translate key to current language"""
    return TRANSLATIONS.get(current_language, TRANSLATIONS['en']).get(key, key)


def set_language(lang_code):
    """Set current language (en/pl)"""
    global current_language
    if lang_code in TRANSLATIONS:
        current_language = lang_code


def get_language():
    """Get current language code"""
    return current_language
