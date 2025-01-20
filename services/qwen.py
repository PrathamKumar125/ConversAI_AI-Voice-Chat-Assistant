import logging
from typing import List, Dict, Optional, Tuple

import torch
from transformers import pipeline
from transformers import pipeline

from config.config import token, device, SYSTEM_PROMPT
from services.whisper import generate_speech, transcribe
from services.search import WebSearcher

logger = logging.getLogger(__name__)

searcher = WebSearcher()

# Qwen Configuration
model_kwargs = {
    "low_cpu_mem_usage": True,
    "torch_dtype": torch.float32,
    'use_cache': True
}
client = pipeline(
    "text-generation",
    model="Qwen/Qwen2.5-0.5B-Instruct",
    token=token,
    trust_remote_code=True,
    device=device,
    model_kwargs=model_kwargs
)

async def respond(
        audio: Optional[str] = None,
        text: Optional[str] = None,
        do_search: bool = False,
        history: List[Dict] = None
    ) -> Tuple[Optional[str], str]:
    try:
        if text:
            user_text = text.strip()
        elif audio:
            user_text = await transcribe(audio)
        else:
            return None, "No input provided"

        # Build conversation context
        messages = []
        messages.append({"role": "system", "content": SYSTEM_PROMPT})
        
        if history:
            messages.extend(history)
        
        # Format message history for Qwen
        prompt = ""
        for msg in messages:
            role = msg["role"]
            content = msg["content"]
            prompt += f"<|im_start|>{role}\n{content}<|im_end|>\n"

        # Add current user message
        prompt += f"<|im_start|>user\n{user_text}<|im_end|>\n<|im_start|>assistant\n"

        # Add web-search context if enabled
        if do_search:
            results = searcher.search(user_text)
            if results:
                search_context = "Based on search results:\n"
                for result in results:
                    snippet = result['content'][:500].strip()
                    search_context += f"{snippet}\n"
                prompt = prompt.replace(SYSTEM_PROMPT, f"{SYSTEM_PROMPT}\n{search_context}")

        # Generate response
        reply = client(
            prompt,
            max_new_tokens=400,
            do_sample=True,
            temperature=0.7,
            top_p=0.9,
            num_return_sequences=1
        )

        # Extract and clean assistant response
        assistant_response = reply[0]['generated_text']
        assistant_response = assistant_response.split("<|im_start|>assistant\n")[-1]
        assistant_response = assistant_response.split("<|im_end|>")[0].strip()

        # Convert response to speech
        audio_path = await generate_speech(assistant_response)
        return audio_path, assistant_response

    except Exception as e:
        logger.error(f"Error in respond: {str(e)}")
        return None, "Sorry, I encountered an error"