import base64

import requests
import streamlit as st

from models import Listing



# ebay api endpoints
TOKEN_URL = "https://api.ebay.com/identity/v1/oauth2/token"
SEARCH_URL = "https://api.ebay.com/buy/browse/v1/item_summary/search"



def _get_token():

    app_id = st.secrets["ebay"]["app_id"]
    cert_id = st.secrets["ebay"]["cert_id"]

    creds = app_id + ":" + cert_id
    auth = base64.b64encode(creds.encode()).decode()

    r = requests.post(
        TOKEN_URL,
        headers={
            "Authorization": "Basic " + auth,
            "Content-Type": "application/x-www-form-urlencoded",
        },
        data={
            "grant_type": "client_credentials",
            "scope": "https://api.ebay.com/oauth/api_scope",
        },
        timeout=10,
    )
    r.raise_for_status()

    return r.json()["access_token"]



def fetch(brand, limit=100):

    token = _get_token()

    r = requests.get(
        SEARCH_URL,
        headers={
            "Authorization": "Bearer " + token,
            "X-EBAY-C-MARKETPLACE-ID": "EBAY_US",
        },
        params={"q": brand, "limit": min(limit, 200)},
        timeout=15,
    )
    r.raise_for_status()

    raw = r.json().get("itemSummaries") or []


    listings = []
    for it in raw:
        title = it.get("title", "")
        seller = (it.get("seller") or {}).get("username", "")
        price = float((it.get("price") or {}).get("value") or 0)
        url = it.get("itemWebUrl", "")

        listings.append(Listing(
            source="ebay",
            title=title,
            seller=seller,
            price=price,
            url=url,
        ))


    return listings
