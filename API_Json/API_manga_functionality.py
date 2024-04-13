import json
import requests

def Api_add_manga(manga_title):

    base_url = "https://api.mangadex.org"
    response = requests.get(f"{base_url}/manga", params={"title": manga_title})
    if response.status_code == requests.codes.ok:
        fetched_data = response.json()
        wanted_manga = [r["attributes"]["title"] for r in fetched_data["data"]][0]

        for key, value in wanted_manga.items():
            return value