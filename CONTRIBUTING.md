# Contributing to Audio Radar

Thank you for your interest in contributing to Audio Radar! This document provides guidelines for contributing to the project.

## Table of Contents

1. [Code of Conduct](#code-of-conduct)
2. [Getting Started](#getting-started)
3. [Development Setup](#development-setup)
4. [How to Contribute](#how-to-contribute)
5. [Coding Standards](#coding-standards)
6. [Testing](#testing)
7. [Documentation](#documentation)
8. [Pull Request Process](#pull-request-process)

## Code of Conduct

This project aims to be welcoming to all contributors. Please be respectful and constructive in all interactions.

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork**:
   ```bash
   git clone https://github.com/YOUR-USERNAME/AudioRadar.git
   cd AudioRadar
   ```
3. **Add upstream remote**:
   ```bash
   git remote add upstream https://github.com/arkadiuszpopiel-eng/AudioRadar.git
   ```

## Development Setup

### Prerequisites
- Python 3.8 or newer
- Git
- Audio loopback device for testing

### Install Development Dependencies

```bash
pip install -r requirements.txt
pip install pytest black mypy  # Development tools
```

### Project Structure

```
AudioRadar/
├── audio_radar_v10/           # Current version
│   └── audio_radar/
│       ├── main.py            # Entry point
│       ├── audio_capture.py   # Audio I/O
│       ├── sound_analysis.py  # Detection algorithms
│       ├── visualization.py   # Pygame display
│       ├── calibrate.py       # Calibration tool
│       └── config.json        # Configuration
├── tests/                     # Test suite
├── docs/                      # Documentation (future)
├── requirements.txt           # Dependencies
└── setup.py                   # Package setup
```

## How to Contribute

### Reporting Bugs

When filing a bug report, please include:
- Audio Radar version
- Python version
- Windows version
- Audio device information
- Steps to reproduce
- Expected vs actual behavior
- Log file contents (if applicable)

### Suggesting Enhancements

Enhancement suggestions are welcome! Please include:
- Clear description of the enhancement
- Use cases and benefits
- Possible implementation approach
- Any potential drawbacks

### Areas for Contribution

We welcome contributions in:

1. **Detection Algorithms**
   - Machine learning models for event classification
   - Improved filtering techniques
   - Better noise reduction
   - HRTF-based directional detection

2. **Visualization**
   - New display modes (3D radar, heatmap, etc.)
   - Distance visualization
   - Event history/trails
   - Custom themes and skins

3. **Performance**
   - GPU acceleration for DSP
   - Lower latency optimizations
   - Reduced CPU usage

4. **Features**
   - Additional sound types (reloads, explosions, etc.)
   - Profile system for different games
   - Network mode for second PC display
   - Integration with game APIs

5. **Documentation**
   - Tutorial videos
   - Game-specific guides
   - Translation to other languages
   - API documentation

6. **Testing**
   - Automated tests
   - Test audio samples
   - Performance benchmarks
   - Cross-platform testing

## Coding Standards

### Python Style

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Use type hints where appropriate
- Maximum line length: 100 characters
- Use meaningful variable names

### Code Formatting

Use `black` for automatic formatting:
```bash
black audio_radar_v10/audio_radar/
```

### Type Checking

Use `mypy` for type checking:
```bash
mypy audio_radar_v10/audio_radar/
```

### Documentation

- Use Google-style docstrings
- Document all public functions and classes
- Include examples in docstrings where helpful
- Keep README and guides up to date

Example:
```python
def detect_event(samples: np.ndarray) -> Optional[str]:
    """Detect sound events in audio samples.
    
    Args:
        samples: Audio samples as numpy array, shape (frames, channels)
        
    Returns:
        Event type ('shot', 'footstep') or None if no event detected
        
    Example:
        >>> audio = np.random.random((1024, 2))
        >>> event = detect_event(audio)
        >>> print(event)
        None
    """
```

## Testing

### Running Tests

```bash
# Run all tests
pytest tests/

# Run specific test file
pytest tests/test_sound_analysis.py

# Run with coverage
pytest --cov=audio_radar_v10 tests/
```

### Writing Tests

- Place tests in `tests/` directory
- Name test files `test_*.py`
- Use descriptive test names
- Test both normal and edge cases
- Include docstrings explaining what is tested

Example:
```python
def test_detect_silent_audio():
    """Test that silent audio produces no events."""
    silent = np.zeros((1024, 2), dtype=np.float32)
    result = detect_event(silent)
    assert result is None
```

## Documentation

### User Documentation

- Update USER_GUIDE.md for user-facing features
- Update INSTALL.md for installation changes
- Add examples and screenshots where helpful

### Code Documentation

- Document all public APIs
- Explain complex algorithms
- Include references to papers or resources
- Update CHANGELOG.md for all changes

## Pull Request Process

### Before Submitting

1. **Update from upstream**:
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

2. **Run tests**:
   ```bash
   pytest tests/
   ```

3. **Format code**:
   ```bash
   black audio_radar_v10/
   ```

4. **Update documentation** as needed

### Submitting a PR

1. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** with clear, atomic commits

3. **Write good commit messages**:
   ```
   Add bandpass filtering for footstep detection
   
   - Implement Butterworth filter in sound_analysis.py
   - Add configurable frequency ranges
   - Update tests to cover new functionality
   - Document filter parameters in config.json
   ```

4. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

5. **Create Pull Request** on GitHub

### PR Description Template

```markdown
## Description
Brief description of changes

## Motivation
Why is this change needed?

## Changes Made
- Bullet point list of changes
- Include any breaking changes

## Testing
How was this tested?

## Checklist
- [ ] Tests pass
- [ ] Code formatted with black
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
```

### Review Process

- Maintainers will review your PR
- Address feedback constructively
- Make requested changes in new commits
- Once approved, PR will be merged

## Development Tips

### Testing Audio Detection

Use the calibration tool to generate test data:
```bash
python calibrate.py --device 1
```

### Debugging

Enable verbose logging in config.json or check log files:
```
audio_radar_v10/audio_radar/log_v10.txt
```

### Common Issues

**Import errors**: Ensure you're in the correct directory and dependencies are installed

**Audio not detected**: Check loopback device is enabled and set as default

**Performance issues**: Profile with:
```bash
python -m cProfile main.py
```

## Questions?

- Open an issue for questions
- Check existing issues first
- Be patient and respectful

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to Audio Radar! 🎮🔊
