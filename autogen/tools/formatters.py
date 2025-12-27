"""Output formatting utilities"""
import re
import ast
from typing import Dict, Any

def format_research_output(raw_output: str) -> str:
    """
    Format raw research output into readable markdown
    
    Args:
        raw_output: Raw output from research agent
    
    Returns:
        Formatted markdown string
    """
    formatted = "## 🔍 Research Summary\n\n"
    
    try:
        # Find all dict start positions
        start_positions = [m.start() for m in re.finditer(r"\{'query':", raw_output)]
        dicts_found = []
        
        for start_pos in start_positions:
            substr = raw_output[start_pos:]
            
            # Count braces to find dict end
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
                dict_str = substr[:end_pos]
                try:
                    data = ast.literal_eval(dict_str)
                    if isinstance(data, dict) and 'query' in data:
                        dicts_found.append(data)
                except:
                    continue
        
        # Format extracted dicts
        if dicts_found:
            for idx, data in enumerate(dicts_found, 1):
                formatted += f"### 🔎 Search Query {idx}\n"
                formatted += f"**Topic:** {data.get('query', 'N/A')}\n\n"
                formatted += f"**Results Found:** {data.get('results_count', 0)}\n\n"
                
                results = data.get('results', [])
                if results:
                    formatted += "**Top Sources:**\n\n"
                    
                    for i, result in enumerate(results[:5], 1):
                        if isinstance(result, dict):
                            formatted += f"**{i}. {result.get('title', 'No title')}**\n"
                            formatted += f"   - 🏢 *Source:* {result.get('source', 'Unknown')}\n"
                            formatted += f"   - 📝 *Summary:* {result.get('snippet', 'N/A')}\n"
                            formatted += f"   - 🔗 *Link:* [{result.get('link', '#')}]({result.get('link', '#')})\n\n"
                
                formatted += "---\n\n"
            
            formatted += "\n💡 **Keywords will be extracted from these sources.**\n"
            return formatted
        
        # Fallback: regex extraction
        else:
            queries = re.findall(r"'query':\s*'([^']+)'", raw_output)
            titles = re.findall(r"'title':\s*'([^']+)'", raw_output)
            links = re.findall(r"'link':\s*'([^']+)'", raw_output)
            snippets = re.findall(r"'snippet':\s*'([^']+)'", raw_output)
            sources = re.findall(r"'source':\s*'([^']+)'", raw_output)
            
            if queries:
                formatted += f"### 🔎 Search Query\n**Topic:** {queries[0]}\n\n"
            
            if titles and links:
                formatted += "**Top Sources:**\n\n"
                max_items = min(len(titles), len(links), 5)
                
                for i in range(max_items):
                    formatted += f"**{i+1}. {titles[i]}**\n"
                    if i < len(sources):
                        formatted += f"   - 🏢 *Source:* {sources[i]}\n"
                    if i < len(snippets):
                        formatted += f"   - 📝 *Summary:* {snippets[i]}\n"
                    formatted += f"   - 🔗 *Link:* [{links[i]}]({links[i]})\n\n"
                
                formatted += "\n💡 **Content will be generated from these findings.**\n"
                return formatted
    
    except Exception as e:
        print(f"Parse error: {e}")
    
    formatted += "⚠️ Parsing failed.\n```\n" + raw_output[:1000] + "...\n```\n"
    return formatted
