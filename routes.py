from flask import render_template, request, jsonify, redirect, url_for, flash
from werkzeug.utils import secure_filename
import os
import logging
from datetime import datetime

from app import app, db
from models import ProcessingJob, JobStatus, BookAnalysis, BookPage, Marginalia
from pdf_processor import PDFProcessor
from ai_services import AIAnalyzer

# Configure allowed file extensions
ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """Main page with PDF upload form"""
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_pdf():
    """Handle PDF upload and start processing"""
    if 'pdf_file' not in request.files:
        flash('No file selected')
        return redirect(url_for('index'))
    
    file = request.files['pdf_file']
    if file.filename == '':
        flash('No file selected')
        return redirect(url_for('index'))
    
    if file and allowed_file(file.filename):
        try:
            # Save uploaded file
            if file.filename:
                filename = secure_filename(file.filename)
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
                unique_filename = timestamp + filename
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
                file.save(file_path)
                
                # Create processing job
                job = ProcessingJob()
                job.filename = filename
                job.file_path = file_path
                job.status = JobStatus.PENDING
                db.session.add(job)
                db.session.commit()
                
                # Start processing (in a real implementation, this would be sent to a task queue)
                try:
                    process_pdf_job(job.id)
                except Exception as e:
                    logging.error(f"Error processing PDF: {str(e)}")
                    job.status = JobStatus.FAILED
                    job.error_message = str(e)
                    db.session.commit()
                    flash(f'Error processing PDF: {str(e)}')
                    return redirect(url_for('index'))
                
                return redirect(url_for('book_reader', job_id=job.id))
            else:
                flash('No filename provided')
                return redirect(url_for('index'))
            
        except Exception as e:
            logging.error(f"Error uploading file: {str(e)}")
            flash(f'Error uploading file: {str(e)}')
            return redirect(url_for('index'))
    else:
        flash('Invalid file type. Please upload a PDF file.')
        return redirect(url_for('index'))

@app.route('/job_status/<int:job_id>')
def job_status(job_id):
    """Get job processing status"""
    job = ProcessingJob.query.get_or_404(job_id)
    return jsonify({
        'status': job.status.value,
        'progress': job.progress,
        'error_message': job.error_message
    })

@app.route('/book/<int:job_id>')
def book_reader(job_id):
    """Display the processed book"""
    job = ProcessingJob.query.get_or_404(job_id)
    
    if job.status != JobStatus.COMPLETED:
        return render_template('book_reader.html', job=job, book_data=None)
    
    # Get book data
    analysis = BookAnalysis.query.filter_by(job_id=job_id).first()
    pages = BookPage.query.filter_by(job_id=job_id).order_by(BookPage.page_number).all()
    
    # Prepare book data for frontend
    book_data = {
        'title': analysis.title if analysis else job.filename,
        'genre': analysis.genre if analysis else 'Unknown',
        'themes': analysis.get_themes_list() if analysis else [],
        'overall_mood': analysis.overall_mood if analysis else 'neutral',
        'total_pages': len(pages),
        'pages': []
    }
    
    for page in pages:
        page_data = {
            'page_number': page.page_number,
            'text_content': page.text_content,
            'text_blocks': page.get_text_blocks_list(),
            'mood': page.mood,
            'themes': page.get_themes_list(),
            'marginalia': []
        }
        
        for margin in page.marginalia:
            margin_data = {
                'image_url': margin.image_url,
                'position_x': margin.position_x,
                'position_y': margin.position_y,
                'width': margin.width,
                'height': margin.height,
                'theme': margin.theme,
                'side': margin.side
            }
            page_data['marginalia'].append(margin_data)
        
        book_data['pages'].append(page_data)
    
    return render_template('book_reader.html', job=job, book_data=book_data)

@app.route('/book_data/<int:job_id>')
def book_data_api(job_id):
    """API endpoint to get book data as JSON"""
    job = ProcessingJob.query.get_or_404(job_id)
    
    if job.status != JobStatus.COMPLETED:
        return jsonify({'error': 'Job not completed'}), 400
    
    analysis = BookAnalysis.query.filter_by(job_id=job_id).first()
    pages = BookPage.query.filter_by(job_id=job_id).order_by(BookPage.page_number).all()
    
    book_data = {
        'title': analysis.title if analysis else job.filename,
        'genre': analysis.genre if analysis else 'Unknown',
        'themes': analysis.get_themes_list() if analysis else [],
        'overall_mood': analysis.overall_mood if analysis else 'neutral',
        'total_pages': len(pages),
        'pages': []
    }
    
    for page in pages:
        page_data = {
            'page_number': page.page_number,
            'text_content': page.text_content,
            'text_blocks': page.get_text_blocks_list(),
            'mood': page.mood,
            'themes': page.get_themes_list(),
            'marginalia': []
        }
        
        for margin in page.marginalia:
            margin_data = {
                'image_url': margin.image_url,
                'position_x': margin.position_x,
                'position_y': margin.position_y,
                'width': margin.width,
                'height': margin.height,
                'theme': margin.theme,
                'side': margin.side
            }
            page_data['marginalia'].append(margin_data)
        
        book_data['pages'].append(page_data)
    
    return jsonify(book_data)

def process_pdf_job(job_id):
    """Process a PDF job - extract text, analyze, and generate marginalia"""
    job = ProcessingJob.query.get(job_id)
    if not job:
        return
    
    try:
        # Update status to processing
        job.status = JobStatus.PROCESSING
        job.progress = 10
        db.session.commit()
        
        # Initialize processors
        pdf_processor = PDFProcessor()
        ai_analyzer = AIAnalyzer()
        
        # Extract text and structure from PDF
        logging.info(f"Extracting text from PDF: {job.file_path}")
        extracted_data = pdf_processor.extract_text_with_coordinates(job.file_path)
        job.progress = 30
        db.session.commit()
        
        # Analyze the document
        logging.info("Analyzing document content")
        full_text = ' '.join([page['text'] for page in extracted_data['pages']])
        analysis_result = ai_analyzer.analyze_document(full_text)
        job.progress = 50
        db.session.commit()
        
        # Create book analysis record
        book_analysis = BookAnalysis()
        book_analysis.job_id = job.id
        book_analysis.genre = analysis_result.get('genre', 'Unknown')
        book_analysis.overall_mood = analysis_result.get('mood', 'neutral')
        book_analysis.total_pages = len(extracted_data['pages'])
        book_analysis.title = analysis_result.get('title', job.filename)
        book_analysis.set_themes_list(analysis_result.get('themes', []))
        db.session.add(book_analysis)
        
        # Process each page
        total_pages = len(extracted_data['pages'])
        for i, page_data in enumerate(extracted_data['pages']):
            logging.info(f"Processing page {i+1} of {total_pages}")
            
            # Analyze page content
            page_analysis = ai_analyzer.analyze_page_content(
                page_data['text'], 
                analysis_result.get('genre', 'Unknown')
            )
            
            # Create page record
            book_page = BookPage()
            book_page.job_id = job.id
            book_page.page_number = i + 1
            book_page.text_content = page_data['text']
            book_page.mood = page_analysis.get('mood', 'neutral')
            book_page.set_text_blocks_list(page_data['text_blocks'])
            book_page.set_themes_list(page_analysis.get('themes', []))
            db.session.add(book_page)
            db.session.flush()  # Get the page ID
            
            # Generate marginalia for this page
            if page_data['text'].strip():  # Only generate if there's text content
                marginalia_images = ai_analyzer.generate_marginalia(
                    page_data['text'],
                    analysis_result.get('genre', 'Unknown'),
                    page_analysis.get('mood', 'neutral'),
                    page_analysis.get('themes', [])
                )
                
                # Create marginalia records
                for j, margin_data in enumerate(marginalia_images):
                    # Calculate position to avoid text overlap
                    margin_x, margin_y, side = pdf_processor.calculate_margin_position(
                        page_data['text_blocks'], 
                        j
                    )
                    
                    marginalia = Marginalia()
                    marginalia.page_id = book_page.id
                    marginalia.image_url = margin_data['image_url']
                    marginalia.position_x = margin_x
                    marginalia.position_y = margin_y
                    marginalia.width = margin_data.get('width', 80)
                    marginalia.height = margin_data.get('height', 80)
                    marginalia.prompt_used = margin_data.get('prompt', '')
                    marginalia.theme = margin_data.get('theme', '')
                    marginalia.side = side
                    db.session.add(marginalia)
            
            # Update progress
            progress = 50 + int((i + 1) / total_pages * 40)
            job.progress = progress
            db.session.commit()
        
        # Mark job as completed
        job.status = JobStatus.COMPLETED
        job.progress = 100
        job.completed_at = datetime.utcnow()
        db.session.commit()
        
        logging.info(f"Successfully processed job {job_id}")
        
    except Exception as e:
        logging.error(f"Error processing job {job_id}: {str(e)}")
        job.status = JobStatus.FAILED
        job.error_message = str(e)
        db.session.commit()
        raise
