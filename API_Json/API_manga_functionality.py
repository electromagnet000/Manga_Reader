import json
import requests

def Api_add_manga(manga_title,index):
    base_url = "https://api.mangadex.org"
    includes = ['author', 'cover_art', 'artist']
    response = requests.get(f"{base_url}/manga", params={"title": manga_title, "includes[]": includes})
    if response.status_code == requests.codes.ok:

        fetched_data = response.json()

        manga_entry = fetched_data["data"][index]
        manga_data = manga_entry.get('attributes')

        manga_wanted = {}

        manga_wanted['id'] = manga_entry.get('id')
        title_manga = manga_data.get('title')
        manga_wanted['title'] = title_manga.get("en") if title_manga else None
        manga_wanted['year'] = manga_data.get('year')
        description_data = manga_data.get('description')
        manga_wanted['description'] = description_data.get('en') if description_data else None

        manga_wanted['cover_art_id'] = None
        manga_wanted['cover_art_filename'] = None
        manga_wanted['author'] = None
        manga_wanted['rating'] = None

        for relationship in manga_entry.get('relationships', []):
            if relationship.get('type') == 'cover_art':
                cover_art_data = relationship.get('attributes')
                manga_wanted['cover_art_id'] = relationship.get('id')
                manga_wanted['cover_art_filename'] = cover_art_data.get('fileName')
            if relationship.get('type') == 'author':
                author_data = relationship.get('attributes')
                manga_wanted['author'] = author_data.get("name")

        try:
            if not manga_wanted:
                return f"Manga : {manga_title} not found in API"
        except KeyError as e:
            return f"Manga : {manga_title} not found in API database"

        return manga_wanted
