"""
OCR processor for extracting text from images.
Optimized for speed with intelligent filtering.
"""

import pytesseract
from PIL import Image, ImageEnhance
from typing import Dict, Any, Tuple
from utils.logger import get_logger

logger = get_logger(__name__)


class OCRProcessor:
    """Process images with OCR to extract text - optimized for speed."""
    
    def __init__(
        self,
        language: str = 'eng',
        confidence_threshold: float = 60.0,
        min_image_size: int = 100,  # Skip images smaller than this
        max_image_size: int = 4000,  # Resize images larger than this
    ):
        """Initialize OCR processor with optimized settings.
        
        Args:
            language: Tesseract language code
            confidence_threshold: Minimum confidence to accept OCR results
            min_image_size: Skip images with width or height below this (likely icons)
            max_image_size: Resize images larger than this for faster processing
        """
        self.language = language
        self.confidence_threshold = confidence_threshold
        self.min_image_size = min_image_size
        self.max_image_size = max_image_size
        
        # Optimized Tesseract config for speed
        self.tesseract_config = (
            '--oem 1 '  # Use LSTM OCR engine (faster)
            '--psm 6 '  # Assume uniform block of text
            '-c tessedit_do_invert=0 '  # Skip inversion
        )
        
        logger.info(f"OCR Processor initialized: lang={language}, min_size={min_image_size}")
    
    def should_process_image(self, image: Image.Image) -> Tuple[bool, str]:
        """Determine if image should be processed based on size and content.
        
        Args:
            image: PIL Image
            
        Returns:
            Tuple of (should_process, reason)
        """
        width, height = image.size
        
        # Skip very small images (likely icons, bullets, decorations)
        if width < self.min_image_size or height < self.min_image_size:
            return False, f"Image too small ({width}x{height})"
        
        # Skip very thin images (likely lines or borders)
        aspect_ratio = max(width, height) / min(width, height)
        if aspect_ratio > 20:
            return False, f"Extreme aspect ratio ({aspect_ratio:.1f})"
        
        return True, "OK"
    
    def optimize_image_for_ocr(self, image: Image.Image) -> Image.Image:
        """Optimize image for faster OCR processing.
        
        Args:
            image: Input PIL Image
            
        Returns:
            Optimized PIL Image
        """
        # Convert to grayscale for faster processing
        if image.mode != 'L':
            image = image.convert('L')
        
        # Resize if too large
        width, height = image.size
        if width > self.max_image_size or height > self.max_image_size:
            # Calculate new size maintaining aspect ratio
            scale = self.max_image_size / max(width, height)
            new_size = (int(width * scale), int(height * scale))
            image = image.resize(new_size, Image.Resampling.LANCZOS)
            logger.debug(f"Resized image from {width}x{height} to {new_size}")
        
        # Simple contrast enhancement (skip heavy preprocessing)
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(1.5)
        
        return image
    
    def extract_text(self, image: Image.Image) -> Dict[str, Any]:
        """Extract text from image using OCR - optimized for speed.
        
        Args:
            image: PIL Image
            
        Returns:
            Dictionary with text, confidence, and word count
        """
        try:
            # Quick extraction with optimized config
            data = pytesseract.image_to_data(
                image,
                lang=self.language,
                config=self.tesseract_config,
                output_type=pytesseract.Output.DICT
            )
            
            # Extract text and calculate confidence
            words = []
            confidences = []
            
            for i, conf in enumerate(data['conf']):
                if conf > 0:  # Valid word
                    text = data['text'][i].strip()
                    if text:
                        words.append(text)
                        confidences.append(conf)
            
            # Calculate average confidence
            avg_confidence = sum(confidences) / len(confidences) if confidences else 0
            
            # Combine words into text
            text = ' '.join(words)
            
            return {
                'text': text,
                'confidence': avg_confidence,
                'word_count': len(words)
            }
            
        except Exception as e:
            logger.error(f"OCR extraction failed: {e}")
            return {
                'text': '',
                'confidence': 0.0,
                'word_count': 0
            }
    
    def process_image(self, image: Image.Image) -> Dict[str, Any]:
        """Process image with OCR - optimized for speed.
        
        Args:
            image: PIL Image
            
        Returns:
            Dictionary with OCR results
        """
        # Early filtering - skip images that won't yield useful text
        should_process, reason = self.should_process_image(image)
        if not should_process:
            logger.debug(f"Skipping image: {reason}")
            return {
                'text': '',
                'confidence': 0.0,
                'word_count': 0,
                'skipped': True,
                'skip_reason': reason
            }
        
        # Optimize image for faster OCR
        optimized_image = self.optimize_image_for_ocr(image)
        
        # Extract text
        result = self.extract_text(optimized_image)
        result['skipped'] = False
        
        # Log results
        if result['word_count'] > 0:
            logger.info(
                f"OCR complete: {result['word_count']} words, "
                f"confidence: {result['confidence']:.1f}%"
            )
        else:
            logger.debug("No text extracted from image")
        
        return result
