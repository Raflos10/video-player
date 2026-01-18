from dataclasses import dataclass


@dataclass
class SubtitleEntry:
    index: int
    start_ms: int
    end_ms: int
    text: str

    @property
    def duration(self) -> float:
        return (self.end_ms - self.start_ms) / 1000.0

    def is_displayed_at(self, time_ms: int) -> bool:
        return self.start_ms <= time_ms <= self.end_ms
