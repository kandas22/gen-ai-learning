"""
Document Processing Module for Enhanced RAG System

This module handles:
- PDF text and image extraction
- OCR for images (with Tamil language support)
- Text chunking with metadata
- Image metadata preservation
"""

import os
import io
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from pathlib import Path
import base64

try:
    import pytesseract
    from PIL import Image
    TESSERACT_AVAILABLE = True
except ImportError:
    TESSERACT_AVAILABLE = False
    print("Warning: pytesseract not available. OCR functionality will be limited.")

try:
    from pdf2image import convert_from_path, convert_from_bytes
    PDF2IMAGE_AVAILABLE = True
except ImportError:
    PDF2IMAGE_AVAILABLE = False
    print("Warning: pdf2image not available. PDF image extraction will be limited.")

from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter


@dataclass
class ProcessedDocument:
    """Container for processed document data"""
    text: str
    chunks: List[Dict[str, any]]
    images: List[Dict[str, any]]
    metadata: Dict[str, any]
    source: str


@dataclass
class OCRResult:
    """Container for OCR results"""
    text: str
    confidence: float
    language: str
    image_path: Optional[str] = None
    image_base64: Optional[str] = None


class OCRProcessor:
    """Handles OCR processing with multilingual support"""
    
    def __init__(self, languages: List[str] = None):
        """
        Initialize OCR processor
        
        Args:
            languages: List of language codes (e.g., ['eng', 'tam'] for English and Tamil)
        """
        if not TESSERACT_AVAILABLE:
            raise ImportError(
                "pytesseract is required for OCR. Install with: pip install pytesseract\n"
                "Also install Tesseract: brew install tesseract tesseract-lang (macOS)"
            )
        
        self.languages = languages or ['eng', 'tam']  # English and Tamil by default
        self.lang_string = '+'.join(self.languages)
        
        # Set Tesseract command path if specified in environment
        tesseract_cmd = os.getenv('TESSERACT_CMD')
        if tesseract_cmd:
            pytesseract.pytesseract.tesseract_cmd = tesseract_cmd
    
    def extract_text_from_image(
        self, 
        image: Image.Image, 
        return_confidence: bool = True
    ) -> OCRResult:
        """
        Extract text from an image using OCR
        
        Args:
            image: PIL Image object
            return_confidence: Whether to calculate confidence score
            
        Returns:
            OCRResult with extracted text and metadata
        """
        try:
            # Extract text
            text = pytesseract.image_to_string(
                image, 
                lang=self.lang_string,
                config='--psm 3'  # Fully automatic page segmentation
            )
            
            # Calculate confidence if requested
            confidence = 0.0
            if return_confidence:
                try:
                    data = pytesseract.image_to_data(
                        image, 
                        lang=self.lang_string,
                        output_type=pytesseract.Output.DICT
                    )
                    # Calculate average confidence from all detected text
                    confidences = [int(conf) for conf in data['conf'] if conf != '-1']
                    confidence = sum(confidences) / len(confidences) / 100.0 if confidences else 0.0
                except Exception as e:
                    print(f"Warning: Could not calculate OCR confidence: {e}")
            
            # Convert image to base64 for storage/display
            buffered = io.BytesIO()
            image.save(buffered, format="PNG")
            img_base64 = base64.b64encode(buffered.getvalue()).decode()
            
            return OCRResult(
                text=text.strip(),
                confidence=confidence,
                language=self.lang_string,
                image_base64=img_base64
            )
            
        except Exception as e:
            print(f"OCR Error: {e}")
            return OCRResult(
                text="",
                confidence=0.0,
                language=self.lang_string
            )
    
    def extract_text_from_image_file(self, image_path: str) -> OCRResult:
        """
        Extract text from an image file
        
        Args:
            image_path: Path to image file
            
        Returns:
            OCRResult with extracted text and metadata
        """
        try:
            image = Image.open(image_path)
            result = self.extract_text_from_image(image)
            result.image_path = image_path
            return result
        except Exception as e:
            print(f"Error loading image {image_path}: {e}")
            return OCRResult(
                text="",
                confidence=0.0,
                language=self.lang_string,
                image_path=image_path
            )


class DocumentProcessor:
    """Main document processor for PDFs, images, and text files with adaptive processing for large files"""
    
    # File size thresholds (in MB)
    SMALL_FILE_THRESHOLD = 10  # < 10MB
    MEDIUM_FILE_THRESHOLD = 30  # 10-30MB
    LARGE_FILE_THRESHOLD = 100  # 30-100MB
    
    def __init__(
        self, 
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
        ocr_languages: List[str] = None,
        max_pages_per_batch: int = 10  # Process PDFs in batches
    ):
        """
        Initialize document processor
        
        Args:
            chunk_size: Size of text chunks (will be adjusted based on file size)
            chunk_overlap: Overlap between chunks
            ocr_languages: Languages for OCR (default: ['eng', 'tam'])
            max_pages_per_batch: Maximum pages to process at once for large files
        """
        self.base_chunk_size = chunk_size
        self.base_chunk_overlap = chunk_overlap
        self.max_pages_per_batch = max_pages_per_batch
        
        # Will be set dynamically based on file size
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        
        # Initialize text splitter (will be recreated for each file based on size)
        self.text_splitter = None
        self._create_text_splitter(chunk_size, chunk_overlap)
        
        # Initialize OCR processor
        try:
            self.ocr_processor = OCRProcessor(languages=ocr_languages)
            self.ocr_available = True
        except ImportError:
            self.ocr_processor = None
            self.ocr_available = False
            print("Warning: OCR not available")
    
    def _create_text_splitter(self, chunk_size: int, chunk_overlap: int):
        """Create or recreate text splitter with specified parameters"""
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", ".", "!", "?", ",", " ", ""]
        )
    
    def _get_file_size_mb(self, file_path: str) -> float:
        """Get file size in MB"""
        return os.path.getsize(file_path) / (1024 * 1024)
    
    def _adjust_processing_params(self, file_size_mb: float) -> Dict[str, int]:
        """
        Adjust processing parameters based on file size for cost-effectiveness
        
        Args:
            file_size_mb: File size in megabytes
            
        Returns:
            Dict with adjusted parameters
        """
        if file_size_mb < self.SMALL_FILE_THRESHOLD:
            # Small files: Standard processing
            return {
                'chunk_size': self.base_chunk_size,
                'chunk_overlap': self.base_chunk_overlap,
                'max_pages_per_batch': 50,
                'skip_images': False,
                'ocr_quality': 'high'
            }
        elif file_size_mb < self.MEDIUM_FILE_THRESHOLD:
            # Medium files: Slightly larger chunks, process more pages
            return {
                'chunk_size': int(self.base_chunk_size * 1.5),
                'chunk_overlap': int(self.base_chunk_overlap * 1.2),
                'max_pages_per_batch': 20,
                'skip_images': False,
                'ocr_quality': 'medium'
            }
        elif file_size_mb < self.LARGE_FILE_THRESHOLD:
            # Large files: Larger chunks, batch processing, skip some images
            return {
                'chunk_size': int(self.base_chunk_size * 2),
                'chunk_overlap': int(self.base_chunk_overlap * 1.5),
                'max_pages_per_batch': self.max_pages_per_batch,
                'skip_images': True,  # Skip OCR on images to save cost
                'ocr_quality': 'low'
            }
        else:
            # Very large files: Maximum optimization
            return {
                'chunk_size': int(self.base_chunk_size * 3),
                'chunk_overlap': int(self.base_chunk_overlap * 2),
                'max_pages_per_batch': 5,
                'skip_images': True,
                'ocr_quality': 'low'
            }
    
    def process_pdf(self, pdf_path: str) -> ProcessedDocument:
        """
        Process a PDF file - extract text and images with adaptive processing
        
        Args:
            pdf_path: Path to PDF file
            
        Returns:
            ProcessedDocument with extracted content
        """
        # Get file size and adjust parameters
        file_size_mb = self._get_file_size_mb(pdf_path)
        params = self._adjust_processing_params(file_size_mb)
        
        print(f"Processing PDF: {pdf_path} ({file_size_mb:.2f} MB)")
        print(f"Using adaptive parameters: chunk_size={params['chunk_size']}, skip_images={params['skip_images']}")
        
        # Recreate text splitter with adjusted parameters
        self._create_text_splitter(params['chunk_size'], params['chunk_overlap'])
        
        # Extract text from PDF
        text_content = []
        images_data = []
        
        try:
            reader = PdfReader(pdf_path)
            total_pages = len(reader.pages)
            
            print(f"Total pages: {total_pages}")
            
            # Process pages in batches for large files
            max_pages = params['max_pages_per_batch']
            
            for page_num, page in enumerate(reader.pages):
                # For very large files, limit total pages processed
                if file_size_mb > self.LARGE_FILE_THRESHOLD and page_num > 100:
                    print(f"Skipping remaining pages (processed first 100 pages)")
                    break
                
                # Extract text
                page_text = page.extract_text()
                if page_text.strip():
                    text_content.append(f"[Page {page_num + 1}]\n{page_text}")
                
                # Process images only if not skipped
                if not params['skip_images'] and hasattr(page, 'images'):
                    # Limit images processed per page for cost savings
                    max_images_per_page = 2 if file_size_mb > self.MEDIUM_FILE_THRESHOLD else 5
                    
                    for img_idx, image in enumerate(page.images[:max_images_per_page]):
                        try:
                            img_data = image.data
                            img = Image.open(io.BytesIO(img_data))
                            
                            # Perform OCR if available and image is large enough
                            if self.ocr_available and img.width > 100 and img.height > 100:
                                # Resize large images to save processing time
                                if img.width > 2000 or img.height > 2000:
                                    img.thumbnail((2000, 2000), Image.Resampling.LANCZOS)
                                
                                ocr_result = self.ocr_processor.extract_text_from_image(img)
                                
                                if ocr_result.text.strip():
                                    images_data.append({
                                        'page': page_num + 1,
                                        'image_index': img_idx,
                                        'ocr_text': ocr_result.text,
                                        'ocr_confidence': ocr_result.confidence,
                                        'image_base64': ocr_result.image_base64,
                                        'source': f"{pdf_path}#page{page_num + 1}_img{img_idx}"
                                    })
                                    
                                    # Add OCR text to main content
                                    text_content.append(
                                        f"[Page {page_num + 1}, Image {img_idx + 1} - OCR]\n{ocr_result.text}"
                                    )
                        except Exception as e:
                            print(f"Error extracting image from page {page_num + 1}: {e}")
                
                # Progress indicator for large files
                if (page_num + 1) % 10 == 0:
                    print(f"Processed {page_num + 1}/{total_pages} pages...")
            
            # Combine all text
            full_text = "\n\n".join(text_content)
            
            # Create chunks with metadata
            chunks = self._create_chunks(
                full_text, 
                source=pdf_path,
                doc_type="pdf"
            )
            
            print(f"Created {len(chunks)} chunks from {len(text_content)} text sections")
            
            return ProcessedDocument(
                text=full_text,
                chunks=chunks,
                images=images_data,
                metadata={
                    'source': pdf_path,
                    'type': 'pdf',
                    'pages': len(reader.pages),
                    'images_count': len(images_data),
                    'file_size_mb': file_size_mb,
                    'processing_params': params
                },
                source=pdf_path
            )
            
        except Exception as e:
            print(f"Error processing PDF {pdf_path}: {e}")
            return ProcessedDocument(
                text="",
                chunks=[],
                images=[],
                metadata={'source': pdf_path, 'type': 'pdf', 'error': str(e)},
                source=pdf_path
            )

    
    def process_image(self, image_path: str) -> ProcessedDocument:
        """
        Process an image file with OCR
        
        Args:
            image_path: Path to image file
            
        Returns:
            ProcessedDocument with OCR text
        """
        print(f"Processing image: {image_path}")
        
        if not self.ocr_available:
            return ProcessedDocument(
                text="",
                chunks=[],
                images=[],
                metadata={'source': image_path, 'type': 'image', 'error': 'OCR not available'},
                source=image_path
            )
        
        try:
            ocr_result = self.ocr_processor.extract_text_from_image_file(image_path)
            
            # Create chunks from OCR text
            chunks = self._create_chunks(
                ocr_result.text,
                source=image_path,
                doc_type="image"
            )
            
            return ProcessedDocument(
                text=ocr_result.text,
                chunks=chunks,
                images=[{
                    'ocr_text': ocr_result.text,
                    'ocr_confidence': ocr_result.confidence,
                    'image_base64': ocr_result.image_base64,
                    'source': image_path
                }],
                metadata={
                    'source': image_path,
                    'type': 'image',
                    'ocr_confidence': ocr_result.confidence,
                    'language': ocr_result.language
                },
                source=image_path
            )
            
        except Exception as e:
            print(f"Error processing image {image_path}: {e}")
            return ProcessedDocument(
                text="",
                chunks=[],
                images=[],
                metadata={'source': image_path, 'type': 'image', 'error': str(e)},
                source=image_path
            )
    
    def process_text_file(self, text_path: str) -> ProcessedDocument:
        """
        Process a text file
        
        Args:
            text_path: Path to text file
            
        Returns:
            ProcessedDocument with text content
        """
        print(f"Processing text file: {text_path}")
        
        try:
            with open(text_path, 'r', encoding='utf-8') as f:
                text = f.read()
            
            chunks = self._create_chunks(
                text,
                source=text_path,
                doc_type="text"
            )
            
            return ProcessedDocument(
                text=text,
                chunks=chunks,
                images=[],
                metadata={
                    'source': text_path,
                    'type': 'text',
                    'size': len(text)
                },
                source=text_path
            )
            
        except Exception as e:
            print(f"Error processing text file {text_path}: {e}")
            return ProcessedDocument(
                text="",
                chunks=[],
                images=[],
                metadata={'source': text_path, 'type': 'text', 'error': str(e)},
                source=text_path
            )
    
    def process_document(self, file_path: str) -> ProcessedDocument:
        """
        Process any supported document type
        
        Args:
            file_path: Path to document
            
        Returns:
            ProcessedDocument with extracted content
        """
        file_ext = Path(file_path).suffix.lower()
        
        if file_ext == '.pdf':
            return self.process_pdf(file_path)
        elif file_ext in ['.png', '.jpg', '.jpeg', '.tiff', '.bmp']:
            return self.process_image(file_path)
        elif file_ext in ['.txt', '.md']:
            return self.process_text_file(file_path)
        else:
            print(f"Unsupported file type: {file_ext}")
            return ProcessedDocument(
                text="",
                chunks=[],
                images=[],
                metadata={'source': file_path, 'error': f'Unsupported file type: {file_ext}'},
                source=file_path
            )
    
    def _create_chunks(
        self, 
        text: str, 
        source: str, 
        doc_type: str
    ) -> List[Dict[str, any]]:
        """
        Create text chunks with metadata
        
        Args:
            text: Text to chunk
            source: Source file path
            doc_type: Type of document
            
        Returns:
            List of chunks with metadata
        """
        if not text.strip():
            return []
        
        # Split text into chunks
        text_chunks = self.text_splitter.split_text(text)
        
        # Create chunk objects with metadata
        chunks = []
        for idx, chunk_text in enumerate(text_chunks):
            chunks.append({
                'text': chunk_text,
                'metadata': {
                    'source': source,
                    'chunk_index': idx,
                    'total_chunks': len(text_chunks),
                    'doc_type': doc_type
                }
            })
        
        return chunks


# Utility functions
def get_supported_extensions() -> List[str]:
    """Get list of supported file extensions"""
    return ['.pdf', '.txt', '.md', '.png', '.jpg', '.jpeg', '.tiff', '.bmp']


def is_supported_file(file_path: str) -> bool:
    """Check if file type is supported"""
    return Path(file_path).suffix.lower() in get_supported_extensions()
