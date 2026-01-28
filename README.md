# Untitled Video Player

A video player application built with PySide6.

## Features

* Fullscreen mode
* Subtitle support  
* Audio muting
* Custom keyboard shortcuts

## Quick Start

```bash
# Clone and setup
git clone <repository-url>
cd untitled-video-player
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install everything
pip install -e ".[dev]"

# Run
python src/main.py
```

## PyCharm Setup

1. **Set interpreter:** Settings → Project → Python Interpreter → Select `venv/bin/python`

2. **Enable MyPy** (type checking):
   - Settings → Plugins → Install "Mypy"
   - Settings → Tools → Mypy → Check "Use Mypy"

3. **Enable Ruff** (linting/formatting):
   - Settings → Tools → Ruff → Check "Use ruff" and "Use ruff format"

## Development Commands

```bash
mypy src/              # Type check
ruff check src/        # Lint
ruff format src/       # Format
pytest                 # Test
```

## Code Standards

All functions require type annotations:
```python
def process_video(path: str, volume: float) -> bool:
    return True
```

Before committing: `mypy src/ && ruff check src/ && pytest`

## License

GNU General Public License v3.0
