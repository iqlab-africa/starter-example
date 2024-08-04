import json
import logging
from click import DateTime
from robocorp import browser
from robocorp.tasks import task
from RPA.Excel.Files import Files as Excel

from pathlib import Path
import os
import requests
from dataclasses import asdict, dataclass
import time
import http.client
import json
from robocorp.tasks import setup

from models.data import FootballVideo

SERPDOG_APIKEY = "66ae2e8af5d49eb9951dcb15"
SERPER_APIKEY = "31d4e6b5598c587634db1fdbbed5c68690b04861"
tag = "🔵 🔵 Premier League/NFL Video Bot 🔵"
WEB_URL = "https://bidvest-backend-irhgo3zz5q-ew.a.run.app/bot/addBotVideos"

premier_league_queries = [
    # "latest Premier League Arsenal highlight videos",
    # "latest Premier League Arsenal player videos",
    "latest Premier League highlight videos",
    "latest Premier League player videos",
    "latest Premier League team videos",
]

nfl_queries = [
    # "latest NFL Baltimore Ravens highlight videos",
    # "latest NFL Baltimore Ravens player videos",
    "latest NFL highlight videos",
    "latest NFL player videos",
    "latest NFL team videos",
]

video_links = []


@setup
def measure_time(task):
    start = time.time()
    yield  # Task executes here
    duration = time.time() - start
    print(f"{tag} Task {task.name} took  🍎🍎 {duration} seconds")


def useSerper(query):
    print(f"{tag}... using SERPER api ...")
    conn = http.client.HTTPSConnection("google.serper.dev")
    payload = json.dumps({"q": query})
    headers = {
        "X-API-KEY": SERPER_APIKEY,
        "Content-Type": "application/json",
    }
    list = []
    conn.request("POST", "/search", payload, headers)
    res = conn.getresponse()
    data = res.read()
    if res.status == 200:
        resultJson = json.loads(data.decode("utf-8"))
        m_list = resultJson["organic"]
        print(f"\n{tag} resultJson:  🥬 🍎🍎 {len(m_list)} elements in list 🍎🍎 🥬 ")
        for x in m_list:
            if "watch?" in x["link"]:
                x["searched"] = time.time()
                list.append(x)
        print(
            f"\n{tag} resultJson after filtering:  🥬 🍎🍎 {len(m_list)} elements in list 🍎🍎 🥬 "
        )

    else:
        print(f"{tag} Houston, we have a problem: {res.reason}")

    return list


@task
def premier_task():
    """Premier Task"""
    print(
        f"{tag} Houston, we are starting ...  💙 queries: {len(premier_league_queries)}"
    )
    # Search for Premier League content
    for query in premier_league_queries:
        result = useSerper(query)
        for fv in result:
            video_links.append(fv)
        print(
            f"{tag} video links so far :  💙 {len(video_links)}, will sleep for 2 seconds ... ${time.ctime()}"
        )
        time.sleep(2)
        print(f"{tag} ... awake now: ${time.ctime()}")
    # Search for National Football League content
    for query in nfl_queries:
        result = useSerper(query)
        for fv in result:
            video_links.append(fv)
        print(
            f"{tag} video links so far :  💙 {len(video_links)}, will sleep for 2 seconds ... ${time.ctime()}"
        )
        time.sleep(2)
        print(f"{tag} ... awake now: ${time.ctime()}")

    print(
        f"\n\n{tag} robot premier_task completed. video links to be returned : 🥬🥬🥬🥬🥬🥬🥬🥬 {len(video_links)} videos \n\n"
    )
    count = 1
    for m in video_links:
        print(f"{tag} video_links 🍎🍎 video #{count}: {m['link']}")
        count = count + 1

    print(f"{tag} video_links type: {type(video_links)}")
    sendResults(video_links)
    return video_links


def sendResults(data_list):
    print(f"{tag} .... sending results: {len(data_list)} to  💦 {WEB_URL} 💦")
    headers = {"Content-Type": "application/json"}
    resp = requests.post(WEB_URL, data=json.dumps(data_list), headers=headers)
    if resp.status_code < 202:
        print(f"\n\n{tag} we very good, Boss!! 🥬🥬🥬 statusCode: {resp.status_code}\n")
    else:
        print(
            f"{tag} ERROR: 👿 status: {resp.status_code} - 👿 reason: {resp.reason} 👿"
        )
        return

    print(f"{tag} 🥬🥬🥬🥬🥬🥬🥬🥬 we seem to be done & dusted, Jack? 🥬🥬🥬🥬🥬🥬🥬🥬")


# def search(query):
#     """Search the web for League info ..."""
#     print(f"\n\n\n{tag} search starting ... 💙 query: {query}")
#     local_list = []
#     payload = {"api_key": SERPDOG_APIKEY, "q": query, "gl": "eu"}
#     resp = requests.get("https://api.serpdog.io/lite_search", params=payload)
#     # Check if the request was successful
#     print(resp.json())
#     if resp.status_code == 200:
#         print(
#             f"{tag} We good, Boss! 💙 Status code: {resp.status_code} elapsed: {resp.elapsed}"
#         )
#     else:
#         print(
#             f"{tag} Call failed. 👿 Status code: {resp.status_code} reason: ${resp.reason}"
#         )
#         res = useSerper(query)
#         return res
#     # process the response
#     m = resp.json()
#     link_list = list(m.values())
#     print(f"{tag} number of links:  💙 {len(link_list)}")
#     count = 0
#     for x in link_list:
#         if count > 2:
#             print(f"{tag} number of elements: 🥦 {len(x)} 🥦")
#             for z in x:
#                 try:
#                     link = z.get("link")
#                     snippet = z.get("snippet")
#                     title = z.get("title")
#                     rank = z.get("rank")
#                     m_date = datetime.now().isoformat()
#                     if link and "watch" in link:
#                         fv = FootballVideo(
#                             snippet=snippet,
#                             title=title,
#                             link=link,
#                             rank=rank,
#                             date=m_date,
#                         )
#                         local_list.append(fv)
#                     else:
#                         print("👿 Link not found for the given item.")
#                 except Exception as e:
#                     print(f"An error occurred: {e}")
#                     continue  # This will skip to the next iteration in case of an exception
#         else:
#             print(f"{tag} ignored ... count: {count}")
#         count = count + 1

#     return local_list
