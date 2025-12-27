"""Keyword extraction utilities"""
import re
from collections import Counter
from typing import List

def extract_keywords_from_content(content: str, max_keywords: int = 10) -> List[str]:
    """
    Extract keywords from content using frequency analysis
    
    Args:
        content: Text content to analyze
        max_keywords: Maximum number of keywords to return
    
    Returns:
        List of extracted keywords
    """
    if not content:
        return []
    
    # Clean text - remove markdown and special characters
    clean_text = re.sub(r'[#*`_\[\]\(\)]', '', content)
    clean_text = clean_text.lower()
    
    # Extract words (minimum 4 characters)
    words = re.findall(r'\b[a-z]{4,}\b', clean_text)
    
    # Generate bigrams (2-word phrases)
    bigrams = []
    for i in range(len(words) - 1):
        bigrams.append(f"{words[i]} {words[i+1]}")
    
    # Generate trigrams (3-word phrases)
    trigrams = []
    for i in range(len(words) - 2):
        trigrams.append(f"{words[i]} {words[i+1]} {words[i+2]}")
    
    # Count phrase frequency
    phrase_freq = Counter(bigrams + trigrams)
    
    # Stop words to filter out
    stop_words = {
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
        'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'be', 'been',
        'this', 'that', 'can', 'will', 'have', 'has', 'had', 'not', 'it',
        # API/JSON junk
        'query', 'results', 'results count', 'position', 'title', 'link',
        'snippet', 'source', 'status', 'error', 'message', 'data'
    }
    
    # Extract quality keywords
    keywords = []
    for phrase, count in phrase_freq.most_common(50):
        phrase_words = phrase.split()
        
        # Skip if contains stop words
        if any(word in stop_words for word in phrase_words):
            continue
        
        # Skip if too short
        if len(phrase) < 5:
            continue
        
        # Skip if contains numbers
        if re.search(r'\d', phrase):
            continue
        
        # Must appear at least 2 times
        if count >= 2:
            keywords.append(phrase)
            if len(keywords) >= max_keywords:
                break
    
    # Fallback to single words if no phrases found
    if not keywords:
        word_freq = Counter(words)
        keywords = [
            word for word, count in word_freq.most_common(30)
            if word not in stop_words
            and len(word) > 5
            and count >= 3
            and not re.search(r'\d', word)
        ][:max_keywords]
    
    return keywords if keywords else ["content", "quality", "information"]


def calculate_keyword_density(content: str, keyword: str) -> float:
    """
    Calculate keyword density in content
    
    Args:
        content: Text content
        keyword: Keyword to analyze
    
    Returns:
        Keyword density as percentage
    """
    if not content or not keyword:
        return 0.0
    
    # Count total words
    total_words = len(content.split())
    
    if total_words == 0:
        return 0.0
    
    # Count keyword occurrences (case-insensitive)
    keyword_count = content.lower().count(keyword.lower())
    
    # Calculate density
    density = (keyword_count / total_words) * 100
    
    return round(density, 2)


def extract_keywords_from_topic(topic: str) -> List[str]:
    """
    Extract potential keywords from topic string
    
    Args:
        topic: Topic string
    
    Returns:
        List of keywords
    """
    if not topic:
        return []
    
    # Clean and lowercase
    clean_topic = topic.lower().strip()
    
    # Split into words
    words = clean_topic.split()
    
    # Return as-is for short topics
    if len(words) <= 3:
        return [clean_topic]
    
    # For longer topics, create variations
    keywords = [clean_topic]  # Full topic
    
    # Add individual significant words (length > 4)
    for word in words:
        if len(word) > 4:
            keywords.append(word)
    
    # Add bigrams
    for i in range(len(words) - 1):
        keywords.append(f"{words[i]} {words[i+1]}")
    
    return keywords[:5]  # Return top 5
