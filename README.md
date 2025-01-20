
# ConversAI_AI-Voice-Chat-Assistant

An intelligent conversational AI assistant that supports both voice and text interactions. ConversAI uses advanced language models for natural conversations and can perform web searches to provide informed responses.

### Deployed Link
Hugging Face Spaces: https://huggingface.co/spaces/pratham0011/ConversAI_AI-Voice-Chat-Assistant

<br>

![image](https://github.com/user-attachments/assets/60d738a7-b7cb-4b8a-84f2-ecdc240db637)

<br>

## Features

- 🎤 Voice interaction with speech-to-text capabilities
- 💬 Text-based chat interface
- 🔍 Web search integration for informed responses
- 🗣️ Natural text-to-speech responses
- 🧠 Context-aware conversations
- 🌐 Web interface built with Gradio

## Technologies

- Python 3.12+
- Transformers (Qwen2.5-0.5B model)
- Edge TTS for speech synthesis
- Whisper for speech recognition
- Gradio for web interface
- DuckDuckGo search integration
- PyTorch

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/PrathamKumar125/ConversAI_AI-Voice-Chat-Assistant.git
   cd ConversAI
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the root directory with:
   ```
   hf_key=your_huggingface_token
   ```

## Usage

1. Start the application:
   ```bash
   python app.py
   ```

2. Open your browser and navigate to:
   ```
   http://localhost:7860
   ```

3. Interact using:
   - Voice input through microphone
   - Text input through chat
   - Toggle web search for enhanced responses

## Configuration

Key configurations in `config.py`:

- **VOICE**: Primary TTS voice (default: "en-US-JennyNeural")
- **FALLBACK_VOICES**: Backup TTS voices
- **SYSTEM_PROMPT**: AI assistant's behavior definition
- **device**: Compute device (CPU/CUDA)
