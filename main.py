import os
from dotenv import load_dotenv
from utils.scrapper import EpisodeQuality, AnimeScrapper
from utils.version import get_version_name
from cliopts import CliArguments, InvalidOptionError

# Setting up default options
load_dotenv()

LINK = os.environ.get(
    "ANIME_DOWNLOAD_LINK", "https://embtaku.pro/videos/one-piece-episode"
)
WDPATH = os.environ.get("WEBDRIVER_PATH", "./chromediver.exe")
QUALITY = os.environ.get("DOWNLOAD_QUALITY", EpisodeQuality.low)

if __name__ == "__main__":
    try:
        # Getting cli args from user
        cli_args = CliArguments(
            name="anime-scrapper",
            options_desc={
                "link": "URL link to the anime series or episodes. The default anime is 'One Piece'.",
                "quality": "Desired video quality for the episodes. 360p, 480p, 720p, or 1080p]. Defaults to '480p'.",
                "start": "The episode number to start processing from. Defaults to 1.",
                "max": "The number of episodes to process. Defaults to 1.",
                "downloads_dir": "Directory for saving downloaded episodes. If None, it will save to the default location.",
                "verbose": "Flag to enable detailed logging output. Defaults to False.",
            },
            options=[
                "link",
                "quality",
                "start",
                "max",
                "downloads_dir",
                "verbose",
            ],
            version=get_version_name(),
            throw_on_invalid_args=True,
        )

        parsed_args = cli_args.to_dict()
        print(parsed_args)

        # Intializing process
        scrapper = AnimeScrapper(
            
            download_folder=os.environ.get(
                "DOWNLOADS_DIR", parsed_args.get("download_dir")
            ),
            wdpath=WDPATH,
            quality=parsed_args.get("quality", QUALITY),
            link=parsed_args.get("link", LINK),
            start_from=parsed_args.get("start", 1),
            max_eps=parsed_args.get("max", 1),
            verbose=parsed_args.get("verbose", False),
        )

        # Starting porcess
        scrapper.init()

    except InvalidOptionError as e:
        print(
            "Invalid option provided.\nPlease check the documentation at https://github.com/Sanmeet007/anime-scrapper or use --help for assistance"
        )
