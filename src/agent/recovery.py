"""Failure classification and bounded retry decisions."""
from __future__ import annotations

from typing import Literal

FailureClass = Literal["retryable", "non_retryable"]


def classify_failure(error: Exception) -> FailureClass:
    """Classify failures that are usually safe to retry."""
    if isinstance(error, (TimeoutError, ConnectionError, OSError, RuntimeError)):
        return "retryable"

    message = str(error).lower()
    retryable_markers = ("timeout", "temporarily unavailable", "rate limit", "connection reset")
    if any(marker in message for marker in retryable_markers):
        return "retryable"
    return "non_retryable"


def should_retry(error: Exception, retry_count: int, max_retries: int) -> bool:
    return retry_count < max_retries and classify_failure(error) == "retryable"
