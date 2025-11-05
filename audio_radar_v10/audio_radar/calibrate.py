#!/usr/bin/env python
"""Calibration utility for Audio Radar.

This script helps users find optimal detection thresholds for their specific
audio setup and games. It monitors audio input and displays real-time
statistics to help tune the configuration.
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

import time
import json
from pathlib import Path
from typing import Dict, Any

try:
    import numpy as np
    import sounddevice as sd
except ImportError:
    print("Error: Required packages not installed.")
    print("Please run: pip install numpy sounddevice")
    sys.exit(1)

from audio_capture import AudioStream, list_audio_input_devices


class AudioCalibrator:
    """Real-time audio calibration tool."""
    
    def __init__(self, device_index=None, samplerate=48000, blocksize=1024):
        self.device_index = device_index
        self.samplerate = samplerate
        self.blocksize = blocksize
        
        # Statistics
        self.peak_values = []
        self.rms_values = []
        self.std_values = []
        self.max_samples = 100  # Keep last 100 blocks
        
        self.running = False
        
    def process_block(self, samples):
        """Process an audio block and update statistics."""
        if samples.ndim == 2:
            mono = samples.mean(axis=1)
        else:
            mono = samples.ravel()
            
        # Normalize if needed
        if np.issubdtype(mono.dtype, np.integer):
            info = np.iinfo(mono.dtype)
            mono = mono.astype(np.float32) / max(abs(info.min), info.max)
            
        # Calculate statistics
        peak = np.max(np.abs(mono))
        rms = np.sqrt(np.mean(mono ** 2))
        std = np.std(mono)
        
        # Store values
        self.peak_values.append(peak)
        self.rms_values.append(rms)
        self.std_values.append(std)
        
        # Trim to max samples
        if len(self.peak_values) > self.max_samples:
            self.peak_values.pop(0)
            self.rms_values.pop(0)
            self.std_values.pop(0)
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get current audio statistics."""
        if not self.peak_values:
            return {
                "peak_current": 0.0,
                "peak_max": 0.0,
                "peak_avg": 0.0,
                "rms_current": 0.0,
                "rms_avg": 0.0,
                "std_current": 0.0,
                "std_max": 0.0,
                "std_avg": 0.0,
            }
        
        return {
            "peak_current": self.peak_values[-1],
            "peak_max": max(self.peak_values),
            "peak_avg": np.mean(self.peak_values),
            "rms_current": self.rms_values[-1],
            "rms_avg": np.mean(self.rms_values),
            "std_current": self.std_values[-1],
            "std_max": max(self.std_values),
            "std_avg": np.mean(self.std_values),
        }
    
    def run(self):
        """Run calibration in interactive mode."""
        print("=== Audio Radar Calibration Tool ===\n")
        
        # Create audio stream
        stream = AudioStream(
            input_device=self.device_index,
            samplerate=self.samplerate,
            blocksize=self.blocksize
        )
        
        stream.on_data = self.process_block
        
        print("Instructions:")
        print("1. Play your game and make various sounds (footsteps, gunshots, etc.)")
        print("2. Observe the statistics below")
        print("3. Press Ctrl+C when done to see recommendations\n")
        
        print("Starting audio monitoring...\n")
        
        try:
            stream.start()
            self.running = True
            
            last_update = time.time()
            while self.running:
                time.sleep(0.1)
                
                # Update display every second
                if time.time() - last_update >= 1.0:
                    stats = self.get_statistics()
                    
                    # Clear screen (works on most terminals)
                    print("\033[2J\033[H", end="")
                    
                    print("=== Audio Statistics (Live) ===\n")
                    print(f"Peak Amplitude:")
                    print(f"  Current: {stats['peak_current']:.4f}")
                    print(f"  Maximum: {stats['peak_max']:.4f}")
                    print(f"  Average: {stats['peak_avg']:.4f}")
                    print()
                    print(f"RMS Level:")
                    print(f"  Current: {stats['rms_current']:.4f}")
                    print(f"  Average: {stats['rms_avg']:.4f}")
                    print()
                    print(f"Standard Deviation:")
                    print(f"  Current: {stats['std_current']:.4f}")
                    print(f"  Maximum: {stats['std_max']:.4f}")
                    print(f"  Average: {stats['std_avg']:.4f}")
                    print()
                    print("Press Ctrl+C to stop and get recommendations...")
                    
                    last_update = time.time()
                    
        except KeyboardInterrupt:
            print("\n\nStopping calibration...")
            self.running = False
        finally:
            stream.stop()
            
        # Show recommendations
        self.show_recommendations()
    
    def show_recommendations(self):
        """Display threshold recommendations based on observed audio."""
        stats = self.get_statistics()
        
        print("\n\n=== Calibration Recommendations ===\n")
        
        if not self.peak_values:
            print("Not enough data collected. Please run calibration longer.")
            return
        
        # Calculate recommended thresholds
        peak_max = stats['peak_max']
        std_max = stats['std_max']
        std_avg = stats['std_avg']
        
        # Gunshot threshold: 70-80% of maximum peak observed
        shot_threshold = max(0.5, min(0.9, peak_max * 0.75))
        
        # Footstep threshold: between average and maximum std
        footstep_threshold = max(0.03, min(0.15, (std_avg + std_max) / 2))
        
        print(f"Based on observed audio:\n")
        print(f"Recommended shot_peak_threshold: {shot_threshold:.2f}")
        print(f"  (Maximum peak observed: {peak_max:.4f})")
        print()
        print(f"Recommended footstep_std_threshold: {footstep_threshold:.3f}")
        print(f"  (Std deviation range: {std_avg:.4f} - {std_max:.4f})")
        print()
        
        # Suggest config update
        print("Suggested config.json settings:\n")
        print('"detection": {')
        print(f'  "shot_peak_threshold": {shot_threshold:.2f},')
        print(f'  "footstep_std_threshold": {footstep_threshold:.3f},')
        print('  "enable_bandpass_filter": true')
        print('}')
        print()
        
        # Ask to save
        response = input("Would you like to update config.json with these values? (y/n): ")
        if response.lower().strip() == 'y':
            self.update_config(shot_threshold, footstep_threshold)
    
    def update_config(self, shot_threshold: float, footstep_threshold: float):
        """Update config.json with new thresholds."""
        config_path = Path(__file__).parent / "config.json"
        
        try:
            # Load existing config
            if config_path.exists():
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
            else:
                config = {}
            
            # Update detection section
            if 'detection' not in config:
                config['detection'] = {}
            
            config['detection']['shot_peak_threshold'] = round(shot_threshold, 2)
            config['detection']['footstep_std_threshold'] = round(footstep_threshold, 3)
            
            # Save config
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2)
            
            print(f"\nConfiguration updated successfully!")
            print(f"Saved to: {config_path}")
            
        except Exception as e:
            print(f"\nError updating config: {e}")


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Audio Radar Calibration Tool")
    parser.add_argument(
        '--list-devices',
        action='store_true',
        help='List available audio input devices'
    )
    parser.add_argument(
        '--device',
        type=int,
        default=None,
        help='Audio input device index'
    )
    parser.add_argument(
        '--samplerate',
        type=int,
        default=48000,
        help='Audio sample rate (default: 48000)'
    )
    
    args = parser.parse_args()
    
    if args.list_devices:
        print("Available audio input devices:\n")
        for idx, name in list_audio_input_devices():
            print(f"  {idx}: {name}")
        return
    
    # Run calibration
    calibrator = AudioCalibrator(
        device_index=args.device,
        samplerate=args.samplerate
    )
    
    calibrator.run()


if __name__ == "__main__":
    main()
