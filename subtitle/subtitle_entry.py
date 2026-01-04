from dataclasses import dataclass


@dataclass
class SubtitleEntry:
    index: int
    start_time: float
    end_time: float
    text: str

    @property
    def duration(self) -> float:
        return self.end_time - self.start_time

    def is_displayed_at(self, time_seconds: float) -> bool:
        return self.start_time <= time_seconds <= self.end_time
