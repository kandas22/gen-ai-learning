"""
Workflow Orchestration for SEO Content Generator
Complete implementation with all methods extracted from original file
"""

import asyncio
import re
from typing import Dict, Any, Optional, Callable, List
from collections import Counter
import ast

# Import from other modules
from config import Config
from core.agents import AgentFactory
from core.seo_scoring import calculate_seo_score, format_seo_output
from tools.search import search_web
from autogen_ext.models.openai import OpenAIChatCompletionClient


class WorkflowOrchestrator:
    """
    Orchestrates the multi-agent SEO content generation workflow
    Uses round-robin execution pattern
    """
    
    def __init__(self, status_callback: Optional[Callable] = None):
        """
        Initialize workflow orchestrator
        
        Args:
            status_callback: Optional callback for status updates
        """
        self.status_callback = status_callback
        self.model_client = None
        self.agents = {}
        self.workflow_state = {}
        
        # Initialize model client
        self.model_client = OpenAIChatCompletionClient(
            model=Config.DEFAULT_MODEL,
            api_key=Config.OPENAI_API_KEY
        )
        
        # Create agents using factory
        self._create_agents()
    
    def _create_agents(self):
        """Create all agents using the factory"""
        factory = AgentFactory(self.model_client)
        
        self.agents = {
            "research": factory.create_research_agent(),
            "content": factory.create_content_agent(),
            "verification": factory.create_verification_agent(),
            "seo_scoring": factory.create_seo_agent(),
            "email_delivery": factory.create_email_agent()
        }
    
    async def execute_workflow(
        self,
        topic: str,
        field: str,
        recipient_email: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Execute the complete SEO content generation workflow
        
        Args:
            topic: Content topic/subject
            field: Domain or field (e.g., "Technology", "Healthcare", or "Any")
            recipient_email: Optional email address for delivery
        
        Returns:
            Dictionary containing all workflow outputs
        """
        results = {
            "topic": topic,
            "field": field,
            "research_output": None,
            "generated_content": None,
            "verification_output": None,
            "seo_score": None,
            "email_status": None,
            "status": "started"
        }
        
        try:
            # Step 1: Research Phase
            if self.status_callback:
                self.status_callback("research", "running", "Conducting research...")
            
            research_output = await self._execute_research(topic, field)
            results["research_output"] = research_output
            
            if self.status_callback:
                self.status_callback("research", "completed", "Research completed")
            
            # Step 2: Content Generation Phase
            if self.status_callback:
                self.status_callback("content", "running", "Generating content...")
            
            content_output = await self._execute_content_generation(
                topic, field, research_output
            )
            results["generated_content"] = content_output
            
            if self.status_callback:
                self.status_callback("content", "completed", "Content generated")
            
            # Step 3: Verification Phase
            if self.status_callback:
                self.status_callback("verification", "running", "Verifying quality...")
            
            verification_output = await self._execute_verification(
                content_output, research_output
            )
            results["verification_output"] = verification_output
            
            if self.status_callback:
                self.status_callback("verification", "completed", "Verification completed")
            
            # Step 4: SEO Scoring Phase
            if self.status_callback:
                self.status_callback("seo_scoring", "running", "Analyzing SEO...")
            
            seo_output = await self._execute_seo_scoring(
                content_output, research_output
            )
            results["seo_score"] = seo_output
            
            if self.status_callback:
                self.status_callback("seo_scoring", "completed", "SEO analysis completed")
            
            # Step 5: Email Delivery Phase (if recipient provided)
            if recipient_email:
                if self.status_callback:
                    self.status_callback("email_delivery", "running", "Sending email...")
                
                email_output = await self._execute_email_delivery(
                    recipient_email, topic, content_output, seo_output
                )
                results["email_status"] = email_output
                
                if self.status_callback:
                    self.status_callback("email_delivery", "completed", "Email sent")
            
            results["status"] = "completed"
            
        except Exception as e:
            results["status"] = "error"
            results["error"] = str(e)
            if self.status_callback:
                self.status_callback("workflow", "error", str(e))
        
        return results
    
    async def _execute_research(self, topic: str, field: str) -> str:
        """Execute research phase"""
        research_agent = self.agents["research"]
        
        # Adjust prompt based on field
        if "Any" in field:
            field_instruction = "Conduct broad research across multiple domains and perspectives."
        else:
            field_instruction = f"Focus specifically on the {field} domain with industry-specific terminology and sources."
        
        prompt = f"""Conduct comprehensive research on: {topic}

Field: {field}

{field_instruction}

**Use search_web to find 2024-2025 information, then provide:**

## Research Summary

### Main Topic: {topic}

### Key Findings:
- [Finding 1 with source]
- [Finding 2 with source]
- [Finding 3 with source]

### Primary SEO Keywords:
1. [keyword 1]
2. [keyword 2]
3. [keyword 3]

### Top Sources:
1. [Title] - [Source] - [URL]
2. [Title] - [Source] - [URL]

### Recommended Angles:
- [Angle 1]
- [Angle 2]

Use the search_web tool to gather information."""

        try:
            response = await research_agent.run(task=prompt)
            
            if hasattr(response, 'messages') and response.messages:
                raw_output = response.messages[-1].content
            elif hasattr(response, 'content'):
                raw_output = response.content
            else:
                raw_output = str(response)
            
            formatted_output = self._format_research_output(raw_output)
            return formatted_output
        
        except Exception as e:
            return f"Research error: {str(e)}"
    
    async def _execute_content_generation(self, topic: str, field: str, research_output: str) -> str:
        """Execute content generation phase"""
        content_agent = self.agents["content"]
        
        prompt = f"""Create SEO-optimized article:

Topic: {topic}
Field: {field}

Research:
{research_output}

REQUIREMENTS:
1. WORD COUNT: 1500-1800 words
2. KEYWORD DENSITY: 2.0-2.5% (30-35 total uses)
3. STRUCTURE: H1 (1) → H2 (5-7) → H3 (8-12)

Write comprehensive, professional content with natural keyword integration."""

        try:
            response = await content_agent.run(task=prompt)
            
            if hasattr(response, 'messages') and response.messages:
                return response.messages[-1].content
            elif hasattr(response, 'content'):
                return response.content
            else:
                return str(response)
        except Exception as e:
            return f"Content generation error: {str(e)}"
    
    async def _execute_verification(self, content: str, research_output: str) -> str:
        """Execute verification phase"""
        verification_agent = self.agents["verification"]
        
        prompt = f"""Verify content accuracy:

CONTENT:
{content}

RESEARCH:
{research_output}

Verify:
1. Factual accuracy
2. Alignment with sources
3. Quality of claims
4. Content integrity

Provide verification report."""

        try:
            response = await verification_agent.run(task=prompt)
            
            if hasattr(response, 'messages') and response.messages:
                return response.messages[-1].content
            elif hasattr(response, 'content'):
                return response.content
            else:
                return str(response)
        except Exception as e:
            return f"Verification error: {str(e)}"
    
    async def _execute_seo_scoring(self, content: str, research_output: str) -> Dict[str, Any]:
        """Execute SEO scoring phase"""
        keywords = self._extract_keywords(research_output)
        
        try:
            raw_score = calculate_seo_score(content, keywords)
            formatted_analysis = format_seo_output(raw_score)
            
            return {
                "analysis": formatted_analysis,
                "keywords_used": keywords,
                "raw_data": raw_score
            }
        except Exception as e:
            return {
                "analysis": f"SEO scoring error: {str(e)}",
                "keywords_used": keywords
            }
    
    async def _execute_email_delivery(
        self, recipient_email: str, topic: str, content: str, seo_output: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute email delivery"""
        from tools.email_sender import send_email
        
        seo_analysis = seo_output.get("analysis", "SEO analysis unavailable")
        
        try:
            return await send_email(
                recipient=recipient_email,
                subject=f"SEO Content: {topic}",
                content=content,
                seo_score=seo_analysis
            )
        except Exception as e:
            return {"status": "error", "message": f"Email failed: {str(e)}"}
    
    def _format_research_output(self, raw_output: str) -> str:
        """Format research output"""
        formatted = "## 🔍 Research Summary\n\n"
        
        try:
            start_positions = [m.start() for m in re.finditer(r"\{'query':", raw_output)]
            dicts_found = []
            
            for start_pos in start_positions:
                substr = raw_output[start_pos:]
                brace_count = 0
                end_pos = 0
                
                for i, char in enumerate(substr):
                    if char == '{':
                        brace_count += 1
                    elif char == '}':
                        brace_count -= 1
                        if brace_count == 0:
                            end_pos = i + 1
                            break
                
                if end_pos > 0:
                    try:
                        data = ast.literal_eval(substr[:end_pos])
                        if isinstance(data, dict) and 'query' in data:
                            dicts_found.append(data)
                    except:
                        continue
            
            if dicts_found:
                for idx, data in enumerate(dicts_found, 1):
                    formatted += f"### 🔎 Search {idx}\n**Topic:** {data.get('query', 'N/A')}\n\n"
                    formatted += f"**Results:** {data.get('results_count', 0)}\n\n**Top Sources:**\n\n"
                    
                    for i, result in enumerate(data.get('results', [])[:5], 1):
                        if isinstance(result, dict):
                            formatted += f"**{i}. {result.get('title', 'No title')}**\n"
                            formatted += f"   - *Source:* {result.get('source', 'Unknown')}\n"
                            formatted += f"   - *Summary:* {result.get('snippet', 'N/A')}\n"
                            formatted += f"   - [Link]({result.get('link', '#')})\n\n"
                    formatted += "---\n\n"
                
                formatted += "💡 Keywords will be extracted.\n"
                return formatted
        except:
            pass
        
        return formatted + raw_output[:1000] if raw_output else formatted
    
    def _extract_keywords(self, research_output: str) -> List[str]:
        """Extract keywords from research"""
        keywords = []
        
        for line in research_output.split('\n'):
            if any(x in line.lower() for x in ['keyword', 'key phrase']):
                cleaned = re.sub(r'^[\s\-\*\d\.•]+', '', line).strip()
                if cleaned and len(cleaned.split()) <= 5:
                    keywords.append(cleaned)
        
        if not keywords:
            words = re.findall(r'\b[a-z]{4,}\b', research_output.lower())
            keywords = [w for w, c in Counter(words).most_common(10) if c >= 3]
        
        return keywords[:10] or ["content", "quality", "optimization"]
