"""
Answer generator using LLM with strict anti-hallucination prompts.
Generates answers based on retrieved context with confidence scoring.
"""

import json
from typing import Dict, Any
from config import settings, prompts
from utils.logger import get_logger

logger = get_logger(__name__)


class AnswerGenerator:
    """Generate answers using LLM with retrieved context."""
    
    def __init__(self):
        """Initialize answer generator."""
        self.provider = settings.llm_provider
        self.model_name = settings.get_llm_model()
        self.temperature = settings.llm_temperature
        self.max_tokens = settings.max_response_tokens
        
        # Initialize LLM client
        if self.provider == "openai":
            self._init_openai()
        elif self.provider == "google":
            self._init_google()
        elif self.provider == "anthropic":
            self._init_anthropic()
        else:
            raise ValueError(f"Unsupported provider: {self.provider}")
        
        logger.info(f"AnswerGenerator initialized with {self.provider}")
    
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
    
    def generate_answer(
        self,
        query: str,
        context: str,
        graph_context: str = "",
        sources: list = None
    ) -> Dict[str, Any]:
        """Generate answer for query using context.
        
        Args:
            query: User's question
            context: Retrieved context from documents
            graph_context: Context from knowledge graph
            sources: List of source metadata
            
        Returns:
            Dictionary with answer, confidence, sources, and reasoning
        """
        logger.info(f"Generating answer for query: {query[:100]}...")
        
        try:
            # Create prompt
            prompt = prompts.ANSWER_GENERATION_PROMPT.format(
                context=context,
                graph_context=graph_context or "No graph context available",
                question=query
            )
            
            # Call LLM
            if self.provider == "openai":
                response = self._call_openai(prompt)
            elif self.provider == "google":
                response = self._call_google(prompt)
            elif self.provider == "anthropic":
                response = self._call_anthropic(prompt)
            
            # Parse response
            parsed = self._parse_response(response)
            
            # Add sources
            parsed['sources'] = sources or []
            
            # Calculate confidence score
            confidence_score = self._calculate_confidence(
                answer=parsed['answer'],
                context=context,
                query=query
            )
            parsed['confidence_score'] = confidence_score
            
            logger.info(f"Answer generated: confidence={parsed['confidence']}")
            return parsed
            
        except Exception as e:
            logger.error(f"Answer generation failed: {e}")
            return {
                'answer': "I apologize, but I encountered an error generating an answer.",
                'confidence': 'Low',
                'confidence_score': 0.0,
                'sources': [],
                'reasoning': f"Error: {str(e)}"
            }
    
    def _call_openai(self, prompt: str) -> str:
        """Call OpenAI API."""
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {"role": "system", "content": "You are a highly accurate question-answering system."},
                {"role": "user", "content": prompt}
            ],
            temperature=self.temperature,
            max_tokens=self.max_tokens
        )
        return response.choices[0].message.content
    
    def _call_google(self, prompt: str) -> str:
        """Call Google API."""
        model = self.client.GenerativeModel(self.model_name)
        response = model.generate_content(
            prompt,
            generation_config={
                'temperature': self.temperature,
                'max_output_tokens': self.max_tokens
            }
        )
        return response.text
    
    def _call_anthropic(self, prompt: str) -> str:
        """Call Anthropic API."""
        response = self.client.messages.create(
            model=self.model_name,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return response.content[0].text
    
    def _parse_response(self, response: str) -> Dict[str, Any]:
        """Parse LLM response into structured format.
        
        Args:
            response: Raw LLM response
            
        Returns:
            Parsed response dictionary
        """
        # Initialize default structure
        parsed = {
            'answer': '',
            'confidence': 'Medium',
            'sources': [],
            'reasoning': ''
        }
        
        # Try to extract sections
        lines = response.split('\n')
        current_section = None
        section_content = []
        
        for line in lines:
            line = line.strip()
            
            if line.startswith('ANSWER:'):
                if current_section:
                    parsed[current_section] = '\n'.join(section_content).strip()
                current_section = 'answer'
                section_content = [line.replace('ANSWER:', '').strip()]
            elif line.startswith('CONFIDENCE:'):
                if current_section:
                    parsed[current_section] = '\n'.join(section_content).strip()
                current_section = 'confidence'
                section_content = [line.replace('CONFIDENCE:', '').strip()]
            elif line.startswith('SOURCES:'):
                if current_section:
                    parsed[current_section] = '\n'.join(section_content).strip()
                current_section = 'sources'
                section_content = []
            elif line.startswith('REASONING:'):
                if current_section:
                    if current_section == 'sources':
                        parsed[current_section] = section_content
                    else:
                        parsed[current_section] = '\n'.join(section_content).strip()
                current_section = 'reasoning'
                section_content = [line.replace('REASONING:', '').strip()]
            elif line and current_section:
                if current_section == 'sources' and line.startswith('-'):
                    section_content.append(line.replace('-', '').strip())
                else:
                    section_content.append(line)
        
        # Add last section
        if current_section:
            if current_section == 'sources':
                parsed[current_section] = section_content
            else:
                parsed[current_section] = '\n'.join(section_content).strip()
        
        # If parsing failed, use entire response as answer
        if not parsed['answer']:
            parsed['answer'] = response
        
        return parsed
    
    def _calculate_confidence(
        self,
        answer: str,
        context: str,
        query: str
    ) -> float:
        """Calculate numerical confidence score.
        
        Args:
            answer: Generated answer
            context: Retrieved context
            query: Original query
            
        Returns:
            Confidence score (0-1)
        """
        # Simple heuristics for confidence
        score = 0.5  # Base score
        
        # Check if answer indicates uncertainty
        uncertainty_phrases = [
            "i don't have enough information",
            "i cannot answer",
            "i'm not sure",
            "unclear",
            "insufficient information"
        ]
        
        answer_lower = answer.lower()
        if any(phrase in answer_lower for phrase in uncertainty_phrases):
            score = 0.2
        else:
            # Check answer length (very short might be uncertain)
            if len(answer) < 50:
                score -= 0.1
            elif len(answer) > 100:
                score += 0.1
            
            # Check if context is substantial
            if len(context) > 500:
                score += 0.1
            
            # Check if answer contains specific details
            if any(char.isdigit() for char in answer):
                score += 0.05
            
            # Cap at 0.95 (never 100% certain)
            score = min(score, 0.95)
        
        return max(0.0, min(1.0, score))
