# src/rag/generator.py
from langchain_community.llms import Ollama  
from clearml import Task
from .__init__ import init_clearml
# from langchain_ollama import Ollama

#Calling the Ollama with context window of 2048 as my GPU could not handle my model.
class Generator:
    def __init__(self, model_name="ros2_assistant"):
        self.task = init_clearml()
        self.llm = Ollama(
            model=model_name,
            temperature=0.7,
            num_ctx=2048,         
            num_thread=4,        
            stop=["### Instruction:", "### Response:"]
        )
        
    def generate_response(self, prompt):
        try:
            response = self.llm.invoke(prompt)
            self.task.get_logger().report_text(f"Generated response for prompt length: {len(prompt)}")
            return response
        except Exception as e:
            error_msg = f"Error generating response: {str(e)}"
            self.task.get_logger().report_text(error_msg, level=self.task.Logger.ERROR)
            return error_msg
