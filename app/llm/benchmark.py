from app.core.logger import logger
from app.core.timing import StreamingTimer
from app.llm.factory import LLMFactory


def run_benchmark(provider_name: str, prompt: str):
    provider = LLMFactory.create(provider_name)

    timer = StreamingTimer()
    timer.start()

    full_response = ""

    for token in provider.stream(prompt):
        timer.on_token(token)
        full_response += token

    timer.stop()

    result = {
        "provider": provider_name,
        "ttft_ms": timer.ttft_ms,
        "ttlt_ms": timer.ttlt_ms,
        "chars_per_sec": timer.chars_per_sec,
        "chars": len(full_response),
    }

    logger.info(f"[BENCHMARK] {result}")

    return result