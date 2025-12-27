"""SEO scoring and analysis"""
import re
from typing import Dict, Any, List
from collections import Counter

def calculate_seo_score(content: str, keywords: List[str]) -> Dict[str, Any]:
    """
    Calculate comprehensive SEO score
    
    NOTE: This is a placeholder. Extract the full calculate_seo_score
    function from your original file (around line 219-350).
    """
    score = 0
    max_score = 100
    metrics = {}
    
    # Content length (20 points)
    words = content.split()
    word_count = len(words)
    
    if word_count >= 1500:
        length_score = 20
    elif word_count >= 1000:
        length_score = 15
    elif word_count >= 500:
        length_score = 10
    else:
        length_score = 5
    
    score += length_score
    metrics['word_count'] = word_count
    metrics['length_score'] = length_score
    
    # Keyword density (25 points)
    if keywords:
        total_keyword_uses = sum(
            content.lower().count(kw.lower()) for kw in keywords
        )
        keyword_density = (total_keyword_uses / word_count * 100) if word_count > 0 else 0
        
        if 1.5 <= keyword_density <= 2.5:
            keyword_score = 25
        elif 1.0 <= keyword_density < 1.5 or 2.5 < keyword_density <= 3.5:
            keyword_score = 20
        elif 0.5 <= keyword_density < 1.0 or 3.5 < keyword_density <= 5.0:
            keyword_score = 15
        else:
            keyword_score = 10
        
        score += keyword_score
        metrics['keyword_density'] = round(keyword_density, 2)
        metrics['keyword_score'] = keyword_score
    
    # Heading structure (20 points)
    h1_count = len(re.findall(r'^#\s+', content, re.MULTILINE))
    h2_count = len(re.findall(r'^##\s+', content, re.MULTILINE))
    h3_count = len(re.findall(r'^###\s+', content, re.MULTILINE))
    
    structure_score = 0
    if h1_count == 1:
        structure_score += 5
    if h2_count >= 3:
        structure_score += 8
    if h3_count >= 2:
        structure_score += 7
    
    score += structure_score
    metrics['headings'] = {'h1': h1_count, 'h2': h2_count, 'h3': h3_count}
    metrics['structure_score'] = structure_score
    
    # Readability (20 points)
    sentences = re.split(r'[.!?]+', content)
    sentences = [s.strip() for s in sentences if s.strip()]
    
    if sentences:
        avg_sentence_length = sum(len(s.split()) for s in sentences) / len(sentences)
        
        if 15 <= avg_sentence_length <= 20:
            readability_score = 20
        elif 12 <= avg_sentence_length < 15 or 20 < avg_sentence_length <= 25:
            readability_score = 15
        else:
            readability_score = 10
        
        score += readability_score
        metrics['avg_sentence_length'] = round(avg_sentence_length, 1)
        metrics['readability_score'] = readability_score
    
    # Uniqueness (15 points)
    unique_sentences = len(set(sentences))
    uniqueness_ratio = unique_sentences / len(sentences) if sentences else 0
    
    uniqueness_score = int(uniqueness_ratio * 15)
    score += uniqueness_score
    
    metrics['uniqueness_ratio'] = round(uniqueness_ratio, 2)
    metrics['uniqueness_score'] = uniqueness_score
    
    # Calculate grade
    percentage = (score / max_score) * 100
    
    if percentage >= 90:
        grade = "A+ (Excellent)"
    elif percentage >= 80:
        grade = "A (Very Good)"
    elif percentage >= 70:
        grade = "B (Good)"
    elif percentage >= 60:
        grade = "C (Fair)"
    else:
        grade = "D (Needs Improvement)"
    
    # Recommendations
    recommendations = []
    if word_count < 1500:
        recommendations.append(f"✨ Aim for 1500+ words (current: {word_count})")
    if 'keyword_density' in metrics:
        if metrics['keyword_density'] < 1.0:
            recommendations.append(f"🎯 Keyword density too low ({metrics['keyword_density']}%). Target: 1-3%")
        elif metrics['keyword_density'] > 3.0:
            recommendations.append(f"⚡ Keyword density high ({metrics['keyword_density']}%). Optimal: 1-3%")
    
    return {
        'total_score': score,
        'max_score': max_score,
        'percentage': round(percentage, 1),
        'grade': grade,
        'metrics': metrics,
        'recommendations': recommendations
    }


def format_seo_output(seo_data: Dict[str, Any]) -> str:
    """Format SEO analysis into readable output without '=' characters"""
    total_score = seo_data.get('total_score', 0)
    max_score = seo_data.get('max_score', 100)
    percentage = seo_data.get('percentage', 0)
    grade = seo_data.get('grade', 'N/A')
    metrics = seo_data.get('metrics', {})
    recommendations = seo_data.get('recommendations', [])
    
    # Emoji based on score
    if percentage >= 90:
        emoji = "🏆"
    elif percentage >= 80:
        emoji = "⭐"
    elif percentage >= 70:
        emoji = "✅"
    else:
        emoji = "⚠️"
    
    output = f"""
📊 SEO PERFORMANCE ANALYSIS REPORT


🎯 OVERALL SCORE
--------------------------------------------------------------------------------
   Score: {total_score}/{max_score} ({percentage}%)
   Grade: {grade}
   Rating: {emoji}

📈 DETAILED METRICS
--------------------------------------------------------------------------------
   📝 Content Length:
      Words: {metrics.get('word_count', 0)}
      Score: {metrics.get('length_score', 0)}/20
      Status: {'✅ Excellent' if metrics.get('word_count', 0) >= 1500 else '⚠️ Could be longer'}

   🎯 Keyword Optimization:
      Density: {metrics.get('keyword_density', 0)}% (Optimal: 1-3%)
      Score: {metrics.get('keyword_score', 0)}/25
      Status: {'✅ Perfect' if 1.5 <= metrics.get('keyword_density', 0) <= 2.5 else '⚠️ Needs adjustment'}

   📑 Content Structure:
      H1 Headings: {metrics.get('headings', {}).get('h1', 0)} (Optimal: 1)
      H2 Headings: {metrics.get('headings', {}).get('h2', 0)} (Optimal: 3+)
      H3 Headings: {metrics.get('headings', {}).get('h3', 0)} (Optimal: 2+)
      Score: {metrics.get('structure_score', 0)}/20
      Status: ✅ Good Structure

   📖 Readability:
      Avg Sentence Length: {metrics.get('avg_sentence_length', 0)} words
      Score: {metrics.get('readability_score', 0)}/20
      Status: ✅ Good

   ✨ Content Uniqueness:
      Unique Sentences: {int(metrics.get('uniqueness_ratio', 0) * 100)}%
      Score: {metrics.get('uniqueness_score', 0)}/15
      Status: ✅ Unique

💡 RECOMMENDATIONS
--------------------------------------------------------------------------------
"""
    
    if recommendations:
        for rec in recommendations:
            output += f"   {rec}\n"
    else:
        output += "   🎉 Excellent! Content is well-optimized.\n"
    
    output += f"\n--------------------------------------------------------------------------------\n✨ End of SEO Analysis Report\n--------------------------------------------------------------------------------\n"
    
    return output
