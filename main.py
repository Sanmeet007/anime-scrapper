import time, cloudscraper, lxml, sys
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging

#####################################################


WEBDRIVER_PATH = "C:\chromedriver\chromedriver.exe"
MAX_EPISODES = 3
START_FROM = 1
FILE = "file.txt"
DEFAULT_LINK = "https://gogoplay1.com/videos/spy-x-family-dub-episode"
DOWNLOAD_URLS_FILE = "download.txt"
HTML_FILE = "index.html"
WAIT_TIME = 60  # in seconds
LOAD_GUESS = 3  # in seconds
QUAILTY = {
    "360p": 0,
    "480p": 1,
    "720p": 2,
    "1080p": 3,
}
SHOULD_PARSE = True

LINK = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_LINK
# Get quality
CURRENT_QUALITY = sys.argv[2] if len(sys.argv) > 2 else "720p"
if CURRENT_QUALITY not in QUAILTY:
    raise Exception("Invalid quailty !")

START_FROM = int(sys.argv[3]) if len(sys.argv) > 3 else START_FROM
MAX_EPISODES = int(sys.argv[4]) if len(sys.argv) > 4 else MAX_EPISODES
SHOULD_PARSE = eval(sys.argv[5]) if len(sys.argv) > 5 else SHOULD_PARSE

# Driver options
options = webdriver.ChromeOptions()
prefs = {"download.default_directory": "H:\downloads"}
options.add_experimental_option("prefs", prefs)
options.add_argument("--window-size=1100,1000")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)


#  Logger
logging.basicConfig(
    filename="anime_log.log",
    filemode="a+",
    level=logging.INFO,
    format="[%(levelname)s] :: %(asctime)-18s :: %(message)s",
    datefmt="%Y-%m-%d|%I:%M%p",
)
logger = logging.getLogger(__name__)


# Scrapper
scraper = cloudscraper.create_scraper()

# Functions
def parse_html():
    with open(FILE, "w+") as f:
        for index, _ in enumerate(range(MAX_EPISODES), start=1):
            contents = scraper.get(f"{LINK}-{START_FROM+ index - 1}").text
            html = BeautifulSoup(markup=contents, features="lxml")
            iframe = html.select_one(selector="iframe")
            src = iframe.get("src")
            src = "https:" + src.replace("streaming.php", "download")
            f.write(f"{src}\n")
            print(f"{'Parsing : ':10} {index/MAX_EPISODES:.1%}", end="\r")
            time.sleep(0.5)
    print("Links parsed successfully")


def chunks(f):
    while True:
        line = f.readline()
        if line != "":
            yield line
        else:
            break


def file_write(content):
    with open(HTML_FILE, "w") as f:
        f.write("" + content.encode("utf8"))


def log_download_url(url):
    with open(DOWNLOAD_URLS_FILE, "a+") as f:
        f.write(f"{url} \n")


def download_links():
    with open(DOWNLOAD_URLS_FILE, "w"):
        pass

    error = False

    with open(FILE, "r") as f:
        for chunk in chunks(f):
            browser.get(chunk)
            try:
                time.sleep(LOAD_GUESS)
                element = WebDriverWait(browser, WAIT_TIME).until(
                    EC.presence_of_element_located((By.ID, "content-download"))
                )
                mirror_links_one = element.find_elements(
                    by=By.CLASS_NAME, value="mirror_link"
                )[0]
                download_links = mirror_links_one.find_elements(
                    by=By.CLASS_NAME, value="dowload"
                )
                link = download_links[CURRENT_QUALITY].find_element(
                    by=By.TAG_NAME, value="a"
                )
                link.click()
                log_download_url(link.get_attribute("href"))

            except Exception as E:
                print("There was an error please check log for details")
                error = True
                # browser.quit()
                logger.error(E)
    # browser.quit() if not error else print("There was an error getting elements.")

    print("Please quit browser when downloading is complete")


if __name__ == "__main__":
    parse_html() if SHOULD_PARSE else None
    browser = webdriver.Chrome(service=Service(WEBDRIVER_PATH), options=options)
    browser.execute_cdp_cmd(
        "Network.setUserAgentOverride",
        {
            "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.53 Safari/537.36"
        },
    )
    browser.get("http://www.google.com/")
    browser.find_element_by_tag_name("body").send_keys(Keys.COMMAND + "t")
    download_links()
