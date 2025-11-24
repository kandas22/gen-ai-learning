"""
Text chunking strategies for document processing.
Splits documents into chunks for embedding and retrieval.
"""

from typing import List, Dict, Any
import re
from config import settings
from utils.logger import get_logger

logger = get_logger(__name__)


class TextChunker:
    """Split text into chunks for processing."""
    
    def __init__(
        self,
        chunk_size: int = None,
        chunk_overlap: int = None
    ):
        """Initialize text chunker.
        
        Args:
            chunk_size: Size of each chunk in characters (default from settings)
            chunk_overlap: Overlap between chunks (default from settings)
        """
        self.chunk_size = chunk_size or settings.chunk_size
        self.chunk_overlap = chunk_overlap or settings.chunk_overlap
        
        logger.info(
            f"TextChunker initialized: chunk_size={self.chunk_size}, "
            f"overlap={self.chunk_overlap}"
        )
    
    def split_by_sentences(self, text: str) -> List[str]:
        """Split text into sentences.
        
        Args:
            text: Input text
            
        Returns:
            List of sentences
        """
        # Simple sentence splitting (can be improved with nltk or spacy)
        sentences = re.split(r'(?<=[.!?])\s+', text)
        return [s.strip() for s in sentences if s.strip()]
    
    def chunk_by_characters(
        self,
        text: str,
        preserve_sentences: bool = True
    ) -> List[str]:
        """Chunk text by character count.
        
        Args:
            text: Input text
            preserve_sentences: Try to preserve sentence boundaries
            
        Returns:
            List of text chunks
        """
        if not text:
            return []
        
        chunks = []
        
        if preserve_sentences:
            sentences = self.split_by_sentences(text)
            current_chunk = ""
            
            for sentence in sentences:
                # If adding this sentence would exceed chunk size
                if len(current_chunk) + len(sentence) > self.chunk_size:
                    # Save current chunk if it's not empty
                    if current_chunk:
                        chunks.append(current_chunk.strip())
                    
                    # Start new chunk with this sentence
                    current_chunk = sentence + " "
                else:
                    current_chunk += sentence + " "
            
            # Add remaining chunk
            if current_chunk:
                chunks.append(current_chunk.strip())
        
        else:
            # Simple character-based chunking
            for i in range(0, len(text), self.chunk_size - self.chunk_overlap):
                chunk = text[i:i + self.chunk_size]
                if chunk.strip():
                    chunks.append(chunk.strip())
        
        return chunks
    
    def chunk_by_paragraphs(self, text: str) -> List[str]:
        """Chunk text by paragraphs.
        
        Args:
            text: Input text
            
        Returns:
            List of paragraph chunks
        """
        # Split by double newlines (paragraphs)
        paragraphs = re.split(r'\n\s*\n', text)
        
        chunks = []
        current_chunk = ""
        
        for para in paragraphs:
            para = para.strip()
            if not para:
                continue
            
            # If adding this paragraph would exceed chunk size
            if len(current_chunk) + len(para) > self.chunk_size:
                # Save current chunk
                if current_chunk:
                    chunks.append(current_chunk.strip())
                
                # If paragraph itself is too large, split it
                if len(para) > self.chunk_size:
                    para_chunks = self.chunk_by_characters(para)
                    chunks.extend(para_chunks[:-1])  # Add all but last
                    current_chunk = para_chunks[-1] if para_chunks else ""
                else:
                    current_chunk = para
            else:
                current_chunk += "\n\n" + para if current_chunk else para
        
        # Add remaining chunk
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        return chunks
    
    def chunk_with_overlap(self, text: str) -> List[Dict[str, Any]]:
        """Chunk text with overlap and metadata.
        
        Args:
            text: Input text
            
        Returns:
            List of chunk dictionaries with metadata
        """
        # Use paragraph-based chunking for better semantic coherence
        base_chunks = self.chunk_by_paragraphs(text)
        
        chunks_with_metadata = []
        
        for i, chunk_text in enumerate(base_chunks):
            # Add overlap from previous chunk
            overlap_text = ""
            if i > 0 and self.chunk_overlap > 0:
                prev_chunk = base_chunks[i - 1]
                # Take last N characters from previous chunk
                overlap_text = prev_chunk[-self.chunk_overlap:] + " "
            
            # Add overlap from next chunk
            next_overlap = ""
            if i < len(base_chunks) - 1 and self.chunk_overlap > 0:
                next_chunk = base_chunks[i + 1]
                # Take first N characters from next chunk
                next_overlap = " " + next_chunk[:self.chunk_overlap]
            
            full_chunk = overlap_text + chunk_text + next_overlap
            
            chunks_with_metadata.append({
                'chunk_index': i,
                'content': full_chunk.strip(),
                'original_content': chunk_text,
                'char_count': len(full_chunk),
                'has_overlap': bool(overlap_text or next_overlap)
            })
        
        return chunks_with_metadata
    
    def chunk_document_pages(
        self,
        pages: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Chunk document pages with page metadata.
        
        Args:
            pages: List of page dictionaries from PDFProcessor
            
        Returns:
            List of chunks with page metadata
        """
        all_chunks = []
        global_chunk_index = 0
        
        for page in pages:
            page_num = page['page_number']
            page_text = page['text']
            
            # Chunk this page's text
            page_chunks = self.chunk_with_overlap(page_text)
            
            # Add page metadata to each chunk
            for chunk in page_chunks:
                all_chunks.append({
                    'chunk_index': global_chunk_index,
                    'page_chunk_index': chunk['chunk_index'],
                    'content': chunk['content'],
                    'page_number': page_num,
                    'char_count': chunk['char_count'],
                    'metadata': {
                        'has_overlap': chunk['has_overlap'],
                        'page_char_count': page['char_count']
                    }
                })
                global_chunk_index += 1
        
        logger.info(f"Created {len(all_chunks)} chunks from {len(pages)} pages")
        return all_chunks
    
    def merge_small_chunks(
        self,
        chunks: List[Dict[str, Any]],
        min_size: int = 100
    ) -> List[Dict[str, Any]]:
        """Merge chunks that are too small.
        
        Args:
            chunks: List of chunk dictionaries
            min_size: Minimum chunk size in characters
            
        Returns:
            List of merged chunks
        """
        if not chunks:
            return []
        
        merged = []
        current_chunk = None
        
        for chunk in chunks:
            if current_chunk is None:
                current_chunk = chunk.copy()
            elif chunk['char_count'] < min_size:
                # Merge with current chunk
                current_chunk['content'] += " " + chunk['content']
                current_chunk['char_count'] = len(current_chunk['content'])
            else:
                # Save current chunk and start new one
                merged.append(current_chunk)
                current_chunk = chunk.copy()
        
        # Add last chunk
        if current_chunk:
            merged.append(current_chunk)
        
        # Re-index
        for i, chunk in enumerate(merged):
            chunk['chunk_index'] = i
        
        logger.info(f"Merged {len(chunks)} chunks into {len(merged)} chunks")
        return merged
