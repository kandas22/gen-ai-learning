from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
import os
from typing import List, Dict, Tuple
from dataclasses import dataclass
from enum import Enum
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class QualityLevel(Enum):
    EXCELLENT = "EXCELLENT"
    GOOD = "GOOD"
    AVERAGE = "AVERAGE"
    POOR = "POOR"

@dataclass
class ContextEvaluation: 
    relevance_score: float
    accuracy_score: float
    completeness_score: float
    specificity_score: float
    overall_quality: QualityLevel
    reasoning: str

class CorrectiveRAG: 
    def __init__(self, model_name: str = "gpt-4o-mini", temperature: float = 0.0):
        self.model = ChatOpenAI(model=model_name, temperature=temperature)

    def evaluate_context(self, context: str, query: str) -> ContextEvaluation: 
        prompt = ChatPromptTemplate.from_template("""
        You are a context evaluator. Your task is to evaluate the quality of the given context for the given question.
        
        Context: {context}
        Query: {query}
        Evaluate the context on these criteria (score 0-1):
        1. Relevance: How well does it address the query?
        2. Completeness: Does it provide sufficient information?
        3. Accuracy: Is the information factually correct?
        4. Specificity: Is it specific enough for the query?
        
        Your response should be in the following format:
        {{
            "relevant_score": <score>,
            "accuracy_score": <score>,
            "completeness_score": <score>,
            "specificity_score": <score>,
            "overall_score": <score>,
            "reasoning": <reasoning>
        }}
        """)
        
        response = self.model.invoke(prompt.format(context=context, query=query))
        # Parse the response
        lines = response.content.strip().split('\n')
        scores = {}
        reasoning = ""
        overall = QualityLevel.AVERAGE

        for line in lines:
            if line.startswith("RELEVANCE:"):
                scores['relevance'] = float(line.split(':')[1].strip())
            elif line.startswith("COMPLETENESS:"):
                scores['completeness'] = float(line.split(':')[1].strip())
            elif line.startswith("ACCURACY:"):
                scores['accuracy'] = float(line.split(':')[1].strip())
            elif line.startswith("SPECIFICITY:"):
                scores['specificity'] = float(line.split(':')[1].strip())
            elif line.startswith("OVERALL:"):
                overall_str = line.split(':')[1].strip()
                overall = QualityLevel[overall_str]
            elif line.startswith("REASONING:"):
                reasoning = line.split(':', 1)[1].strip()

        return ContextEvaluation(
            relevance_score=scores.get('relevance', 0.0),
            completeness_score=scores.get('completeness', 0.0),
            accuracy_score=scores.get('accuracy', 0.0),
            specificity_score=scores.get('specificity', 0.0),
            overall_quality=overall,
            reasoning=reasoning
        )

class CorrectiveRAGSystem:
    def __init__(self, documents: List[str]):
        self.llm = ChatOpenAI(model="gpt-4", temperature=0)
        self.evaluator = CorrectiveRAG(model_name="gpt-4", temperature=0)
        self.embeddings = OpenAIEmbeddings()
        
        # Create vector store
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        chunks = text_splitter.create_documents(documents)
        self.vectorstore = Chroma.from_documents(
            documents=chunks,
            embedding=self.embeddings
        )
    
    def retrieve(self, query: str, k: int = 5) -> List[str]:
        """Retrieve relevant documents"""
        docs = self.vectorstore.similarity_search(query, k=k)
        return [doc.page_content for doc in docs]
    
    def refine_query(self, original_query: str, evaluation: ContextEvaluation) -> str:
        """Generate a refined query based on evaluation"""
        
        refine_prompt = ChatPromptTemplate.from_template("""
The original query did not retrieve good context.

Original Query: {query}
Problem: {reasoning}

Create a refined search query that will retrieve better context.
Focus on: keywords, specific terms, and related concepts.

Refined Query:""")
        
        response = self.llm.invoke(
            refine_prompt.format(
                query=original_query,
                reasoning=evaluation.reasoning
            )
        )
        
        return response.content.strip()
    
    def process_query(self, query: str, max_attempts: int = 3) -> Dict:
        """Process query with correction mechanism"""
        
        attempt = 1
        correction_needed = False
        
        while attempt <= max_attempts:
            print(f"\n🔄 Attempt {attempt}/{max_attempts}")
            
            # Retrieve context
            if attempt == 1:
                search_query = query
            else:
                search_query = self.refine_query(query, evaluation)
                correction_needed = True
            
            context_list = self.retrieve(search_query, k=5)
            context = "\n\n".join(context_list)
            
            # Evaluate context
            evaluation = self.evaluator.evaluate_context(query, context)
            
            print(f"📊 Quality: {evaluation.overall_quality.value}")
            print(f"   Relevance: {evaluation.relevance_score:.2f}")
            print(f"   Completeness: {evaluation.completeness_score:.2f}")
            print(f"   Accuracy: {evaluation.accuracy_score:.2f}")
            print(f"   Specificity: {evaluation.specificity_score:.2f}")
            
            # Check if quality is acceptable
            if evaluation.overall_quality in [QualityLevel.GOOD, QualityLevel.EXCELLENT]:
                break
            
            attempt += 1
        
        # Generate final answer
        answer_prompt = ChatPromptTemplate.from_template("""
Based on the following context, answer the query.

Query: {query}
Context: {context}

Answer:""")
        
        response = self.llm.invoke(
            answer_prompt.format(query=query, context=context)
        )
        
        return {
            "query": query,
            "context_quality": evaluation.overall_quality.value,
            "relevance_score": evaluation.relevance_score,
            "completeness_score": evaluation.completeness_score,
            "accuracy_score": evaluation.accuracy_score,
            "specificity_score": evaluation.specificity_score,
            "answer": response.content,
            "correction_applied": correction_needed,
            "attempts": attempt,
            "context_sources": context_list[:3]  # First 3 chunks
        }
# Example usage
documents = [
    "Machine learning is a subset of AI that enables computers to learn from data.",
    "Overfitting occurs when a model learns training data too well, including noise.",
    "Overfitting leads to poor generalization on new data and high variance.",
    "To prevent overfitting, use techniques like regularization and cross-validation.",
    "Cross-validation helps assess model performance and detect overfitting."
]

# Create system
corrective_rag = CorrectiveRAGSystem(documents)

# Process query
result = corrective_rag.process_query(
    "What are the side effects of Machine Learning overfitting?"
)

# Display results
print("\n" + "="*60)
print("🔍 CORRECTIVE RAG RESULTS")
print("="*60)
print(f"📊 Context Quality: {result['context_quality']}")
print(f"🎯 Answer: {result['answer']}")
print(f"⚠️  Correction Applied: {result['correction_applied']}")
print(f"🔄 Attempts: {result['attempts']}")