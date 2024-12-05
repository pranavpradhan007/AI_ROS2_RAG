# src/app.py
import gradio as gr
from clearml import Task
from src.rag.rag_pipeline import RAGPipeline

# current_task = Task.current_task()
# if current_task:
#     current_task.close()

task = Task.init(project_name='RAG_System', task_name='App')

#Processing query and calling the RAG pipeline
def process_query(query, query_type):
    rag = RAGPipeline()
    result = rag.process_query(query, query_type)
    task.get_logger().report_text(f"Generated response with {len(result['sources'])} sources")
    # Format response with sources
    response = result['response'] + "\n\nSources in respective github repository:\n"
    for source in result['sources']:
        response += f"- {source['path']}\n"
    
    return response

SAMPLE_QUESTIONS = [
    "Tell me how can I navigate to a specific pose - include replanning aspects in your answer.",
    "Can you provide me with code for this task?",
]

#Gradio interface
iface = gr.Interface(
        fn=process_query,
        inputs=[
            gr.Dropdown(
                choices=SAMPLE_QUESTIONS,
                label="Select a question or type your own",
                allow_custom_value=True
            ),
            gr.Radio(
                choices=["Question", "Code"],
                label="Query Type",
                value="Question"
            )
        ],
        outputs=gr.Textbox(
            label="Response",
            lines=10
        ),
        title="ROS2 Documentation Assistant",
        description="Ask questions about ROS2, Nav2, MoveIt2, and Gazebo",
        examples=[[q, "Question"] for q in SAMPLE_QUESTIONS]
    )


if __name__ == "__main__":
    iface.launch()