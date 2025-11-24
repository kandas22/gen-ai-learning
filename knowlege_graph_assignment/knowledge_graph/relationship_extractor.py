"""
Relationship extraction from text using LLM.
Identifies relationships between entities.
"""

import json
from typing import List, Dict, Any
from config import settings, prompts
from utils.logger import get_logger

logger = get_logger(__name__)


class RelationshipExtractor:
    """Extract relationships between entities using LLM."""
    
    def __init__(self):
        """Initialize relationship extractor."""
        self.provider = settings.llm_provider
        self.model_name = settings.get_llm_model()
        
        # Initialize LLM client
        if self.provider == "openai":
            self._init_openai()
        elif self.provider == "google":
            self._init_google()
        elif self.provider == "anthropic":
            self._init_anthropic()
        else:
            raise ValueError(f"Unsupported provider: {self.provider}")
        
        logger.info(f"RelationshipExtractor initialized with {self.provider}")
    
    def _init_openai(self):
        """Initialize OpenAI client."""
        from openai import OpenAI
        self.client = OpenAI(api_key=settings.get_llm_api_key())
    
    def _init_google(self):
        """Initialize Google client."""
        import google.generativeai as genai
        genai.configure(api_key=settings.get_llm_api_key())
        self.client = genai
    
    def _init_anthropic(self):
        """Initialize Anthropic client."""
        from anthropic import Anthropic
        self.client = Anthropic(api_key=settings.get_llm_api_key())
    
    def extract_relationships(
        self,
        text: str,
        entities: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Extract relationships between entities in text.
        
        Args:
            text: Input text
            entities: List of entities found in the text
            
        Returns:
            List of relationship dictionaries
        """
        if not text or not entities or len(entities) < 2:
            return []
        
        try:
            # Format entities for prompt
            entities_str = json.dumps(entities, indent=2)
            
            # Create prompt
            prompt = prompts.RELATIONSHIP_EXTRACTION_PROMPT.format(
                entities=entities_str,
                text=text
            )
            
            # Call LLM
            if self.provider == "openai":
                response = self._call_openai(prompt)
            elif self.provider == "google":
                response = self._call_google(prompt)
            elif self.provider == "anthropic":
                response = self._call_anthropic(prompt)
            
            # Parse JSON response
            relationships = self._parse_relationships(response)
            
            logger.info(f"Extracted {len(relationships)} relationships from text")
            return relationships
            
        except Exception as e:
            logger.error(f"Relationship extraction failed: {e}")
            return []
    
    def _call_openai(self, prompt: str) -> str:
        """Call OpenAI API."""
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {"role": "system", "content": "You are an expert relationship extraction system. Always return valid JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.1,
            response_format={"type": "json_object"}
        )
        return response.choices[0].message.content
    
    def _call_google(self, prompt: str) -> str:
        """Call Google API."""
        model = self.client.GenerativeModel(self.model_name)
        response = model.generate_content(
            prompt,
            generation_config={
                'temperature': 0.1
            }
        )
        return response.text
    
    def _call_anthropic(self, prompt: str) -> str:
        """Call Anthropic API."""
        response = self.client.messages.create(
            model=self.model_name,
            max_tokens=2000,
            temperature=0.1,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return response.content[0].text
    
    def _parse_relationships(self, response: str) -> List[Dict[str, Any]]:
        """Parse relationships from LLM response.
        
        Args:
            response: JSON response from LLM
            
        Returns:
            List of parsed relationships
        """
        try:
            # Clean response string (remove markdown code blocks)
            response = response.strip()
            if response.startswith("```json"):
                response = response[7:]
            elif response.startswith("```"):
                response = response[3:]
            if response.endswith("```"):
                response = response[:-3]
            response = response.strip()

            data = json.loads(response)
            
            # Handle different response formats
            if isinstance(data, list):
                relationships = data
            elif isinstance(data, dict) and 'relationships' in data:
                relationships = data['relationships']
            else:
                logger.warning(f"Unexpected response format: {data}")
                return []
            
            # Validate and clean relationships
            cleaned_relationships = []
            for rel in relationships:
                if self._validate_relationship(rel):
                    cleaned_relationships.append({
                        'source': rel.get('source', ''),
                        'relationship': rel.get('relationship', 'RELATED_TO'),
                        'target': rel.get('target', ''),
                        'confidence': float(rel.get('confidence', 0.5)),
                        'evidence': rel.get('evidence', '')
                    })
            
            return cleaned_relationships
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response: {e}")
            return []
    
    def _validate_relationship(self, relationship: Dict[str, Any]) -> bool:
        """Validate relationship structure.
        
        Args:
            relationship: Relationship dictionary
            
        Returns:
            True if valid
        """
        required_fields = ['source', 'relationship', 'target']
        return all(field in relationship for field in required_fields)
    
    def deduplicate_relationships(
        self,
        relationships: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Remove duplicate relationships.
        
        Args:
            relationships: List of relationships
            
        Returns:
            Deduplicated list
        """
        seen = set()
        unique_relationships = []
        
        for rel in relationships:
            # Create key from source, relationship, target
            key = (
                rel['source'].lower(),
                rel['relationship'],
                rel['target'].lower()
            )
            
            if key not in seen:
                seen.add(key)
                unique_relationships.append(rel)
            else:
                # Update confidence if higher
                for existing in unique_relationships:
                    existing_key = (
                        existing['source'].lower(),
                        existing['relationship'],
                        existing['target'].lower()
                    )
                    if existing_key == key:
                        if rel['confidence'] > existing['confidence']:
                            existing['confidence'] = rel['confidence']
                            existing['evidence'] = rel['evidence']
                        break
        
        return unique_relationships
