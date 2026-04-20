import json
import requests
from app.core.logger import logger
from app.core.config import settings
from app.llm.base import LLMProvider


class OpenRouterProvider(LLMProvider):

    def stream(self, prompt: str):
        response = self._send_request(prompt)
        yield from self._parse_stream(response)

    def _send_request(self, prompt: str):
        url = "https://openrouter.ai/api/v1/chat/completions"

        headers = {
            "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": settings.OPENROUTER_MODEL,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "stream": True
        }

        response = requests.post(
            url,
            headers=headers,
            json=payload,
            stream=True,
            timeout=60
        )

        response.raise_for_status()
        return response

    def _parse_stream(self, response):
        for raw_line in response.iter_lines(decode_unicode=True):

            if not raw_line:
                continue

            if raw_line.startswith(":"):
                continue

            if not raw_line.startswith("data:"):
                continue

            data = raw_line.removeprefix("data:").strip()

            if data == "[DONE]":
                break

            chunk = json.loads(data)

            # provider-side streamed error payload
            if "error" in chunk:
                logger.error(f"[LLM_ERROR] provider response error: {chunk}")
                raise ValueError(chunk["error"]["message"])

            token = (
                chunk.get("choices", [{}])[0]
                .get("delta", {})
                .get("content")
            )

            if token:
                yield token


