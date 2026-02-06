"""Tests for save_session_summary.py."""

import io
import json
import os
from unittest import mock

import save_session_summary


class TestSlugify:
    def test_normal_text(self):
        """Converts a simple phrase to a hyphenated slug."""
        assert save_session_summary.slugify("Hello World") == "hello-world"

    def test_special_characters_stripped(self):
        """Non-alphanumeric characters are removed."""
        assert save_session_summary.slugify("Fix bug #123!") == "fix-bug-123"

    def test_respects_max_words(self):
        """Only the first max_words words are kept."""
        text = "one two three four five six seven eight"
        assert save_session_summary.slugify(text, max_words=3) == "one-two-three"

    def test_default_max_words_is_six(self):
        """Default max_words is 6."""
        text = "a b c d e f g h"
        assert save_session_summary.slugify(text) == "a-b-c-d-e-f"

    def test_empty_string_returns_session(self):
        """An empty string produces the fallback slug 'session'."""
        assert save_session_summary.slugify("") == "session"

    def test_truncates_to_60_characters(self):
        """The slug is truncated to at most 60 characters."""
        text = "a" * 200
        result = save_session_summary.slugify(text)
        assert len(result) <= 60

    def test_whitespace_only_returns_session(self):
        """Whitespace-only input produces the fallback slug."""
        assert save_session_summary.slugify("   ") == "session"


class TestExtractTurns:
    def _write_jsonl(self, path, messages):
        """Write a list of dicts as JSONL."""
        with open(path, "w") as f:
            for msg in messages:
                f.write(json.dumps(msg) + "\n")

    def test_string_content(self, tmp_path):
        """Extracts turns when content is a plain string."""
        transcript = tmp_path / "transcript.jsonl"
        self._write_jsonl(transcript, [
            {"message": {"role": "user", "content": "What is Python?"}},
            {"message": {"role": "assistant", "content": "A programming language."}},
        ])
        turns = save_session_summary.extract_turns(str(transcript))
        assert turns == [
            ("user", "What is Python?"),
            ("assistant", "A programming language."),
        ]

    def test_list_content_with_text_blocks(self, tmp_path):
        """Extracts text from content that is a list of typed blocks."""
        transcript = tmp_path / "transcript.jsonl"
        self._write_jsonl(transcript, [
            {"message": {
                "role": "assistant",
                "content": [
                    {"type": "text", "text": "Here is the answer."},
                    {"type": "tool_use", "name": "Read"},
                    {"type": "text", "text": "And more detail."},
                ],
            }},
        ])
        turns = save_session_summary.extract_turns(str(transcript))
        assert len(turns) == 1
        assert turns[0][0] == "assistant"
        assert "Here is the answer." in turns[0][1]
        assert "And more detail." in turns[0][1]

    def test_skips_system_and_tool_roles(self, tmp_path):
        """Messages with roles other than user/assistant are ignored."""
        transcript = tmp_path / "transcript.jsonl"
        self._write_jsonl(transcript, [
            {"message": {"role": "system", "content": "You are helpful."}},
            {"message": {"role": "user", "content": "Hi"}},
            {"message": {"role": "tool", "content": "file contents..."}},
        ])
        turns = save_session_summary.extract_turns(str(transcript))
        assert len(turns) == 1
        assert turns[0] == ("user", "Hi")

    def test_empty_file(self, tmp_path):
        """An empty transcript returns no turns."""
        transcript = tmp_path / "transcript.jsonl"
        transcript.write_text("")
        assert save_session_summary.extract_turns(str(transcript)) == []

    def test_skips_malformed_json_lines(self, tmp_path):
        """Invalid JSON lines are silently skipped."""
        transcript = tmp_path / "transcript.jsonl"
        transcript.write_text(
            'not json\n'
            + json.dumps({"message": {"role": "user", "content": "Hello"}}) + '\n'
        )
        turns = save_session_summary.extract_turns(str(transcript))
        assert len(turns) == 1

    def test_unwrapped_messages(self, tmp_path):
        """Messages without a 'message' wrapper key still work."""
        transcript = tmp_path / "transcript.jsonl"
        self._write_jsonl(transcript, [
            {"role": "user", "content": "Direct message"},
        ])
        turns = save_session_summary.extract_turns(str(transcript))
        assert turns == [("user", "Direct message")]


class TestBuildSummary:
    def test_contains_session_id(self):
        """The summary includes the session ID."""
        turns = [("user", "Hello")]
        summary = save_session_summary.build_summary(turns, "abc-123")
        assert "abc-123" in summary

    def test_contains_user_and_assistant_headers(self):
        """User and assistant turns get markdown headers."""
        turns = [
            ("user", "What is Python?"),
            ("assistant", "A language."),
        ]
        summary = save_session_summary.build_summary(turns, "s1")
        assert "## User" in summary
        assert "## Assistant" in summary
        assert "What is Python?" in summary
        assert "A language." in summary

    def test_truncates_long_user_messages(self):
        """User messages longer than 500 characters are truncated."""
        long_msg = "x" * 600
        turns = [("user", long_msg)]
        summary = save_session_summary.build_summary(turns, "s1")
        assert "[...truncated]" in summary
        # The full 600-char message should NOT appear
        assert long_msg not in summary

    def test_does_not_truncate_assistant_messages(self):
        """Assistant messages are not truncated regardless of length."""
        long_msg = "y" * 600
        turns = [("assistant", long_msg)]
        summary = save_session_summary.build_summary(turns, "s1")
        assert long_msg in summary


class TestMainIntegration:
    def test_writes_summary_file(self, tmp_path):
        """main() creates a dated markdown file in the context directory."""
        # Create a transcript
        transcript = tmp_path / "transcript.jsonl"
        with open(transcript, "w") as f:
            f.write(json.dumps({
                "message": {"role": "user", "content": "Fix the login bug"}
            }) + "\n")
            f.write(json.dumps({
                "message": {"role": "assistant", "content": "I found the issue."}
            }) + "\n")

        # Create a project directory for output
        project_dir = tmp_path / "project"
        project_dir.mkdir()

        hook_input = json.dumps({
            "transcript_path": str(transcript),
            "session_id": "test-session-42",
            "cwd": str(project_dir),
        })

        with mock.patch("sys.stdin", io.StringIO(hook_input)):
            save_session_summary.main()

        context_dir = project_dir / "ai-coding-tools" / "context"
        assert context_dir.exists()
        md_files = list(context_dir.glob("*.md"))
        assert len(md_files) == 1

        content = md_files[0].read_text()
        assert "test-session-42" in content
        assert "Fix the login bug" in content

    def test_no_transcript_path_exits_quietly(self):
        """main() exits without error when no transcript path is provided."""
        hook_input = json.dumps({"session_id": "s1"})
        with mock.patch("sys.stdin", io.StringIO(hook_input)):
            # Should not raise
            save_session_summary.main()

    def test_empty_transcript_exits_quietly(self, tmp_path):
        """main() exits without error when the transcript has no turns."""
        transcript = tmp_path / "transcript.jsonl"
        transcript.write_text("")

        hook_input = json.dumps({
            "transcript_path": str(transcript),
            "session_id": "s1",
            "cwd": str(tmp_path),
        })
        with mock.patch("sys.stdin", io.StringIO(hook_input)):
            save_session_summary.main()

        # No context directory should have been created
        assert not (tmp_path / "ai-coding-tools" / "context").exists()
