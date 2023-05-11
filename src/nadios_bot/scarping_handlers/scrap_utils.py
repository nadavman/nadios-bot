from bs4 import BeautifulSoup
import requests

beautifulsoup_parser = "html.parser"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
}


def get_data_from_url(url: str) -> BeautifulSoup:
    result = requests.get(url, headers=headers)
    return BeautifulSoup(result.text, beautifulsoup_parser)
