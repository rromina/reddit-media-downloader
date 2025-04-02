import os
import praw
import requests
import csv
import urllib.request
from datetime import date
import logging
import json
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# Configure logging
log_folder = "logs"
os.makedirs(log_folder, exist_ok=True)
logging.basicConfig(filename=os.path.join(log_folder, 'reddit_downloader.log'), level=logging.INFO)

# Function to count the difference of days between today and a given date
def days_diff(day):
    d1 = [int(i) for i in day.split('-')]
    d2 = [int(i) for i in str(date.today()).split('-')]
    if d1[:2] == d2[:2]:
        return d2[2] - d1[2]
    elif d1[0] == d2[0]:
        if d1[1] < d2[1]:
            return ((30 - d1[2]) + d2[2] + 30 * (d2[1] - d1[1] - 1))
    else:
        return 365  # No need to check if years are different

def safe_title(title):
    # Replace invalid characters in the title to create a safe filename
    invalid_chars = r'\/:*?"<>|'
    for char in invalid_chars:
        title = title.replace(char, '_')
    return title

def configure_logger():
    logger = logging.getLogger(__name__)
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger

def load_config(filename='config.json'):
    with open(filename, 'r') as f:
        config = json.load(f)
        # Check if DOWNLOAD_LIMIT is present and not null, otherwise set it to float('inf')
        config["DOWNLOAD_LIMIT"] = config.get("DOWNLOAD_LIMIT", float('inf'))
        return config

def handle_keyboard_interrupt(logger):
    logger.info(f"{Fore.RED}Execution interrupted by user (Ctrl+C). Cleaning up...{Style.RESET_ALL}")
    logger.info(f"{Fore.RED}Cleanup complete. Exiting...{Style.RESET_ALL}")
    exit()

def main():
    # Initialize logger
    logger = configure_logger()

    # Load configuration
    config = load_config()

    # Getting downloaded content list
    try:
        with open("downloaded.csv", "r") as f:
            downloaded_content = [i[0] for i in csv.reader(f) if i]
    except FileNotFoundError:
        downloaded_content = []

    # Creating folders if they don't exist
    for subfolder in config["SUBREDDITS"]:
        if not os.path.exists(subfolder):
            os.makedirs(subfolder)

    downloaded = 0
    # Getting content from Reddit
    subreddit = config["SUBREDDITS"][0]
    reddit = praw.Reddit(
        client_id=config["CLIENT_ID"],
        client_secret=config["CLIENT_SECRET"],
        user_agent=config["USER_AGENT"]
    )

    try:
        for submission in reddit.subreddit(subreddit).hot(limit=None):
            content_id = submission.id
            if content_id not in downloaded_content:
                author = str(submission.author)
                truncated_author = author[:10]
                truncated_title = submission.title[:50]

                logger.info(f"{Fore.CYAN}Processing: {truncated_title} by {truncated_author}{Style.RESET_ALL}")

                # Process media content
                if submission.media_only:
                    media_url = submission.url
                    file_type = media_url.split('.')[-1]
                    safe_filename = f"{safe_title(truncated_title)}_{safe_title(truncated_author)}.{file_type}"
                    folder_path = os.path.join(subreddit, safe_filename)
                    response = requests.get(media_url)
                    with open(folder_path, 'wb') as f:
                        f.write(response.content)
                    logger.info(f"{Fore.GREEN}Downloaded: {safe_filename}{Style.RESET_ALL}")
                elif submission.url.endswith(('.jpg', '.jpeg', '.png', '.gif')):
                    file_type = submission.url.split('.')[-1]
                    safe_filename = f"{safe_title(truncated_title)}_{safe_title(truncated_author)}.{file_type}"
                    folder_path = os.path.join(subreddit, safe_filename)
                    urllib.request.urlretrieve(submission.url, folder_path)  # Download the content
                    logger.info(f"{Fore.GREEN}Downloaded: {safe_filename}{Style.RESET_ALL}")
                elif submission.is_video and submission.media and 'reddit_video' in submission.media:
                    video_url = submission.media['reddit_video']['fallback_url']
                    file_type = "mp4"
                    safe_filename = f"{safe_title(truncated_title)}_{safe_title(truncated_author)}.{file_type}"
                    folder_path = os.path.join(subreddit, safe_filename)
                    urllib.request.urlretrieve(video_url, folder_path)  # Download the content
                    logger.info(f"{Fore.GREEN}Downloaded: {safe_filename}{Style.RESET_ALL}")
                elif submission.media and 'gallery_data' in submission.media:
                    gallery_data = submission.media['gallery_data']
                    gallery_title = safe_title(truncated_title)
                    gallery_folder = os.path.join(subreddit, gallery_title)

                    # Create a folder for the gallery if it doesn't exist
                    if not os.path.exists(gallery_folder):
                        os.makedirs(gallery_folder)

                    # Download each item in the gallery
                    for idx, item in enumerate(gallery_data['items'], start=1):
                        media_url = item['media_url']
                        file_type = media_url.split('.')[-1]
                        safe_filename = f"file{idx}_{safe_title(truncated_author)}.{file_type}"
                        folder_path = os.path.join(gallery_folder, safe_filename)
                        urllib.request.urlretrieve(media_url, folder_path)  # Download the content
                        logger.info(f"{Fore.GREEN}Downloaded: {safe_filename} in gallery {gallery_title}{Style.RESET_ALL}")
                else:
                    logger.warning(f"{Fore.YELLOW}Unsupported format for: {truncated_title} by {truncated_author}")
                    logger.warning(f"{Fore.YELLOW}URL: {submission.url}{Style.RESET_ALL}")

                # Save downloaded content id onto file
                with open("downloaded.csv", "a", newline="") as f:
                    csv.writer(f).writerow([content_id, date.today()])

                downloaded += 1
                if config["DOWNLOAD_LIMIT"] is not None and downloaded >= config["DOWNLOAD_LIMIT"]:
                    break
            else:
                logger.warning(f"{Fore.YELLOW}Already downloaded: {submission.title} by {submission.author}{Style.RESET_ALL}")

            # Switch the subreddit
            if config["SUBREDDITS"].index(subreddit) == len(config["SUBREDDITS"]) - 1:
                subreddit = config["SUBREDDITS"][0]
            else:
                subreddit = config["SUBREDDITS"][config["SUBREDDITS"].index(subreddit) + 1]

    except KeyboardInterrupt:
        handle_keyboard_interrupt(logger)

if __name__ == "__main__":
    main()
