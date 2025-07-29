from app import db
from datetime import datetime
from enum import Enum
import json

class JobStatus(Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class ProcessingJob(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(500), nullable=False)
    status = db.Column(db.Enum(JobStatus), default=JobStatus.PENDING, nullable=False)
    progress = db.Column(db.Integer, default=0)  # 0-100
    error_message = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    
    # Relationships
    pages = db.relationship('BookPage', backref='job', lazy=True, cascade='all, delete-orphan')
    analysis = db.relationship('BookAnalysis', backref='job', uselist=False, cascade='all, delete-orphan')

class BookAnalysis(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey('processing_job.id'), nullable=False)
    genre = db.Column(db.String(100))
    themes = db.Column(db.Text)  # JSON string of themes
    overall_mood = db.Column(db.String(50))
    total_pages = db.Column(db.Integer)
    title = db.Column(db.String(500))
    
    def get_themes_list(self):
        if self.themes:
            return json.loads(self.themes)
        return []
    
    def set_themes_list(self, themes_list):
        self.themes = json.dumps(themes_list)

class BookPage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey('processing_job.id'), nullable=False)
    page_number = db.Column(db.Integer, nullable=False)
    text_content = db.Column(db.Text)
    text_blocks = db.Column(db.Text)  # JSON string of text blocks with coordinates
    mood = db.Column(db.String(50))
    dominant_themes = db.Column(db.Text)  # JSON string of themes for this page
    
    # Relationships
    marginalia = db.relationship('Marginalia', backref='page', lazy=True, cascade='all, delete-orphan')
    
    def get_text_blocks_list(self):
        if self.text_blocks:
            return json.loads(self.text_blocks)
        return []
    
    def set_text_blocks_list(self, blocks_list):
        self.text_blocks = json.dumps(blocks_list)
    
    def get_themes_list(self):
        if self.dominant_themes:
            return json.loads(self.dominant_themes)
        return []
    
    def set_themes_list(self, themes_list):
        self.dominant_themes = json.dumps(themes_list)

class Marginalia(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    page_id = db.Column(db.Integer, db.ForeignKey('book_page.id'), nullable=False)
    image_url = db.Column(db.Text)
    position_x = db.Column(db.Float)  # X coordinate in percentage
    position_y = db.Column(db.Float)  # Y coordinate in percentage
    width = db.Column(db.Float, default=80.0)  # Width in pixels
    height = db.Column(db.Float, default=80.0)  # Height in pixels
    prompt_used = db.Column(db.Text)
    theme = db.Column(db.String(100))
    side = db.Column(db.String(10), default='right')  # 'left' or 'right' margin
