import os
import logging
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()
token = os.getenv("hf_key")

# Set compute device (cpu/cuda)
device = "cpu"
logger.info(f"Device set to use {device}")

# AI Assistant Configuration
SYSTEM_PROMPT = """You are ConversAI, a helpful AI assistant who remembers conversation history. Keep responses clear, friendly and natural. Always refer to previous context when responding."""

# Text-to-Speech Voice Settings (primary/backup)
VOICE = "en-US-JennyNeural" 
FALLBACK_VOICES = ["en-US-ChristopherNeural", "en-US-EricNeural"]

# Audio Output Configuration
OUTPUT_FORMAT = "audio-24khz-48kbit-mono-mp3"