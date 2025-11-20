
from langchain_openai import ChatOpenAI
from langchain_community.chains.graph_qa.base import GraphQAChain
from langchain_community.graphs.networkx_graph import NetworkxEntityGraph, KnowledgeTriple
import networkx as nx
import matplotlib.pyplot as plt
from dotenv import load_dotenv
# Load environment variables
load_dotenv()

llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)

graph = NetworkxEntityGraph()

text = """
Alice works at Tinisoft as a Software Engineer.
Bob works at Tinisoft as a Product Manager.
Charlie works at Tinisoft as a Marketing Manager.
Alice and Bob are friends.
Bob and Charlie are friends.
Alice and Charlie are not friends.
Alice likes to eat pizza.
Bob likes to eat pasta.
Charlie likes to eat sushi.
"""

graph.add_triple(KnowledgeTriple("Alice", "works_at", "Tinisoft"))
graph.add_triple(KnowledgeTriple("Bob", "works_at", "Tinisoft"))
graph.add_triple(KnowledgeTriple("Charlie", "works_at", "Tinisoft"))
graph.add_triple(KnowledgeTriple("Alice", "works_as", "Software Engineer"))
graph.add_triple(KnowledgeTriple("Bob", "works_as", "Product Manager"))
graph.add_triple(KnowledgeTriple("Charlie", "works_as", "Marketing Manager"))
graph.add_triple(KnowledgeTriple("Alice", "is_friend_with", "Bob"))
graph.add_triple(KnowledgeTriple("Bob", "is_friend_with", "Charlie"))
graph.add_triple(KnowledgeTriple("Alice", "is_friend_with", "Charlie"))
graph.add_triple(KnowledgeTriple("Alice", "likes", "pizza"))
graph.add_triple(KnowledgeTriple("Bob", "likes", "pasta"))
graph.add_triple(KnowledgeTriple("Charlie", "likes", "sushi")) 

chain = GraphQAChain.from_llm(llm=llm, graph=graph, verbose=True)

response = chain.invoke("Who works at TechCorp?")
print(response)


response = chain.invoke("Where does Alice live?")
print(response)

