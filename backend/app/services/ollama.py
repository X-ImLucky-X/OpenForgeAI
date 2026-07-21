import httpx
import json
import logging
from typing import List, Dict, Any, Optional

logger = logging.getLogger("openforge.ollama")

OLLAMA_BASE_URL = "http://localhost:11434"

class OllamaService:
    def __init__(self, base_url: str = OLLAMA_BASE_URL):
        self.base_url = base_url

    async def check_health(self) -> bool:
        """Check if Ollama is running locally."""
        try:
            async with httpx.AsyncClient(timeout=2.0) as client:
                res = await client.get(f"{self.base_url}/api/tags")
                return res.status_code == 200
        except Exception as e:
            logger.warning(f"Ollama health check failed: {e}")
            return False

    async def get_available_models(self) -> List[str]:
        """Fetch list of models available in local Ollama."""
        try:
            async with httpx.AsyncClient(timeout=3.0) as client:
                res = await client.get(f"{self.base_url}/api/tags")
                if res.status_code == 200:
                    data = res.json()
                    models = [m.get("name", "") for m in data.get("models", [])]
                    short_names = [m.split(":")[0] for m in models if ":" in m]
                    all_models = list(dict.fromkeys(models + short_names))
                    if all_models:
                        return all_models
        except Exception as e:
            logger.warning(f"Failed to fetch Ollama models: {e}")
        
        return ["qwen2.5:7b", "gemma3", "llama3", "template-engine (fallback)"]

    async def generate(
        self, 
        model: str, 
        prompt: str, 
        system_prompt: Optional[str] = None, 
        temperature: float = 0.7,
        timeout: float = 25.0
    ) -> Optional[str]:
        """Generate response from Ollama model, automatically resolving available models."""
        if not await self.check_health():
            logger.info("Ollama daemon is offline. Triggering template fallback.")
            return None

        # Resolve requested model to actual installed model if needed
        avail = await self.get_available_models()
        target_model = model
        if target_model not in avail:
            # Pick best installed fallback model
            matches = [m for m in avail if m in ["qwen2.5:7b", "qwen2.5", "llama3:latest", "llama3", "gemma:latest", "gemma"]]
            if matches:
                target_model = matches[0]
            elif avail:
                target_model = avail[0]

        payload: Dict[str, Any] = {
            "model": target_model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": temperature
            }
        }
        if system_prompt:
            payload["system"] = system_prompt

        try:
            async with httpx.AsyncClient(timeout=timeout) as client:
                res = await client.post(f"{self.base_url}/api/generate", json=payload)
                if res.status_code == 200:
                    data = res.json()
                    return data.get("response", "").strip()
                else:
                    logger.warning(f"Ollama model '{target_model}' returned status {res.status_code}. Using fallback.")
                    return None
        except Exception as e:
            logger.warning(f"Ollama request timed out or failed: {e}")
            return None

ollama_service = OllamaService()
