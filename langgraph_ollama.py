# langgraph_ollama.py
"""
LangGraph + Ollama integration for code analysis.
"""
import os
from langgraph import Graph, Node
import httpx

OLLAMA_API_URL = os.environ.get("OLLAMA_API_URL", "http://localhost:11434/api/generate")
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "llama3")

class CodeAnalysisNode(Node):
    def run(self, codebase_path: str) -> str:
        """
        Analyze the codebase and return a Mermaid.js UML diagram as a string.
        """
        # Collect all code files (Python example)
        code = ""
        for root, _, files in os.walk(codebase_path):
            for f in files:
                if f.endswith(('.py', '.js', '.ts', '.java', '.go', '.cpp', '.c', '.cs')):
                    with open(os.path.join(root, f), encoding='utf-8', errors='ignore') as file:
                        code += f"\n# File: {f}\n" + file.read()[:2000]  # Limit per file
        prompt = f"""
You are an expert software architect. Analyze the following codebase and generate the most suitable UML class diagram in Mermaid.js format. Only output the Mermaid code block.

{code}
"""
        response = httpx.post(OLLAMA_API_URL, json={
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False
        })
        if response.status_code == 200:
            result = response.json()
            return result.get("response", "")
        return ""

def analyze_codebase_with_ollama(codebase_path: str) -> str:
    graph = Graph()
    node = CodeAnalysisNode()
    graph.add_node("analyze", node)
    graph.set_entry("analyze")
    return graph.run(codebase_path)
