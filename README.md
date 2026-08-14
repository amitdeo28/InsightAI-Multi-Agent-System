# InsightAI

InsightAI is a multi-agent research assistant that turns a topic into a structured, source-informed research brief. It uses specialized agents to discover information, read a relevant source, write a report, and review the finished result.

## Features

- Web research powered by Tavily
- Source reading and content extraction
- AI-generated, structured research briefs
- Editorial review with strengths, improvement areas, and a score
- Downloadable Markdown reports
- Dark Streamlit interface

## Research workflow

1. **Scout sources** - finds recent and reliable information for the topic.
2. **Read deeply** - selects and scrapes a relevant source for additional context.
3. **Shape the brief** - creates a detailed report from the gathered research.
4. **Editorial review** - evaluates the report and suggests improvements.

## Requirements

- Python 3.10 or newer
- A [Mistral API key](https://console.mistral.ai/)
- A [Tavily API key](https://tavily.com/)

## Local setup

Clone or download this project, then open a terminal in the project directory.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pip install streamlit
```

Create a `.env` file in the project root:

```env
MISTRAL_API_KEY=your_mistral_api_key
TAVILY_API_KEY=your_tavily_api_key
```

Start the application:

```powershell
streamlit run app.py
```

Open the local address displayed in the terminal, usually `http://localhost:8501`.

## Project structure

```text
.
├── app.py           # Streamlit user interface
├── agents.py        # Search, reader, writer, and critic agents
├── tools.py         # Tavily search and web-scraping tools
├── pipeline.py      # Command-line version of the research workflow
├── requirements.txt # Python dependencies
└── .env             # Local API keys (do not commit)
```

## Deploy to Streamlit Community Cloud

1. Add `streamlit>=1.36.0` to `requirements.txt`.
2. Push the project to a GitHub repository. Do **not** commit `.env`.
3. In Streamlit Community Cloud, select **Create app** and choose your repository, branch, and `app.py` as the entry point.
4. Open **Advanced settings → Secrets** and add:

   ```toml
   MISTRAL_API_KEY = "your_mistral_api_key"
   TAVILY_API_KEY = "your_tavily_api_key"
   ```

5. Click **Deploy**.

## Security note

Keep API keys private. Add the following entries to `.gitignore` before pushing the project to GitHub:

```gitignore
.env
.streamlit/secrets.toml
.venv/
__pycache__/
```

## Run from the command line

You can also run the non-UI pipeline:

```powershell
python pipeline.py
```

Enter a research topic when prompted. The final report and editorial feedback will be printed in the terminal.
