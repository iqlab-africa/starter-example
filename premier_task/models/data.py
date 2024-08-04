import json
from dataclasses import asdict, dataclass
from xml.etree.ElementTree import tostring


@dataclass
class FootballVideo:
    snippet: str
    title: str
    link: str
    rank: int
    date: str

    def __str__(self):
        return json.dumps(asdict(self))
        # m = {
        #     "title": self.title,
        #     "link": self.link,
        #     "rank": self.rank,
        #     "snippet": self.snippet,
        #     'date': self.date
        # }
        # return json.dumps(m)
    def __dict__(self):
        return json.dumps(asdict(self))
    
