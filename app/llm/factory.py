class LLMFactory:
    @staticmethod
    def create(provider_name: str):
        raise NotImplementedError(
            "LLM providers not implemented yet. Will be added in next commit."
        )