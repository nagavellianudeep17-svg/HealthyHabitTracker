from dataclasses import dataclass, asdict
from datetime import date
from typing import Optional

@dataclass
class HabitRecord:
    id: str
    date: str
    habit: str
    amount: float
    unit: str
    note: str = ""
    created_at: str = ""

    def to_dict(self):
        return asdict(self)
