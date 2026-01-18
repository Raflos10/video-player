import re
from enum import Enum, auto
from typing import List, Optional

from subtitle.subtitle_entry import SubtitleEntry


class SubtitleFormat(Enum):
    AUTO = auto()
    SRT = auto()
    VTT = auto()


def _parse_timestamp_line(line: str) -> Optional[tuple]:
    timestamp_match = re.match(
        r"(\d{2}):(\d{2}):(\d{2})[,.](\d{3})\s*-->\s*(\d{2}):(\d{2}):(\d{2})[,.](\d{3})",
        line,
    )

    if timestamp_match:
        start_h, start_m, start_s, start_ms, end_h, end_m, end_s, end_ms = map(
            int, timestamp_match.groups()
        )

        start_time_ms = ((start_h * 3600 + start_m * 60 + start_s) * 1000) + start_ms
        end_time_ms = ((end_h * 3600 + end_m * 60 + end_s) * 1000) + end_ms

        return start_time_ms, end_time_ms

    return None


def _parse_srt(content: str, strip_text: bool = True) -> List[SubtitleEntry]:
    result = []
    blocks = content.strip().split("\n\n")

    for block in blocks:
        lines = block.strip().split("\n")
        if len(lines) < 3:
            continue

        try:
            index = int(lines[0])
        except ValueError:
            continue

        times = _parse_timestamp_line(lines[1])

        if times:
            start_ms, end_ms = times
            text_lines = lines[2:]
            if strip_text:
                text_lines = [line.strip() for line in text_lines]
            text = "\n".join(text_lines)

            result.append(
                SubtitleEntry(index=index, start_ms=start_ms, end_ms=end_ms, text=text)
            )

    return result


def _parse_vtt(content: str, strip_text: bool = True) -> List[SubtitleEntry]:
    result = []

    content = re.sub(r"^WEBVTT[^\n]*\n\n?", "", content, flags=re.MULTILINE)

    blocks = content.strip().split("\n\n")
    index = 1

    for block in blocks:
        lines = block.strip().split("\n")
        if len(lines) < 2:
            continue

        timestamp_line_idx = 0
        if "-->" not in lines[0] and len(lines) > 1:
            timestamp_line_idx = 1

        times = _parse_timestamp_line(lines[timestamp_line_idx])

        if times:
            start_ms, end_ms = times
            text_lines = lines[timestamp_line_idx + 1:]
            if strip_text:
                text_lines = [line.strip() for line in text_lines]
            text = "\n".join(text_lines)

            result.append(
                SubtitleEntry(index=index, start_ms=start_ms, end_ms=end_ms, text=text)
            )
            index += 1

    return result


def parse(
        content: str,
        subtitle_format: SubtitleFormat = SubtitleFormat.AUTO,
        strip_text: bool = True,
) -> List[SubtitleEntry]:
    match subtitle_format:
        case SubtitleFormat.SRT:
            return _parse_srt(content, strip_text)
        case SubtitleFormat.VTT:
            return _parse_vtt(content, strip_text)
        case _:
            return (
                _parse_vtt(content, strip_text)
                if "WEBVTT" in content[:20]
                else _parse_srt(content, strip_text)
            )
