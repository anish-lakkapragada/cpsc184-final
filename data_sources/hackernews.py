from datetime import datetime

import requests

from models import Mention

SEARCH_URL = "https://hn.algolia.com/api/v1/search"


def fetch(brand, limit=100):
    r = requests.get(
        SEARCH_URL,
        params={"query": brand, "hitsPerPage": min(limit, 1000)},
        timeout=10,
    )
    r.raise_for_status()
    hits = r.json().get("hits", [])

    mentions = []
    for h in hits[:limit]:
        body = h.get("story_text") or h.get("comment_text") or ""
        title = h.get("title") or ""
        text = f"{title}\n{body}".strip()
        mentions.append(Mention(
            source="hackernews",
            text=text,
            url=f"https://news.ycombinator.com/item?id={h['objectID']}",
            timestamp=datetime.fromtimestamp(h["created_at_i"]),
        ))

    return mentions
