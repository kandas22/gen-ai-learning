"""
Entity extraction from text using LLM.
Identifies and extracts named entities with types and confidence scores.
"""

import json
from typing import List, Dict, Any
from config import settings, prompts
from utils.logger import get_logger

logger = get_logger(__name__)


class EntityExtractor:
    """Extract entities from text using LLM."""
    
    def __init__(self):
        """Initialize entity extractor."""
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
        
        logger.info(f"EntityExtractor initialized with {self.provider}")
    
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
    
    def extract_entities(self, text: str) -> List[Dict[str, Any]]:
        """Extract entities from text.
        
        Args:
            text: Input text
            
        Returns:
            List of entity dictionaries
        """
        if not text or len(text.strip()) < 10:
            return []
        
        try:
            # Create prompt
            prompt = prompts.ENTITY_EXTRACTION_PROMPT.format(text=text)
            
            # Call LLM
            if self.provider == "openai":
                response = self._call_openai(prompt)
            elif self.provider == "google":
                response = self._call_google(prompt)
            elif self.provider == "anthropic":
                response = self._call_anthropic(prompt)
            
            # Parse JSON response
            entities = self._parse_entities(response)
            
            logger.info(f"Extracted {len(entities)} entities from text")
            return entities
            
        except Exception as e:
            logger.error(f"Entity extraction failed: {e}")
            return []
    
    def _call_openai(self, prompt: str) -> str:
        """Call OpenAI API.
        
        Args:
            prompt: Input prompt
            
        Returns:
            Response text
        """
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {"role": "system", "content": "You are an expert entity extraction system. Always return valid JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.1,
            response_format={"type": "json_object"}
        )
        return response.choices[0].message.content
    
    def _call_google(self, prompt: str) -> str:
        """Call Google API.
        
        Args:
            prompt: Input prompt
            
        Returns:
            Response text
        """
        model = self.client.GenerativeModel(self.model_name)
        response = model.generate_content(
            prompt,
            generation_config={
                'temperature': 0.1
            }
        )
        return response.text
    
    def _call_anthropic(self, prompt: str) -> str:
        """Call Anthropic API.
        
        Args:
            prompt: Input prompt
            
        Returns:
            Response text
        """
        response = self.client.messages.create(
            model=self.model_name,
            max_tokens=2000,
            temperature=0.1,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return response.content[0].text
    
    def _parse_entities(self, response: str) -> List[Dict[str, Any]]:
        """Parse entities from LLM response.
        
        Args:
            response: JSON response from LLM
            
        Returns:
            List of parsed entities
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

            # Try to parse as JSON
            data = json.loads(response)
            
            # Handle different response formats
            if isinstance(data, list):
                entities = data
            elif isinstance(data, dict) and 'entities' in data:
                entities = data['entities']
            else:
                logger.warning(f"Unexpected response format: {data}")
                return []
            
            # Validate and clean entities
            cleaned_entities = []
            for entity in entities:
                if self._validate_entity(entity):
                    cleaned_entities.append({
                        'text': entity.get('text', ''),
                        'type': entity.get('type', 'UNKNOWN'),
                        'confidence': float(entity.get('confidence', 0.5)),
                        'context': entity.get('context', '')
                    })
            
            return cleaned_entities
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response: {e}")
            logger.debug(f"Response: {response}")
            return []
    
    def _validate_entity(self, entity: Dict[str, Any]) -> bool:
        """Validate entity structure.
        
        Args:
            entity: Entity dictionary
            
        Returns:
            True if valid
        """
        required_fields = ['text', 'type']
        return all(field in entity for field in required_fields)
    
    def extract_entities_batch(
        self,
        texts: List[str],
        show_progress: bool = True
    ) -> List[List[Dict[str, Any]]]:
        """Extract entities from multiple texts.
        
        Args:
            texts: List of input texts
            show_progress: Whether to show progress
            
        Returns:
            List of entity lists
        """
        all_entities = []
        
        for i, text in enumerate(texts):
            if show_progress and i % 10 == 0:
                logger.info(f"Processing text {i+1}/{len(texts)}")
            
            entities = self.extract_entities(text)
            all_entities.append(entities)
        
        return all_entities
    
    def deduplicate_entities(
        self,
        entities: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Remove duplicate entities.
        
        Args:
            entities: List of entities
            
        Returns:
            Deduplicated list
        """
        seen = set()
        unique_entities = []
        
        for entity in entities:
            # Create key from text and type
            key = (entity['text'].lower(), entity['type'])
            
            if key not in seen:
                seen.add(key)
                unique_entities.append(entity)
            else:
                # Update confidence if higher
                for existing in unique_entities:
                    if (existing['text'].lower(), existing['type']) == key:
                        if entity['confidence'] > existing['confidence']:
                            existing['confidence'] = entity['confidence']
                        break
        
        return unique_entities
