import logging
from pathlib import Path

import requests
import pandas as pd
from tqdm import tqdm

import re


def clean_summary(text: str) -> str:
    # Remove markdown-like formatting (**, *, etc.)
    text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)  # bold
    text = re.sub(r"\*(.*?)\*", r"\1", text)  # italic
    text = re.sub(r"`{1,3}(.*?)`{1,3}", r"\1", text)  # inline code
    text = re.sub(r"^[-*]\s+", "", text, flags=re.MULTILINE)  # bullet points

    # Remove newlines, tabs, and excessive whitespace
    text = re.sub(r"[\r\n\t]+", " ", text)
    text = re.sub(r"\s+", " ", text)

    # Trim final result
    return text.strip()


def make_request(url: str, api_key: str, logger: logging.Logger) -> str:
    payload = {
        "model": "sonar",
        "messages": [
            {
                "role": "system",
                "content": (
                    "Summarize the article using natural, human-like prose in a formal tone. "
                    "Do not use any markdown, formatting characters (like asterisks or underscores), or bullet points. "
                    "Do not include any newlines or line breaks. Return a single paragraph suitable for display in a CSV file."
                ),
            },
            {
                "role": "user",
                "content": f"Please read and summarize the article at '{url}'.",
            },
        ],
    }
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

    try:
        response = requests.post(
            "https://api.perplexity.ai/chat/completions", json=payload, headers=headers
        )
        response.raise_for_status()
        raw_summary = response.json()["choices"][0]["message"]["content"]
        return clean_summary(raw_summary)
    except Exception as e:
        logger.error(f"Error summarizing {url}: {str(e)}")
        return "ERROR: Failed to summarize."


def prompt_for_file(logger: logging.Logger) -> Path:
    input_dir = Path("input")
    input_dir.mkdir(exist_ok=True)
    while True:
        file_name = input(
            "Enter the name of the CSV input file (e.g., 'data.csv'): "
        ).strip()
        file_path = input_dir / file_name
        if file_path.exists():
            return file_path
        logger.error(f"File '{file_path}' not found. Please try again.")


def prompt_for_api_key() -> str:
    return input("Enter your Perplexity API key: ").strip()


def main():
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s"
    )
    logger = logging.getLogger(__name__)
    logger.info("Starting Perplexity summarization tool...")

    input_path = prompt_for_file(logger)
    api_key = prompt_for_api_key()

    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    output_path = output_dir / f"perplexity-summary-{input_path.stem}.csv"

    input_df = pd.read_csv(input_path)
    if not {"URL", "Title"}.issubset(input_df.columns):
        logger.error("Input CSV must contain 'URL' and 'Title' columns.")
        return

    output_data = []

    for _, row in tqdm(
        input_df.iterrows(), total=len(input_df), desc="Summarizing articles"
    ):
        url, title = row["URL"], row["Title"]
        summary = make_request(url, api_key, logger)
        output_data.append({"URL": url, "Title": title, "Summary": summary})

    pd.DataFrame(output_data).to_csv(output_path, index=False)
    logger.info(f"Summaries saved to '{output_path}'.")


if __name__ == "__main__":
    main()
