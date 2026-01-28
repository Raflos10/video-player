from bisect import bisect_right

from subtitle.subtitle_entry import SubtitleEntry
from subtitle.subtitle_parser import parse


class Subtitle:
    def __init__(self, file_content: str) -> None:
        entries = parse(file_content)

        self._entries = sorted(entries, key=lambda e: e.start_ms)
        self._start_times = [e.start_ms for e in self._entries]

    def get_all_at_time(self, time_ms: int) -> list[SubtitleEntry]:
        result = []
        idx = bisect_right(self._start_times, time_ms) - 1

        while idx >= 0:
            entry = self._entries[idx]
            if entry.is_displayed_at(time_ms):
                result.append(entry)
                idx -= 1
            else:
                break

        return list(reversed(result))
