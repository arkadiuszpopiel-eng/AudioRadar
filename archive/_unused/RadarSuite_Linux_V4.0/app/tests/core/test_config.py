"""
RadarSuite v3.5.0 - Point 12: ConfigManager Tests
Tests for core/config.py
"""

from tests.compat import pytest
import json
import tempfile
from pathlib import Path
from unittest.mock import patch
from core.config import ConfigManager


class TestConfigManager:
    """Test suite for ConfigManager class"""

    @pytest.fixture
    def config_manager(self, tmp_path):
        """Create ConfigManager with temporary directory"""
        with patch.object(ConfigManager, '__init__', lambda self: None):
            mgr = ConfigManager()
            mgr.config_dir = tmp_path / 'RadarSuite'
            mgr.config_file = mgr.config_dir / 'config.json'
            mgr.CONFIG_SCHEMA = ConfigManager.CONFIG_SCHEMA
            mgr.default_config = {
                "audio": {
                    "sample_rate": 48000,
                    "block_size": 2048,
                    "channels": 2,
                },
                "performance": {
                    "use_gpu": True,
                    "max_workers": 4
                }
            }
            return mgr

    def test_init_creates_config_dir(self):
        """Test that __init__ creates config directory"""
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch('core.config.Path.home', return_value=Path(tmpdir)):
                mgr = ConfigManager()
                # Config dir should be created
                assert mgr.config_dir.exists()

    def test_load_nonexistent_file_returns_defaults(self, config_manager):
        """Test loading when config file doesn't exist"""
        result = config_manager.load()
        assert result == config_manager.default_config

    def test_load_valid_config(self, config_manager):
        """Test loading valid config file"""
        config_manager.config_dir.mkdir(parents=True, exist_ok=True)

        test_config = {
            "audio": {
                "sample_rate": 44100,
                "block_size": 1024
            }
        }

        with open(config_manager.config_file, 'w') as f:
            json.dump(test_config, f)

        result = config_manager.load()

        # Should merge with defaults
        assert result['audio']['sample_rate'] == 44100
        assert result['audio']['block_size'] == 1024
        assert result['audio']['channels'] == 2  # From defaults

    def test_load_invalid_json_returns_defaults(self, config_manager):
        """Test loading invalid JSON returns defaults"""
        config_manager.config_dir.mkdir(parents=True, exist_ok=True)

        with open(config_manager.config_file, 'w') as f:
            f.write("{ invalid json }")

        result = config_manager.load()
        assert result == config_manager.default_config

    def test_save_creates_file(self, config_manager):
        """Test that save() creates config file"""
        test_config = {"audio": {"sample_rate": 48000}}

        config_manager.save(test_config)

        assert config_manager.config_file.exists()

        with open(config_manager.config_file) as f:
            saved = json.load(f)
            assert saved['audio']['sample_rate'] == 48000

    def test_validate_value_type_check(self, config_manager):
        """Test _validate_value() type checking"""
        schema = {"type": int}

        # Valid type
        is_valid, value = config_manager._validate_value("test", 42, schema)
        assert is_valid
        assert value == 42

        # Invalid type
        is_valid, value = config_manager._validate_value("test", "42", schema)
        assert not is_valid

    def test_validate_value_range_check(self, config_manager):
        """Test _validate_value() range checking"""
        schema = {"type": int, "range": (0, 100)}

        # Within range
        is_valid, value = config_manager._validate_value("test", 50, schema)
        assert is_valid

        # Below range
        is_valid, value = config_manager._validate_value("test", -10, schema)
        assert not is_valid

        # Above range
        is_valid, value = config_manager._validate_value("test", 150, schema)
        assert not is_valid

        # Edge cases
        is_valid, value = config_manager._validate_value("test", 0, schema)
        assert is_valid

        is_valid, value = config_manager._validate_value("test", 100, schema)
        assert is_valid

    def test_validate_value_whitelist_check(self, config_manager):
        """Test _validate_value() whitelist checking"""
        schema = {"type": str, "values": ["en", "pl"]}

        # Valid value
        is_valid, value = config_manager._validate_value("lang", "en", schema)
        assert is_valid

        # Invalid value
        is_valid, value = config_manager._validate_value("lang", "fr", schema)
        assert not is_valid

    def test_validate_value_multiple_types(self, config_manager):
        """Test _validate_value() with multiple allowed types"""
        schema = {"type": (int, float)}

        is_valid, _ = config_manager._validate_value("test", 42, schema)
        assert is_valid

        is_valid, _ = config_manager._validate_value("test", 42.5, schema)
        assert is_valid

        is_valid, _ = config_manager._validate_value("test", "42", schema)
        assert not is_valid

    def test_validate_config_filters_invalid_values(self, config_manager):
        """Test _validate_config() filters out invalid values"""
        # Set up a schema
        config_manager.CONFIG_SCHEMA = {
            "audio": {
                "sample_rate": {"type": int, "values": [44100, 48000]},
                "block_size": {"type": int, "range": (128, 8192)}
            }
        }

        user_config = {
            "audio": {
                "sample_rate": 44100,  # Valid
                "block_size": 99999    # Invalid (out of range)
            }
        }

        validated = config_manager._validate_config(user_config)

        # sample_rate should be kept
        assert validated['audio']['sample_rate'] == 44100
        # block_size should be filtered out
        assert 'block_size' not in validated['audio']

    def test_merge_configs(self, config_manager):
        """Test _merge_configs() merges user config with defaults"""
        default = {
            "audio": {
                "sample_rate": 48000,
                "block_size": 2048,
                "channels": 2
            },
            "ui": {
                "language": "en"
            }
        }

        user = {
            "audio": {
                "sample_rate": 44100  # Override
                # block_size and channels missing (use defaults)
            }
            # ui section missing (use defaults)
        }

        merged = config_manager._merge_configs(default, user)

        assert merged['audio']['sample_rate'] == 44100  # User override
        assert merged['audio']['block_size'] == 2048     # Default
        assert merged['audio']['channels'] == 2          # Default
        assert merged['ui']['language'] == "en"          # Default

    def test_config_schema_exists(self):
        """Test that CONFIG_SCHEMA is properly defined"""
        assert hasattr(ConfigManager, 'CONFIG_SCHEMA')
        schema = ConfigManager.CONFIG_SCHEMA

        # Should have main sections
        assert 'audio' in schema
        assert 'detection' in schema
        assert 'ui' in schema
        assert 'performance' in schema

        # Audio should have required fields
        assert 'sample_rate' in schema['audio']
        assert 'block_size' in schema['audio']
        assert 'channels' in schema['audio']

    def test_default_config_valid(self):
        """Test that default config matches schema"""
        mgr = ConfigManager()

        # Default config should pass validation
        validated = mgr._validate_config(mgr.default_config)

        # All defaults should be valid
        for section in mgr.CONFIG_SCHEMA.keys():
            if section in mgr.default_config:
                assert section in validated or section not in mgr.default_config
