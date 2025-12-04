"""
RadarSuite v4.1.0 - Target Tracking
Target and TargetTracker for multi-target tracking
FIXED v4.1.0: Thread-safe operations with locks
"""

import time
import math
import threading
from collections import deque

from core.logger import log


class Target:
    """Represents a single tracked target"""

    def __init__(self, target_id, angle, distance, elevation=0, target_type='unknown'):
        self.id = target_id
        self.angle = angle  # Azimuth in degrees
        self.distance = distance  # Distance in meters
        self.elevation = elevation  # Elevation in degrees
        self.type = target_type  # 'footstep', 'voice', 'shot', 'unknown'

        # Tracking data
        self.last_update_time = time.time()
        self.lifetime = 0.0
        self.update_count = 1

        # Movement history (for trails)
        self.history = [(angle, distance, elevation)]
        self.max_history = 10

        # Confidence and persistence
        self.confidence = 1.0
        self.is_active = True

    def update(self, angle, distance, elevation):
        """Update target position"""
        self.angle = angle
        self.distance = distance
        self.elevation = elevation
        self.last_update_time = time.time()
        self.update_count += 1
        self.confidence = min(1.0, self.confidence + 0.1)

        # Add to history
        self.history.append((angle, distance, elevation))
        if len(self.history) > self.max_history:
            self.history.pop(0)

    def decay(self, dt):
        """Decay confidence over time (for targets not updated)"""
        self.confidence -= dt * 0.5  # Lose 50% confidence per second
        self.lifetime += dt

        if self.confidence <= 0:
            self.is_active = False

    def get_color(self):
        """Get target color based on type and confidence"""
        # Base colors by type
        type_colors = {
            'footstep': (0, 1, 0),      # Green
            'voice': (0, 0.7, 1),        # Cyan
            'shot': (1, 0, 0),           # Red
            'unknown': (1, 1, 0)         # Yellow
        }

        base_color = type_colors.get(self.type, (1, 1, 0))
        alpha = max(0.3, self.confidence)  # Fade out as confidence decreases

        return (*base_color, alpha)



class TargetTracker:
    """
    Multi-target tracking system
    Tracks up to 3 simultaneous targets
    Assigns IDs, manages persistence, and handles target updates

    FIXED v4.1.0: Thread-safe with lock protection
    """

    def __init__(self, max_targets=3):
        log("TargetTracker.__init__", "INFO")

        self.max_targets = max_targets
        self.targets = {}  # {target_id: Target}
        self.next_id = 1

        # Tracking parameters
        self.merge_distance = 15.0  # Merge targets closer than 15m
        self.merge_angle = 20.0     # Merge targets within 20° angle
        self.timeout = 2.0          # Remove targets after 2s of no updates

        self.last_update_time = time.time()

        # FIXED v4.1.0: Thread safety
        self._lock = threading.Lock()

    def update(self, detections):
        """
        Update tracker with new detections (THREAD-SAFE v4.1.0)

        Args:
            detections: List of detection dicts with keys:
                       'angle', 'distance', 'elevation', 'type'
        """
        with self._lock:
            current_time = time.time()
            dt = current_time - self.last_update_time
            self.last_update_time = current_time

            # Decay existing targets
            for target in self.targets.values():
                target.decay(dt)

            # Remove inactive targets
            self.targets = {tid: t for tid, t in self.targets.items() if t.is_active}

            # Process new detections
            for detection in detections:
                angle = detection.get('angle', 0)
                distance = detection.get('distance', 50)
                elevation = detection.get('elevation', 0)
                target_type = detection.get('type', 'unknown')

                # Try to match with existing target
                matched_target = self._find_matching_target_unlocked(angle, distance, elevation)

                if matched_target:
                    # Update existing target
                    matched_target.update(angle, distance, elevation)
                elif len(self.targets) < self.max_targets:
                    # Create new target
                    new_target = Target(self.next_id, angle, distance, elevation, target_type)
                    self.targets[self.next_id] = new_target
                    self.next_id += 1
                    log(f"New target #{new_target.id} created: {target_type} at {distance:.1f}m", "INFO")

            return self._get_active_targets_unlocked()

    def _find_matching_target_unlocked(self, angle, distance, elevation):
        """Find existing target that matches the detection (must hold lock)"""
        best_match = None
        min_score = float('inf')

        for target in self.targets.values():
            # Calculate angular difference (handle wrap-around at 0°/360°)
            angle_diff = abs(angle - target.angle)
            if angle_diff > 180:
                angle_diff = 360 - angle_diff

            # Calculate distance difference
            dist_diff = abs(distance - target.distance)

            # Calculate elevation difference
            elev_diff = abs(elevation - target.elevation)

            # Combined score (lower is better)
            score = angle_diff + dist_diff + elev_diff * 0.5

            # Check if within merge thresholds
            if (angle_diff < self.merge_angle and
                dist_diff < self.merge_distance and
                score < min_score):
                best_match = target
                min_score = score

        return best_match

    def _get_active_targets_unlocked(self):
        """Get list of active targets (must hold lock)"""
        return [
            {
                'id': target.id,
                'angle': target.angle,
                'distance': target.distance,
                'elevation': target.elevation,
                'type': target.type,
                'confidence': target.confidence,
                'color': target.get_color(),
                'history': list(target.history)  # Copy to prevent concurrent modification
            }
            for target in self.targets.values()
            if target.is_active
        ]

    def get_active_targets(self):
        """Get list of active targets for display (THREAD-SAFE v4.1.0)"""
        with self._lock:
            return self._get_active_targets_unlocked()

    def clear(self):
        """Clear all targets (THREAD-SAFE v4.1.0)"""
        with self._lock:
            self.targets = {}
            self.next_id = 1

