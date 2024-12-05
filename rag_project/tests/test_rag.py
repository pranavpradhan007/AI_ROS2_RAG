# tests/test_rag.py
from src.rag.rag_pipeline import RAGPipeline

def test_rag_system():
    # Initialize RAG pipeline
    rag = RAGPipeline()
    
    # Test questions
    test_questions = [
        {
            "query": "How do I create a basic ROS2 publisher?",
            "type": "code"
        },
        {
            "query": "What is Nav2 and what are its main components?",
            "type": "qa"
        }
    ]
    
    # Process each question
    for question in test_questions:
        print(f"\nQuestion: {question['query']}")
        print("Processing...")
        
        result = rag.process_query(
            query=question['query'],
            query_type=question['type']
        )
        
        print("\nResponse:")
        print(result['response'])
        print("\nSources:")
        for source in result['sources']:
            print(f"- {source['path']}")
        print("-" * 80)

if __name__ == "__main__":
    test_rag_system()