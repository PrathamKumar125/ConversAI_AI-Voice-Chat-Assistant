import os
import tempfile
import logging
from typing import Optional

import torch
import librosa
import edge_tts
from transformers import WhisperProcessor, WhisperForConditionalGeneration

from config.config import VOICE, FALLBACK_VOICES


logger = logging.getLogger(__name__)

# Whisper model for speech to text
processor = WhisperProcessor.from_pretrained(
    "openai/whisper-tiny",
    local_files_only=False
)
model = WhisperForConditionalGeneration.from_pretrained(
    "openai/whisper-tiny",
    local_files_only=False,
    low_cpu_mem_usage=True,
    torch_dtype=torch.float32,
).to("cpu")

# Voice selection handling
async def get_valid_voice() -> str:
    available_voices = await edge_tts.list_voices()
    voice_names = [VOICE] + FALLBACK_VOICES
    
    available_voice_names = {v["ShortName"] for v in available_voices}
    for voice in voice_names:
        if voice in available_voice_names:
            return voice
            
    raise RuntimeError("No valid voice found")

# Text-to-speech conversion using Edge TTS
async def generate_speech(text: str) -> Optional[str]:
    if not text or not isinstance(text, str):
        raise ValueError("Invalid text input")

    voice = await get_valid_voice()
    logger.info(f"Using voice: {voice}")

    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
        tmp_path = tmp_file.name
        
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(tmp_path)

    if not os.path.exists(tmp_path) or os.path.getsize(tmp_path) == 0:
        raise RuntimeError("Speech file empty or not created")

    logger.info(f"Speech generated successfully: {tmp_path}")
    return tmp_path

# Speech-to-text using Whisper
async def transcribe(audio_file: str) -> str:
    audio, sr = librosa.load(
        audio_file,
        sr=16000,
        mono=True,
        duration=30
    )
    
    inputs = processor(
        audio,
        sampling_rate=sr,
        return_tensors="pt",
        return_attention_mask=True
    ).to(model.device)

    with torch.no_grad():
        generated_ids = model.generate(
            input_features=inputs.input_features,
            attention_mask=inputs.attention_mask,
            language="en",
            task="transcribe",
            max_length=448,
            temperature=0.0
        )
        
        transcription = processor.batch_decode(
            generated_ids,
            skip_special_tokens=True
        )[0].strip()

    logger.info(f"Transcribed text: {transcription}")
    return transcription