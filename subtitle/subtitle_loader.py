from pathlib import Path
from typing import List, Optional

SUBTITLE_EXTENSIONS = ['.srt', '.vtt']


def _find_subtitle_paths(video_path: Path) -> List[Path]:
    video_name = video_path.stem
    search_dirs = [video_path.parent, video_path.parent / 'subs']

    return [
        sub_path
        for search_dir in search_dirs
        if search_dir.exists()
        for ext in SUBTITLE_EXTENSIONS
        if (sub_path := search_dir / f"{video_name}{ext}").exists()
    ]


def _find_subtitle_file(video_path: str) -> Optional[Path]:
    paths = _find_subtitle_paths(Path(video_path))
    return paths[0] if paths else None


def _load_subtitle_file(subtitle_path: Path) -> Optional[str]:
    if not subtitle_path.exists():
        return None

    try:
        return subtitle_path.read_text(encoding='utf-8')
    except (OSError, UnicodeDecodeError):
        return None


def load_subtitles(video_path: str) -> Optional[str]:
    subtitle_path = _find_subtitle_file(video_path)
    return _load_subtitle_file(subtitle_path) if subtitle_path else None
