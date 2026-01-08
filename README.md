# Personal Task Automation Agent 🤖

A complete AI-powered automation agent with natural language task execution, resume analysis, and job matching capabilities. Built with Python, FastAPI, Streamlit, and OpenAI.

## 🌟 Features

### Task Automation
- **Natural Language Commands** - Execute complex tasks with simple English instructions
- **Multi-Step Planning** - AI-powered (GPT-4) or rule-based task planning
- **Web Search** - Real-time search using SerpAPI with Google results
- **Web Scraping** - JavaScript-capable scraping with Playwright
- **Content Summarization** - AI-powered summaries using OpenAI
- **Email Notifications** - Send results via SMTP with clickable HTML links
- **Execution Logging** - Complete task history and logs

### Resume Analysis & Job Matching
- **Resume Parser** - Extract text from PDF, DOCX, and TXT files
- **OCR Support** - Handle scanned PDFs with Tesseract OCR
- **AI Analysis** - Intelligent resume analysis with skill extraction
- **Job Matching** - Automatic job search based on resume analysis
- **Multi-format Support** - Works with various document formats

### User Interface
- **Streamlit GUI** - Modern web interface for all features
- **FastAPI Backend** - RESTful API for programmatic access
- **Real-time Updates** - Live execution progress and results
- **Task History** - View and manage previous executions

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Git
- Tesseract OCR (for scanned PDF support)
- Poppler (for PDF processing)

### Installation

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd Project
```

2. **Create virtual environment**
```bash
python -m venv .venv
.venv\Scripts\Activate.ps1  # Windows
source .venv/bin/activate    # Linux/Mac
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment**
```bash
cp .env.example .env
```

Edit `.env` with your API keys:
```env
OPENAI_API_KEY=your_openai_key
SERPAPI_KEY=your_serpapi_key
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=your_app_password
DEFAULT_FROM=your_email@gmail.com
```

### Running the Application

**Streamlit GUI (Recommended)**
```bash
streamlit run src/app_gui.py
```
Open http://localhost:8501

**FastAPI Backend**
```bash
uvicorn src.main:app --reload --port 8000
```
API docs at http://localhost:8000/docs

## 📖 Usage Examples

### Task Execution
```
"Search for latest AI news and email me a summary"
"Find Python developer jobs in remote and send results to my email"
"Scrape data from example.com and summarize the content"
```

### Resume Analysis
1. Upload your resume (PDF/DOCX/TXT)
2. Click "Analyze Resume"
3. View extracted skills, experience, and career interests
4. Search for matching jobs automatically

## 🏗️ Project Structure

```
Project/
├── src/
│   ├── agent/              # Core agent logic
│   │   ├── planner.py      # Rule-based planner
│   │   ├── planner_llm.py  # LLM-based planner
│   │   ├── controller.py   # Task execution controller
│   │   └── memory.py       # Context management
│   ├── tools/              # Modular tool system
│   │   ├── search_tool_enhanced.py
│   │   ├── scraper_tool_enhanced.py
│   │   ├── summarizer_tool.py
│   │   ├── email_tool.py
│   │   ├── resume_parser_tool.py
│   │   ├── resume_analyzer_tool.py
│   │   └── job_matcher_tool.py
│   ├── app_gui.py          # Streamlit GUI
│   └── main.py             # FastAPI application
├── tests/                  # Unit and integration tests
├── .github/workflows/      # CI/CD pipelines
├── Dockerfile              # Container configuration
├── docker-compose.yml      # Multi-container setup
└── requirements.txt        # Python dependencies
```

## 🛠️ Technology Stack

- **Backend**: Python 3.10+, FastAPI, asyncio
- **Frontend**: Streamlit
- **AI/ML**: OpenAI GPT-4, sentence-transformers
- **Search**: SerpAPI, Google Custom Search
- **Scraping**: Playwright (JavaScript support)
- **OCR**: Tesseract, pdf2image
- **Document Parsing**: PyPDF2, python-docx
- **Testing**: pytest, pytest-asyncio
- **CI/CD**: GitHub Actions
- **Deployment**: Docker, Docker Compose

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENAI_API_KEY` | OpenAI API key for AI features | Yes |
| `SERPAPI_KEY` | SerpAPI key for web search | Yes |
| `SMTP_HOST` | SMTP server hostname | For email |
| `SMTP_PORT` | SMTP server port | For email |
| `SMTP_USER` | SMTP username | For email |
| `SMTP_PASSWORD` | SMTP password | For email |
| `PLANNER_MODE` | `rule` or `llm` | Optional |
| `SCRAPER_MODE` | `playwright` or `basic` | Optional |

## 🚢 Deployment

### Docker
```bash
docker-compose up -d
```

### Streamlit Cloud
1. Push to GitHub
2. Connect repository to Streamlit Cloud
3. Add environment variables in dashboard
4. Deploy

### Render/Railway
1. Create new web service
2. Connect GitHub repository
3. Set environment variables
4. Deploy with `streamlit run src/app_gui.py`

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src tests/

# Run specific test
pytest tests/test_agent.py
```

## 📝 API Documentation

### POST /run
Execute a natural language task

**Request:**
```json
{
  "command": "Search for AI news and email results",
  "email": "user@example.com"
}
```

**Response:**
```json
{
  "success": true,
  "plan": {...},
  "logs": [...],
  "timestamp": "2025-11-18T..."
}
```

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📄 License

MIT License - see LICENSE file for details

## 🙏 Acknowledgments

- OpenAI for GPT models
- SerpAPI for search capabilities
- Streamlit for the amazing UI framework
- All open-source contributors

## 📧 Support

For issues and questions, please open a GitHub issue or contact the maintainers.
