"""
Image Generation Module for Enhanced RAG

This module provides:
- Generate images using Google Imagen or other models
- Create visual examples for educational content
- Enhance RAG responses with illustrations
"""

import os
from typing import Optional, Dict, Any
import google.generativeai as genai
from PIL import Image
import io
import base64


class ImageGenerator:
    """Generate images to illustrate RAG responses"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize image generator
        
        Args:
            api_key: Gemini API key
        """
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            raise ValueError("Gemini API key required for image generation")
        
        genai.configure(api_key=self.api_key)
        
        # Check if Imagen is available
        self.imagen_available = self._check_imagen_availability()
        
        print(f"ImageGenerator initialized (Imagen available: {self.imagen_available})")
    
    def _check_imagen_availability(self) -> bool:
        """Check if Imagen API is available"""
        try:
            # Try to list models and check for imagen
            models = genai.list_models()
            for model in models:
                if 'imagen' in model.name.lower():
                    return True
            return False
        except Exception as e:
            print(f"Could not check Imagen availability: {e}")
            return False
    
    def generate_educational_diagram(
        self,
        concept: str,
        description: str,
        style: str = "simple educational diagram"
    ) -> Optional[Dict[str, Any]]:
        """
        Generate an educational diagram
        
        Args:
            concept: The concept to illustrate (e.g., "rest and motion")
            description: Detailed description of what to show
            style: Visual style (simple, detailed, cartoon, realistic)
            
        Returns:
            Dict with image data and metadata, or None if failed
        """
        if not self.imagen_available:
            print("Imagen not available. Using text-based description instead.")
            return self._generate_text_diagram(concept, description)
        
        try:
            # Create a detailed prompt for educational content
            prompt = f"""Create a {style} showing {concept}.

Description: {description}

Style requirements:
- Clear and easy to understand
- Suitable for students
- Clean, simple design
- Labels and annotations where helpful
- Bright, engaging colors"""
            
            # Note: Imagen API syntax may vary - this is a placeholder
            # You'll need to check the actual Gemini/Imagen API documentation
            response = genai.generate_images(
                prompt=prompt,
                number_of_images=1
            )
            
            # Process the generated image
            image_data = response.images[0]
            
            return {
                'image': image_data,
                'prompt': prompt,
                'concept': concept,
                'type': 'generated'
            }
            
        except Exception as e:
            print(f"Error generating image: {e}")
            return self._generate_text_diagram(concept, description)
    
    def _generate_text_diagram(self, concept: str, description: str) -> Dict[str, Any]:
        """
        Generate a text-based ASCII diagram as fallback
        
        Args:
            concept: The concept to illustrate
            description: Description of the concept
            
        Returns:
            Dict with ASCII art and metadata
        """
        # For rest and motion example
        if "rest" in concept.lower() and "motion" in concept.lower():
            ascii_art = """
╔════════════════════════════════════════════════════════╗
║           REST vs MOTION - Book on Table               ║
╚════════════════════════════════════════════════════════╝

    REST (Book not moving)
    ┌─────────────────────┐
    │                     │
    │   📕 BOOK           │  ← Book stays in same position
    │                     │
    └─────────────────────┘
         TABLE
    
    
    MOTION (Book being pushed)
    ┌─────────────────────┐
    │                     │
    │        📕 BOOK →    │  ← Book changes position
    │     (moving)        │
    └─────────────────────┘
         TABLE
    
    
    KEY POINTS:
    • REST: Object stays in the same position
    • MOTION: Object changes position over time
"""
        else:
            # Generic diagram
            ascii_art = f"""
╔════════════════════════════════════════════════════════╗
║  {concept.upper()}                                      ║
╚════════════════════════════════════════════════════════╝

{description}

[Visual representation would be generated here]
"""
        
        return {
            'ascii_art': ascii_art,
            'concept': concept,
            'description': description,
            'type': 'text_diagram'
        }
    
    def create_comparison_diagram(
        self,
        concept1: str,
        concept2: str,
        differences: list
    ) -> str:
        """
        Create a side-by-side comparison diagram
        
        Args:
            concept1: First concept
            concept2: Second concept
            differences: List of key differences
            
        Returns:
            ASCII art comparison
        """
        diagram = f"""
╔═══════════════════════════════════════════════════════════════╗
║         {concept1.upper()} vs {concept2.upper()}              ║
╚═══════════════════════════════════════════════════════════════╝

┌──────────────────────┬──────────────────────┐
│   {concept1:^20} │   {concept2:^20} │
├──────────────────────┼──────────────────────┤
"""
        
        for diff in differences:
            left, right = diff.split('|') if '|' in diff else (diff, diff)
            diagram += f"│ {left.strip():<20} │ {right.strip():<20} │\n"
        
        diagram += "└──────────────────────┴──────────────────────┘"
        
        return diagram


# Utility function for integration with RAG
def enhance_response_with_visual(
    query: str,
    answer: str,
    generator: ImageGenerator
) -> Dict[str, Any]:
    """
    Enhance RAG response with visual elements
    
    Args:
        query: User's question
        answer: RAG system's text answer
        generator: ImageGenerator instance
        
    Returns:
        Enhanced response with visual elements
    """
    # Detect if visual would be helpful
    visual_keywords = ['what is', 'explain', 'show', 'example', 'difference between']
    
    needs_visual = any(keyword in query.lower() for keyword in visual_keywords)
    
    if not needs_visual:
        return {
            'answer': answer,
            'visual': None
        }
    
    # Extract concept from query
    # Simple extraction - can be improved with NLP
    if 'what is' in query.lower():
        concept = query.lower().replace('what is', '').strip('?').strip()
    else:
        concept = query.strip('?').strip()
    
    # Generate visual
    visual = generator.generate_educational_diagram(
        concept=concept,
        description=answer[:500],  # Use part of answer as description
        style="simple educational diagram"
    )
    
    return {
        'answer': answer,
        'visual': visual
    }
