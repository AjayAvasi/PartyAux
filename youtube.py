import requests
import json

def get_music_info(search_query):
    uncleaned_song_list =[]
    cleaned_song_list = []
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/json",
            "Origin": "https://music.youtube.com",
            "Referer": "https://music.youtube.com/",
            "Connection": "keep-alive"
        }
        url = "https://music.youtube.com/youtubei/v1/search"
        payload = {
    "context": {
        "client": {
            "hl": "en",
            "gl": "US",
            "remoteHost": "2600:4040:a8e0:5b00:2813:91f2:bd72:5aec",
            "deviceMake": "",
            "deviceModel": "",
            "visitorData": "CgtXVl9DQ1JnVzFmYyjxy7TDBjIKCgJVUxIEGgAgHg%3D%3D",
            "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36,gzip(gfe)",
            "clientName": "WEB_REMIX",
            "clientVersion": "1.20250702.03.00",
            "osName": "Windows",
            "osVersion": "10.0",
            "originalUrl": "https://music.youtube.com/",
            "platform": "DESKTOP",
            "clientFormFactor": "UNKNOWN_FORM_FACTOR",
            "configInfo": {
                "appInstallData": "CPHLtMMGEKOuzxwQ2JzPHBCZmLEFENr3zhwQh6zOHBD2us8cEImwzhwQy8DPHBCXtc8cEK-GzxwQu9nOHBDFu88cEKuXgBMQvZmwBRC8nM8cEJOGzxwQudnOHBDT4a8FEParsAUQ4riwBRCI468FEIHNzhwQ_LLOHBCQvM8cELfq_hIQ8OLOHBCKgoATEJT-sAUQmY2xBRC45M4cEL22rgUQ5a7PHBCCoM8cEKS2zxwQiIewBRDpu88cEIuvzxwQyfevBRDM364FEJSazxwQ7qDPHBDTts8cELWwzxwQ3rzOHBDg4P8SEL6KsAUQntCwBRDwnc8cKihDQU1TR0JVVHBiMndETnprQnVIZGhRckwzQTZ2aUFhdTJ3WWRCdz09",
                "coldConfigData": "CPHLtMMGGjJBT2pGb3gzTHFsUHphQW4tdlVJeTRJUEVOSFZBem9xTWJLOGp0SWkyS3hrX1ZPZW9YdyIyQU9qRm94M0xxbFB6YUFuLXZVSXk0SVBFTkhWQXpvcU1iSzhqdElpMkt4a19WT2VvWHc%3D",
                "coldHashData": "CPHLtMMGEhM4MzcyMjg4Nzg1MDY2MDg0NzkyGPHLtMMGMjJBT2pGb3gzTHFsUHphQW4tdlVJeTRJUEVOSFZBem9xTWJLOGp0SWkyS3hrX1ZPZW9YdzoyQU9qRm94M0xxbFB6YUFuLXZVSXk0SVBFTkhWQXpvcU1iSzhqdElpMkt4a19WT2VvWHc%3D",
                "hotHashData": "CPHLtMMGEhM1MDk1ODQ3ODY0ODIwNTkxNzMyGPHLtMMGMjJBT2pGb3gzTHFsUHphQW4tdlVJeTRJUEVOSFZBem9xTWJLOGp0SWkyS3hrX1ZPZW9YdzoyQU9qRm94M0xxbFB6YUFuLXZVSXk0SVBFTkhWQXpvcU1iSzhqdElpMkt4a19WT2VvWHc%3D"
            },
            "browserName": "Chrome",
            "browserVersion": "137.0.0.0",
            "acceptHeader": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "deviceExperimentId": "ChxOelV5TkRjeE1qSTNNVEV4TmpZMk5EWXlPUT09EPHLtMMGGPHLtMMG",
            "rolloutToken": "CP-U_-7uiraWkwEQnI7ywbetjgMYnI7ywbetjgM%3D",
            "screenWidthPoints": 1091,
            "screenHeightPoints": 894,
            "screenPixelDensity": 2,
            "screenDensityFloat": 1.75,
            "utcOffsetMinutes": -240,
            "userInterfaceTheme": "USER_INTERFACE_THEME_DARK",
            "timeZone": "America/New_York",
            "musicAppInfo": {
                "pwaInstallabilityStatus": "PWA_INSTALLABILITY_STATUS_UNKNOWN",
                "webDisplayMode": "WEB_DISPLAY_MODE_BROWSER",
                "storeDigitalGoodsApiSupportStatus": {
                    "playStoreDigitalGoodsApiSupportStatus": "DIGITAL_GOODS_API_SUPPORT_STATUS_UNSUPPORTED"
                }
            }
        },
        "user": {
            "lockedSafetyMode": False
        },
        "request": {
            "useSsl": True,
            "internalExperimentFlags": [],
            "consistencyTokenJars": []
        },
        "clickTracking": {
            "clickTrackingParams": "CJACEPleGAEiEwi3v__Dt62OAxWMguQGHTRcE1w="
        },
        "adSignalsInfo": {
            "params": [
                {"key": "dt", "value": "1751983601945"},
                {"key": "flash", "value": "0"},
                {"key": "frm", "value": "0"},
                {"key": "u_tz", "value": "-240"},
                {"key": "u_his", "value": "4"},
                {"key": "u_h", "value": "1029"},
                {"key": "u_w", "value": "1646"},
                {"key": "u_ah", "value": "981"},
                {"key": "u_aw", "value": "1646"},
                {"key": "u_cd", "value": "24"},
                {"key": "bc", "value": "31"},
                {"key": "bih", "value": "894"},
                {"key": "biw", "value": "1076"},
                {"key": "brdim", "value": "0,0,0,0,1646,0,1646,981,1091,894"},
                {"key": "vis", "value": "1"},
                {"key": "wgl", "value": "true"},
                {"key": "ca_type", "value": "image"}
            ]
        }
    },
    "query": search_query,
    "params": "EgWKAQIIAWoSEAMQCRAEEA4QChAFEBAQERAV"
}
        
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        
        data = response.json()
        uncleaned_song_list = data["contents"]["tabbedSearchResultsRenderer"]["tabs"][0]["tabRenderer"]["content"]["sectionListRenderer"]["contents"][0]["musicShelfRenderer"]["contents"]
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



