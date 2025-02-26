import gradio as gr
from notebook_processor import summarize, clean, modularize

def create_gradio_interface():
    """Creates a Gradio interface for processing Jupyter Notebooks."""
    with gr.Blocks() as demo:
        gr.Markdown("# 📝 Jupyter Notebook Processor")
        notebook_input = gr.File(label="Upload a Jupyter Notebook", type="filepath")
        summary_output = gr.Textbox(label="Summary", interactive=False)
        cleaned_notebook_output = gr.File(label="Cleaned Notebook", file_count="single")
        modularized_output = gr.File(label="Download Modularized Code", file_count="single")

        with gr.Row():
            summarize_button = gr.Button("Summarize")
            clean_button = gr.Button("Clean")
            modularize_button = gr.Button("Modularize")

        summarize_button.click(fn=summarize, inputs=[notebook_input], outputs=[summary_output])
        clean_button.click(fn=clean, inputs=[notebook_input], outputs=[cleaned_notebook_output])
        modularize_button.click(fn=modularize, inputs=[notebook_input], outputs=[modularized_output])

    demo.launch()