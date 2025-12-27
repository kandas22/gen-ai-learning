"""Agent factory for creating specialized agents"""
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from tools.search import search_web

class AgentFactory:
    """Factory for creating specialized agents"""
    
    def __init__(self, model_client: OpenAIChatCompletionClient):
        self.model_client = model_client
    
    def create_research_agent(self) -> AssistantAgent:
        """Create research agent with search capabilities"""
        system_message = """You are an expert Research Agent.

Your responsibilities:
1. Conduct thorough web searches using the search_web tool
2. Identify 5-10 primary SEO keywords
3. Find authoritative sources (2024-2025)
4. Extract key insights with temporal context
5. Provide structured research summary

Output format:
- Research Summary
- Primary Keywords (list 5-10 clearly)
- Key Sources with links
- Recommended content angles
"""
        
        return AssistantAgent(
            name="research_agent",
            model_client=self.model_client,
            system_message=system_message,
            tools=[search_web]
        )
    
    def create_content_agent(self) -> AssistantAgent:
        """Create content generation agent"""
        system_message = """You are an expert Content Generation Agent.

Your responsibilities:
1. Create engaging, long-form content (1500-1800 words)
2. Use proper heading hierarchy (H1, H2, H3)
3. TARGET: 2.0-2.5% keyword density
4. Write in clear, professional language
5. Structure content for readability

KEYWORD INTEGRATION:
- For 1500 words: Use keywords 30-35 times total
- Natural placement only
- Avoid keyword stuffing

Content Requirements:
- One H1 title with main keyword
- 5-7 H2 sections
- 8-12 H3 subsections
- Target: 1500-1800 words
- Clear paragraphs (3-5 sentences each)

Writing Style:
- Professional yet accessible
- Active voice preferred
- Sentence length: 15-20 words average
- Include specific examples
"""
        
        return AssistantAgent(
            name="content_generation_agent",
            model_client=self.model_client,
            system_message=system_message
        )
    
    def create_verification_agent(self) -> AssistantAgent:
        """Create verification agent"""
        system_message = """You are an expert Verification Agent.

Your responsibilities:
1. Verify factual claims against research data
2. Check for outdated or incorrect information
3. Ensure alignment with source materials
4. Identify weak or unsupported claims
5. Validate overall content quality

Verification Checklist:
- Are facts accurate and current?
- Do claims align with research sources?
- Are statistics and data points correct?
- Is the content free from misinformation?
- Are there any logical inconsistencies?

Output format:
- Verification Status (PASSED/NEEDS_REVISION)
- Accurate Claims (list)
- Issues Found (list with severity)
- Improvement Recommendations
"""
        
        return AssistantAgent(
            name="verification_agent",
            model_client=self.model_client,
            system_message=system_message
        )
    
    def create_seo_agent(self) -> AssistantAgent:
        """Create SEO scoring agent"""
        system_message = """You are an SEO Analysis Expert.

Analyze content for:
1. Keyword optimization
2. Content structure
3. Readability
4. SEO best practices

Provide detailed scores and recommendations."""
        
        return AssistantAgent(
            name="seo_scoring_agent",
            model_client=self.model_client,
            system_message=system_message
        )
    
    def create_email_agent(self) -> AssistantAgent:
        """Create email delivery agent"""
        system_message = """You are an Email Delivery Agent.

Format and send professional emails with:
1. Clear subject lines
2. Well-structured content
3. SEO analysis summary
4. Professional formatting
"""
        
        return AssistantAgent(
            name="email_delivery_agent",
            model_client=self.model_client,
            system_message=system_message
        )
