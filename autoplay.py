import json
import os
import random
from youtube import get_music_info

GRAPH_FILE = "song_transitions.json"

def load_graph():
    if not os.path.exists(GRAPH_FILE):
        return {}
    try:
        with open(GRAPH_FILE, 'r') as f:
            return json.load(f)
    except:
        return {}

def save_graph(graph):
    with open(GRAPH_FILE, 'w') as f:
        json.dump(graph, f)

def record_transition(current_song, next_song):
    if not current_song or not next_song:
        return
    
    current_id = current_song.get('url')
    next_id = next_song.get('url')
    
    if not current_id or not next_id:
        return
    
    graph = load_graph()
    if current_id not in graph:
        graph[current_id] = {}
    if next_id not in graph[current_id]:
        graph[current_id][next_id] = 0
    graph[current_id][next_id] += 1
    save_graph(graph)

def get_next_from_graph(current_song):
    if not current_song:
        return None
    
    current_id = current_song.get('url')
    if not current_id:
        return None
    
    graph = load_graph()
    if current_id not in graph:
        return None
    
    transitions = graph[current_id]
    if not transitions:
        return None
    
    next_id = max(transitions, key=transitions.get)
    return {"url": next_id}

def get_random_by_artist(current_song):
    if not current_song or not current_song.get('artist'):
        return None
    
    try:
        results = get_music_info(current_song['artist'])
        if not results:
            return None
        
        filtered = [s for s in results if s.get('url') != current_song.get('url')]
        if not filtered:
            return None
        
        return random.choice(filtered)
    except:
        return None

def get_autoplay_song(current_song):
    if not current_song:
        return None
    
    next_song = get_next_from_graph(current_song)
    if next_song:
        return next_song
    
    return get_random_by_artist(current_song)
