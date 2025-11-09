"""Audio Test Window - Live audio level monitoring for Audio Radar.

This module provides a diagnostic window that displays real-time audio
levels, helping users verify that audio is being captured correctly from
their selected device. It shows RMS (average) and Peak levels, detection
counts, and provides feedback about signal quality.

Usage
-----
Can be launched standalone or from the main Audio Radar application.
Press 'T' in the main window to toggle test mode, or run:

    python audio_test_window.py --device <device_id>
"""

from __future__ import annotations

try:
    import pygame
except ImportError:
    pygame = None  # type: ignore

try:
    import sounddevice as sd
except ImportError:
    sd = None  # type: ignore

import numpy as np  # type: ignore
import time
from typing import Optional, Callable


class AudioTestWindow:
    """Pygame window for testing audio input levels.
    
    Displays real-time RMS and Peak levels, detection counts, and provides
    visual feedback about signal quality. Users can observe whether their
    audio device is working and if levels are appropriate for detection.
    
    Parameters
    ----------
    device_id : Optional[int]
        The audio device to test. If None, uses system default.
    samplerate : int
        Sample rate for audio capture (default 48000 Hz).
    blocksize : int
        Buffer size for audio capture (default 2048 samples).
    threshold : float
        Detection threshold for counting events (default 0.05).
    """
    
    def __init__(
        self,
        device_id: Optional[int] = None,
        samplerate: int = 48000,
        blocksize: int = 2048,
        threshold: float = 0.05
    ) -> None:
        if pygame is None:
            raise RuntimeError("Pygame library is required for AudioTestWindow")
        if sd is None:
            raise RuntimeError("sounddevice library is required for AudioTestWindow")
        
        pygame.init()
        self.screen = pygame.display.set_mode((600, 500))
        pygame.display.set_caption("Audio Test - AudioRadar v10.1")
        self.clock = pygame.time.Clock()
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 32)
        self.font_small = pygame.font.Font(None, 24)
        
        self.device_id = device_id
        self.samplerate = samplerate
        self.blocksize = blocksize
        self.threshold = threshold
        
        # Stats
        self.current_rms = 0.0
        self.current_peak = 0.0
        self.max_rms = 0.0
        self.max_peak = 0.0
        self.detection_count = 0
        self.frame_count = 0
        
        # Audio stream
        self.stream: Optional[sd.InputStream] = None
        self.is_running = False
        
        # Log messages
        self.log_messages = []
        self.max_log_lines = 8
        
    def add_log(self, message: str) -> None:
        """Add a message to the log display."""
        self.log_messages.append(f"{time.strftime('%H:%M:%S')}: {message}")
        if len(self.log_messages) > self.max_log_lines:
            self.log_messages.pop(0)
    
    def audio_callback(self, indata: np.ndarray, frames: int, time_info, status) -> None:
        """Callback for audio stream - processes incoming audio."""
        if not self.is_running:
            return
        
        if status:
            self.add_log(f"Status: {status}")
        
        # Calculate levels
        if indata.size > 0:
            # Convert to mono if multi-channel
            if indata.ndim == 2 and indata.shape[1] > 1:
                mono = indata.mean(axis=1)
            else:
                mono = indata.ravel()
            
            # Calculate RMS and Peak
            rms = float(np.sqrt(np.mean(mono**2)))
            peak = float(np.max(np.abs(mono)))
            
            # Update current values
            self.current_rms = rms
            self.current_peak = peak
            
            # Update maximums
            self.max_rms = max(self.max_rms, rms)
            self.max_peak = max(self.max_peak, peak)
            
            # Count detections
            if peak > self.threshold:
                self.detection_count += 1
                if self.detection_count % 10 == 0:
                    self.add_log(f"Detection #{self.detection_count}: Peak={peak:.4f}")
            
            self.frame_count += 1
    
    def start_stream(self) -> bool:
        """Start the audio stream. Returns True on success."""
        try:
            self.add_log("Starting audio stream...")
            self.add_log(f"Device: {self.device_id or 'default'}")
            self.add_log(f"Samplerate: {self.samplerate} Hz")
            self.add_log(f"Blocksize: {self.blocksize} samples")
            
            # Calculate latency
            latency_ms = (self.blocksize / self.samplerate) * 1000
            self.add_log(f"Buffer latency: {latency_ms:.1f} ms")
            
            self.is_running = True
            self.stream = sd.InputStream(
                device=self.device_id,
                channels=2,
                samplerate=self.samplerate,
                blocksize=self.blocksize,
                callback=self.audio_callback
            )
            self.stream.start()
            self.add_log("✓ Stream started successfully")
            return True
        except Exception as e:
            self.add_log(f"✗ ERROR: {e}")
            self.is_running = False
            return False
    
    def stop_stream(self) -> None:
        """Stop the audio stream."""
        self.is_running = False
        if self.stream:
            try:
                self.stream.stop()
                self.stream.close()
                self.add_log("Stream stopped")
            except Exception as e:
                self.add_log(f"Error stopping stream: {e}")
            finally:
                self.stream = None
    
    def draw_bar(self, y: int, label: str, value: float, max_value: float, color: tuple) -> None:
        """Draw a level bar with label."""
        bar_x = 150
        bar_y = y
        bar_width = 400
        bar_height = 30
        
        # Label
        text = self.font_small.render(label, True, (200, 200, 200))
        self.screen.blit(text, (10, bar_y))
        
        # Background bar
        pygame.draw.rect(self.screen, (40, 40, 40), (bar_x, bar_y, bar_width, bar_height))
        
        # Value bar
        if value > 0:
            filled_width = int(min(value * 1000, bar_width))
            pygame.draw.rect(self.screen, color, (bar_x, bar_y, filled_width, bar_height))
        
        # Border
        pygame.draw.rect(self.screen, (100, 100, 100), (bar_x, bar_y, bar_width, bar_height), 2)
        
        # Value text
        value_text = f"{value:.6f}"
        max_text = f"max: {max_value:.6f}"
        text_surf = self.font_small.render(value_text, True, (255, 255, 255))
        max_surf = self.font_small.render(max_text, True, (150, 150, 150))
        self.screen.blit(text_surf, (bar_x + 5, bar_y + 5))
        self.screen.blit(max_surf, (bar_x + bar_width - 150, bar_y + 5))
    
    def draw(self) -> None:
        """Draw the test window interface."""
        self.screen.fill((20, 20, 25))
        
        # Title
        title = self.font_large.render("🔊 AUDIO TEST", True, (100, 200, 255))
        self.screen.blit(title, (150, 10))
        
        # Instructions
        inst = self.font_small.render("Odtwórz coś GŁOŚNO i obserwuj poziomy", True, (180, 180, 180))
        self.screen.blit(inst, (120, 60))
        
        # RMS bar
        self.draw_bar(100, "RMS:", self.current_rms, self.max_rms, (50, 200, 50))
        
        # Peak bar
        self.draw_bar(150, "Peak:", self.current_peak, self.max_peak, (200, 200, 50))
        
        # Threshold indicator
        threshold_y = 210
        thresh_text = f"Próg detekcji: {self.threshold:.3f}"
        thresh_surf = self.font_small.render(thresh_text, True, (200, 150, 50))
        self.screen.blit(thresh_surf, (150, threshold_y))
        
        # Detection count
        det_text = f"Wykrycia: {self.detection_count}"
        det_color = (50, 255, 50) if self.detection_count > 0 else (150, 150, 150)
        det_surf = self.font_medium.render(det_text, True, det_color)
        self.screen.blit(det_surf, (150, threshold_y + 30))
        
        # Signal quality indicator
        quality_y = threshold_y + 70
        if self.max_peak < 0.001:
            quality = "⚠️ Prawie zero sygnału!"
            quality_color = (255, 50, 50)
            advice = "Sprawdź wybrane urządzenie i czy coś gra"
        elif self.max_peak < 0.05:
            quality = "⚠️ Słaby sygnał"
            quality_color = (255, 200, 50)
            advice = "Zwiększ głośność lub zmniejsz próg"
        else:
            quality = "✓ Sygnał OK!"
            quality_color = (50, 255, 50)
            advice = "Audio działa prawidłowo"
        
        quality_surf = self.font_medium.render(quality, True, quality_color)
        self.screen.blit(quality_surf, (150, quality_y))
        
        advice_surf = self.font_small.render(advice, True, (180, 180, 180))
        self.screen.blit(advice_surf, (150, quality_y + 35))
        
        # Log section
        log_y = 380
        log_title = self.font_small.render("Log:", True, (150, 150, 150))
        self.screen.blit(log_title, (10, log_y))
        
        for i, msg in enumerate(self.log_messages[-6:]):
            msg_surf = self.font_small.render(msg[:70], True, (200, 200, 200))
            self.screen.blit(msg_surf, (10, log_y + 25 + i * 18))
        
        # Controls
        controls = "ESC - zamknij test"
        controls_surf = self.font_small.render(controls, True, (100, 100, 100))
        self.screen.blit(controls_surf, (10, 475))
    
    def run(self) -> None:
        """Run the test window main loop."""
        if not self.start_stream():
            # Failed to start, show error for a moment then close
            time.sleep(2)
            return
        
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
            
            self.draw()
            pygame.display.flip()
            self.clock.tick(30)  # 30 FPS for test window
        
        # Show summary before closing
        self.add_log("")
        self.add_log("=== PODSUMOWANIE ===")
        self.add_log(f"Max RMS: {self.max_rms:.6f}")
        self.add_log(f"Max Peak: {self.max_peak:.6f}")
        self.add_log(f"Wykrycia: {self.detection_count}")
        self.draw()
        pygame.display.flip()
        time.sleep(2)  # Show summary for 2 seconds
        
        self.stop_stream()
        pygame.quit()


def main() -> None:
    """Standalone entry point for audio testing."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Audio Test Window for AudioRadar")
    parser.add_argument("--device", type=int, help="Audio device ID", default=None)
    parser.add_argument("--samplerate", type=int, help="Sample rate", default=48000)
    parser.add_argument("--blocksize", type=int, help="Block size", default=2048)
    parser.add_argument("--threshold", type=float, help="Detection threshold", default=0.05)
    
    args = parser.parse_args()
    
    window = AudioTestWindow(
        device_id=args.device,
        samplerate=args.samplerate,
        blocksize=args.blocksize,
        threshold=args.threshold
    )
    window.run()


if __name__ == "__main__":
    main()
