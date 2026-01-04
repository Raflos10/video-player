from bisect import bisect_right
from typing import List

from subtitle.subtitle_entry import SubtitleEntry
from subtitle.subtitle_parser import parse


class Subtitle:
    def __init__(self, file_content: str):
        entries = parse(file_content)

        self._entries = sorted(entries, key=lambda e: e.start_time)
        self._start_times = [e.start_time for e in self._entries]

    def get_all_at_time(self, time_seconds: float) -> List[SubtitleEntry]:
        result = []
        idx = bisect_right(self._start_times, time_seconds) - 1

        while idx >= 0:
            entry = self._entries[idx]
            if entry.is_displayed_at(time_seconds):
                result.append(entry)
                idx -= 1
            else:
                break

        return list(reversed(result))
