"""Graphical visualisation for the Audio Radar project.

This module uses Pygame to create a simple 2D overlay that shows the
direction of detected sound events (footsteps and gunshots). Eight
radial bars emanate from the centre of the window, one for each
compass direction (N, NE, E, SE, S, SW, W, NW). When an event is
detected the corresponding bar lights up briefly with a colour
indicating the type of sound.

Users can adjust the width, height and transparency of the bars at
runtime via keyboard controls:

* ``Z/X`` – increase/decrease bar width
* ``C/V`` – increase/decrease bar height
* ``B/N`` – increase/decrease bar transparency

These adjustments are saved between sessions if written back to
``config.json`` by the calling code. Collision detection prevents bars
from overlapping by clamping the width to a sensible maximum.

Note that Pygame must be installed for this module to function. The
visualisation runs in its own loop; use ``trigger_event`` to signal
detected sounds from another thread.
"""

from __future__ import annotations

try:
    import pygame
except ImportError:
    pygame = None  # type: ignore
import math
import time
from typing import Tuple, List


class Bar:
    """Represents a single radial bar on the visualisation.

    Each bar knows its orientation (angle in radians), size and the
    duration for which it should remain lit after an event. The bar is
    drawn as a rotated rectangle anchored at the centre of the screen.
    """

    def __init__(
        self,
        angle_deg: float,
        width: int,
        height: int,
        transparency: int,
        colour_footstep: Tuple[int, int, int] = (0, 255, 0),
        colour_shot: Tuple[int, int, int] = (255, 0, 0),
    ) -> None:
        self.angle = math.radians(angle_deg)
        self.width = width
        self.height = height
        self.transparency = transparency
        self.colour_footstep = colour_footstep
        self.colour_shot = colour_shot
        self.event_end_time = 0.0
        self.event_type: str | None = None

    def trigger(self, event_type: str, duration: float = 0.5) -> None:
        """Light up this bar for a given duration.

        Parameters
        ----------
        event_type : str
            Either 'footstep' or 'shot'. Determines the colour used.
        duration : float
            Number of seconds the bar remains lit.
        """
        self.event_type = event_type
        self.event_end_time = time.time() + duration

    def update(self) -> None:
        """Update bar state based on the current time."""
        if time.time() > self.event_end_time:
            self.event_type = None

    def draw(self, surface: pygame.Surface, center: Tuple[int, int]) -> None:
        """Draw the bar onto the given surface.

        Parameters
        ----------
        surface : pygame.Surface
            Surface on which to draw.
        center : tuple
            (x, y) coordinates of the centre of the radial diagram.
        """
        if self.event_type is None:
            return
        # Choose colour based on event type
        colour = self.colour_shot if self.event_type == 'shot' else self.colour_footstep
        # Create an intermediate surface with per‑pixel alpha
        bar_surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        # Fill with chosen colour and transparency
        bar_surf.fill((*colour, self.transparency))
        # Rotate surface around its centre
        rotated = pygame.transform.rotate(bar_surf, -math.degrees(self.angle))
        rect = rotated.get_rect()
        # Position such that one end of the bar touches the centre and the bar extends outward
        # Compute offset vector for the midpoint of the bar's bottom edge in rotated space
        # In local coords the bar's top left is (0,0), we want to align the bottom centre (width/2, height)
        # After rotation, we compute how far that point moves from the rotated surface's topleft
        w_local, h_local = self.width, self.height
        # Point to align in the unrotated bar
        point = pygame.Vector2(w_local / 2, h_local)
        # Rotate that point around the centre of the bar surface
        rot_point = point.rotate(-math.degrees(self.angle))
        # Compute top‑left position so that rot_point + top_left = centre
        top_left_x = center[0] - rot_point.x
        top_left_y = center[1] - rot_point.y
        surface.blit(rotated, (top_left_x, top_left_y))


class Visualizer:
    """Pygame visualisation showing eight directional bars.

    Use the ``trigger_event`` method to light up a bar corresponding to
    either a footstep or a gunshot. The bars will fade after a short
    period. Keyboard controls allow dynamic adjustment of bar width,
    height and transparency. The ``run`` method blocks until the user
    closes the window.
    """

    DIRECTIONS_DEG = [0, 45, 90, 135, 180, 225, 270, 315]
    MAX_BAR_WIDTH = 120
    MIN_BAR_WIDTH = 10
    MAX_BAR_HEIGHT = 400
    MIN_BAR_HEIGHT = 50
    MAX_TRANSPARENCY = 255
    MIN_TRANSPARENCY = 20

    def __init__(self, bar_width: int = 40, bar_height: int = 200, transparency: int = 180, show_stats: bool = True) -> None:
        if pygame is None:
            raise RuntimeError("Pygame library is required for Visualizer")
        # Initialise Pygame only once
        pygame.init()
        # Create borderless window for modern widget look
        self.screen = pygame.display.set_mode((600, 600), pygame.NOFRAME)
        pygame.display.set_caption("Audio Radar")
        self.clock = pygame.time.Clock()
        # Create bars for each direction
        self.bars: List[Bar] = [
            Bar(angle_deg=d, width=bar_width, height=bar_height, transparency=transparency)
            for d in self.DIRECTIONS_DEG
        ]
        self.bar_width = bar_width
        self.bar_height = bar_height
        self.transparency = transparency
        self.show_stats = show_stats
        
        # Stats tracking
        self.peak_value = 0.0
        self.rms_value = 0.0
        self.last_event_type = None
        self.last_event_time = 0
        
        # Initialize font for stats display
        try:
            self.font = pygame.font.Font(None, 24)
            self.small_font = pygame.font.Font(None, 18)
        except:
            self.font = None
            self.small_font = None
        
        # Window dragging
        self.dragging = False
        self.drag_offset_x = 0
        self.drag_offset_y = 0

    def update_stats(self, peak: float, rms: float) -> None:
        """Update audio statistics for display.
        
        Parameters
        ----------
        peak : float
            Peak amplitude value (0.0-1.0)
        rms : float
            RMS (root mean square) value (0.0-1.0)
        """
        self.peak_value = peak
        self.rms_value = rms
    
    def trigger_event(self, event_type: str, direction: int = None, distance: float = None) -> None:
        """Light up the appropriate bar for a detected event.

        Parameters
        ----------
        event_type : str
            Either 'footstep' or 'shot'. Uses the event type to colour
            the bar appropriately.
        direction : int, optional
            Direction in degrees (0-359). If provided, lights up the bar
            closest to this direction. If None, uses default mapping:
            footsteps light up the 'front' bar (0°) and shots light up
            the bar behind the player (180°).
        distance : float, optional
            Relative distance (0.0-1.0). Currently not used but reserved
            for future distance visualization features.
        """
        if not self.bars:
            return
        
        if direction is not None:
            # Find closest bar to the specified direction
            index = self._find_closest_bar(direction)
        else:
            # Use default mapping: footsteps front, shots back
            index = 0 if event_type == 'footstep' else 4
        
        bar = self.bars[index]
        bar.trigger(event_type)
        
        # Track last event for stats display
        self.last_event_type = event_type
        self.last_event_time = time.time()
    
    def _find_closest_bar(self, direction: int) -> int:
        """Find the bar index closest to the given direction.
        
        Parameters
        ----------
        direction : int
            Direction in degrees (0-359), where 0 is front/north.
            
        Returns
        -------
        int
            Index of the closest bar.
        """
        min_diff = 360
        closest_idx = 0
        
        for idx, angle_deg in enumerate(self.DIRECTIONS_DEG):
            # Calculate angular difference
            diff = abs(direction - angle_deg)
            # Handle wraparound (e.g., 350° vs 10°)
            if diff > 180:
                diff = 360 - diff
            
            if diff < min_diff:
                min_diff = diff
                closest_idx = idx
        
        return closest_idx
    
    def _draw_stats(self) -> None:
        """Draw real-time statistics overlay."""
        if not self.font:
            return
        
        # Position stats in top-left corner
        y_offset = 10
        x_offset = 10
        line_height = 25
        
        # Draw semi-transparent background for readability
        stats_bg = pygame.Surface((220, 120), pygame.SRCALPHA)
        stats_bg.fill((0, 0, 0, 180))
        self.screen.blit(stats_bg, (5, 5))
        
        # Draw Peak value
        peak_text = f"Peak: {self.peak_value:.3f}"
        peak_surface = self.font.render(peak_text, True, (0, 255, 0))
        self.screen.blit(peak_surface, (x_offset, y_offset))
        y_offset += line_height
        
        # Draw RMS value
        rms_text = f"RMS:  {self.rms_value:.3f}"
        rms_surface = self.font.render(rms_text, True, (0, 255, 0))
        self.screen.blit(rms_surface, (x_offset, y_offset))
        y_offset += line_height
        
        # Draw last event info
        if self.last_event_type and (time.time() - self.last_event_time) < 2.0:
            event_color = (255, 0, 0) if self.last_event_type == 'shot' else (0, 255, 0)
            event_text = f"Event: {self.last_event_type.upper()}"
            event_surface = self.font.render(event_text, True, event_color)
            self.screen.blit(event_surface, (x_offset, y_offset))
        y_offset += line_height
        
        # Draw help text
        if self.small_font:
            help_text = "Z/X: Width | C/V: Height | B/N: Alpha"
            help_surface = self.small_font.render(help_text, True, (150, 150, 150))
            self.screen.blit(help_surface, (x_offset, y_offset))

    def _clamp_values(self) -> None:
        """Ensure bar width/height/transparency remain within safe bounds."""
        self.bar_width = max(self.MIN_BAR_WIDTH, min(self.bar_width, self.MAX_BAR_WIDTH))
        self.bar_height = max(self.MIN_BAR_HEIGHT, min(self.bar_height, self.MAX_BAR_HEIGHT))
        self.transparency = max(self.MIN_TRANSPARENCY, min(self.transparency, self.MAX_TRANSPARENCY))
        # Update bars with new sizes
        for b in self.bars:
            b.width = self.bar_width
            b.height = self.bar_height
            b.transparency = self.transparency

    def run(self) -> None:
        """Enter the main Pygame loop.

        This loop updates the display at ~60 Hz. It listens for
        keyboard events to adjust bar properties and handles window
        close events. Bars automatically fade when their event
        duration expires.
        """
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_z:
                        self.bar_width += 2
                    elif event.key == pygame.K_x:
                        self.bar_width -= 2
                    elif event.key == pygame.K_c:
                        self.bar_height += 10
                    elif event.key == pygame.K_v:
                        self.bar_height -= 10
                    elif event.key == pygame.K_b:
                        self.transparency += 10
                    elif event.key == pygame.K_n:
                        self.transparency -= 10
                    # Clamp after adjustments
                    self._clamp_values()

            # Clear screen
            self.screen.fill((0, 0, 0))
            # Draw faint base outlines for each bar so the user sees the radar even
            # when no events have been detected. The outlines use a low alpha
            # value to remain unobtrusive. We compute the same rotation and
            # offset logic as in Bar.draw to position each bar correctly.
            center = (self.screen.get_width() // 2, self.screen.get_height() // 2)
            base_alpha = 40  # transparency for base outlines (0‑255)
            base_colour = (80, 80, 80)  # grey colour for outlines
            for bar in self.bars:
                width, height = bar.width, bar.height
                # Create a surface with per‑pixel alpha for the base bar
                base_surf = pygame.Surface((width, height), pygame.SRCALPHA)
                base_surf.fill((*base_colour, base_alpha))
                # Rotate the surface around its centre
                angle_deg = -math.degrees(bar.angle)
                rotated_base = pygame.transform.rotate(base_surf, angle_deg)
                # Compute the position such that the bottom centre of the bar
                # aligns with the centre of the screen
                point = pygame.math.Vector2(width / 2.0, height)
                rot_point = point.rotate(angle_deg)
                top_left_x = center[0] - rot_point.x
                top_left_y = center[1] - rot_point.y
                self.screen.blit(rotated_base, (top_left_x, top_left_y))

            # Update and draw active bars (events)
            for bar in self.bars:
                bar.update()
                bar.draw(self.screen, center)
            
            # Draw stats overlay if enabled
            if self.show_stats and self.font:
                self._draw_stats()
            
            pygame.display.flip()
            # Limit to ~60 frames per second
            self.clock.tick(60)

        pygame.quit()