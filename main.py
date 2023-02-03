import os
from dotenv import load_dotenv
from utils.scrapper import EpisodeQuality, AnimeScrapper
from utils.cli import CliArguments

# Setting up default options
load_dotenv()

LINK = os.environ.get(
    "ANIME_DOWNLOAD_LINK", "https://gogo-play.tv/videos/one-piece-episode"
)
WDPATH = os.environ.get("WEBDRIVER_PATH", "./chromediver.exe")
QUALITY = os.environ.get("DOWNLOAD_QUALITY", EpisodeQuality.low)

if __name__ == "__main__":
    # Getting cli args from user
    cli_args = CliArguments(
        options=[
            "link",
            "quality",
            "start",
            "max",
            "download_dir",
        ]
    ).todict()

    # Intializing process
    scrapper = AnimeScrapper(
        download_folder=os.environ.get("DOWNLOADS_DIR", cli_args.get("download_dir")),
        wdpath=WDPATH,
        quality=cli_args.get("quality", QUALITY),
        link=cli_args.get("link", LINK),
        start_from=cli_args.get("start", 1),
        max_eps=cli_args.get("max", 1),
    )

    # Starting porcess
    scrapper.init()
