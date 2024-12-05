# tests/evaluate_rag.py
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.rag.rag_pipeline import RAGPipeline
import json


def evaluate_rag():
    # Load test cases
    test_cases = [
        {
            "query": "How do I create a basic ROS2 publisher?",
            "expected_keywords": ["node", "publisher", "create_publisher", "msg"]
        },
        {
            "query": "What are the key components of Nav2?",
            "expected_keywords": ["planner", "controller", "recovery", "behavior"]
        }
    ]
    
    rag = RAGPipeline()
    results = []
    
    for case in test_cases:
        result = rag.process_query(case["query"])
        
        # Check for expected keywords
        keyword_matches = sum(1 for keyword in case["expected_keywords"] 
                            if keyword.lower() in result['response'].lower())
        
        accuracy = keyword_matches / len(case["expected_keywords"])
        
        results.append({
            "query": case["query"],
            "accuracy": accuracy,
            "response": result['response']
        })
        
    return results

if __name__ == "__main__":
    results = evaluate_rag()
    print(json.dumps(results, indent=2))
