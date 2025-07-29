# Setup Guide for AI-Enhanced PDF Reader

## GitHub Integration Steps

### 1. Create GitHub Repository

1. **Your GitHub Repository is Ready**:
   - Repository: https://github.com/JC230903/PageGenie
   - Description: "AI-Enhanced PDF Reader with thematic marginalia generation"
   - This will be your main project repository

### 2. Connect Your Replit to GitHub

1. **In Replit**, click the version control icon (Git) in the sidebar
2. **Click "Create a Git repo"** if not already done
3. **Add remote**: Use this command in the Replit shell:
   ```bash
   git remote add origin https://github.com/JC230903/PageGenie.git
   ```
4. **Set up authentication** (if needed):
   - Use GitHub Personal Access Token
   - Or connect your GitHub account in Replit settings

### 3. Initial Push to GitHub

```bash
# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: AI-Enhanced PDF Reader with Gemini integration"

# Push to GitHub
git push -u origin main
```

### 4. Required Dependencies

When someone clones your project, they need these Python packages:
```
Flask==3.1.0
Flask-SQLAlchemy==3.1.1  
SQLAlchemy==2.0.36
PyMuPDF==1.25.2
google-genai==0.8.2
psycopg2-binary==2.9.10
gunicorn==23.0.0
Werkzeug==3.1.3
email-validator==2.2.0
python-multipart==0.0.19
reportlab==4.4.3
Pillow==11.3.0
```

## Running the Project

### On Replit (Easiest)

1. **Fork/Clone** the repository to Replit
2. **Add Secrets** in Replit sidebar:
   - `GEMINI_API_KEY`: Your Google Gemini API key
   - `DATABASE_URL`: Automatically provided by Replit
   - `SESSION_SECRET`: Any random string (e.g., "your-secret-key-123")
3. **Click Run** - Replit handles everything automatically!

### Local Development

1. **Clone the repository**:
   ```bash
   git clone https://github.com/YOUR_USERNAME/ai-enhanced-pdf-reader.git
   cd ai-enhanced-pdf-reader
   ```

2. **Install Python 3.11+** if not already installed

3. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. **Install dependencies**:
   ```bash
   pip install Flask Flask-SQLAlchemy PyMuPDF google-genai psycopg2-binary gunicorn Werkzeug email-validator python-multipart reportlab Pillow
   ```

5. **Set environment variables**:
   ```bash
   export DATABASE_URL="sqlite:///app.db"  # For local development
   export GEMINI_API_KEY="your-api-key-here"
   export SESSION_SECRET="your-secret-key"
   ```

6. **Initialize database**:
   ```bash
   python -c "from app import app, db; app.app_context().push(); db.create_all()"
   ```

7. **Run the application**:
   ```bash
   gunicorn --bind 0.0.0.0:5000 --reuse-port --reload main:app
   ```

8. **Open browser** to `http://localhost:5000`

## Getting Gemini API Key

1. **Visit Google AI Studio**: https://aistudio.google.com/
2. **Create an account** or sign in
3. **Generate API key** in the API section
4. **Copy the key** and add it to your environment

Note: The application works with mock responses if no API key is provided, so you can test it immediately!

## Project Features Working

✅ **PDF Upload & Processing** - Upload any PDF up to 16MB  
✅ **Text Extraction** - Advanced text extraction with PyMuPDF  
✅ **AI Content Analysis** - Genre, theme, and mood detection  
✅ **Marginalia Generation** - AI-created thematic artwork  
✅ **Book Reader Interface** - Immersive reading experience  
✅ **Progress Tracking** - Real-time processing status  
✅ **Database Storage** - PostgreSQL with automatic setup  
✅ **Responsive Design** - Works on all devices  

## File Structure

```
ai-enhanced-pdf-reader/
├── README.md           # Main documentation
├── SETUP.md           # This setup guide
├── .gitignore         # Git ignore rules
├── app.py             # Flask app configuration
├── main.py            # Application entry point
├── models.py          # Database models
├── routes.py          # Web routes and API
├── pdf_processor.py   # PDF text extraction
├── ai_services.py     # AI analysis and generation
├── templates/         # HTML templates
├── static/           # CSS and JavaScript
└── uploads/          # PDF file storage
```

## Troubleshooting

**Can't push to GitHub?**
- Check your GitHub username and repository name
- Ensure you have push permissions
- Try using a Personal Access Token instead of password

**Application won't start?**
- Check all environment variables are set
- Ensure database is accessible
- Look at console logs for specific errors

**PDF processing fails?**
- Ensure file is under 16MB
- Check it's a text-based PDF (not scanned image)
- Verify uploads/ directory exists

## Next Steps

1. **Test the application** with various PDF files
2. **Add your Gemini API key** for real AI analysis
3. **Customize the styling** in static/css/book-style.css
4. **Add new features** like user accounts or sharing
5. **Deploy to production** when ready

---

Your AI-Enhanced PDF Reader is ready to transform documents into immersive digital experiences!