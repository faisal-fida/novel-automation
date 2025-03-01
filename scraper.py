import requests
from bs4 import BeautifulSoup
from typing import Dict, Optional


class NovelScraper:
    def __init__(self):
        self.headers = {"User-Agent": "Mozilla/5.0"}

    def get_page_content(self, url: str) -> Optional[str]:
        """Fetch and extract text content from a novel chapter page."""
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")
            paragraphs = soup.select("#chr-content p")

            return " ".join(p.get_text() for p in paragraphs)
        except requests.RequestException as e:
            print(f"Error fetching page: {e}")
            return None

    def extract_novel_info(self, url: str) -> Dict[str, any]:
        """Extract novel metadata from the novel's main page."""
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")

            title = soup.select_one(".title")
            title_text = title.text.strip() if title else "Title not found"

            genres = soup.select('ul.info li a[href^="https://novelbin.me/novelbin-genres/"]')
            genre_list = [genre.text.strip() for genre in genres]

            description = soup.select_one('.desc-text[itemprop="description"]')
            description_text = description.text.strip() if description else "Description not found"

            return {"title": title_text, "genres": genre_list, "description": description_text}
        except requests.RequestException as e:
            print(f"Error extracting novel info: {e}")
            return {}
