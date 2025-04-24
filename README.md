# Summarize

A command‑line tool that uses the Perplexity Chat Completion API to generate concise, single‑paragraph summaries of articles listed in a CSV file.


## Prerequisites

Before you begin, ensure you have the following installed:

-	[Python 3.12+](https://www.python.org/downloads/release/python-31210/)
-	[Poetry](https://python-poetry.org/docs/#installing-with-the-official-installer)
-	A [Perplexity API key](https://www.perplexity.ai/account/api) (available from your Perplexity account)


## Installation

1.	Clone the repository

```bash
git clone git@github.com:simon-lentz/summarize.git
```

2. Navigate to the summarize directory

```bash
cd summarize
```

3. Install the summarize tool and its dependencies

```bash
poetry install
```

## Usage

To run the summarization tool:

```bash
poetry run summarize
```

You will be prompted for:

- **Input CSV filename** (located in the `input/` directory).
- **Perplexity API key** (paste your key when prompted).

Once complete, summaries are written to `output/perplexity-summary-<input_stem>.csv`

## Exporting links with Session Buddy

If you use the Session Buddy Chrome extension to collect links:

- Open Session Buddy and select the tabs you wish to summarize.
- Click Export → CSV and save the file directly into input/.
- Use the exported filename when prompted by the summarize program.

