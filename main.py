from scraper import NovelScraper
from translator import Translator
import json
import os
from dotenv import load_dotenv
from typing import Dict
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def load_env():
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("API key not found in environment variables")
    return api_key


def process_novel_chapter(scraper: NovelScraper, translator: Translator, url: str) -> str:
    """Scrape and translate a novel chapter."""
    try:
        chapter_text = scraper.get_page_content(url)
        if not chapter_text:
            logger.error("Failed to fetch chapter content")
            return ""

        translation = translator.translate_to_french(chapter_text)
        return translation.get("translated_text", "")
    except Exception as e:
        logger.error(f"Error processing chapter: {e}")
        return ""


def get_novel_metadata(scraper: NovelScraper, url: str) -> Dict:
    """Fetch novel metadata."""
    try:
        novel_info = scraper.extract_novel_info(url)
        logger.info("Successfully fetched novel metadata")
        return novel_info
    except Exception as e:
        logger.error(f"Error fetching novel metadata: {e}")
        return {}


def main():
    # Load API key
    GEMINI_API_KEY = load_env()

    # Initialize components
    scraper = NovelScraper()
    translator = Translator(api_key=GEMINI_API_KEY)

    # Example URLs
    chapter_url = "https://novelbin.com/b/unrivaled-medicine-god/chapter-2"
    novel_url = "https://novelbin.me/novel-book/extras-death-i-am-the-son-of-hades"

    # Process chapter
    translated_text = process_novel_chapter(scraper, translator, chapter_url)
    if translated_text:
        logger.info("Successfully translated chapter")
        print("Translated text:", translated_text[:200] + "...")  # Preview first 200 chars

    # Get novel information
    novel_info = get_novel_metadata(scraper, novel_url)
    if novel_info:
        print("\nNovel Information:")
        print(json.dumps(novel_info, indent=2))

    # Save to file
    if translated_text and novel_info:
        import csv

        with open("translated_chapter.csv", "w", newline="") as csvfile:
            fieldnames = ["novel_title", "chapter_title", "chapter_text"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow(
                {
                    "novel_title": novel_info.get("title"),
                    "chapter_title": "Chapter 2",
                    "chapter_text": translated_text,
                }
            )


if __name__ == "__main__":
    main()
