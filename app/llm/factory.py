from app.llm.providers.openrouter import OpenRouterProvider
from app.llm.providers.groq import GroqProvider

class LLMFactory:

    PROVIDERS = {
        "openrouter": OpenRouterProvider,
        "groq": GroqProvider,
    }

    @staticmethod
    def create(provider_name: str):
        provider_name = provider_name.lower()

        provider_cls = LLMFactory.PROVIDERS.get(provider_name)

        if not provider_cls:
            raise ValueError(f"Unsupported provider: {provider_name}")

        return provider_cls()