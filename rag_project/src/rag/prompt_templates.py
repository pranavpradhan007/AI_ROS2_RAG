# src/rag/prompt_templates.py

class PromptTemplates:
    @staticmethod
    def get_qa_template():
        return """Answer the question based on the provided context. If you cannot answer the question based on the context, say "I cannot answer this question based on the provided information."

Context:
{context}

Question: {question}

Answer: Let me help you with that.
"""

    @staticmethod
    def get_code_template():
        return """Based on the provided context, generate code that addresses the question. Include explanatory comments.

Context:
{context}

Question: {question}

Code Solution:
"""

    @staticmethod
    def format_context(relevant_chunks):
        formatted_chunks = []
        for chunk in relevant_chunks:
            formatted_chunks.append(f"[Source: {chunk['path']}]\n{chunk['content']}\n")
        return "\n".join(formatted_chunks)