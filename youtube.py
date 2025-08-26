import requests
import json
import youtube_config

def get_music_info(search_query):
    uncleaned_song_list =[]
    cleaned_song_list = []
    try:
        headers = youtube_config.headers
        url = "https://music.youtube.com/youtubei/v1/search"
        payload = {
    "context": youtube_config.context,
    "query": search_query,
    "params": "EgWKAQIIAWoSEAMQCRAEEA4QChAFEBAQERAV"
}
        
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        
        data = response.json()
        temp_list = data["contents"]["tabbedSearchResultsRenderer"]["tabs"][0]["tabRenderer"]["content"]["sectionListRenderer"]["contents"]
        uncleaned_song_list = None
        for section in temp_list:
            if "musicShelfRenderer" in section:
                uncleaned_song_list = section["musicShelfRenderer"]["contents"]
                break
        if not uncleaned_song_list:
            return []
        for song in uncleaned_song_list:
            if "musicResponsiveListItemRenderer" in song:
                song = song["musicResponsiveListItemRenderer"]
                summary = song["flexColumns"][1]["musicResponsiveListItemFlexColumnRenderer"]["text"]["accessibility"]["accessibilityData"]["label"].split(" \u2022 ")
                artist = summary[0]
                album = summary[1]
                duration = summary[2]
                title = song["flexColumns"][0]["musicResponsiveListItemFlexColumnRenderer"]["text"]["runs"][0]["text"]
                url = song["overlay"]["musicItemThumbnailOverlayRenderer"]["content"]["musicPlayButtonRenderer"]["playNavigationEndpoint"]["watchEndpoint"]["videoId"]
                art_size = 500
                album_art = song["thumbnail"]["musicThumbnailRenderer"]["thumbnail"]["thumbnails"][0]["url"].split("=")[0] + f"=w{art_size}-h{art_size}-l90-rj"
                cleaned_song_list.append({"artist": artist, "album": album, "duration": duration, "title": title, "url": url, "album_art": album_art})
        
    except Exception as e:
        print("Error: " + search_query + " " + str(e))
    return cleaned_song_list


def get_search_suggestion(search_query):
    suggestions = []
    try:
        headers = youtube_config.headers
        url = f"https://music.youtube.com/youtubei/v1/music/get_search_suggestions"
        payload = {
            "context": youtube_config.context,
            "input": search_query
        }
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        data = response.json()
        uncleaned_list = data["contents"][0]["searchSuggestionsSectionRenderer"]["contents"]
        suggestions = [{"complete_query": item["searchSuggestionRenderer"]["navigationEndpoint"]["searchEndpoint"], "completion_parts": item["searchSuggestionRenderer"]["suggestion"]["runs"]} for item in uncleaned_list]

    except Exception as e:
        print("Error: " + search_query + " " + str(e))
    return suggestions
