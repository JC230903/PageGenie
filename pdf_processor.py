import fitz  # PyMuPDF
import logging
import re
from typing import List, Dict, Tuple

class PDFProcessor:
    """Handles PDF text extraction with coordinate information"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def extract_text_with_coordinates(self, pdf_path: str) -> Dict:
        """
        Extract text from PDF with coordinate information for each text block
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Dictionary containing pages with text blocks and coordinates
        """
        try:
            doc = fitz.open(pdf_path)
            extracted_data = {
                'total_pages': len(doc),
                'pages': []
            }
            
            for page_num in range(len(doc)):
                page = doc[page_num]  # type: fitz.Page
                
                # Get page dimensions
                page_rect = page.rect
                page_width = page_rect.width
                page_height = page_rect.height
                
                # Extract text blocks with coordinates  
                text_blocks = page.get_text("dict")
                
                page_text = ""
                structured_blocks = []
                
                for block in text_blocks["blocks"]:
                    if "lines" in block:  # Text block
                        block_text = ""
                        block_bbox = block["bbox"]
                        
                        for line in block["lines"]:
                            line_text = ""
                            for span in line["spans"]:
                                line_text += span["text"]
                            
                            if line_text.strip():
                                block_text += line_text + " "
                        
                        if block_text.strip():
                            page_text += block_text + "\n"
                            
                            # Calculate relative positions (as percentages)
                            rel_x = (block_bbox[0] / page_width) * 100
                            rel_y = (block_bbox[1] / page_height) * 100
                            rel_width = ((block_bbox[2] - block_bbox[0]) / page_width) * 100
                            rel_height = ((block_bbox[3] - block_bbox[1]) / page_height) * 100
                            
                            structured_blocks.append({
                                'text': block_text.strip(),
                                'bbox': block_bbox,
                                'relative_position': {
                                    'x': rel_x,
                                    'y': rel_y,
                                    'width': rel_width,
                                    'height': rel_height
                                }
                            })
                
                page_data = {
                    'page_number': page_num + 1,
                    'text': page_text.strip(),
                    'text_blocks': structured_blocks,
                    'page_dimensions': {
                        'width': page_width,
                        'height': page_height
                    }
                }
                
                extracted_data['pages'].append(page_data)
                
                self.logger.debug(f"Extracted {len(structured_blocks)} text blocks from page {page_num + 1}")
            
            doc.close()
            self.logger.info(f"Successfully extracted text from {len(extracted_data['pages'])} pages")
            return extracted_data
            
        except Exception as e:
            self.logger.error(f"Error extracting text from PDF {pdf_path}: {str(e)}")
            raise
    
    def calculate_margin_position(self, text_blocks: List[Dict], marginalia_index: int) -> Tuple[float, float, str]:
        """
        Calculate position for marginalia to avoid overlapping with text
        
        Args:
            text_blocks: List of text blocks with position information
            marginalia_index: Index of the marginalia item for positioning
            
        Returns:
            Tuple of (x_position, y_position, side) where positions are percentages
        """
        if not text_blocks:
            # Default position if no text blocks
            return (85.0, 20.0, 'right')
        
        # Define margin areas (as percentages of page width/height)
        left_margin_x = 5.0  # 5% from left edge
        right_margin_x = 85.0  # 85% from left edge (15% from right)
        
        # Find available vertical space
        occupied_y_positions = []
        min_text_x = float('inf')
        max_text_x = 0
        
        for block in text_blocks:
            rel_pos = block.get('relative_position', {})
            if rel_pos:
                occupied_y_positions.append((rel_pos['y'], rel_pos['y'] + rel_pos['height']))
                min_text_x = min(min_text_x, rel_pos['x'])
                max_text_x = max(max_text_x, rel_pos['x'] + rel_pos['width'])
        
        # Determine which margin to use based on text layout
        use_left_margin = min_text_x > 25  # If text starts far from left, use left margin
        use_right_margin = max_text_x < 75  # If text ends before right area, use right margin
        
        # Choose side based on marginalia index and available space
        if use_left_margin and (marginalia_index % 2 == 0 or not use_right_margin):
            side = 'left'
            x_position = left_margin_x
        else:
            side = 'right'
            x_position = right_margin_x
        
        # Find vertical position that doesn't overlap with text
        y_position = self._find_available_y_position(occupied_y_positions, marginalia_index)
        
        return (x_position, y_position, side)
    
    def _find_available_y_position(self, occupied_positions: List[Tuple[float, float]], index: int) -> float:
        """
        Find an available Y position that doesn't overlap with text
        
        Args:
            occupied_positions: List of (y_start, y_end) tuples for text blocks
            index: Index for staggering multiple marginalia items
            
        Returns:
            Y position as percentage
        """
        # Sort occupied positions by Y coordinate
        occupied_positions.sort()
        
        # Define marginalia height (in percentage)
        marginalia_height = 8.0  # Approximately 8% of page height
        
        # Start positions for marginalia (staggered)
        base_positions = [15, 35, 55, 75]  # Percentage positions
        start_y = base_positions[index % len(base_positions)]
        
        # Check if this position overlaps with text
        for occupied_start, occupied_end in occupied_positions:
            if (start_y < occupied_end + 2 and start_y + marginalia_height > occupied_start - 2):
                # Overlap detected, try to find space after this text block
                start_y = occupied_end + 3  # 3% buffer
        
        # Ensure we don't go beyond page bounds
        if start_y + marginalia_height > 95:
            start_y = 95 - marginalia_height
        
        return max(5.0, start_y)  # Minimum 5% from top
    
    def chunk_text_semantically(self, text: str, max_chunk_size: int = 1000) -> List[str]:
        """
        Split text into semantic chunks for analysis
        
        Args:
            text: Input text to chunk
            max_chunk_size: Maximum size of each chunk
            
        Returns:
            List of text chunks
        """
        if not text or len(text) <= max_chunk_size:
            return [text] if text else []
        
        # Split by paragraphs first
        paragraphs = re.split(r'\n\s*\n', text)
        chunks = []
        current_chunk = ""
        
        for paragraph in paragraphs:
            paragraph = paragraph.strip()
            if not paragraph:
                continue
            
            # If adding this paragraph would exceed the limit, start a new chunk
            if len(current_chunk) + len(paragraph) + 1 > max_chunk_size and current_chunk:
                chunks.append(current_chunk.strip())
                current_chunk = paragraph
            else:
                if current_chunk:
                    current_chunk += "\n\n" + paragraph
                else:
                    current_chunk = paragraph
        
        # Add the last chunk
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        return chunks
