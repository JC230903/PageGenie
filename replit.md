# AI-Enhanced PDF Reader

## Overview

This is a Flask-based web application that transforms PDF documents into immersive, AI-enhanced digital reading experiences. The system extracts text from PDFs, performs AI-powered analysis to understand content themes and mood, and presents the content in an interactive book-style interface.

## Recent Changes (January 29, 2025)

✓ Successfully migrated from OpenAI to Google Gemini API integration
✓ Fixed database schema to support large base64 image storage (TEXT fields)
✓ Completed end-to-end PDF processing pipeline with real AI analysis
✓ Created comprehensive documentation (README.md and SETUP.md)
✓ Established GitHub integration guidelines and deployment instructions
✓ Application fully functional with both Gemini API and mock fallback responses

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

The application follows a three-tier architecture with asynchronous processing capabilities:

### Frontend Architecture
- **Technology**: Vanilla JavaScript with Bootstrap for UI components
- **Design Pattern**: Single Page Application (SPA) with server-side rendering for initial load
- **Key Features**: 
  - Interactive book reader with page-turning animations
  - Real-time progress tracking during PDF processing
  - Drag-and-drop file upload interface
  - Responsive design with dark theme

### Backend Architecture
- **Framework**: Flask with SQLAlchemy ORM
- **Database**: SQLite (configurable to PostgreSQL via DATABASE_URL)
- **Processing Pattern**: Synchronous processing (designed for asynchronous expansion)
- **File Handling**: Secure file uploads with timestamp-based naming

### AI Services Integration
- **Primary Provider**: Google Gemini API (when available)
- **Fallback**: Mock responses for development/testing
- **Capabilities**: Document analysis for genre, themes, and mood detection
- **Image Generation**: Gemini 2.0 Flash for marginalia artwork creation

## Key Components

### 1. PDF Processing Engine (`pdf_processor.py`)
- **Purpose**: Extract text content with coordinate information from PDF files
- **Technology**: PyMuPDF (fitz library)
- **Features**: 
  - Text extraction with positional data
  - Page dimension analysis
  - Structured text block parsing

### 2. AI Analysis Service (`ai_services.py`)
- **Purpose**: Analyze document content for thematic and emotional insights
- **Integration**: OpenAI API with graceful fallback
- **Analysis Types**:
  - Genre classification
  - Theme extraction
  - Overall mood assessment

### 3. Data Models (`models.py`)
- **ProcessingJob**: Tracks PDF processing status and progress
- **BookAnalysis**: Stores document-level analysis results
- **BookPage**: Contains page-specific content and analysis
- **Job Status Enum**: Manages processing states (pending, processing, completed, failed)

### 4. Web Interface
- **Upload Interface**: Clean, modern file upload with drag-and-drop
- **Book Reader**: Immersive reading experience with page navigation
- **Progress Tracking**: Real-time status updates during processing

## Data Flow

1. **Upload Phase**:
   - User uploads PDF via web interface
   - File is securely stored with unique filename
   - ProcessingJob record created in database

2. **Processing Phase**:
   - PDF text extraction with coordinate mapping
   - AI-powered content analysis
   - Results stored in database models

3. **Presentation Phase**:
   - Processed content retrieved from database
   - Interactive book interface rendered
   - Enhanced reading experience with AI insights

## External Dependencies

### Required Python Packages
- **Flask**: Web framework and routing
- **SQLAlchemy**: Database ORM and migrations
- **PyMuPDF**: PDF text extraction and processing
- **OpenAI**: AI analysis services (optional)

### Frontend Dependencies
- **Bootstrap**: UI framework and responsive design
- **Font Awesome**: Icon library
- **PDF.js**: Client-side PDF rendering (for reference views)

### Environment Variables
- `GEMINI_API_KEY`: Google Gemini API access (optional)
- `DATABASE_URL`: Database connection string
- `SESSION_SECRET`: Flask session security key

## Deployment Strategy

### Development Setup
- SQLite database for local development
- Flask development server with debug mode
- File-based uploads to local directory

### Production Considerations
- **Database**: Designed to work with PostgreSQL via DATABASE_URL
- **File Storage**: Local filesystem (expandable to cloud storage)
- **Security**: ProxyFix middleware for proper HTTPS handling
- **Scalability**: Architecture supports async task queue integration (Celery/Redis)

### Key Configuration
- Maximum file upload size: 16MB
- Database connection pooling enabled
- Automatic table creation via SQLAlchemy
- Secure filename handling for uploads

## Architecture Decisions

### Database Choice
- **Problem**: Need flexible data storage for development and production
- **Solution**: SQLAlchemy with configurable database backends
- **Rationale**: Allows SQLite for development, PostgreSQL for production

### AI Service Design
- **Problem**: Reliable AI analysis with graceful degradation
- **Solution**: OpenAI integration with mock fallbacks
- **Rationale**: Ensures application functionality regardless of API availability

### Processing Architecture
- **Problem**: PDF processing can be time-intensive
- **Solution**: Job-based processing with status tracking
- **Rationale**: Provides user feedback and enables async expansion

### Frontend Approach
- **Problem**: Need rich, interactive reading experience
- **Solution**: JavaScript-heavy frontend with server-side data
- **Rationale**: Balances interactivity with SEO and initial load performance