import os
import json
import logging
from typing import Dict, List
import random

# Use Gemini for AI services
try:
    from google import genai
    from google.genai import types
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    genai = None
    types = None

class AIAnalyzer:
    """Handles AI-powered content analysis and image generation"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        if GEMINI_AVAILABLE and genai is not None:
            api_key = os.environ.get("GEMINI_API_KEY")
            if api_key:
                try:
                    self.client = genai.Client(api_key=api_key)
                    self.has_gemini = True
                    self.logger.info("Gemini client initialized successfully")
                except Exception as e:
                    self.has_gemini = False
                    self.logger.warning(f"Failed to initialize Gemini client: {e}")
                    self.logger.info("Using mock responses for testing")
            else:
                self.has_gemini = False
                self.logger.warning("Gemini API key not found, using mock responses")
        else:
            self.has_gemini = False
            self.logger.warning("Gemini library not available, using mock responses")
    
    def analyze_document(self, text: str) -> Dict:
        """
        Analyze the entire document for genre, themes, and overall mood
        
        Args:
            text: Full document text
            
        Returns:
            Dictionary with analysis results
        """
        if not text.strip():
            return self._get_default_analysis()
        
        if self.has_gemini:
            return self._analyze_document_with_gemini(text)
        else:
            return self._get_mock_document_analysis(text)
    
    def _analyze_document_with_gemini(self, text: str) -> Dict:
        """Analyze document using Gemini API"""
        try:
            # Truncate text if too long (keep first 4000 characters for analysis)
            analysis_text = text[:4000] if len(text) > 4000 else text
            
            prompt = f"""
            Analyze the following text and provide a JSON response with the following fields:
            - "genre": The primary genre (e.g., "Fantasy", "Science Fiction", "Historical Fiction", "Mystery", "Romance", "Non-fiction", "Academic", "Biography", etc.)
            - "themes": An array of 3-5 main themes or topics found in the text
            - "mood": The overall emotional tone (e.g., "optimistic", "melancholic", "suspenseful", "peaceful", "dramatic", "humorous")
            - "title": A suggested title based on the content (if not apparent from the text)
            
            Text to analyze:
            {analysis_text}
            
            Respond only with valid JSON.
            """
            
            response = self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=[
                    types.Content(role="user", parts=[types.Part(text=prompt)])
                ],
                config=types.GenerateContentConfig(
                    system_instruction="You are a literary analysis expert. Respond only with valid JSON.",
                    response_mime_type="application/json"
                )
            )
            
            if response.text:
                result = json.loads(response.text)
                self.logger.info(f"Document analysis completed: {result.get('genre', 'Unknown')} genre detected")
                return result
            else:
                raise ValueError("Empty response from Gemini")
            
        except Exception as e:
            self.logger.error(f"Error in Gemini document analysis: {str(e)}")
            return self._get_mock_document_analysis(text)
    
    def analyze_page_content(self, text: str, genre: str) -> Dict:
        """
        Analyze individual page content for themes and mood
        
        Args:
            text: Page text content
            genre: Document genre from overall analysis
            
        Returns:
            Dictionary with page-specific analysis
        """
        if not text.strip():
            return {"themes": [], "mood": "neutral"}
        
        if self.has_gemini:
            return self._analyze_page_with_gemini(text, genre)
        else:
            return self._get_mock_page_analysis(text, genre)
    
    def _analyze_page_with_gemini(self, text: str, genre: str) -> Dict:
        """Analyze page content using Gemini API"""
        try:
            prompt = f"""
            Analyze this page of text from a {genre} document and provide a JSON response with:
            - "themes": An array of 1-3 specific themes or topics on this page
            - "mood": The emotional tone of this specific page (e.g., "tense", "peaceful", "mysterious", "joyful", "somber")
            
            Page text:
            {text[:1000]}
            
            Respond only with valid JSON.
            """
            
            response = self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=[
                    types.Content(role="user", parts=[types.Part(text=prompt)])
                ],
                config=types.GenerateContentConfig(
                    system_instruction="You are a literary analysis expert. Respond only with valid JSON.",
                    response_mime_type="application/json"
                )
            )
            
            if response.text:
                result = json.loads(response.text)
                return result
            else:
                raise ValueError("Empty response from Gemini")
            
        except Exception as e:
            self.logger.error(f"Error in Gemini page analysis: {str(e)}")
            return self._get_mock_page_analysis(text, genre)
    
    def generate_marginalia(self, page_text: str, genre: str, mood: str, themes: List[str]) -> List[Dict]:
        """
        Generate marginalia images for a page
        
        Args:
            page_text: Text content of the page
            genre: Document genre
            mood: Page mood
            themes: List of themes for the page
            
        Returns:
            List of marginalia image data
        """
        if not page_text.strip():
            return []
        
        # Generate 1-3 marginalia items per page based on content length
        num_marginalia = min(3, max(1, len(page_text) // 500))
        
        marginalia_items = []
        
        for i in range(num_marginalia):
            if self.has_gemini:
                image_data = self._generate_marginalia_with_gemini(page_text, genre, mood, themes, i)
            else:
                image_data = self._get_mock_marginalia(genre, mood, themes, i)
            
            if image_data:
                marginalia_items.append(image_data)
        
        return marginalia_items
    
    def _generate_marginalia_with_gemini(self, page_text: str, genre: str, mood: str, themes: List[str], index: int) -> Dict:
        """Generate marginalia using Gemini image generation"""
        try:
            # Create a prompt for the marginalia based on content analysis
            theme = themes[index % len(themes)] if themes else "general"
            
            # Craft a specific prompt for marginalia style
            style_descriptors = {
                "Fantasy": "medieval manuscript illumination, ornate border decoration",
                "Science Fiction": "technical diagram sketch, futuristic doodle",
                "Mystery": "detective's notebook sketch, noir-style illustration",
                "Romance": "delicate floral border, elegant calligraphy ornament",
                "Historical Fiction": "period-appropriate marginalia, vintage illustration",
                "Academic": "scholarly annotation, scientific diagram",
                "Biography": "portrait sketch, timeline illustration"
            }
            
            mood_styles = {
                "tense": "sharp lines, dramatic shadows",
                "peaceful": "soft curves, gentle shading",
                "mysterious": "hidden symbols, cryptic imagery",
                "joyful": "flowing lines, bright imagery",
                "somber": "minimal lines, subdued tones"
            }
            
            base_style = style_descriptors.get(genre, "simple line art marginalia")
            mood_style = mood_styles.get(mood, "balanced composition")
            
            prompt = f"""
            A small {base_style} drawing for a book margin, relating to "{theme}".
            Style: {mood_style}, black ink on white paper, minimalist, 
            medieval manuscript marginalia style, decorative border element,
            simple line art, no text, suitable for book margins, 
            size appropriate for marginalia (small decorative element)
            """
            
            # Use Gemini's image generation capability
            response = self.client.models.generate_content(
                model="gemini-2.0-flash-preview-image-generation",
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_modalities=['TEXT', 'IMAGE']
                )
            )
            
            # Extract image data from response
            image_url = None
            if response.candidates and len(response.candidates) > 0:
                content = response.candidates[0].content
                if content and content.parts:
                    for part in content.parts:
                        if part.inline_data and part.inline_data.data:
                            # Convert the binary data to a data URL
                            import base64
                            image_data = base64.b64encode(part.inline_data.data).decode('utf-8')
                            image_url = f"data:image/png;base64,{image_data}"
                            break
            
            if not image_url:
                # If image generation fails, use mock marginalia
                return self._get_mock_marginalia(genre, mood, themes, index)
            
            self.logger.info(f"Generated marginalia image for theme: {theme}")
            
            return {
                'image_url': image_url,
                'prompt': prompt,
                'theme': theme,
                'width': 80,
                'height': 80
            }
            
        except Exception as e:
            self.logger.error(f"Error generating marginalia with Gemini: {str(e)}")
            return self._get_mock_marginalia(genre, mood, themes, index)
    
    def _get_default_analysis(self) -> Dict:
        """Return default analysis for empty documents"""
        return {
            "genre": "Unknown",
            "themes": [],
            "mood": "neutral",
            "title": "Untitled Document"
        }
    
    def _get_mock_document_analysis(self, text: str) -> Dict:
        """Generate mock analysis based on text characteristics"""
        # Simple heuristics for mock analysis
        text_lower = text.lower()
        
        # Genre detection based on keywords
        genre = "General"
        if any(word in text_lower for word in ["magic", "dragon", "wizard", "fantasy", "quest"]):
            genre = "Fantasy"
        elif any(word in text_lower for word in ["space", "robot", "future", "technology", "science"]):
            genre = "Science Fiction"
        elif any(word in text_lower for word in ["murder", "detective", "mystery", "crime", "investigation"]):
            genre = "Mystery"
        elif any(word in text_lower for word in ["love", "romance", "heart", "relationship"]):
            genre = "Romance"
        elif any(word in text_lower for word in ["history", "historical", "century", "war", "ancient"]):
            genre = "Historical Fiction"
        
        # Extract themes from common words
        common_words = ["adventure", "friendship", "family", "power", "knowledge", "journey", "discovery"]
        themes = [word for word in common_words if word in text_lower][:3]
        if not themes:
            themes = ["life", "experience", "story"]
        
        # Determine mood
        mood = "neutral"
        if any(word in text_lower for word in ["happy", "joy", "celebration", "success"]):
            mood = "optimistic"
        elif any(word in text_lower for word in ["sad", "death", "loss", "tragedy"]):
            mood = "melancholic"
        elif any(word in text_lower for word in ["danger", "fear", "threat", "suspense"]):
            mood = "tense"
        
        return {
            "genre": genre,
            "themes": themes,
            "mood": mood,
            "title": f"A {genre} Story"
        }
    
    def _get_mock_page_analysis(self, text: str, genre: str) -> Dict:
        """Generate mock page analysis"""
        text_lower = text.lower()
        
        # Extract 1-2 themes from the page
        theme_keywords = {
            "Fantasy": ["magic", "adventure", "quest", "power"],
            "Science Fiction": ["technology", "discovery", "future", "exploration"],
            "Mystery": ["investigation", "clues", "secrets", "truth"],
            "Romance": ["love", "relationship", "emotion", "connection"],
            "Historical Fiction": ["tradition", "change", "society", "culture"]
        }
        
        possible_themes = theme_keywords.get(genre, ["experience", "knowledge", "growth", "challenge"])
        themes = [theme for theme in possible_themes if theme in text_lower][:2]
        if not themes:
            themes = [random.choice(possible_themes)]
        
        # Determine page mood
        mood = "neutral"
        if any(word in text_lower for word in ["exciting", "amazing", "wonderful"]):
            mood = "joyful"
        elif any(word in text_lower for word in ["difficult", "challenging", "problem"]):
            mood = "tense"
        elif any(word in text_lower for word in ["calm", "peaceful", "quiet"]):
            mood = "peaceful"
        
        return {
            "themes": themes,
            "mood": mood
        }
    
    def _get_mock_marginalia(self, genre: str, mood: str, themes: List[str], index: int) -> Dict:
        """Generate mock marginalia data with placeholder images"""
        theme = themes[index % len(themes)] if themes else "general"
        
        # Use a placeholder image service for mock marginalia
        # This creates consistent, themed placeholder images
        image_size = "80x80"
        placeholder_url = f"https://via.placeholder.com/{image_size}/404040/ffffff?text={theme[:3].upper()}"
        
        return {
            'image_url': placeholder_url,
            'prompt': f"Mock {genre} marginalia for {theme}",
            'theme': theme,
            'width': 80,
            'height': 80
        }
