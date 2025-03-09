import yt_dlp
import random
import time
import subprocess
from urllib.parse import urlparse

# Specify the external application to download the videos
EXTERNAL_APP = "./yt-dlp.exe"
DOWNLOAD_FOLDER = "./YShorts"

# Function to check if a URL is valid
def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

# Function to search for a specified number of YouTube Shorts videos based on tags
def search_youtube_shorts(tags, num_videos=100):
    """Searches for a specified number of YouTube Shorts videos based on tags."""
    try:
        # Create a search query from the tags
        search_query = " ".join(tags) + " shorts"

        # Options for searching videos
        ydl_opts_search = {
            'quiet': True,
            'extract_flat': "in_playlist",
            'force_ipv4': True,
            'playlistend': num_videos * 3,
        }

        # Search for videos using yt_dlp
        with yt_dlp.YoutubeDL(ydl_opts_search) as ydl_search:
            try:
                search_results = ydl_search.extract_info(f"ytsearch{num_videos * 3}:{search_query}", download=False)
                video_urls = [
                    entry['url']
                    for entry in search_results['entries']
                    if entry.get('url') and is_valid_url(entry.get('url')) and entry.get('_type') == 'url'
                ]

                # If no videos are found, print a message and return
                if not video_urls:
                    print(f"No Shorts found for tags: {', '.join(tags)}")
                    return

                # Shuffle the video URLs and select the required number of videos
                random.shuffle(video_urls)
                video_urls = video_urls[:num_videos]

                # Log the video URLs to the console and download them using the external app
                for idx, url in enumerate(video_urls, start=1):
                    print(f"{idx}. {url}")
                    download_video(url)

            except yt_dlp.DownloadError as search_error:
                print(f"Error during search: {search_error}")
            except Exception as e:
                print(f"An unexpected error occurred during search: {e}")

    except Exception as general_error:
        print(f"An unexpected error occurred: {general_error}")

# Function to download a video using the external application
def download_video(url):
    try:
        subprocess.run([EXTERNAL_APP, url, "-P", DOWNLOAD_FOLDER], check=True)
        print(f"Downloaded: {url}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to download {url}: {e}")
    except Exception as e:
        print(f"An unexpected error occurred while downloading {url}: {e}")

if __name__ == "__main__":
    try:
        # Get user input for tags
        user_tags_input = input("Enter tags separated by spaces (e.g., cats funny memes): ")
        user_tags = user_tags_input.split()

        # Call the function to search YouTube Shorts
        search_youtube_shorts(user_tags)

        print("Search process completed.")

    except KeyboardInterrupt:
        print("\nSearch interrupted by user.")
    except Exception as main_error:
        print(f"An unexpected error occurred in the main process: {main_error}")
