"""AudioRadar v11 - Modern GUI with Control Panel

This is the main GUI application featuring:
- Borderless draggable window
- Always-on-top mode
- Control panel with sliders and buttons
- Real-time stats overlay (Peak/RMS)
- Comprehensive logging
- Auto-detect Stereo Mix
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
import logging
from pathlib import Path
from datetime import datetime
import json
from typing import Optional, Dict, Any

try:
    import pygame
except ImportError:
    pygame = None

try:
    import sounddevice as sd
    import numpy as np
except ImportError:
    sd = None
    np = None


class AudioRadarGUI:
    """Modern GUI for AudioRadar v11 with full control panel."""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("AudioRadar v11")
        
        # Configuration
        self.config = self.load_config()
        self.is_detecting = False
        self.is_dragging = False
        self.drag_x = 0
        self.drag_y = 0
        
        # Audio stats
        self.current_peak = 0.0
        self.current_rms = 0.0
        self.current_direction = 0
        self.current_distance = 0.0
        
        # Setup logging
        self.setup_logging()
        self.logger.info("AudioRadar v11 starting...")
        
        # Build GUI
        self.setup_window()
        self.create_widgets()
        self.setup_bindings()
        
        # Initialize audio
        self.audio_thread = None
        self.pygame_surface = None
        
        self.logger.info("GUI initialized successfully")
    
    def setup_logging(self):
        """Setup comprehensive logging to file."""
        log_dir = Path(__file__).parent
        log_file = log_dir / "audioradar_v11.log"
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s [%(levelname)s] %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def load_config(self) -> Dict[str, Any]:
        """Load configuration from file or create defaults."""
        config_path = Path(__file__).parent / "config_v11.json"
        
        default_config = {
            "window": {
                "width": 800,
                "height": 600,
                "always_on_top": True,
                "borderless": False,
                "opacity": 0.95
            },
            "detection": {
                "volume_threshold": 0.3,
                "sensitivity": 0.5,
                "enable_filter": True,
                "auto_calibrate": False,
                "shot_peak_threshold": 0.6,
                "footstep_std_threshold": 0.05
            },
            "audio": {
                "samplerate": 48000,
                "blocksize": 1024,
                "channels": 2,
                "device": None
            },
            "visualization": {
                "show_stats": True,
                "fade_duration": 0.5,
                "footstep_color": [0, 255, 0],
                "shot_color": [255, 0, 0]
            }
        }
        
        if config_path.exists():
            try:
                with open(config_path, 'r') as f:
                    loaded = json.load(f)
                    # Merge with defaults
                    for key in default_config:
                        if key in loaded:
                            default_config[key].update(loaded[key])
            except Exception as e:
                print(f"Error loading config: {e}")
        
        return default_config
    
    def save_config(self):
        """Save current configuration to file."""
        config_path = Path(__file__).parent / "config_v11.json"
        try:
            with open(config_path, 'w') as f:
                json.dump(self.config, f, indent=2)
            self.logger.info("Configuration saved")
        except Exception as e:
            self.logger.error(f"Error saving config: {e}")
    
    def setup_window(self):
        """Setup window properties."""
        # Window size
        width = self.config["window"]["width"]
        height = self.config["window"]["height"]
        
        # Center on screen
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        
        # Always on top
        if self.config["window"]["always_on_top"]:
            self.root.attributes('-topmost', True)
        
        # Opacity
        self.root.attributes('-alpha', self.config["window"]["opacity"])
        
        # Optional borderless (can be toggled)
        if self.config["window"]["borderless"]:
            self.root.overrideredirect(True)
    
    def create_widgets(self):
        """Create all GUI widgets."""
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        # Title bar (for dragging when borderless)
        title_frame = ttk.Frame(main_frame)
        title_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        title_label = ttk.Label(title_frame, text="AudioRadar v11", font=('Arial', 14, 'bold'))
        title_label.pack(side=tk.LEFT)
        
        # Control Panel Frame
        control_frame = ttk.LabelFrame(main_frame, text="Control Panel", padding="10")
        control_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N), padx=(0, 10))
        
        # Buttons
        btn_frame = ttk.Frame(control_frame)
        btn_frame.grid(row=0, column=0, columnspan=2, pady=(0, 10))
        
        self.start_btn = ttk.Button(btn_frame, text="Start Detection", command=self.start_detection)
        self.start_btn.pack(side=tk.LEFT, padx=5)
        
        self.stop_btn = ttk.Button(btn_frame, text="Stop Detection", command=self.stop_detection, state=tk.DISABLED)
        self.stop_btn.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(btn_frame, text="Calibrate", command=self.calibrate).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Reset", command=self.reset_settings).pack(side=tk.LEFT, padx=5)
        
        # Sliders
        row = 1
        
        # Volume Threshold
        ttk.Label(control_frame, text="Volume Threshold:").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.volume_slider = ttk.Scale(control_frame, from_=0.0, to=1.0, orient=tk.HORIZONTAL,
                                        command=self.on_volume_change)
        self.volume_slider.set(self.config["detection"]["volume_threshold"])
        self.volume_slider.grid(row=row, column=1, sticky=(tk.W, tk.E), pady=5)
        self.volume_label = ttk.Label(control_frame, text=f"{self.config['detection']['volume_threshold']:.2f}")
        self.volume_label.grid(row=row, column=2, padx=5)
        row += 1
        
        # Sensitivity
        ttk.Label(control_frame, text="Sensitivity:").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.sensitivity_slider = ttk.Scale(control_frame, from_=0.0, to=1.0, orient=tk.HORIZONTAL,
                                            command=self.on_sensitivity_change)
        self.sensitivity_slider.set(self.config["detection"]["sensitivity"])
        self.sensitivity_slider.grid(row=row, column=1, sticky=(tk.W, tk.E), pady=5)
        self.sensitivity_label = ttk.Label(control_frame, text=f"{self.config['detection']['sensitivity']:.2f}")
        self.sensitivity_label.grid(row=row, column=2, padx=5)
        row += 1
        
        # Window Opacity
        ttk.Label(control_frame, text="Window Opacity:").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.opacity_slider = ttk.Scale(control_frame, from_=0.3, to=1.0, orient=tk.HORIZONTAL,
                                        command=self.on_opacity_change)
        self.opacity_slider.set(self.config["window"]["opacity"])
        self.opacity_slider.grid(row=row, column=1, sticky=(tk.W, tk.E), pady=5)
        self.opacity_label = ttk.Label(control_frame, text=f"{self.config['window']['opacity']:.2f}")
        self.opacity_label.grid(row=row, column=2, padx=5)
        row += 1
        
        # Checkboxes
        self.show_stats_var = tk.BooleanVar(value=self.config["visualization"]["show_stats"])
        ttk.Checkbutton(control_frame, text="Show Stats", variable=self.show_stats_var,
                        command=self.on_checkbox_change).grid(row=row, column=0, columnspan=2, sticky=tk.W, pady=5)
        row += 1
        
        self.enable_filter_var = tk.BooleanVar(value=self.config["detection"]["enable_filter"])
        ttk.Checkbutton(control_frame, text="Enable Filter", variable=self.enable_filter_var,
                        command=self.on_checkbox_change).grid(row=row, column=0, columnspan=2, sticky=tk.W, pady=5)
        row += 1
        
        self.auto_calibrate_var = tk.BooleanVar(value=self.config["detection"]["auto_calibrate"])
        ttk.Checkbutton(control_frame, text="Auto-Calibrate", variable=self.auto_calibrate_var,
                        command=self.on_checkbox_change).grid(row=row, column=0, columnspan=2, sticky=tk.W, pady=5)
        row += 1
        
        # Stats Display Frame
        stats_frame = ttk.LabelFrame(main_frame, text="Real-time Statistics", padding="10")
        stats_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Status indicator
        self.status_label = ttk.Label(stats_frame, text="Status: Idle", font=('Arial', 10, 'bold'))
        self.status_label.grid(row=0, column=0, columnspan=2, pady=(0, 10))
        
        # Stats
        ttk.Label(stats_frame, text="Peak:").grid(row=1, column=0, sticky=tk.W, pady=3)
        self.peak_value = ttk.Label(stats_frame, text="0.000")
        self.peak_value.grid(row=1, column=1, sticky=tk.W, pady=3)
        
        ttk.Label(stats_frame, text="RMS:").grid(row=2, column=0, sticky=tk.W, pady=3)
        self.rms_value = ttk.Label(stats_frame, text="0.000")
        self.rms_value.grid(row=2, column=1, sticky=tk.W, pady=3)
        
        ttk.Label(stats_frame, text="Direction:").grid(row=3, column=0, sticky=tk.W, pady=3)
        self.direction_value = ttk.Label(stats_frame, text="0°")
        self.direction_value.grid(row=3, column=1, sticky=tk.W, pady=3)
        
        ttk.Label(stats_frame, text="Distance:").grid(row=4, column=0, sticky=tk.W, pady=3)
        self.distance_value = ttk.Label(stats_frame, text="0.0m")
        self.distance_value.grid(row=4, column=1, sticky=tk.W, pady=3)
        
        ttk.Label(stats_frame, text="Audio Device:").grid(row=5, column=0, sticky=tk.W, pady=3)
        self.device_value = ttk.Label(stats_frame, text="None")
        self.device_value.grid(row=5, column=1, sticky=tk.W, pady=3)
        
        # Radar Visualization Frame
        radar_frame = ttk.LabelFrame(main_frame, text="Radar Visualization", padding="10")
        radar_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        
        # Placeholder for radar (will use pygame or canvas)
        self.radar_canvas = tk.Canvas(radar_frame, width=400, height=400, bg='black')
        self.radar_canvas.pack()
        
        # Draw basic radar circles
        self.draw_radar_base()
        
        # Configure grid weights for resizing
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
    
    def draw_radar_base(self):
        """Draw base radar circles and lines."""
        canvas = self.radar_canvas
        width = 400
        height = 400
        center_x = width // 2
        center_y = height // 2
        
        # Draw concentric circles
        for radius in [50, 100, 150, 180]:
            canvas.create_oval(center_x - radius, center_y - radius,
                             center_x + radius, center_y + radius,
                             outline='dark green', width=1)
        
        # Draw direction lines (8 directions)
        import math
        for angle in range(0, 360, 45):
            rad = math.radians(angle)
            x = center_x + 180 * math.cos(rad)
            y = center_y + 180 * math.sin(rad)
            canvas.create_line(center_x, center_y, x, y, fill='dark green', width=1)
        
        # Center dot
        canvas.create_oval(center_x-3, center_y-3, center_x+3, center_y+3, fill='green')
    
    def setup_bindings(self):
        """Setup event bindings for dragging etc."""
        # Bind title label for dragging
        def start_drag(event):
            self.is_dragging = True
            self.drag_x = event.x
            self.drag_y = event.y
        
        def stop_drag(event):
            self.is_dragging = False
        
        def do_drag(event):
            if self.is_dragging:
                x = self.root.winfo_x() + event.x - self.drag_x
                y = self.root.winfo_y() + event.y - self.drag_y
                self.root.geometry(f"+{x}+{y}")
        
        # Bind to root for dragging anywhere when borderless
        if self.config["window"]["borderless"]:
            self.root.bind("<Button-1>", start_drag)
            self.root.bind("<ButtonRelease-1>", stop_drag)
            self.root.bind("<B1-Motion>", do_drag)
    
    def on_volume_change(self, value):
        """Handle volume threshold slider change."""
        val = float(value)
        self.config["detection"]["volume_threshold"] = val
        self.volume_label.config(text=f"{val:.2f}")
        self.logger.debug(f"Volume threshold changed to {val:.2f}")
    
    def on_sensitivity_change(self, value):
        """Handle sensitivity slider change."""
        val = float(value)
        self.config["detection"]["sensitivity"] = val
        self.sensitivity_label.config(text=f"{val:.2f}")
        self.logger.debug(f"Sensitivity changed to {val:.2f}")
    
    def on_opacity_change(self, value):
        """Handle opacity slider change."""
        val = float(value)
        self.config["window"]["opacity"] = val
        self.opacity_label.config(text=f"{val:.2f}")
        self.root.attributes('-alpha', val)
        self.logger.debug(f"Opacity changed to {val:.2f}")
    
    def on_checkbox_change(self):
        """Handle checkbox state changes."""
        self.config["visualization"]["show_stats"] = self.show_stats_var.get()
        self.config["detection"]["enable_filter"] = self.enable_filter_var.get()
        self.config["detection"]["auto_calibrate"] = self.auto_calibrate_var.get()
        self.logger.debug(f"Checkbox states updated")
    
    def start_detection(self):
        """Start audio detection."""
        if self.is_detecting:
            return
        
        self.logger.info("Starting detection...")
        self.is_detecting = True
        self.start_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        self.status_label.config(text="Status: Detecting", foreground='green')
        
        # Auto-detect Stereo Mix or loopback device
        device = self.auto_detect_device()
        if device is not None:
            self.device_value.config(text=device[1] if isinstance(device, tuple) else str(device))
            self.logger.info(f"Using audio device: {device}")
        else:
            self.logger.warning("No loopback device found, using default")
        
        # Start audio processing thread
        self.audio_thread = threading.Thread(target=self.audio_processing_loop, daemon=True)
        self.audio_thread.start()
        
        # Start stats update
        self.update_stats()
    
    def stop_detection(self):
        """Stop audio detection."""
        if not self.is_detecting:
            return
        
        self.logger.info("Stopping detection...")
        self.is_detecting = False
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.status_label.config(text="Status: Idle", foreground='black')
    
    def auto_detect_device(self):
        """Auto-detect Stereo Mix or other loopback device."""
        if sd is None:
            return None
        
        try:
            devices = sd.query_devices()
            loopback_keywords = ['stereo mix', 'wave out mix', 'what u hear', 'loopback']
            
            for idx, dev in enumerate(devices):
                if dev.get('max_input_channels', 0) > 0:
                    name_lower = dev.get('name', '').lower()
                    for keyword in loopback_keywords:
                        if keyword in name_lower:
                            self.logger.info(f"Auto-detected loopback device: {dev['name']}")
                            return (idx, dev['name'])
            
            self.logger.warning("No loopback device found automatically")
            return None
        except Exception as e:
            self.logger.error(f"Error detecting device: {e}")
            return None
    
    def audio_processing_loop(self):
        """Main audio processing loop (runs in separate thread)."""
        if sd is None or np is None:
            self.logger.error("sounddevice or numpy not available")
            return
        
        try:
            samplerate = self.config["audio"]["samplerate"]
            blocksize = self.config["audio"]["blocksize"]
            channels = self.config["audio"]["channels"]
            device = self.config["audio"]["device"]
            
            def callback(indata, frames, time_info, status):
                if status:
                    self.logger.warning(f"Audio status: {status}")
                
                if not self.is_detecting:
                    return
                
                # Calculate stats
                audio_data = indata[:, 0] if channels > 1 else indata
                self.current_peak = float(np.max(np.abs(audio_data)))
                self.current_rms = float(np.sqrt(np.mean(audio_data**2)))
                
                # Simple direction detection (placeholder)
                if self.current_peak > self.config["detection"]["volume_threshold"]:
                    self.current_direction = (self.current_direction + 45) % 360
                    self.current_distance = self.current_peak * 10
            
            with sd.InputStream(callback=callback, channels=channels,
                              samplerate=samplerate, blocksize=blocksize,
                              device=device):
                self.logger.info("Audio stream opened")
                while self.is_detecting:
                    time.sleep(0.1)
        
        except Exception as e:
            self.logger.error(f"Audio processing error: {e}", exc_info=True)
            self.root.after(0, lambda: messagebox.showerror("Audio Error", str(e)))
            self.root.after(0, self.stop_detection)
    
    def update_stats(self):
        """Update statistics display."""
        if self.is_detecting:
            self.peak_value.config(text=f"{self.current_peak:.3f}")
            self.rms_value.config(text=f"{self.current_rms:.3f}")
            self.direction_value.config(text=f"{self.current_direction}°")
            self.distance_value.config(text=f"{self.current_distance:.1f}m")
            
            # Update radar visualization
            if self.current_peak > self.config["detection"]["volume_threshold"]:
                self.draw_detection_on_radar(self.current_direction, self.current_peak)
            
            self.root.after(50, self.update_stats)
    
    def draw_detection_on_radar(self, direction, intensity):
        """Draw detection indicator on radar."""
        import math
        canvas = self.radar_canvas
        center_x = 200
        center_y = 200
        
        # Clear previous
        canvas.delete("detection")
        
        # Draw detection line
        rad = math.radians(direction - 90)  # Adjust for canvas coordinates
        length = 150 * min(intensity * 3, 1.0)
        x = center_x + length * math.cos(rad)
        y = center_y + length * math.sin(rad)
        
        color = 'red' if intensity > 0.7 else 'yellow' if intensity > 0.4 else 'green'
        canvas.create_line(center_x, center_y, x, y, fill=color, width=3, tags="detection")
        canvas.create_oval(x-5, y-5, x+5, y+5, fill=color, tags="detection")
    
    def calibrate(self):
        """Run calibration process."""
        self.logger.info("Calibration started")
        messagebox.showinfo("Calibration", 
                          "Calibration started. Play typical game audio for 5 seconds.\n\n"
                          "The system will automatically adjust sensitivity.")
        
        # TODO: Implement actual calibration logic
        if self.config["detection"]["auto_calibrate"]:
            # Auto-calibration logic here
            pass
    
    def reset_settings(self):
        """Reset all settings to defaults."""
        if messagebox.askyesno("Reset", "Reset all settings to defaults?"):
            self.config = self.load_config()
            self.volume_slider.set(self.config["detection"]["volume_threshold"])
            self.sensitivity_slider.set(self.config["detection"]["sensitivity"])
            self.opacity_slider.set(self.config["window"]["opacity"])
            self.show_stats_var.set(self.config["visualization"]["show_stats"])
            self.enable_filter_var.set(self.config["detection"]["enable_filter"])
            self.auto_calibrate_var.set(self.config["detection"]["auto_calibrate"])
            self.logger.info("Settings reset to defaults")
    
    def on_closing(self):
        """Handle window close event."""
        if self.is_detecting:
            self.stop_detection()
        
        self.save_config()
        self.logger.info("AudioRadar v11 shutting down")
        self.root.destroy()
    
    def run(self):
        """Start the GUI main loop."""
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.logger.info("Starting GUI main loop")
        self.root.mainloop()


def main():
    """Main entry point."""
    app = AudioRadarGUI()
    app.run()


if __name__ == "__main__":
    main()
