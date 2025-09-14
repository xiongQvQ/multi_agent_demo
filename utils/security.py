import re


class OutputFilter:
    """Minimal output filtering to reduce accidental leakage of sensitive data
    and prevent overly long outputs from impacting performance.
    """

    SENSITIVE_PATTERNS = [
        re.compile(r"\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b"),  # credit card-like
        re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"),  # email
        re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),  # SSN-like
    ]

    def __init__(self, max_len: int = 10000):
        self.max_len = max_len

    def filter_output(self, content: str) -> str:
        text = content or ""
        for pattern in self.SENSITIVE_PATTERNS:
            text = pattern.sub("[REDACTED]", text)
        if len(text) > self.max_len:
            text = text[: self.max_len - 50] + "\n...[TRUNCATED]"
        return text

