# AGENTS.md

## Project Overview

This is a PySide6-based video player application with a modular architecture. The codebase emphasizes clean separation of concerns and signal-based communication between components.

## Architecture Patterns

### Signal Connection Pattern

**IMPORTANT**: Each class that emits or handles signals has a `connect_signals()` method. This is the **preferred and required** way to connect signals in this project.

```python
# Example from ApplicationWindow
self.mediaController.connect_signals(self.videoControls, self.videoDisplay)
self.videoControls.connect_signals(self.mediaController)
self.videoDisplay.connect_signals(self.mediaController, self.toggle_fullscreen, file_dialog_handler)
```

**Do not** connect signals directly in `__init__` methods or scattered throughout the code. Always use the `connect_signals()` method pattern.

### Styling Pattern

All styling is centralized in `theme.py` using the `Theme` class. **Do not** use inline stylesheets or individual widget styling.

```python
# In main.py
app.setStyleSheet(Theme.DARK)
```

When adding new widgets, add their styles to `theme.py` following the existing pattern.

## Project Structure

```
src/
├── window/              # Window classes (main windows, dialogs)
│   └── application_window.py
├── primitive/           # Custom QWidget subclasses
│   └── slider.py
├── helpers.py          # Helper functions (formatting, file operations)
├── theme.py           # Centralized styling
├── main.py            # Application entry point
└── [component].py     # Main components (media_controller, video_controls, etc.)
```

### File Organization Rules

- **Custom QWidget subclasses** → `src/primitive/`
- **Windows and dialogs** → `src/window/`
- **Helper/utility functions** → `src/helpers.py`
- **Styling** → `src/theme.py`
- **Main application window** → Keep `ApplicationWindow` clean and minimal

## Key Components

### ApplicationWindow (window/application_window.py)

The main application window. **Keep this class as clean as possible.** It should primarily:
- Initialize components
- Connect signals via `connect_signals()` methods
- Handle high-level window state (fullscreen toggling)
- Delegate functionality to specialized components

### MediaController (media_controller.py)

Manages the QMediaPlayer and audio output. Handles media playback logic.

### VideoControls (video_controls.py)

The control panel UI (play/pause, seek slider, volume). Updates based on media state.

### VideoDisplay (video_display.py)

The video rendering widget with user interaction handling.

## Important Notes for AI Agents

### DO NOT Run the Project

**CRITICAL**: Do not attempt to run this project or execute the code. The application requires:
- Audio devices
- Video codecs
- Qt multimedia plugins
- A display environment

Instead:
- Analyze code statically
- Check for syntax errors
- Verify imports and method signatures
- Review logic and patterns
- Use linting tools if available

### Audio Device Handling

The project includes `audio_check.py` which handles missing audio devices gracefully. This is especially important for Linux systems where PySide6 may not detect audio devices correctly.

### Common Tasks

**Adding a new custom widget:**
1. Create class in `src/primitive/`
2. Add styling to `theme.py`
3. Use `connect_signals()` pattern if it emits/handles signals

**Adding a new window:**
1. Create class in `src/window/`
2. Add styling to `theme.py`
3. Keep signal connections in `connect_signals()` method

**Adding helper functions:**
- Add to `src/helpers.py`
- Keep functions pure and focused

## Code Style

- Use descriptive variable names
- Follow PySide6 naming conventions (camelCase for Qt objects)
- Keep methods focused and single-purpose
- Use signals for component communication
- Avoid tight coupling between components