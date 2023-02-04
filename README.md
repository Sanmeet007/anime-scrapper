# Anime scrapper

Clean anime scrapper & downloader made using selenium automation.

![AS](https://i.ibb.co/G0ZJkmp/poster.png)

Bulk download your favourite anime episodes from gogoanime website all you need to do is setup some environment variables (basically options for downloading) and use the CLI.

Sample usage :

```bash
py main.py --link="LINK" --quality="QUALITY" --start="START" --max="MAX"
```

## Quick Setup

Before you begin to automate your favourite anime downloading you need to install the required dependencies.

### 1. Cloning the repo

The first step would be to clone the repo.

### 2. Getting Dependencies

- `ChromeDriver.exe` : Required by selenium to control chrome browser.
- `Modules` :
  - Selenium : Core for automation.
  - Cloudscrapper : For getting html.
  - BeautifulSoup : Used for scrapping.
  - Python Dotenv : For loading env.

Chrome diver download link : [Official download link](https://chromedriver.chromium.org/downloads)

> You need to download the exact version of chromedriver as your chrome browser. For checking the version of your chrome browser , you can type `chrome://version/` in search bar and hit enter to check the version.

### 3. Installing packages

All packages are listed in the requirements.txt all you need to so is run this simple command :

```bash
pip install -r requirements.txt
```

> This command recursively downloads the required python packages and install them.

```txt
Dev tip : Use a virtual environment to prevent making the packages global which might cause conflicts !
```

### 3. Setting up environment variables

After successfully installing chrome driver and python packages , you need to setup some environment variables to get things ready to be in action. You can do so by filling up required envs values in `.env` file.

Environment vars :

- `WEBDRIVER_PATH` : Requires the absolute path of chromedriver.exe file you downloaded.
- `DOWNLOAD_DIRECTORY` : Sets the default download directory path to which the downloads will be stored.
- `ANIME_DOWNLOAD_LINK` : Sets the anime download link.
- `DOWNLOAD_QUALITY` : Sets the quality.

> You need to get the link for `ANIME_DOWNLOAD_LINK` from the `gogo-play.tv` website in an exact pattern like : <https://playgo1.cc/videos/one-piece-dub-episode>

> Accepted values for `DOWNLOAD_QUALITY` are 420p , 720p, 360p & 1080p.

Sample of a .env file :

```.env
WEBDRIVER_PATH = "C:\chromedriver\chromedriver.exe"
DOWNLOAD_DIRECTORY = "D:\Anime\One-Piece"
ANIME_DOWNLOAD_LINK = "https://playgo1.cc/videos/one-piece-dub-episode"
DOWNLOAD_QUALITY = "720p"
```

### 4. Downloading

You need to run these following commands which are basically flags .

#### Flags

- `link` : Used to replace the original `ANIME_DOWNLOAD_LINK` if present in .env file with the param passed in cli.
- `start` : Sets the episode from which the loop starts.
- `max` : Sets the maximum episodes to download . Basically helps in creating a range from start till start + max


##### Usage

Without shorthand args

```bash
py main.py --link="https://playgo1.cc/videos/gintama-episode" --quality="720p" --start=1 --max=10 --downloads_dir="C:/User/Downloads"
```

With shorthand args

```bash
py main.py -l "LINK" -q "QUALITY" -s "START" -m "MAX" -d "DOWNLOADS_DIR"
```

## Developer Contact

If any queries feel to get in touch with me .
<br>
Email : ssanmeet123@gmail.com

HAPPY ANIME WATCHING :-)
