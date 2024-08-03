import json
from dataclasses import asdict, dataclass


@dataclass
class FootballVideo:
    snippet: str
    title: str
    link: str
    rank: int
    date: str

    def __str__(self):
        return json.dumps(asdict(self))
