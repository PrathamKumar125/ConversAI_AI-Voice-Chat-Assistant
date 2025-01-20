import asyncio
import logging
import gradio as gr

from services.qwen import respond


logger = logging.getLogger(__name__)

# Track conversation state
conversation_history = []

def clear_conversation():
    global conversation_history
    conversation_history = []
    return [],None

def sync_respond(audio, text_input, do_search, history):
    if not audio and not text_input:
        return None, history
    
    logger.info(f"Processing request with search enabled: {do_search}")
    result = asyncio.run(respond(audio, text_input, do_search, history))
    audio_path, response_text = result
    
    if audio:
        user_message = {"role": "user", "content": "Voice message"}
    else:
        user_message = {"role": "user", "content": text_input}
        
    assistant_message = {"role": "assistant", "content": response_text}
    history.extend([user_message, assistant_message])
    
    return audio_path, history

# Build Gradio interface
with gr.Blocks(
    theme=gr.themes.Soft(),
    css=""".message { font-family: "Times New Roman", Times, serif !important;}"""
    ) as interface:
    gr.Markdown(
        """
        <div style="text-align: center; margin-bottom: 1rem;">
            <h1 style="font-weight: bold;">ConversAI: AI Voice & Chat Assistant</h1>
        </div>
        """,
        show_label=False
    )
    
    # Input components (left column)
    with gr.Row():
        with gr.Column(scale=2):
            audio_input = gr.Audio(
                label="Your Voice Input",
                type="filepath",
                sources=["microphone"]
            )
            text_input = gr.Textbox(
                label="Or Type Your Message",
                placeholder="Type here..."
            )
            search_checkbox = gr.Checkbox(
                label="Enable web search",
                value=False
                )
            clear_btn = gr.Button("Clear Chat")
        
        # Output components (right column)   
        with gr.Column(scale=3):
            chatbot = gr.Chatbot(label="Conversation", type="messages")
            audio_output = gr.Audio(
                label="AI Voice Response",
                type="filepath",
                autoplay=True
            )

    # Define input event handlers
    input_events = [
        audio_input.change(
            fn=sync_respond,
            inputs=[audio_input, text_input,search_checkbox, chatbot],
            outputs=[audio_output, chatbot]
        ),
        text_input.submit(
            fn=sync_respond,
            inputs=[audio_input, text_input, search_checkbox, chatbot],
            outputs=[audio_output, chatbot]
        )
    ]
    
    # Clear chat button handler
    clear_btn.click(
        fn=clear_conversation,
        outputs=[chatbot, audio_output]
    )

# Start server
if __name__ == "__main__":
    interface.launch(
        server_name="0.0.0.0",
        server_port=7860,
        debug=True
    )