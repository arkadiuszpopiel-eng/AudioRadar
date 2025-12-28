"""
Radar Games ML v4.3.1 - Event Handlers
ADDED v4.3.1: Extracted from MainWindow to reduce complexity

Event handlers for user interactions (buttons, sliders, shortcuts, etc.)
Reduces MainWindow from 2080 lines to ~1880 lines (~200 line reduction)
"""

from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QTimer

from app.core.logger import log
from app.core.translations import get_language, set_language, tr
from app.core.constants import VERSION


class EventHandlers:
    """
    Event handlers for MainWindow UI interactions.

    Delegates back to MainWindow for accessing widgets and state.
    All methods require self.window to be set to the MainWindow instance.
    """

    def __init__(self, main_window):
        """
        Initialize event handlers with reference to MainWindow.

        Args:
            main_window: MainWindow instance (provides access to widgets and state)
        """
        self.window = main_window
        log("EventHandlers initialized", "DEBUG")

    # ========================================================================
    # LANGUAGE & UI UPDATES
    # ========================================================================

    def toggle_language(self):
        """Toggle between EN and PL (FIXED v3.5.2: Use get_language function)"""
        current_lang = get_language()

        if current_lang == 'en':
            set_language('pl')
        else:
            set_language('en')

        log(f"Language changed to: {get_language()}", "INFO")
        self.update_ui_translations()

    def update_ui_translations(self):
        """Update all UI text with current language (FIXED v3.5.2: Use get_language function)"""
        lang = get_language()

        # Main window
        self.window.setWindowTitle(f"{tr('app_title')} {VERSION}")

        # Start/Stop button
        if not self.window.is_running:
            self.window.start_btn.setText("▶ START")
        else:
            self.window.start_btn.setText("⏹ STOP")

        # Status bar
        if not self.window.is_running:
            self.window.status_bar.showMessage("✓ Ready - All systems operational" if lang == 'en' else "✓ Gotowy - Wszystkie systemy sprawne")
        else:
            self.window.status_bar.showMessage("● RUNNING - Detection active" if lang == 'en' else "● DZIAŁA - Detekcja aktywna")

        if hasattr(self.window, 'test_btn'):
            self.window.test_btn.setText(tr('self_test'))
            self.window.test_btn.setToolTip(tr('self_test_title'))

        # Update language button to show current language
        if hasattr(self.window, 'lang_btn'):
            self.window.lang_btn.setText("🇬🇧 EN" if lang == 'en' else "🇵🇱 PL")
            self.window.lang_btn.setChecked(lang == 'pl')

        # ENHANCED v4.3.1-k0006: Update tab titles dynamically (no restart needed!)
        if hasattr(self.window, 'main_tabs'):
            self.window.main_tabs.setTabText(0, f"🎯 {tr('tab_radar_view')}")
            self.window.main_tabs.setTabText(1, f"🔊 {tr('tab_detection_audio')}")
            self.window.main_tabs.setTabText(2, f"🎮 {tr('tab_game_detection')}")
            self.window.main_tabs.setTabText(3, f"📊 {tr('tab_analysis')}")
            self.window.main_tabs.setTabText(4, f"🧠 {tr('tab_ml_training')}")

        # ENHANCED v4.3.1-k0006: Update radar sub-tabs
        if hasattr(self.window, 'radar_tabs'):
            self.window.radar_tabs.setTabText(0, f"🎯 {tr('military_hud')}")
            self.window.radar_tabs.setTabText(1, f"🌐 {tr('3d_wallhack')}")

        # Update panels
        self.window.dev_panel.update_translations()
        self.window.det_panel.update_translations()

        # Update detached windows titles
        if self.window.detached_radar:
            self.window.detached_radar.setWindowTitle(f"{tr('radar')} - Radar Games ML {VERSION}")

        if self.window.detached_led:
            self.window.detached_led.setWindowTitle(f"{tr('led_alert')} - Radar Games ML {VERSION}")

    # ========================================================================
    # KEYBOARD SHORTCUTS
    # ========================================================================

    def toggle_start_stop_shortcut(self):
        """Toggle start/stop via keyboard shortcut (with toast notification)"""
        if self.window.is_running:
            self.window.stop()
            self.window.toast.show_toast("Audio detection stopped", "info", 2000)
        else:
            self.window.start()
            self.window.toast.show_toast("Audio detection started", "success", 2000)

    def reset_radar(self):
        """Reset radar display"""
        # Reset radar angle
        self.window.radar_angle = 0.0
        self.window.toast.show_toast("Radar reset", "info", 1500)
        log("Radar reset via keyboard shortcut", "INFO")

    def quick_mute_toggle(self):
        """Quick mute toggle (Space key)"""
        # Stop/start audio without changing UI state
        if self.window.is_running:
            self.window.audio.stop()
            self.window.toast.show_toast("Audio muted", "warning", 1500)
            log("Audio muted via keyboard shortcut", "INFO")
        else:
            self.window.audio.start()
            self.window.toast.show_toast("Audio unmuted", "success", 1500)
            log("Audio unmuted via keyboard shortcut", "INFO")

    def toggle_fullscreen(self):
        """Toggle fullscreen mode (F11)"""
        if self.window.isFullScreen():
            self.window.showNormal()
            self.window.toast.show_toast("Exited fullscreen", "info", 1500)
        else:
            self.window.showFullScreen()
            self.window.toast.show_toast("Entered fullscreen (F11 to exit)", "info", 2000)

    # ========================================================================
    # DETACHED WINDOWS
    # ========================================================================

    def update_radar_alpha(self, value):
        """Update radar opacity"""
        opacity = value / 100.0

        if self.window.detached_radar:
            self.window.detached_radar.set_opacity(opacity)

    def update_led_alpha(self, value):
        """Update LED opacity"""
        opacity = value / 100.0

        if self.window.detached_led:
            self.window.detached_led.set_opacity(opacity)
        else:
            self.window.led_widget.global_alpha = opacity

    def toggle_detach_radar(self, checked):
        """Toggle radar detachment (v4.3.1: Added position persistence)"""
        from widgets.radar import DetachableRadarWidget

        if checked:
            # Create detached radar
            self.window.detached_radar = DetachableRadarWidget()
            self.window.detached_radar.set_opacity(self.window.radar_alpha.value() / 100.0)

            # ADDED v4.3.1: Restore position from config
            self.window.config_manager.restore_detached_radar_state(
                self.window.detached_radar,
                self.window.config
            )

            self.window.detached_radar.show()
            log("Radar detached (position restored from config)", "INFO")
        else:
            # ADDED v4.3.1: Save position before closing
            if self.window.detached_radar:
                self.window.config = self.window.config_manager.save_detached_radar_state(
                    self.window.detached_radar,
                    self.window.config
                )
                self.window.config_manager.save(self.window.config)

                self.window.detached_radar.close()
                self.window.detached_radar = None
                log("Radar attached (position saved to config)", "INFO")

    def toggle_detach_led(self, checked):
        """Toggle LED detachment (v4.3.1: Added position persistence)"""
        from widgets.led import DetachableLedWidget

        if checked:
            # Create detached LED
            self.window.detached_led = DetachableLedWidget()
            self.window.detached_led.set_opacity(self.window.led_alpha.value() / 100.0)

            # ADDED v4.3.1: Restore position from config
            self.window.config_manager.restore_detached_led_state(
                self.window.detached_led,
                self.window.config
            )

            self.window.detached_led.show()
            log("LED detached (position restored from config)", "INFO")
        else:
            # ADDED v4.3.1: Save position before closing
            if self.window.detached_led:
                self.window.config = self.window.config_manager.save_detached_led_state(
                    self.window.detached_led,
                    self.window.config
                )
                self.window.config_manager.save(self.window.config)

                self.window.detached_led.close()
                self.window.detached_led = None
                log("LED attached (position saved to config)", "INFO")

    def toggle_radar_frameless(self, checked):
        """Toggle radar frameless mode"""
        if self.window.detached_radar:
            self.window.detached_radar.set_frameless(checked)

    def toggle_led_frameless(self, checked):
        """Toggle LED frameless mode"""
        if self.window.detached_led:
            self.window.detached_led.set_frameless(checked)

    # ========================================================================
    # AUDIO CONTROL
    # ========================================================================

    def toggle_start_stop(self):
        """Toggle audio capture"""
        if not self.window.is_running:
            self.window.start()
        else:
            self.window.stop()

    def toggle_recording(self):
        """Toggle audio recording (Module 9 - v3.3.0)"""
        if not self.window.audio_recorder.is_recording:
            # Start recording
            self.window.audio_recorder.start_recording()
            self.window.record_btn.setText("⏹ STOP REC")
            self.window.record_btn.setStyleSheet("""
                QPushButton {
                    background: #00aa00;
                    color: white;
                    font-weight: bold;
                    padding: 8px 15px;
                    border-radius: 4px;
                }
                QPushButton:hover {
                    background: #00cc00;
                }
            """)
            log("Recording started", "INFO")
        else:
            # Stop recording and save
            self.window.audio_recorder.stop_recording()

            # Generate filename with timestamp
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"Radar Games ML_Recording_{timestamp}.wav"

            # Save to file
            if self.window.audio_recorder.save_to_wav(filename):
                self.window.status_bar.showMessage(f"✓ Recording saved: {filename}")
            else:
                self.window.status_bar.showMessage("❌ Failed to save recording")

            # Reset button
            self.window.record_btn.setText("⏺ REC")
            self.window.record_btn.setStyleSheet("""
                QPushButton {
                    background: #aa0000;
                    color: white;
                    font-weight: bold;
                    padding: 8px 15px;
                    border-radius: 4px;
                }
                QPushButton:hover {
                    background: #cc0000;
                }
            """)

            log(f"Recording saved to {filename}", "INFO")

    # ========================================================================
    # QUICK SETUP
    # ========================================================================

    def quick_setup_game_audio(self):
        """Quick setup for game audio capture (v3.1.0 - Fixed to restart audio when running)"""
        log("Quick Setup: Enabling game audio capture", "INFO")

        try:
            # Remember if we were running
            was_running = self.window.is_running

            # Stop audio if running (to apply new settings)
            if self.window.is_running:
                log("Quick Setup: Stopping audio to apply new settings", "INFO")
                self.window.stop()

            # Enable loopback mode
            self.window.dev_panel.loopback_mode.setChecked(True)

            # Try to find and select a loopback device
            found_loopback = False
            for i in range(self.window.dev_panel.device_combo.count()):
                device_name = self.window.dev_panel.device_combo.itemText(i).lower()
                if 'loopback' in device_name or 'speaker' in device_name or 'output' in device_name:
                    self.window.dev_panel.device_combo.setCurrentIndex(i)
                    log(f"Quick Setup: Selected device: {self.window.dev_panel.device_combo.itemText(i)}", "INFO")
                    found_loopback = True
                    break

            # Apply settings
            self.window.dev_panel.apply_settings()

            # Restart audio if it was running before
            if was_running:
                log("Quick Setup: Restarting audio with new settings", "INFO")
                self.window.start()

            # Show success message
            if found_loopback:
                self.window.status_bar.showMessage(
                    "✓ Quick Setup Complete! Loopback mode enabled. Press START to capture game audio." if get_language() == 'en'
                    else "✓ Szybka konfiguracja zakończona! Tryb loopback włączony. Naciśnij START aby przechwycić dźwięk."
                )
            else:
                self.window.status_bar.showMessage(
                    "⚠ Loopback mode enabled, but no loopback device found. Check Tab 2 settings." if get_language() == 'en'
                    else "⚠ Tryb loopback włączony, ale nie znaleziono urządzenia. Sprawdź ustawienia w Zakładce 2."
                )

            # Switch to Detection & Audio tab to see settings
            self.window.main_tabs.setCurrentIndex(1)

        except Exception as e:
            log(f"Error in quick_setup_game_audio: {e}", "ERROR")
            import traceback
            log(traceback.format_exc(), "ERROR")
            self.window.status_bar.showMessage(
                "❌ Quick Setup failed - please configure manually (Tab 2)" if get_language() == 'en'
                else "❌ Szybka konfiguracja nie powiodła się - skonfiguruj ręcznie (Zakładka 2)"
            )
