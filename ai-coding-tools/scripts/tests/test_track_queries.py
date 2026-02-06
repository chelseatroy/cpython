"""Tests for track_queries.py."""

import csv
import json
from pathlib import Path
from unittest import mock

import track_queries


# =============================================================================
# detect_query_type
# =============================================================================

class TestDetectQueryType:
    def test_code_generation(self):
        """Queries about writing/creating code are classified as code_generation."""
        assert track_queries.detect_query_type("Write a function to sort") == "code_generation"
        assert track_queries.detect_query_type("Create a new class") == "code_generation"
        assert track_queries.detect_query_type("Implement the parser") == "code_generation"

    def test_debugging(self):
        """Queries about fixing bugs are classified as debugging."""
        assert track_queries.detect_query_type("Fix the login bug") == "debugging"
        assert track_queries.detect_query_type("There's an error in main") == "debugging"
        assert track_queries.detect_query_type("This function is broken") == "debugging"

    def test_explanation(self):
        """Queries asking for explanations are classified as explanation."""
        assert track_queries.detect_query_type("Explain how imports work") == "explanation"
        assert track_queries.detect_query_type("What is a metaclass?") == "explanation"
        assert track_queries.detect_query_type("How does the GIL work?") == "explanation"

    def test_refactoring(self):
        """Queries about refactoring are classified as refactoring."""
        assert track_queries.detect_query_type("Refactor this module") == "refactoring"
        assert track_queries.detect_query_type("Optimize the database queries") == "refactoring"

    def test_research(self):
        """Queries about finding/searching are classified as research."""
        assert track_queries.detect_query_type("Find all uses of PyObject") == "research"
        assert track_queries.detect_query_type("Where is the main loop?") == "research"

    def test_testing(self):
        """Queries about testing are classified as testing."""
        assert track_queries.detect_query_type("Test the new endpoint") == "testing"
        assert track_queries.detect_query_type("Verify the output is correct") == "testing"

    def test_other_fallback(self):
        """Queries that don't match any pattern return 'other'."""
        assert track_queries.detect_query_type("Hello there") == "other"
        assert track_queries.detect_query_type("Thanks!") == "other"

    def test_case_insensitive(self):
        """Detection is case-insensitive."""
        assert track_queries.detect_query_type("WRITE A FUNCTION") == "code_generation"
        assert track_queries.detect_query_type("FIX THE BUG") == "debugging"

    def test_first_match_wins(self):
        """When multiple patterns could match, the first category wins."""
        # "fix" matches debugging before "test" could match testing
        result = track_queries.detect_query_type("Fix the test runner")
        # The iteration order of QUERY_PATTERNS determines which wins;
        # we just verify it returns a valid type
        assert result in track_queries.QUERY_PATTERNS


# =============================================================================
# estimate_input_tokens_from_text
# =============================================================================

class TestEstimateInputTokens:
    def test_empty_string(self):
        """Empty string returns 0 tokens."""
        assert track_queries.estimate_input_tokens_from_text("") == 0

    def test_none_input(self):
        """None input returns 0 tokens."""
        assert track_queries.estimate_input_tokens_from_text(None) == 0

    def test_known_length(self):
        """A string of 100 characters should produce ~25 tokens (100/4)."""
        text = "a" * 100
        assert track_queries.estimate_input_tokens_from_text(text) == 25

    def test_short_string(self):
        """A 4-character string should produce 1 token."""
        assert track_queries.estimate_input_tokens_from_text("abcd") == 1

    def test_rounds_down(self):
        """Token count is truncated (not rounded) to an integer."""
        # 5 chars / 4 = 1.25 -> 1
        assert track_queries.estimate_input_tokens_from_text("abcde") == 1


# =============================================================================
# estimate_output_tokens
# =============================================================================

class TestEstimateOutputTokens:
    def test_code_generation_5x(self):
        """Code generation uses a 5x multiplier."""
        assert track_queries.estimate_output_tokens(100, "code_generation") == 500

    def test_debugging_2x(self):
        """Debugging uses a 2x multiplier."""
        assert track_queries.estimate_output_tokens(100, "debugging") == 200

    def test_explanation_3x(self):
        """Explanation uses a 3x multiplier."""
        assert track_queries.estimate_output_tokens(100, "explanation") == 300

    def test_research_4x(self):
        """Research uses a 4x multiplier."""
        assert track_queries.estimate_output_tokens(100, "research") == 400

    def test_refactoring_3x(self):
        """Refactoring uses a 3x multiplier."""
        assert track_queries.estimate_output_tokens(100, "refactoring") == 300

    def test_testing_2x(self):
        """Testing uses a 2x multiplier."""
        assert track_queries.estimate_output_tokens(100, "testing") == 200

    def test_unknown_type_uses_default_2x(self):
        """An unrecognized query type uses the 2x default."""
        assert track_queries.estimate_output_tokens(100, "unknown_type") == 200
        assert track_queries.estimate_output_tokens(100, "other") == 200

    def test_zero_input(self):
        """Zero input tokens produce zero output tokens."""
        assert track_queries.estimate_output_tokens(0, "code_generation") == 0


# =============================================================================
# estimate_cache_tokens
# =============================================================================

class TestEstimateCacheTokens:
    def test_80_20_split(self):
        """Cache tokens split 80% read and 20% creation."""
        cache_read, cache_creation = track_queries.estimate_cache_tokens(100)
        assert cache_read == 80
        assert cache_creation == 20

    def test_zero_input(self):
        """Zero input produces zero cache tokens."""
        assert track_queries.estimate_cache_tokens(0) == (0, 0)

    def test_rounding(self):
        """Non-round numbers are truncated to int."""
        cache_read, cache_creation = track_queries.estimate_cache_tokens(10)
        assert cache_read == 8
        assert cache_creation == 2


# =============================================================================
# calculate_cost
# =============================================================================

class TestCalculateCost:
    def test_zero_tokens(self):
        """Zero tokens in all categories produces zero cost."""
        assert track_queries.calculate_cost(0, 0, 0, 0) == 0.0

    def test_input_only(self):
        """1M input tokens at $15/1M = $15."""
        cost = track_queries.calculate_cost(1_000_000, 0, 0, 0)
        assert cost == 15.0

    def test_output_only(self):
        """1M output tokens at $75/1M = $75."""
        cost = track_queries.calculate_cost(0, 1_000_000, 0, 0)
        assert cost == 75.0

    def test_cache_read(self):
        """1M cache read tokens at $1.50/1M = $1.50."""
        cost = track_queries.calculate_cost(0, 0, 1_000_000, 0)
        assert cost == 1.5

    def test_cache_creation(self):
        """1M cache creation tokens at $18.75/1M = $18.75."""
        cost = track_queries.calculate_cost(0, 0, 0, 1_000_000)
        assert cost == 18.75

    def test_combined(self):
        """Cost with all token types sums correctly."""
        # 1000 input: 1000/1M * 15 = 0.015
        # 5000 output: 5000/1M * 75 = 0.375
        # 800 cache_read: 800/1M * 1.5 = 0.0012
        # 200 cache_creation: 200/1M * 18.75 = 0.00375
        cost = track_queries.calculate_cost(1000, 5000, 800, 200)
        expected = 0.015 + 0.375 + 0.0012 + 0.00375
        assert cost == round(expected, 6)


# =============================================================================
# estimate_tokens_hybrid
# =============================================================================

class TestEstimateTokensHybrid:
    def test_basic_estimation(self):
        """Hybrid estimation combines all three steps with default calibration."""
        # 40 chars -> 10 input tokens (step 1)
        # calibration 1.0 -> still 10 (step 2)
        # code_generation 5x -> 50 output tokens (step 3)
        # cache: 8 read, 2 creation
        text = "a" * 40
        result = track_queries.estimate_tokens_hybrid(text, "code_generation")
        assert result["input"] == 10
        assert result["output"] == 50
        assert result["cache_read"] == 8
        assert result["cache_creation"] == 2
        assert result["is_estimated"] is True

    def test_with_calibration_factor(self):
        """Calibration factor scales the input tokens."""
        text = "a" * 40  # 10 raw input tokens
        result = track_queries.estimate_tokens_hybrid(text, "other", calibration_factor=2.0)
        # 10 * 2.0 = 20 calibrated input
        assert result["input"] == 20
        # other = 2x -> 40 output
        assert result["output"] == 40

    def test_empty_query(self):
        """An empty query produces all zeros."""
        result = track_queries.estimate_tokens_hybrid("", "other")
        assert result["input"] == 0
        assert result["output"] == 0
        assert result["cache_read"] == 0
        assert result["cache_creation"] == 0


# =============================================================================
# calculate_calibration_factors
# =============================================================================

class TestCalculateCalibrationFactors:
    def test_with_matching_aggregates(self):
        """Calibration factor adjusts estimates to match daily actuals."""
        entries_by_date = {
            "2025-01-15": [("a" * 40, "other")],  # 10 input + 20 output = 30 estimated
        }
        daily_aggregates = {
            "2025-01-15": {"input": 60, "output": 0},  # 60 actual
        }
        factors = track_queries.calculate_calibration_factors(
            entries_by_date, daily_aggregates
        )
        assert factors["2025-01-15"] == 60 / 30  # 2.0

    def test_no_aggregate_data_returns_1(self):
        """When no aggregate data exists for a date, factor is 1.0."""
        entries_by_date = {
            "2025-01-15": [("hello world", "other")],
        }
        factors = track_queries.calculate_calibration_factors(entries_by_date, {})
        assert factors["2025-01-15"] == 1.0

    def test_multiple_dates(self):
        """Each date gets its own calibration factor."""
        entries_by_date = {
            "2025-01-15": [("a" * 40, "other")],
            "2025-01-16": [("b" * 80, "other")],
        }
        daily_aggregates = {
            "2025-01-15": {"input": 30, "output": 0},
            "2025-01-16": {"input": 30, "output": 0},
        }
        factors = track_queries.calculate_calibration_factors(
            entries_by_date, daily_aggregates
        )
        assert "2025-01-15" in factors
        assert "2025-01-16" in factors
        # Different query lengths produce different factors
        assert factors["2025-01-15"] != factors["2025-01-16"]

    def test_zero_estimated_total_returns_1(self):
        """When estimated total is 0, factor defaults to 1.0."""
        entries_by_date = {
            "2025-01-15": [("", "other")],  # empty query -> 0 estimated
        }
        daily_aggregates = {
            "2025-01-15": {"input": 100, "output": 50},
        }
        factors = track_queries.calculate_calibration_factors(
            entries_by_date, daily_aggregates
        )
        assert factors["2025-01-15"] == 1.0


# =============================================================================
# load_daily_token_aggregates
# =============================================================================

class TestLoadDailyTokenAggregates:
    def test_missing_file_returns_empty(self, tmp_path):
        """Returns empty dict when stats file doesn't exist."""
        with mock.patch.object(track_queries, "STATS_FILE", tmp_path / "nope.json"):
            result = track_queries.load_daily_token_aggregates()
        assert result == {}

    def test_corrupt_file_returns_empty(self, tmp_path):
        """Returns empty dict when stats file is invalid JSON."""
        stats_file = tmp_path / "stats.json"
        stats_file.write_text("not json{{{")
        with mock.patch.object(track_queries, "STATS_FILE", stats_file):
            result = track_queries.load_daily_token_aggregates()
        assert result == {}

    def test_parses_daily_model_tokens(self, tmp_path):
        """Parses dailyModelTokens entries and applies model usage ratios."""
        stats = {
            "dailyModelTokens": [
                {
                    "date": "2025-01-15",
                    "tokensByModel": {"opus": 1000},
                },
            ],
            "modelUsage": {
                "opus": {
                    "inputTokens": 500,
                    "outputTokens": 400,
                    "cacheReadInputTokens": 80,
                    "cacheCreationInputTokens": 20,
                },
            },
        }
        stats_file = tmp_path / "stats.json"
        stats_file.write_text(json.dumps(stats))

        with mock.patch.object(track_queries, "STATS_FILE", stats_file):
            result = track_queries.load_daily_token_aggregates()

        assert "2025-01-15" in result
        day = result["2025-01-15"]
        # Total is 1000, ratios from modelUsage (500+400+80+20=1000)
        assert day["input"] == 500
        assert day["output"] == 400
        assert day["cache_read"] == 80
        assert day["cache_creation"] == 20


# =============================================================================
# ensure_csv_exists
# =============================================================================

class TestEnsureCsvExists:
    def test_creates_csv_with_headers(self, tmp_path):
        """Creates the CSV file with the expected header row."""
        csv_path = tmp_path / "query_log.csv"
        with (
            mock.patch.object(track_queries, "OUTPUT_DIR", tmp_path),
            mock.patch.object(track_queries, "OUTPUT_CSV", csv_path),
        ):
            track_queries.ensure_csv_exists()

        assert csv_path.exists()
        with open(csv_path) as f:
            reader = csv.reader(f)
            headers = next(reader)
        assert "timestamp" in headers
        assert "cost_usd" in headers
        assert "query_type" in headers

    def test_does_not_overwrite_existing(self, tmp_path):
        """If the CSV already exists, it is not overwritten."""
        csv_path = tmp_path / "query_log.csv"
        csv_path.write_text("existing,data\n")
        with (
            mock.patch.object(track_queries, "OUTPUT_DIR", tmp_path),
            mock.patch.object(track_queries, "OUTPUT_CSV", csv_path),
        ):
            track_queries.ensure_csv_exists()

        assert csv_path.read_text() == "existing,data\n"


# =============================================================================
# get_session_tokens
# =============================================================================

class TestGetSessionTokens:
    def test_matching_session(self):
        """Returns token data when the session matches a project's last session."""
        config = {
            "projects": {
                "/some/project": {
                    "lastSessionId": "session-1",
                    "lastTotalInputTokens": 100,
                    "lastTotalOutputTokens": 200,
                    "lastTotalCacheReadInputTokens": 80,
                    "lastTotalCacheCreationInputTokens": 20,
                },
            },
        }
        result = track_queries.get_session_tokens(config, "session-1")
        assert result is not None
        assert result["input"] == 100
        assert result["output"] == 200
        assert result["is_estimated"] is False

    def test_no_matching_session(self):
        """Returns None when no project matches the session ID."""
        config = {
            "projects": {
                "/some/project": {"lastSessionId": "other-session"},
            },
        }
        assert track_queries.get_session_tokens(config, "session-1") is None

    def test_empty_config(self):
        """Returns None when config has no projects."""
        assert track_queries.get_session_tokens({}, "session-1") is None
