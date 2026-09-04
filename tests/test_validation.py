"""Tests for username validation and normalization."""

import pytest
from uscan.utils.validation import validate_username, normalize_username, generate_variants


class TestValidateUsername:
    def test_valid_simple(self):
        valid, err = validate_username("inter")
        assert valid is True
        assert err == ""

    def test_valid_with_dots(self):
        valid, _ = validate_username("john.doe")
        assert valid is True

    def test_valid_with_underscore(self):
        valid, _ = validate_username("john_doe")
        assert valid is True

    def test_valid_with_dash(self):
        valid, _ = validate_username("john-doe")
        assert valid is True

    def test_empty(self):
        valid, err = validate_username("")
        assert valid is False
        assert "empty" in err.lower()

    def test_too_long(self):
        valid, err = validate_username("a" * 100)
        assert valid is False
        assert "long" in err.lower()

    def test_invalid_chars(self):
        valid, err = validate_username("user name!")
        assert valid is False
        assert "Invalid" in err

    def test_unicode_rejected(self):
        valid, _ = validate_username("usér")
        assert valid is False


class TestNormalizeUsername:
    def test_strip_whitespace(self):
        assert normalize_username("  inter  ") == "inter"

    def test_strip_at_sign(self):
        assert normalize_username("@inter") == "inter"

    def test_preserve_case(self):
        assert normalize_username("Inter") == "Inter"

    def test_nfkc_normalization(self):
        result = normalize_username("ｉｎｔｅｒ")
        assert result == "inter"


class TestGenerateVariants:
    def test_includes_original(self):
        variants = generate_variants("inter")
        assert variants[0] == "inter"

    def test_generates_multiple(self):
        variants = generate_variants("inter")
        assert len(variants) > 1

    def test_no_duplicates(self):
        variants = generate_variants("inter")
        assert len(variants) == len(set(variants))

    def test_max_eight(self):
        variants = generate_variants("test")
        assert len(variants) <= 8
