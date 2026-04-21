from app.llm.providers.openrouter import OpenRouterProvider
from app.llm.providers.groq import GroqProvider
from app.llm.exceptions import LLMProviderError


class LLMFactory:

    PROVIDERS = {
        "openrouter": OpenRouterProvider,
        "groq": GroqProvider,
    }

    @staticmethod
    def create(provider_name: str):
        provider_cls = LLMFactory.PROVIDERS.get(provider_name.lower())

        if not provider_cls:
            raise LLMProviderError(f"Unsupported provider: {provider_name}")

        return provider_cls()