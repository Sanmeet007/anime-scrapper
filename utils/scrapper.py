import colorama
from tqdm import tqdm
import sys
import time
import cloudscraper
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class EpisodeQuality:
    poor = "360p"
    low = "480p"
    mid = "720p"
    high = "1080p"


class AnimeScrapper:

    AVAILABLE_QUALITIES = {
        "360p": 0,
        "480p": 1,
        "720p": 2,
        "1080p": 3,
    }

    WAIT_TIME = 60  # in seconds
    LOAD_GUESS = 5  # in seconds

    VLINKS_FILE = "vlinks.txt"
    DLINKS_FILE = "dlinks.txt"

    def __init__(
        self,
        wdpath: str = None,
        max_eps: int = 1,
        start_from: int = 1,
        quality: str = EpisodeQuality.low,
        link: str = "",
        logfile: str = "anime_scrapper.log",
        download_folder=None,
        verbose=False,
    ) -> None:
        """_summary_

        Args:
            wdpath (str, optional): _description_. Defaults to None.
            max_eps (int, optional): _description_. Defaults to 1.
            start_from (int, optional): _description_. Defaults to 1.
            quality (str, optional): _description_. Defaults to "480p".
            link (str, optional): _description_. Defaults to "".
            logfile (str, optional): _description_. Defaults to "anime_scrapper.log".
            download_folder (str, optional): _description_. Defaults to None.
            verbose (bool, optional): _description_. Defaults to False.
        """

        if quality not in AnimeScrapper.AVAILABLE_QUALITIES:
            print("Invalid quailty -> Swithing to default 480p quality")
            quality = "480p"

        # Initalizing scrapper opts
        self.ANIME_LINK = link
        self.MAX_EPISODES = max_eps
        self.START_FROM = start_from
        self.QUAILTY = AnimeScrapper.AVAILABLE_QUALITIES[quality]
        self.__degbugging = verbose
        self.__wdpath = wdpath
        self.__download_folder = download_folder
        self.bar = None

        # Setting links
        self.__vlinks, self.__dlinks = [], []

        # Enabling debugger
        if self.__degbugging == True:
            print(AnimeScrapper.coloredgrey("------------------------"))
            print(AnimeScrapper.coloredgrey("| Enabled Debugging mode |"))
            print(AnimeScrapper.coloredgrey("------------------------"))
            print("")
            self.__enable_debugger(logfile=logfile)

    def init(self) -> None:
        self.__init_scrapper()
        return

    @staticmethod
    def coloredinfo(string: str):
        return colorama.Fore.BLUE + f"{'[INFO]':9}" + colorama.Fore.RESET + string

    @staticmethod
    def colorederror(string: str, level: str = "ERROR"):
        level = "[" + level
        level += "]"
        return colorama.Fore.RED + f"{level:9}" + colorama.Fore.RESET + string

    @staticmethod
    def coloredsuccess(string: str, level: str = "DONE"):
        level = "[" + level
        level += "]"
        return colorama.Fore.GREEN + f"{level:9}" + colorama.Fore.RESET + string

    @staticmethod
    def coloredgrey(string: str):
        return colorama.Fore.LIGHTBLACK_EX + string + colorama.Fore.RESET

    def __init_scrapper(self):
        try:
            # Start prompt
            colorama.Fore.RESET
            print(AnimeScrapper.coloredinfo("Starting process"))

            # Parsing
            self.__parse()

            # Opening browser
            self.browser = webdriver.Chrome(
                service_log_path=None,
                service=Service(self.__wdpath),
                options=self.__getwdopts(),
            )
            self.browser.execute_cdp_cmd(
                "Network.setUserAgentOverride",
                {
                    "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.53 Safari/537.36"
                },
            )
            self.browser.get("http://www.google.com/")
            self.browser.find_element(by=By.TAG_NAME, value="body").send_keys(
                Keys.CONTROL + "t"
            )

            # Downloading
            self.__download()

        except KeyboardInterrupt:
            if self.bar:
                self.bar.close()
            print(AnimeScrapper.coloredgrey("\n**************************************"))
            print(AnimeScrapper.coloredinfo("Ending process"))
            sys.exit()

        except Exception as E:
            if self.__degbugging:
                self.__logger.error(E)

            print(AnimeScrapper.colorederror("*Process exited due to an error."))
            sys.exit()

    def __getwdopts(self):
        options = webdriver.ChromeOptions()
        prefs = {"download.default_directory": self.__download_folder}
        options.add_experimental_option("prefs", prefs)
        if self.__degbugging:
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
        else:
            options.add_experimental_option(
                "excludeSwitches", ["enable-automation", "enable-logging"]
            )

        options.add_experimental_option("useAutomationExtension", False)
        return options

    def __enable_debugger(self, logfile=None) -> None:
        import logging

        logging.basicConfig(
            filename="anime_scrapper.log" if logfile is None else logfile,
            filemode="a+",
            level=logging.INFO,
            format="[%(levelname)s] :: %(asctime)-18s :: %(message)s",
            datefmt="%Y-%m-%d|%I:%M%p",
        )
        self.__logger = logging.getLogger(__name__)

    def __parse(self) -> list[str]:
        try:
            scraper = cloudscraper.create_scraper()
            print(AnimeScrapper.coloredinfo("Parsing"))
            self.bar = tqdm(
                total=100, desc=AnimeScrapper.coloredinfo("Progress "), colour="green"
            )

            for index, _ in enumerate(range(self.MAX_EPISODES), start=1):
                contents = scraper.get(
                    f"{self.ANIME_LINK}-{self.START_FROM+ index - 1}"
                ).text
                html = BeautifulSoup(markup=contents, features="lxml")
                iframe = html.select_one(selector="iframe")
                src = iframe.get("src")
                src = "https:" + src.replace("streaming.php", "download")
                self.__vlinks.append(src)
                self.bar.update(100 / self.MAX_EPISODES)
                time.sleep(0.5)

            self.bar.close()
            print(AnimeScrapper.coloredsuccess("Links parsed successfully"))
            print(
                AnimeScrapper.coloredgrey("\n***********  DOWNLOADING  ************\n")
            )

            if self.__degbugging:
                with open(AnimeScrapper.VLINKS_FILE, "w") as f:
                    f.write("\n".join(self.__vlinks))

        except Exception as E:
            self.bar.close()
            print(AnimeScrapper.colorederror("Parser Error :"))
            print(
                AnimeScrapper.coloredgrey(
                    f"{'':9}An error occured while parsing !\n"
                    f"{'':9}It might be due to unstable internet connection.\n"
                    f"{'':9}You may try using vpn in case error persits."
                )
            )
            print("")
            sys.exit()

    def __download(self) -> None:
        for vlink in self.__vlinks:
            self.browser.get(vlink)
            try:
                time.sleep(AnimeScrapper.LOAD_GUESS)

                self.browser.execute_script(
                    """return document.querySelector("#content-download").querySelectorAll(".mirror_link > .dowload a")[%s].click()
                """
                    % self.QUAILTY
                )

                link = self.browser.execute_script(
                    """return document.querySelector("#content-download").querySelectorAll(".mirror_link > .dowload a")[%s].href
                """
                    % self.QUAILTY
                )

                self.__dlinks.append(link)
                print(AnimeScrapper.coloredsuccess("Downloading - %s" % (vlink)))

            except Exception as E:
                print(
                    AnimeScrapper.colorederror(
                        "Error downloading episode - %s" % (vlink)
                    )
                )

                if self.__degbugging:
                    print(AnimeScrapper.coloredinfo("Please check log for details !"))
                    self.__logger.error(E)

        if self.__degbugging:
            with open(AnimeScrapper.DLINKS_FILE, "w") as f:
                f.write("\n".join(self.__dlinks))

        print(
            "\n"
            + AnimeScrapper.coloredsuccess(
                "Please quit browser when downloading is complete"
            )
        )

        # An infinte loop to keep the window opened
        while 1:
            pass
