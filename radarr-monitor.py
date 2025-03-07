import requests
import time

# Configuration
RADARR_API_URL = "http://localhost:7878/api/v3"
RADARR_API_KEY = "your_radarr_api_key"
CHECK_INTERVAL = 60  # Check every 60 seconds

def get_queue():
    response = requests.get(f"{RADARR_API_URL}/queue", headers={"X-Api-Key": RADARR_API_KEY})
    response.raise_for_status()
    return response.json()

def blocklist_download(download_id):
    response = requests.delete(f"{RADARR_API_URL}/queue/{download_id}", headers={"X-Api-Key": RADARR_API_KEY})
    response.raise_for_status()

def search_again(movie_id):
    response = requests.post(f"{RADARR_API_URL}/command", json={"name": "MoviesSearch", "movieIds": [movie_id]}, headers={"X-Api-Key": RADARR_API_KEY})
    response.raise_for_status()

def monitor_radarr():
    while True:
        print("Checking Radarr queue...")
        queue = get_queue()
        for item in queue.get("records", []):
            status_messages = item.get("statusMessages", [])
            skip_download = False
            for message in status_messages:
                if "This movie has individual episode mappings on TheXEM but the mapping for this episode has not been confirmed yet by their administrators. TheXEM needs manual input." in message.get("messages", []):
                    print(f"Skipping download {item.get('id')} due to pending XEM mapping")
                    skip_download = True
                    break
            if skip_download:
                continue
            if item.get("status") == "failed" or item.get("trackedDownloadState") == "importBlocked":
                download_id = item.get("id")
                movie_id = item.get("movieId")
                print(f"Blocking download {download_id} and searching again for movie {movie_id}")
                blocklist_download(download_id)
                search_again(movie_id)
        print(f"Sleeping for {CHECK_INTERVAL} seconds...")
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    monitor_radarr()