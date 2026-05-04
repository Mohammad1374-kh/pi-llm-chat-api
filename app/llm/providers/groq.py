import json
import requests

from app.core.config import settings
from app.core.logger import logger
from app.llm.base import LLMProvider
from app.llm.exceptions import LLMProviderError


class GroqProvider(LLMProvider):

    def stream(self, prompt: str):
        # Entry point: sends request and yields streamed tokens
        response = self._send_request(prompt)
        yield from self._parse_stream(response)

    def _send_request(self, prompt: str):
        # Sends HTTP request to Groq API with streaming enabled
        url = "https://api.groq.com/openai/v1/chat/completions"

        try:
            response = requests.post(
                url,
                headers={
                    "Authorization": f"Bearer {settings.GROQ_API_KEY}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": settings.GROQ_MODEL,
                    "messages": [{"role": "user", "content": prompt}],
                    "stream": True
                },
                # stream=True enables incremental token delivery
                stream=True,
                timeout=60
            )

            response.raise_for_status()
            return response

        except requests.RequestException as e:
            logger.error(f"[LLM_GROQ] request failed: {str(e)}")
            # Network / timeout / HTTP errors from provider
            raise LLMProviderError(str(e))

    def _parse_stream(self, response):
        # Parse Server-Sent Events (SSE) stream and yield tokens incrementally
        for raw_line in response.iter_lines(decode_unicode=True):

            # Skip empty keep-alive lines
            if not raw_line:
                continue

            # Process only SSE data lines
            if not raw_line.startswith("data:"):
                continue

            data = raw_line.removeprefix("data:").strip()

            # End of stream signal from provider
            if data == "[DONE]":
                break

            chunk = json.loads(data)

            # Provider may send structured error in stream
            if "error" in chunk:
                logger.error(f"[LLM_GROQ] provider error: {chunk}")
                raise LLMProviderError(chunk["error"]["message"])

            token = (
                chunk.get("choices", [{}])[0]
                .get("delta", {})
                .get("content")
            )

            if token:
                yield token