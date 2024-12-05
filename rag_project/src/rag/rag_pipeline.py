# src/rag/rag_pipeline.py
from .retriever import Retriever
from .generator import Generator
from .prompt_templates import PromptTemplates
from src.config import YOUTUBE_URLS
from src.rag import get_task, init_clearml

task = init_clearml()

class RAGPipeline:
    def __init__(self):
        self.task = init_clearml()
        self.retriever = Retriever()
        self.generator = Generator()
        self.prompt_templates = PromptTemplates()

    def process_query(self, query, query_type="qa"):
        self.task.get_logger().report_text(f"Processing query: {query}")
        # Get relevant chunks
        relevant_chunks = self.retriever.get_relevant_chunks(query)
        
        # Format context
        formatted_context = self.prompt_templates.format_context(relevant_chunks)
        
        # Select template based on query type
        if query_type == "code":
            template = self.prompt_templates.get_code_template()
        else:
            template = self.prompt_templates.get_qa_template()
            
        # Format prompt
        prompt = template.format(
            context=formatted_context,
            question=query
        )
        
        # Generate response
        response = self.generator.generate_response(prompt)
        self.task.get_logger().report_text(f"Generated response with {len(relevant_chunks)} sources")
        return {
            'response': response,
            'sources': [{'url': chunk['url'], 'path': chunk['path']} for chunk in relevant_chunks]
        }
    