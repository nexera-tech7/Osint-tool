"""Response classification logic."""

from __future__ import annotations

from uscan.scanner.models import ScanStatus, Confidence


class ResponseClassifier:
    """Classifies HTTP responses into scan statuses with confidence."""

    @staticmethod
    def classify(
        http_status: int | None,
        body: str = "",
        *,
        not_found_indicators: list[str] | None = None,
        found_indicators: list[str] | None = None,
        error_body_indicators: list[str] | None = None,
    ) -> tuple[ScanStatus, Confidence]:
        if http_status is None:
            return ScanStatus.ERROR, Confidence.NONE

        if http_status == 429:
            return ScanStatus.RATE_LIMITED, Confidence.HIGH

        if http_status == 403:
            return ScanStatus.BLOCKED, Confidence.MEDIUM

        if http_status == 404:
            return ScanStatus.NOT_FOUND, Confidence.HIGH

        if http_status >= 500:
            return ScanStatus.ERROR, Confidence.NONE

        if http_status in (301, 302, 303, 307, 308):
            return ScanStatus.UNKNOWN, Confidence.LOW

        if http_status == 200:
            body_lower = body.lower()

            if not_found_indicators:
                for indicator in not_found_indicators:
                    if indicator.lower() in body_lower:
                        return ScanStatus.NOT_FOUND, Confidence.HIGH

            if error_body_indicators:
                for indicator in error_body_indicators:
                    if indicator.lower() in body_lower:
                        return ScanStatus.UNKNOWN, Confidence.LOW

            if found_indicators:
                matches = sum(
                    1 for ind in found_indicators if ind.lower() in body_lower
                )
                if matches >= 2:
                    return ScanStatus.FOUND, Confidence.HIGH
                if matches == 1:
                    return ScanStatus.FOUND, Confidence.MEDIUM
                return ScanStatus.UNKNOWN, Confidence.LOW

            return ScanStatus.FOUND, Confidence.LOW

        return ScanStatus.UNKNOWN, Confidence.NONE
