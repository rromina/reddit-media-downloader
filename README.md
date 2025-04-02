# Reddit Media Downloader

This Python script simplifies the process of bulk downloading media content from Reddit. It uses the PRAW library to interact with the Reddit API, enabling easy retrieval and local storage of media files.

## Table of Contents

- [Reddit Media Downloader](#reddit-media-downloader)
  - [Table of Contents](#table-of-contents)
  - [Project Structure](#project-structure)
  - [Installation](#installation)
  - [Configuration](#configuration)
  - [Usage](#usage)
  - [KeyboardInterrupt Handling](#keyboardinterrupt-handling)
  - [Additional Information](#additional-information)

## Project Structure

```plaintext
└── reddit-media-downloader
    ├── main.py
    ├── config.json
    ├── downloaded.csv
    ├── logs/
    ├── LICENSE.md
    ├── CONTRIBUTING.md
    └── README.md
```

1. **main.py**: The main script for interacting with the Reddit API and downloading media content.

2. **config.json**: Configuration file containing details such as Reddit API credentials, user agent, subreddits, and download limit.

3. **downloaded.csv**: A CSV file to keep track of downloaded content IDs and dates.

4. **logs/**: A folder for storing logs generated during the script's execution.

5. **LICENSE.md**: The license file detailing the permissions and limitations of using the project.

6. **CONTRIBUTING.md**: Guidelines for community contributions, including reporting issues and submitting pull requests.

## Installation

1. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/rromina/reddit-media-downloader.git
   ```

2. Navigate to the project folder:

   ```bash
   cd reddit-media-downloader
   ```

3. Install dependencies using pip:

   ```bash
   pip install praw requests colorama
   ```

## Configuration

1. Make a `config.json` file and provide the necessary information:

   ```json
   {
     "CLIENT_ID": "your_reddit_client_id",
     "CLIENT_SECRET": "your_reddit_client_secret",
     "USER_AGENT": "your_user_agent",
     "SUBREDDITS": ["subreddit1", "subreddit2"],
     "DOWNLOAD_LIMIT": null
   }
   ```

   - `CLIENT_ID` and `CLIENT_SECRET`: Obtain these by creating a Reddit app [here](https://www.reddit.com/prefs/apps).
   - `USER_AGENT`: A unique identifier for your application. It can be any string, for example: "example test bla bla bla".
   - `SUBREDDITS`: List of subreddits from which you want to download content.
   - `DOWNLOAD_LIMIT`: Limit the number of downloads. Use `null` for unlimited downloads.

## Usage

1. Run the script by executing the following command:

   ```bash
   python main.py
   ```

2. The script will fetch and download media content from the specified subreddits to their respective folders.

## KeyboardInterrupt Handling

The script has enhanced handling for KeyboardInterrupt (Ctrl+C). If you interrupt the execution, it will clean up and exit gracefully.

## Additional Information

- This script supports various media formats, including images, videos, and galleries.
- Downloaded content IDs and dates are logged in the `downloaded.csv` file to avoid duplicate downloads.

---

Thank you for using Reddit Media Downloader! If you encounter any issues or have suggestions for improvements, feel free to contribute or open an issue.
