"""
RadarSuite v3.5.0 - Game Process Detector
Detects running games for ARC Raiders, Tarkov, CS2, etc.
"""

import time
import re
import psutil

from core.logger import log


class GameProcessDetector:
    """
    Detects running games and game engines
    Identifies Unreal Engine 5, Unity, Source, CryEngine, and other games
    Auto-detects audio sources from game processes
    """

    def __init__(self):
        log("GameProcessDetector.__init__", "INFO")

        # Known game engines and their process patterns
        self.game_engines = {
            'Unreal Engine 5': ['UE5-', '-Win64-Shipping', 'UnrealEditor'],
            'Unreal Engine 4': ['UE4-', '-Win64-Shipping', 'UnrealEditor'],
            'Unity': ['Unity.exe', 'UnityPlayer.dll'],
            'Source Engine': ['hl2.exe', 'csgo.exe', 'tf2.exe'],
            'CryEngine': ['CryEngine', 'CRYENGINE'],
            'Frostbite': ['bf', 'Battlefield'],
            'id Tech': ['Doom', 'Quake'],
            'RE Engine': ['re_chunk'],
        }

        # Known games by exe name and process names
        # Multiple patterns per game to catch different process names
        # Format: 'Display Name': ['process1', 'process2', 'folder_name', 'cmdline_arg']
        self.known_games = {
            # ARC Raiders uses PioneerGame.exe (Unreal Engine 5)
            'ARC Raiders': ['ARCRaiders', 'ARC-Win64', 'PioneerGame', 'Pioneer', 'ARC Raiders'],

            # Tarkov
            'Escape from Tarkov': ['EscapeFromTarkov', 'Tarkov', 'EFT'],

            # Call of Duty series
            'Call of Duty': ['cod', 'ModernWarfare', 'Warzone', 'BlackOps'],

            # Counter-Strike 2
            'CS2': ['cs2.exe', 'cs2', 'Counter-Strike 2'],

            # Valorant
            'Valorant': ['VALORANT', 'RiotClient', 'VALORANT-Win64-Shipping'],

            # Apex Legends
            'Apex Legends': ['r5apex.exe', 'r5apex', 'Apex'],

            # PUBG
            'PUBG': ['TslGame', 'PUBG', 'TslGame-Win64-Shipping'],

            # Fortnite
            'Fortnite': ['FortniteClient-Win64-Shipping', 'Fortnite', 'FortniteLauncher'],

            # Overwatch
            'Overwatch': ['Overwatch.exe', 'Overwatch'],

            # Rainbow Six Siege
            'Rainbow Six Siege': ['RainbowSix', 'RainbowSixGame', 'R6'],

            # Destiny 2
            'Destiny 2': ['destiny2.exe', 'Destiny2'],

            # Hunt: Showdown
            'Hunt Showdown': ['HuntGame', 'Hunt'],

            # The Cycle: Frontier
            'The Cycle': ['Prospect', 'TheCycle'],

            # Marauders
            'Marauders': ['Marauders', 'MaraudersGame'],
        }

        # Currently detected games/processes
        self.active_games = []
        self.active_engines = []
        self.last_scan_time = 0.0
        self.scan_interval = 5.0  # Scan every 5 seconds

    def scan_processes(self):
        """
        Scan for running game processes
        Returns: dict with detected games and engines
        """
        try:
            current_time = time.time()

            # Don't scan too frequently
            if current_time - self.last_scan_time < self.scan_interval:
                return {
                    'games': self.active_games,
                    'engines': self.active_engines,
                    'has_games': len(self.active_games) > 0
                }

            self.last_scan_time = current_time

            detected_games = []
            detected_engines = []

            # Scan all running processes (enhanced detection with cmdline)
            for proc in psutil.process_iter(['name', 'exe', 'cmdline']):
                try:
                    proc_name = proc.info['name'] or ''
                    proc_exe = proc.info['exe'] or ''
                    proc_cmdline = ' '.join(proc.info['cmdline']) if proc.info.get('cmdline') else ''

                    if not proc_name:
                        continue

                    # Build searchable text from all sources
                    # This catches:
                    # - Process name (e.g., "PioneerGame.exe")
                    # - Full exe path (e.g., "C:\Games\ARC Raiders\PioneerGame.exe")
                    # - Command line args (e.g., "PioneerGame.exe -windowed ARC Raiders")
                    search_text = f"{proc_name} {proc_exe} {proc_cmdline}".lower()

                    # Check for known games
                    for game_name, patterns in self.known_games.items():
                        for pattern in patterns:
                            if pattern.lower() in search_text:
                                if game_name not in detected_games:
                                    detected_games.append(game_name)
                                    log(f"Detected game: {game_name} (process: {proc_name})", "INFO")
                                break  # Found this game, check next game

                    # Check for game engines
                    for engine_name, patterns in self.game_engines.items():
                        for pattern in patterns:
                            if pattern.lower() in search_text:
                                if engine_name not in detected_engines:
                                    detected_engines.append(engine_name)
                                    log(f"Detected engine: {engine_name} (process: {proc_name})", "INFO")
                                break  # Found this engine, check next engine

                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    # Process ended or no access - skip it
                    continue

            self.active_games = detected_games
            self.active_engines = detected_engines

            return {
                'games': self.active_games,
                'engines': self.active_engines,
                'has_games': len(self.active_games) > 0
            }

        except Exception as e:
            log(f"Error in GameProcessDetector.scan_processes: {e}", "ERROR")
            return {
                'games': [],
                'engines': [],
                'has_games': False
            }

    def get_detailed_game_info(self):
        """
        Get detailed information about detected game process for UI display.
        Returns dict with process name, PID, memory, window title, etc.
        """
        try:
            # Scan first if needed
            self.scan_processes()

            if not self.active_games:
                return {'detected': False}

            # Find the first detected game's process
            for proc in psutil.process_iter(['name', 'exe', 'cmdline', 'pid', 'memory_info']):
                try:
                    proc_name = proc.info['name'] or ''
                    proc_exe = proc.info['exe'] or ''
                    proc_cmdline = ' '.join(proc.info['cmdline']) if proc.info.get('cmdline') else ''
                    search_text = f"{proc_name} {proc_exe} {proc_cmdline}".lower()

                    # Check if this process matches any active game
                    matched_game = None
                    for game_name in self.active_games:
                        patterns = self.known_games.get(game_name, [])
                        for pattern in patterns:
                            if pattern.lower() in search_text:
                                matched_game = game_name
                                break
                        if matched_game:
                            break

                    if matched_game:
                        # Get memory info
                        memory_info = proc.info.get('memory_info')
                        memory_mb = memory_info.rss / (1024 * 1024) if memory_info else 0

                        # Try to get window title (Windows only)
                        window_title = "—"
                        try:
                            import ctypes
                            from ctypes import wintypes

                            EnumWindows = ctypes.windll.user32.EnumWindows
                            GetWindowText = ctypes.windll.user32.GetWindowTextW
                            GetWindowTextLength = ctypes.windll.user32.GetWindowTextLengthW
                            GetWindowThreadProcessId = ctypes.windll.user32.GetWindowThreadProcessId

                            titles = []

                            def callback(hwnd, lParam):
                                pid = wintypes.DWORD()
                                GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
                                if pid.value == proc.info['pid']:
                                    length = GetWindowTextLength(hwnd)
                                    if length > 0:
                                        buff = ctypes.create_unicode_buffer(length + 1)
                                        GetWindowText(hwnd, buff, length + 1)
                                        if buff.value:
                                            titles.append(buff.value)
                                return True

                            EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, wintypes.HWND, wintypes.LPARAM)
                            EnumWindows(EnumWindowsProc(callback), 0)

                            if titles:
                                window_title = titles[0]
                        except Exception:
                            pass

                        # Get engine
                        engine = self.active_engines[0] if self.active_engines else 'Unknown'

                        return {
                            'detected': True,
                            'game_name': matched_game,
                            'process_name': proc_name,
                            'pid': proc.info['pid'],
                            'memory_mb': memory_mb,
                            'window_title': window_title,
                            'engine': engine,
                            'exe_path': proc_exe
                        }

                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    continue

            return {'detected': False}

        except Exception as e:
            log(f"Error in get_detailed_game_info: {e}", "ERROR")
            return {'detected': False}


# ============================================================================
# PLATFORM LAUNCHER DETECTOR (v3.4.1 - Gaming Platform Integration)
# ============================================================================
