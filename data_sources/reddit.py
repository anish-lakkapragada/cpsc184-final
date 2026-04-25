from datetime import datetime

import praw
import streamlit as st

from models import Mention



def fetch(brand, limit=100):

    reddit = praw.Reddit(
        client_id=st.secrets["reddit"]["client_id"],
        client_secret=st.secrets["reddit"]["client_secret"],
        user_agent=st.secrets["reddit"]["user_agent"],
    )


    mentions = []

    # search all of reddit for the brand name
    for s in reddit.subreddit("all").search(brand, limit=limit):

        text = (s.title + "\n" + (s.selftext or "")).strip()

        mentions.append(Mention(
            source="reddit",
            text=text,
            url="https://reddit.com" + s.permalink,
            timestamp=datetime.fromtimestamp(s.created_utc),
        ))


    return mentions
