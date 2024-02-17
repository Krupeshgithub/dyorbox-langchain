#!/usr/bin/python3
"""
This module constrains can use for calling the `langchain` api to get
answer according our previos questions.
"""
from __future__ import annotations

from typing import Union

import requests
import atexit
from apscheduler.schedulers.background import BackgroundScheduler


JsonType = Union["JsonType", str]


def ask_question_to_langchain(user_id: str, question: str) -> JsonType:
    response = requests.post(
        url=f"http://localhost:8000/dev/question",
        headers={
            "Content-Type": "application/json"
        },
        json={
            "question": question,
            "user_id": user_id
        }
    )
    return response.json()["answer"]


def interval_cronjob() -> None:
    """
    This function start the cronjob and end the cronjob when the server will be
    shutdown.
    """
    from chat.conversation import LangChain
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=LangChain().fetch_and_save_data, trigger="interval", seconds=1800) # (30*60)
    scheduler.start()
    atexit.register(lambda: scheduler.shutdown())
