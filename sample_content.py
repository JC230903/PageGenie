#!/usr/bin/env python3
"""
Create a sample PDF for testing the AI-Enhanced PDF Reader
"""

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
import os

def create_sample_pdf():
    """Create a sample fantasy story PDF for testing"""
    
    # Create the PDF file
    filename = "uploads/sample_fantasy_story.pdf"
    doc = SimpleDocTemplate(filename, pagesize=letter, topMargin=72, bottomMargin=72)
    
    # Get styles
    styles = getSampleStyleSheet()
    
    # Create custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        alignment=TA_CENTER,
        spaceAfter=30
    )
    
    story_style = ParagraphStyle(
        'Story',
        parent=styles['Normal'],
        fontSize=12,
        alignment=TA_JUSTIFY,
        spaceAfter=12,
        leftIndent=20,
        rightIndent=20
    )
    
    # Story content
    story = []
    
    # Title
    story.append(Paragraph("The Enchanted Forest of Eldoria", title_style))
    story.append(Spacer(1, 20))
    
    # Chapter 1
    story.append(Paragraph("Chapter 1: The Mysterious Portal", styles['Heading2']))
    story.append(Spacer(1, 12))
    
    paragraphs = [
        """In the heart of the ancient kingdom of Eldoria, where mystical creatures roamed freely and magic flowed through every leaf and stone, there stood a forest unlike any other. The Enchanted Forest was said to hold secrets that could change the fate of kingdoms, and legends spoke of a hidden portal that connected worlds.""",
        
        """Young Aria, a brave apprentice mage with flowing auburn hair and eyes that sparkled like emeralds, had always been drawn to the mysteries of the forest. Her master, the wise wizard Theron, had warned her countless times about the dangers that lurked within the shadowy depths, but curiosity burned within her heart like an unquenchable flame.""",
        
        """On this particular morning, as golden sunlight filtered through the ancient oak trees, Aria discovered something extraordinary. A shimmering portal, its edges crackling with purple lightning, had appeared in a clearing she had visited a thousand times before. The air around it hummed with magical energy, and she could hear faint whispers calling her name.""",
        
        """Without hesitation, and perhaps against her better judgment, Aria stepped through the portal. The world around her dissolved into swirling colors and starlight, and when her vision cleared, she found herself in a realm beyond imagination. Crystal spires reached toward a sky painted in shades of violet and gold, and in the distance, she could see magnificent dragons soaring through clouds that sparkled like diamonds."""
    ]
    
    for paragraph in paragraphs:
        story.append(Paragraph(paragraph, story_style))
        story.append(Spacer(1, 12))
    
    # Chapter 2
    story.append(Spacer(1, 20))
    story.append(Paragraph("Chapter 2: The Dragon's Wisdom", styles['Heading2']))
    story.append(Spacer(1, 12))
    
    more_paragraphs = [
        """As Aria explored this wondrous new realm, she encountered Zephyr, an ancient dragon with scales that shimmered like liquid silver. Unlike the fearsome beasts of legend, Zephyr possessed a gentle wisdom that had been cultivated over centuries of guarding the sacred knowledge of the realm.""",
        
        """'Young mage,' Zephyr spoke, his voice resonating like distant thunder, 'you have been chosen to restore the balance between our worlds. The portal you discovered is one of seven, and each holds a piece of the Crystal of Eternal Harmony. Without this crystal, both our realms will fall into eternal darkness.'""",
        
        """Aria felt the weight of destiny settling upon her shoulders. She thought of her home, of Master Theron, and of all the innocent lives that would be lost if she failed. With determination blazing in her heart, she accepted the quest that would test her courage, her magical abilities, and her belief in the power of friendship and love.""",
        
        """Thus began an adventure that would take her through enchanted valleys where flowers sang lullabies, across treacherous mountains guarded by stone giants, and into the depths of underwater cities where mermaids held ancient secrets. Each challenge would teach her something new about the magic that flowed within her and the strength that comes from believing in oneself."""
    ]
    
    for paragraph in more_paragraphs:
        story.append(Paragraph(paragraph, story_style))
        story.append(Spacer(1, 12))
    
    # Build the PDF
    doc.build(story)
    print(f"Sample PDF created: {filename}")
    return filename

if __name__ == "__main__":
    create_sample_pdf()