import json
import logging
from robocorp import browser
from robocorp.tasks import task
from RPA.Excel.Files import Files as Excel

from pathlib import Path
import os
import requests
from dataclasses import asdict, dataclass
from datetime import datetime


@dataclass
class FootballVideo:
    snippet: str
    title: str
    link: str
    rank: int
    date: str

    def __str__(self):
        return json.dumps(asdict(self))


APIKEY = "66ae2e8af5d49eb9951dcb15"
mm = "🔵 🔵 Premier League/NFL Video Bot 🔵"

premier_league_queries = [
    "latest Premier League Arsenal highlight videos",
    "latest Premier League Arsenal player videos",
    "latest Premier League Arsenal team videos",
]

nfl_queries = [
    "latest NFL Baltimore Ravens highlight videos",
    "latest NFL Baltimore Ravens player videos",
    "latest NFL Baltimore Ravens team videos",
]

video_links = []

@task
def premier_task():
    """Premier Task"""
    print(f"{mm} Houston, we are starting ...  💙 queries: {len(premier_league_queries)}")
    # Search for Premier League content
    for query in premier_league_queries:
        result = search(query)
        for fv in result:
            video_links.append(fv)
        print(f"{mm} video links so far :  💙 {len(video_links)}")

    # Search for National Football League content
    for query in nfl_queries:
        result = search(query)
        for fv in result:
            video_links.append(fv)
        print(f"{mm} video links so far :  💙 {len(video_links)}")

    print(
        f"\n\n{mm} robot premier_task completed. video links to be returned : 🥬🥬🥬🥬🥬🥬🥬🥬 {len(video_links)} videos \n\n"
    )
    count = 1
    for m in video_links:
        print(f'{mm} video #{count}: {m.link}')
        count = count + 1
    return video_links


def search(query):
    """Search the web for League info ..."""
    print(f"\n\n\n{mm} search starting ... 💙 query: {query}")
    local_list = []
    payload = {"api_key": APIKEY, "q": query, "gl": "eu"}
    resp = requests.get("https://api.serpdog.io/lite_search", params=payload)
    # Check if the request was successful
    if resp.status_code == 200:
        print(
            f"{mm} We good, Boss! 💙 Status code: {resp.status_code} elapsed: {resp.elapsed}"
        )
    else:
        print(f"{mm} Call failed. 👿 Status code: {resp.status_code} reason: ${resp.reason}")
        return []
    # process the response
    m = resp.json()
    link_list = list(m.values())
    print(f"{mm} number of links:  💙 {len(link_list)}")
    count = 0
    for x in link_list:
        if count > 2:
            print(f"{mm} number of elements: 🥦 {len(x)} 🥦")
            for z in x:
                try:
                    link = z.get("link")
                    snippet = z.get("snippet")
                    title = z.get("title")
                    rank = z.get("rank")
                    m_date = datetime.now().isoformat()
                    if link and 'watch' in link:
                        fv = FootballVideo(
                            snippet=snippet,
                            title=title,
                            link=link,
                            rank=rank,
                            date=m_date,
                        )
                        local_list.append(fv)
                    else:
                        print("👿 Link not found for the given item.")
                except Exception as e:
                    print(f"An error occurred: {e}")
                    continue  # This will skip to the next iteration in case of an exception
        else:
            print(f"{mm} ignored ... count: {count}")
        count = count + 1
    
    return local_list
