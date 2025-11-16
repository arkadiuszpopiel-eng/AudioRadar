"""
Theme Manager for AudioRadar PyQt5
Manages application themes including dark mode and custom color schemes.
"""

from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import Qt
from dataclasses import dataclass
from typing import Dict

from logger import get_logger


@dataclass
class Theme:
    """Represents a visual theme."""
    name: str
    background: QColor
    foreground: QColor
    base: QColor
    alternate_base: QColor
    tooltip_base: QColor
    tooltip_text: QColor
    text: QColor
    button: QColor
    button_text: QColor
    bright_text: QColor
    highlight: QColor
    highlight_text: QColor
    disabled_text: QColor
    window: QColor
    window_text: QColor


class ThemeManager:
    """Manages application themes and color schemes."""

    def __init__(self):
        self.logger = get_logger()
        self.logger.info("Initializing Theme Manager")

        self.current_theme_name = "dark"
        self.themes: Dict[str, Theme] = {}

        # Initialize built-in themes
        self._initialize_themes()

        self.logger.info(f"Theme Manager initialized with {len(self.themes)} themes")

    def _initialize_themes(self):
        """Initialize built-in themes."""
        # Dark theme (default)
        self.themes["dark"] = Theme(
            name="Dark",
            background=QColor(25, 25, 35),
            foreground=QColor(220, 220, 230),
            base=QColor(18, 18, 28),
            alternate_base=QColor(30, 30, 40),
            tooltip_base=QColor(50, 50, 60),
            tooltip_text=QColor(220, 220, 230),
            text=QColor(220, 220, 230),
            button=QColor(45, 45, 55),
            button_text=QColor(220, 220, 230),
            bright_text=QColor(255, 255, 255),
            highlight=QColor(42, 130, 218),
            highlight_text=QColor(255, 255, 255),
            disabled_text=QColor(120, 120, 130),
            window=QColor(25, 25, 35),
            window_text=QColor(220, 220, 230)
        )

        # Light theme
        self.themes["light"] = Theme(
            name="Light",
            background=QColor(240, 240, 245),
            foreground=QColor(30, 30, 40),
            base=QColor(255, 255, 255),
            alternate_base=QColor(245, 245, 250),
            tooltip_base=QColor(255, 255, 225),
            tooltip_text=QColor(30, 30, 40),
            text=QColor(30, 30, 40),
            button=QColor(225, 225, 235),
            button_text=QColor(30, 30, 40),
            bright_text=QColor(0, 0, 0),
            highlight=QColor(42, 130, 218),
            highlight_text=QColor(255, 255, 255),
            disabled_text=QColor(150, 150, 160),
            window=QColor(240, 240, 245),
            window_text=QColor(30, 30, 40)
        )

        # Blue dark theme
        self.themes["blue_dark"] = Theme(
            name="Blue Dark",
            background=QColor(15, 25, 45),
            foreground=QColor(200, 220, 240),
            base=QColor(10, 18, 35),
            alternate_base=QColor(20, 30, 50),
            tooltip_base=QColor(30, 45, 70),
            tooltip_text=QColor(200, 220, 240),
            text=QColor(200, 220, 240),
            button=QColor(35, 50, 75),
            button_text=QColor(200, 220, 240),
            bright_text=QColor(255, 255, 255),
            highlight=QColor(60, 140, 230),
            highlight_text=QColor(255, 255, 255),
            disabled_text=QColor(100, 120, 150),
            window=QColor(15, 25, 45),
            window_text=QColor(200, 220, 240)
        )

        # Green dark theme (Matrix style)
        self.themes["matrix"] = Theme(
            name="Matrix",
            background=QColor(5, 15, 5),
            foreground=QColor(0, 255, 0),
            base=QColor(0, 10, 0),
            alternate_base=QColor(10, 20, 10),
            tooltip_base=QColor(20, 40, 20),
            tooltip_text=QColor(0, 255, 0),
            text=QColor(0, 255, 0),
            button=QColor(15, 30, 15),
            button_text=QColor(0, 255, 0),
            bright_text=QColor(100, 255, 100),
            highlight=QColor(0, 180, 0),
            highlight_text=QColor(255, 255, 255),
            disabled_text=QColor(0, 100, 0),
            window=QColor(5, 15, 5),
            window_text=QColor(0, 255, 0)
        )

    def get_available_themes(self) -> list:
        """Get list of available theme names."""
        return list(self.themes.keys())

    def apply_theme(self, theme_name: str, app: QApplication = None):
        """Apply a theme to the application."""
        if theme_name not in self.themes:
            self.logger.warning(f"Theme '{theme_name}' not found, using default")
            theme_name = "dark"

        theme = self.themes[theme_name]
        self.current_theme_name = theme_name

        self.logger.info(f"Applying theme: {theme.name}")

        # Get application instance
        if app is None:
            app = QApplication.instance()

        if app is None:
            self.logger.error("No QApplication instance found")
            return

        # Create palette
        palette = QPalette()

        # Set colors
        palette.setColor(QPalette.Window, theme.window)
        palette.setColor(QPalette.WindowText, theme.window_text)
        palette.setColor(QPalette.Base, theme.base)
        palette.setColor(QPalette.AlternateBase, theme.alternate_base)
        palette.setColor(QPalette.ToolTipBase, theme.tooltip_base)
        palette.setColor(QPalette.ToolTipText, theme.tooltip_text)
        palette.setColor(QPalette.Text, theme.text)
        palette.setColor(QPalette.Button, theme.button)
        palette.setColor(QPalette.ButtonText, theme.button_text)
        palette.setColor(QPalette.BrightText, theme.bright_text)
        palette.setColor(QPalette.Link, theme.highlight)
        palette.setColor(QPalette.Highlight, theme.highlight)
        palette.setColor(QPalette.HighlightedText, theme.highlight_text)

        # Disabled colors
        palette.setColor(QPalette.Disabled, QPalette.Text, theme.disabled_text)
        palette.setColor(QPalette.Disabled, QPalette.ButtonText, theme.disabled_text)

        # Apply palette
        app.setPalette(palette)

        # Apply stylesheet for additional styling
        stylesheet = self._get_stylesheet(theme)
        app.setStyleSheet(stylesheet)

        self.logger.info(f"Theme '{theme.name}' applied successfully")

    def _get_stylesheet(self, theme: Theme) -> str:
        """Get stylesheet for theme."""
        return f"""
            QWidget {{
                background-color: {theme.background.name()};
                color: {theme.text.name()};
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 10pt;
            }}

            QPushButton {{
                background-color: {theme.button.name()};
                color: {theme.button_text.name()};
                border: 1px solid {theme.highlight.name()};
                border-radius: 4px;
                padding: 5px 15px;
                min-width: 80px;
            }}

            QPushButton:hover {{
                background-color: {theme.highlight.name()};
                color: {theme.highlight_text.name()};
            }}

            QPushButton:pressed {{
                background-color: {theme.highlight.darker(120).name()};
            }}

            QPushButton:disabled {{
                background-color: {theme.alternate_base.name()};
                color: {theme.disabled_text.name()};
                border: 1px solid {theme.disabled_text.name()};
            }}

            QLineEdit, QSpinBox, QDoubleSpinBox, QComboBox {{
                background-color: {theme.base.name()};
                color: {theme.text.name()};
                border: 1px solid {theme.highlight.name()};
                border-radius: 3px;
                padding: 3px 5px;
            }}

            QLineEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus, QComboBox:focus {{
                border: 2px solid {theme.highlight.name()};
            }}

            QComboBox::drop-down {{
                border: none;
            }}

            QComboBox::down-arrow {{
                image: none;
                border-left: 4px solid transparent;
                border-right: 4px solid transparent;
                border-top: 6px solid {theme.text.name()};
                margin-right: 5px;
            }}

            QLabel {{
                color: {theme.text.name()};
                background: transparent;
            }}

            QGroupBox {{
                border: 1px solid {theme.highlight.name()};
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
                font-weight: bold;
            }}

            QGroupBox::title {{
                color: {theme.highlight.name()};
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 0 5px;
                background-color: {theme.background.name()};
            }}

            QSlider::groove:horizontal {{
                background: {theme.base.name()};
                height: 6px;
                border-radius: 3px;
            }}

            QSlider::handle:horizontal {{
                background: {theme.highlight.name()};
                width: 14px;
                margin: -4px 0;
                border-radius: 7px;
            }}

            QSlider::handle:horizontal:hover {{
                background: {theme.highlight.lighter(120).name()};
            }}

            QTabWidget::pane {{
                border: 1px solid {theme.highlight.name()};
                border-radius: 3px;
            }}

            QTabBar::tab {{
                background-color: {theme.button.name()};
                color: {theme.button_text.name()};
                border: 1px solid {theme.highlight.name()};
                border-bottom: none;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                padding: 5px 10px;
                margin-right: 2px;
            }}

            QTabBar::tab:selected {{
                background-color: {theme.highlight.name()};
                color: {theme.highlight_text.name()};
            }}

            QTabBar::tab:hover {{
                background-color: {theme.highlight.darker(150).name()};
            }}

            QProgressBar {{
                background-color: {theme.base.name()};
                border: 1px solid {theme.highlight.name()};
                border-radius: 3px;
                text-align: center;
            }}

            QProgressBar::chunk {{
                background-color: {theme.highlight.name()};
                border-radius: 2px;
            }}

            QScrollBar:vertical {{
                background: {theme.base.name()};
                width: 12px;
                border-radius: 6px;
            }}

            QScrollBar::handle:vertical {{
                background: {theme.button.name()};
                min-height: 20px;
                border-radius: 6px;
            }}

            QScrollBar::handle:vertical:hover {{
                background: {theme.highlight.name()};
            }}

            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                height: 0px;
            }}

            QToolTip {{
                background-color: {theme.tooltip_base.name()};
                color: {theme.tooltip_text.name()};
                border: 1px solid {theme.highlight.name()};
                border-radius: 3px;
                padding: 3px;
            }}
        """

    def get_current_theme_name(self) -> str:
        """Get current theme name."""
        return self.current_theme_name

    def get_theme(self, theme_name: str) -> Theme:
        """Get theme object by name."""
        return self.themes.get(theme_name, self.themes["dark"])
