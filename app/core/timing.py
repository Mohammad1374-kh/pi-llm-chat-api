import time


class StreamingTimer:

    def __init__(self):
        self.start_time = None
        self.first_token_time = None
        self.end_time = None
        self.char_count = 0

    def start(self):
        self.start_time = time.perf_counter()

    def on_token(self, token: str):
        now = time.perf_counter()

        if self.first_token_time is None:
            self.first_token_time = now

        self.char_count += len(token)

    def stop(self):
        self.end_time = time.perf_counter()

    @property
    def ttft_ms(self):
        if not self.first_token_time:
            return None
        return round((self.first_token_time - self.start_time) * 1000, 2)

    @property
    def ttlt_ms(self):
        if not self.end_time:
            return None
        return round((self.end_time - self.start_time) * 1000, 2)

    @property
    def chars_per_sec(self):
        if not self.first_token_time or not self.end_time:
            return None

        generation_time = self.end_time - self.first_token_time

        if generation_time <= 0:
            return None

        return round(self.char_count / generation_time, 2)