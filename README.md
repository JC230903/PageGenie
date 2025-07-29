# AI-Enhanced PDF Reader

Transform your PDF documents into immersive, AI-illustrated digital books with thematic marginalia artwork.

![AI-Enhanced PDF Reader](https://img.shields.io/badge/status-active-brightgreen)
![Python](https://img.shields.io/badge/python-3.11-blue)
![Flask](https://img.shields.io/badge/flask-latest-lightgrey)

## Features

- **PDF Text Extraction**: Advanced text extraction with coordinate mapping using PyMuPDF
- **AI Content Analysis**: Intelligent genre, theme, and mood detection using Google Gemini API
- **Thematic Marginalia**: AI-generated decorative artwork positioned in book margins
- **Immersive Reading Experience**: Beautiful book-style interface with page-turning animations
- **Real-time Processing**: Progress tracking during PDF analysis and enhancement
- **Responsive Design**: Works seamlessly on desktop and mobile devices

## Live Demo

The application processes PDFs and creates an interactive book reader experience:

1. Upload any PDF document
2. AI analyzes content for genre, themes, and emotional tone
3. Generates thematic artwork for margins
4. Presents content in an immersive book interface

## Quick Start

### Prerequisites

- Python 3.11+
- PostgreSQL database (or SQLite for development)
- Google Gemini API key (optional - falls back to high-quality mock responses)

### Installation & Setup

1. **Clone this repository**:
   ```bash
   git clone https://github.com/JC230903/PageGenie.git
   cd PageGenie
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   
   Or if using uv (recommended):
   ```bash
   uv sync
   ```

3. **Set up environment variables**:
   Create a `.env` file in the project root:
   ```env
   DATABASE_URL=postgresql://user:password@localhost/dbname
   GEMINI_API_KEY=your_gemini_api_key_here
   SESSION_SECRET=your_secret_key_for_sessions
   ```

4. **Initialize the database**:
   ```bash
   python -c "from app import app, db; app.app_context().push(); db.create_all()"
   ```

5. **Start the application**:
   ```bash
   gunicorn --bind 0.0.0.0:5000 --reuse-port --reload main:app
   ```

6. **Open your browser** and navigate to `http://localhost:5000`

### Alternative: Run on Replit

This project is optimized for Replit deployment:

1. Fork this repository to your GitHub account
2. Import it into Replit
3. Add your `GEMINI_API_KEY` to Replit Secrets
4. Click Run - the application will start automatically!

## Usage

### Uploading PDFs

1. Click "Choose PDF File" or drag and drop a PDF onto the upload area
2. Click "Upload and Process" to begin analysis
3. Wait for processing to complete (progress shown in real-time)
4. Enjoy your enhanced digital book!

### Supported PDF Types

- Text-based PDFs (not scanned images)
- Academic papers, novels, reports, documentation
- Maximum file size: 16MB
- Any length document (optimized for books and long-form content)

## Architecture

### Backend (Flask)
- **Framework**: Flask with SQLAlchemy ORM
- **Database**: PostgreSQL (production) / SQLite (development)
- **PDF Processing**: PyMuPDF for text extraction with coordinates
- **AI Integration**: Google Gemini API for content analysis and image generation

### Frontend (Vanilla JavaScript)
- **Styling**: Bootstrap with custom dark theme
- **Interactions**: Progressive enhancement with JavaScript
- **Reading Experience**: Custom book reader with page navigation
- **Responsive**: Mobile-first design approach

### Database Schema
- `ProcessingJob`: Tracks PDF processing status and progress
- `BookAnalysis`: Document-level analysis (genre, themes, mood)
- `BookPage`: Page-specific content and analysis
- `Marginalia`: AI-generated artwork with positioning data

## Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `DATABASE_URL` | PostgreSQL connection string | Yes |
| `GEMINI_API_KEY` | Google Gemini API key | No* |
| `SESSION_SECRET` | Flask session encryption key | Yes |

*Falls back to high-quality mock responses if not provided

### Google Gemini API Setup

1. Visit [Google AI Studio](https://aistudio.google.com/)
2. Create a new API key
3. Add the key to your environment variables
4. Restart the application

The application uses:
- **Gemini 2.5 Flash**: For content analysis (genre, themes, mood)
- **Gemini 2.0 Flash**: For marginalia image generation

## Development

### Local Development Setup

1. **Install development dependencies**:
   ```bash
   pip install -e .
   ```

2. **Enable debug mode**:
   ```bash
   export FLASK_ENV=development
   export FLASK_DEBUG=1
   ```

3. **Run with hot reload**:
   ```bash
   flask run --host=0.0.0.0 --port=5000 --debug
   ```

### Project Structure

```
ai-enhanced-pdf-reader/
├── app.py              # Flask application setup
├── main.py             # Application entry point
├── models.py           # Database models
├── routes.py           # Web routes and API endpoints
├── pdf_processor.py    # PDF text extraction logic
├── ai_services.py      # AI analysis and image generation
├── templates/          # Jinja2 templates
│   ├── index.html     # Upload interface
│   └── book_reader.html # Reading experience
├── static/            # CSS, JavaScript, images
│   ├── css/book-style.css
│   └── js/book-reader.js
└── uploads/           # Uploaded PDF storage
```

### Adding New Features

1. **Database Changes**: Update `models.py` and restart
2. **API Endpoints**: Add routes in `routes.py`
3. **Frontend**: Modify templates and static files
4. **AI Features**: Extend `ai_services.py`

## Deployment

### Replit (Recommended)

1. **Fork** this repository on GitHub
2. **Import** into Replit from GitHub
3. **Add secrets** in Replit sidebar:
   - `GEMINI_API_KEY`
   - `DATABASE_URL` (automatically provided)
   - `SESSION_SECRET` (generate a random string)
4. **Click Run** - automatic deployment!

### Manual Deployment

1. **Set up PostgreSQL database**
2. **Configure environment variables**
3. **Install dependencies**: `pip install -r requirements.txt`
4. **Initialize database**: Run database setup commands
5. **Start with Gunicorn**: `gunicorn main:app`

## Troubleshooting

### Common Issues

**PDF Upload Fails**
- Ensure file is under 16MB
- Check file is a valid PDF with text content
- Verify uploads/ directory exists and is writable

**AI Analysis Not Working**
- Check `GEMINI_API_KEY` is set correctly
- Verify internet connection for API calls
- Application falls back to mock responses automatically

**Database Errors**
- Ensure PostgreSQL is running and accessible
- Check `DATABASE_URL` format: `postgresql://user:pass@host:port/db`
- Run `db.create_all()` to initialize tables

### Logs and Debugging

Enable debug logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

Check application logs for detailed error information.

## Contributing

1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature-name`
3. **Commit** changes: `git commit -am 'Add feature'`
4. **Push** to branch: `git push origin feature-name`
5. **Submit** a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- **PyMuPDF** for robust PDF text extraction
- **Google Gemini** for AI-powered content analysis
- **Bootstrap** for responsive UI components
- **Flask** ecosystem for web framework
- **Replit** for seamless deployment platform

## Support

For issues and questions:
- Create an issue on GitHub
- Check the troubleshooting section above
- Review the application logs for error details

---

**Built with ❤️ for immersive reading experiences**