"""
PDF text extraction using PyMuPDF (fitz).
Extracts text, images, and metadata from PDF documents.
"""

import fitz  # PyMuPDF
from typing import List, Dict, Any, Tuple
from pathlib import Path
import io
from PIL import Image
from utils.logger import get_logger
from utils.validators import validate_pdf

logger = get_logger(__name__)


class PDFProcessor:
    """Process PDF documents to extract text and images."""
    
    def __init__(self, pdf_path: str):
        """Initialize PDF processor.
        
        Args:
            pdf_path: Path to PDF file
        """
        # Validate PDF
        is_valid, error_msg = validate_pdf(pdf_path)
        if not is_valid:
            raise ValueError(f"Invalid PDF: {error_msg}")
        
        self.pdf_path = pdf_path
        self.filename = Path(pdf_path).name
        self.doc = None
        self._open_document()
    
    def _open_document(self):
        """Open PDF document."""
        try:
            self.doc = fitz.open(self.pdf_path)
            logger.info(f"Opened PDF: {self.filename} ({self.doc.page_count} pages)")
        except Exception as e:
            logger.error(f"Failed to open PDF: {e}")
            raise
    
    def get_metadata(self) -> Dict[str, Any]:
        """Extract PDF metadata.
        
        Returns:
            Dictionary with metadata
        """
        metadata = {
            'filename': self.filename,
            'page_count': self.doc.page_count,
            'file_size': Path(self.pdf_path).stat().st_size,
            'title': self.doc.metadata.get('title', ''),
            'author': self.doc.metadata.get('author', ''),
            'subject': self.doc.metadata.get('subject', ''),
            'creator': self.doc.metadata.get('creator', ''),
            'producer': self.doc.metadata.get('producer', ''),
            'creation_date': self.doc.metadata.get('creationDate', ''),
        }
        return metadata
    
    def extract_text_from_page(self, page_num: int) -> str:
        """Extract text from a specific page.
        
        Args:
            page_num: Page number (0-indexed)
            
        Returns:
            Extracted text
        """
        try:
            page = self.doc[page_num]
            text = page.get_text()
            return text.strip()
        except Exception as e:
            logger.error(f"Failed to extract text from page {page_num}: {e}")
            return ""
    
    def extract_all_text(self) -> List[Dict[str, Any]]:
        """Extract text from all pages.
        
        Returns:
            List of dictionaries with page number and text
        """
        pages_text = []
        
        for page_num in range(self.doc.page_count):
            text = self.extract_text_from_page(page_num)
            
            if text:
                pages_text.append({
                    'page_number': page_num + 1,  # 1-indexed for user display
                    'text': text,
                    'char_count': len(text)
                })
        
        logger.info(f"Extracted text from {len(pages_text)} pages")
        return pages_text
    
    def extract_images_from_page(self, page_num: int) -> List[Dict[str, Any]]:
        """Extract images from a specific page.
        
        Args:
            page_num: Page number (0-indexed)
            
        Returns:
            List of image dictionaries
        """
        images = []
        
        try:
            page = self.doc[page_num]
            image_list = page.get_images()
            
            for img_index, img_info in enumerate(image_list):
                try:
                    xref = img_info[0]
                    base_image = self.doc.extract_image(xref)
                    
                    image_bytes = base_image["image"]
                    image_ext = base_image["ext"]
                    
                    # Convert to PIL Image
                    pil_image = Image.open(io.BytesIO(image_bytes))
                    
                    images.append({
                        'page_number': page_num + 1,
                        'image_index': img_index,
                        'image': pil_image,
                        'format': image_ext,
                        'size': pil_image.size,
                        'mode': pil_image.mode
                    })
                    
                except Exception as e:
                    logger.warning(f"Failed to extract image {img_index} from page {page_num}: {e}")
                    continue
            
        except Exception as e:
            logger.error(f"Failed to extract images from page {page_num}: {e}")
        
        return images
    
    def extract_all_images(self) -> List[Dict[str, Any]]:
        """Extract all images from the PDF.
        
        Returns:
            List of image dictionaries
        """
        all_images = []
        
        for page_num in range(self.doc.page_count):
            images = self.extract_images_from_page(page_num)
            all_images.extend(images)
        
        logger.info(f"Extracted {len(all_images)} images from PDF")
        return all_images
    
    def extract_tables(self, page_num: int) -> List[List[str]]:
        """Extract tables from a page (basic implementation).
        
        Args:
            page_num: Page number (0-indexed)
            
        Returns:
            List of tables (each table is a list of rows)
        """
        try:
            page = self.doc[page_num]
            # Get text with layout preserved
            text = page.get_text("blocks")
            
            # This is a simplified table detection
            # For production, consider using libraries like camelot or tabula
            tables = []
            
            # Basic heuristic: look for aligned text blocks
            # This is a placeholder - implement more sophisticated logic as needed
            
            return tables
            
        except Exception as e:
            logger.error(f"Failed to extract tables from page {page_num}: {e}")
            return []
    
    def get_page_dimensions(self, page_num: int) -> Tuple[float, float]:
        """Get page dimensions.
        
        Args:
            page_num: Page number (0-indexed)
            
        Returns:
            Tuple of (width, height) in points
        """
        page = self.doc[page_num]
        rect = page.rect
        return (rect.width, rect.height)
    
    def process_document(self) -> Dict[str, Any]:
        """Process entire document and extract all information.
        
        Returns:
            Dictionary with all extracted data
        """
        logger.info(f"Processing document: {self.filename}")
        
        # Extract metadata
        metadata = self.get_metadata()
        
        # Extract text from all pages
        pages_text = self.extract_all_text()
        
        # Extract all images
        images = self.extract_all_images()
        
        result = {
            'metadata': metadata,
            'pages': pages_text,
            'images': images,
            'total_pages': self.doc.page_count,
            'total_images': len(images),
            'total_chars': sum(p['char_count'] for p in pages_text)
        }
        
        logger.info(
            f"Document processing complete: {result['total_pages']} pages, "
            f"{result['total_chars']} characters, {result['total_images']} images"
        )
        
        return result
    
    def close(self):
        """Close PDF document."""
        if self.doc:
            self.doc.close()
            logger.info(f"Closed PDF: {self.filename}")
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
