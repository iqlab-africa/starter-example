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

from dotenv import load_dotenv
from models.data import FootballVideo

tag = "🔵🔵 Premier League/NFL Video Bot 🔵"
WEB_URL = "https://bidvest-backend-irhgo3zz5q-ew.a.run.app/bot/addBotVideos"

premier_league_queries = [
    # "latest Premier League Arsenal highlight videos",
    # "latest Premier League Arsenal player videos",
    "latest Premier League highlight videos",
    "latest Premier League player videos",
    "latest Premier League team videos",
    "latest Supersport DSTV highlight videos",
    "latest African Football League videos",
    "latest Champions League videos",
]

nfl_queries = [
    # "latest NFL Baltimore Ravens highlight videos",
    # "latest NFL Baltimore Ravens player videos",
    "latest NFL highlight videos",
    "latest NFL player videos",
    "latest NFL team videos",
]

video_links = []


def init():
    """Initialize api keys"""
    load_dotenv()
    key = os.getenv("SERPER_APIKEY")
    # print(f"{tag} api key from .env: {key}")
    return key


@setup
def measure_time(task):
    start = time.time()
    yield  # Task executes here
    duration = time.time() - start
    elapsed = round(duration, 1)
    print(f"{tag} Task {task.name} took  🍎🍎 {elapsed} seconds\n\n")


def search_video(query):
    conn = http.client.HTTPSConnection("google.serper.dev")
    payload = json.dumps({"q": query})
    api_key = init()
    headers = {
        "X-API-KEY": api_key,
        "Content-Type": "application/json",
    }
    list = []
    conn.request("POST", "/search", payload, headers)
    res = conn.getresponse()
    data = res.read()
    if res.status == 200:
        resultJson = json.loads(data.decode("utf-8"))
        organic_results = resultJson["organic"]
        print(f"{tag} organic results: 🍎 {len(organic_results)} videos ")

        for video_element in organic_results:
            if "watch?" in video_element["link"]:
                video_element["searched"] = time.time()
                video_element["iso_date"] = time.ctime()
                list.append(video_element)

        print(f"{tag} organic_results after filtering: 🥬 {len(list)} ")
    else:
        print(f"{tag} Houston, 👿👿👿 we have a problem: {res.reason}")

    return list


SLEEP_TIME = 2


def chill():
    """Sleep for a few seconds"""
    print(f"{tag} will sleep for {SLEEP_TIME} seconds: {time.ctime()} ...")
    time.sleep(SLEEP_TIME)
    print(f"{tag} awake now after sleeping for {SLEEP_TIME} seconds: {time.ctime()}")


@task
def premier_task():
    """Premier Task is a bot that searches for sports videos based on static queries.
    Results are written to a backend api that stores them in a database."""
    print(f"\n\n\n{tag} Houston, we are starting the engines!  🚀 🚀 🚀")
    print(
        f"{tag} 💙 💙 💙 💙 💙  static queries: {len(premier_league_queries) + len(nfl_queries)} 💙 "
    )
    init()
    query_count = 1

    blues = "🔵🔵🔵🔵🔵"
    # Search for Premier League content
    for query in premier_league_queries:
        print(
            f"\n{tag}{blues} Processing Premier League search query #{query_count} .....\n"
        )
        result = search_video(query)
        query_count = query_count + 1
        for fv in result:
            video_links.append(fv)
        chill()
    # Search for National Football League content
    for query in nfl_queries:
        print(f"\n{tag}{blues} Processing NFL search query #{query_count} .....\n")
        result = search_video(query)
        query_count = query_count + 1
        for fv in result:
            video_links.append(fv)
        chill()

    print(
        f"\n\n{tag} robot premier_task completed. video links to be returned : 🥬🥬🥬🥬🥬🥬🥬🥬 {len(video_links)} videos \n\n"
    )
    count = 1
    for m in video_links:
        print(f"{tag} video_links 🍎🍎 video #{count}: {m['link']}")
        count = count + 1

    print(f"{tag} {len(video_links)} 🍎🍎🍎🍎 video elements processed! \n\n")
    sendResults(video_links)
    return video_links


def sendResults(data_list):
    print(
        f"{tag} .... sending {len(data_list)} videos to backend server  💦 {WEB_URL} 💦"
    )

    headers = {"Content-Type": "application/json"}
    resp = requests.post(WEB_URL, data=json.dumps(data_list), headers=headers)
    if resp.status_code < 202:
        print(
            f"{tag} we sitting pretty good, Boss!! 🥬🥬🥬 statusCode: {resp.status_code}\n"
        )
    else:
        print(
            f"{tag} ERROR: 👿 status: {resp.status_code} - 👿 reason: {resp.reason} 👿"
        )
        return

    print(
        f"\n{tag} 🥬🥬🥬🥬🥬🥬🥬🥬 we seem to be done & dusted, Boss!! 🥬🥬🥬🥬🥬🥬🥬🥬\n"
    )
