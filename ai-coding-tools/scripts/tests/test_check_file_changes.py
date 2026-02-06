"""Tests for check_file_changes.py."""

import hashlib
import json
from io import StringIO
from unittest import mock

import check_file_changes


class TestSha256:
    def test_known_content(self, tmp_path):
        """sha256() returns the correct hex digest for known content."""
        p = tmp_path / "hello.txt"
        p.write_bytes(b"hello world")
        expected = hashlib.sha256(b"hello world").hexdigest()
        assert check_file_changes.sha256(p) == expected

    def test_empty_file(self, tmp_path):
        """sha256() handles an empty file."""
        p = tmp_path / "empty.txt"
        p.write_bytes(b"")
        expected = hashlib.sha256(b"").hexdigest()
        assert check_file_changes.sha256(p) == expected

    def test_binary_content(self, tmp_path):
        """sha256() works with binary content."""
        data = bytes(range(256))
        p = tmp_path / "binary.bin"
        p.write_bytes(data)
        expected = hashlib.sha256(data).hexdigest()
        assert check_file_changes.sha256(p) == expected


class TestMain:
    def _setup_project(self, tmp_path):
        """Create a minimal project directory with tracked files."""
        # Create a CLAUDE.md (matches TRACKED_PATTERNS)
        (tmp_path / "CLAUDE.md").write_text("# Project")
        # Create a process file (matches ai-coding-tools/processes/*.md)
        processes_dir = tmp_path / "ai-coding-tools" / "processes"
        processes_dir.mkdir(parents=True)
        (processes_dir / "guide.md").write_text("# Guide")
        return tmp_path

    def test_first_run_outputs_all_tracked_files(self, tmp_path, capsys):
        """On first run, all tracked files should be reported as changed."""
        project = self._setup_project(tmp_path)

        with mock.patch.dict("os.environ", {"CLAUDE_PROJECT_DIR": str(project)}):
            check_file_changes.main()

        output = capsys.readouterr().out
        assert "CLAUDE.md" in output
        assert "guide.md" in output

    def test_second_run_no_changes_produces_no_output(self, tmp_path, capsys):
        """A second run with no file modifications should produce no output."""
        project = self._setup_project(tmp_path)

        with mock.patch.dict("os.environ", {"CLAUDE_PROJECT_DIR": str(project)}):
            check_file_changes.main()
            capsys.readouterr()  # discard first-run output
            check_file_changes.main()

        output = capsys.readouterr().out
        assert output == ""

    def test_detects_file_modification(self, tmp_path, capsys):
        """Modifying a tracked file between runs should be detected."""
        project = self._setup_project(tmp_path)

        with mock.patch.dict("os.environ", {"CLAUDE_PROJECT_DIR": str(project)}):
            check_file_changes.main()
            capsys.readouterr()

            # Modify the file
            (project / "CLAUDE.md").write_text("# Updated Project")
            check_file_changes.main()

        output = capsys.readouterr().out
        assert "CLAUDE.md" in output
        # The unmodified file should NOT appear
        assert "guide.md" not in output

    def test_creates_state_directory(self, tmp_path):
        """The .ai-data/ state directory is created if it doesn't exist."""
        project = self._setup_project(tmp_path)
        state_dir = project / ".ai-data"
        assert not state_dir.exists()

        with mock.patch.dict("os.environ", {"CLAUDE_PROJECT_DIR": str(project)}):
            check_file_changes.main()

        assert state_dir.exists()
        assert (state_dir / ".file_checksums").exists()

    def test_state_file_is_valid_json(self, tmp_path):
        """The saved state file should be valid JSON mapping paths to hashes."""
        project = self._setup_project(tmp_path)

        with mock.patch.dict("os.environ", {"CLAUDE_PROJECT_DIR": str(project)}):
            check_file_changes.main()

        state = json.loads((project / ".ai-data" / ".file_checksums").read_text())
        assert "CLAUDE.md" in state
        assert len(state["CLAUDE.md"]) == 64  # SHA256 hex digest length

    def test_corrupt_state_file_treated_as_empty(self, tmp_path, capsys):
        """A corrupt state file should be treated as if no state exists."""
        project = self._setup_project(tmp_path)
        state_dir = project / ".ai-data"
        state_dir.mkdir(parents=True)
        (state_dir / ".file_checksums").write_text("not json{{{")

        with mock.patch.dict("os.environ", {"CLAUDE_PROJECT_DIR": str(project)}):
            check_file_changes.main()

        # Should behave like first run — output all files
        output = capsys.readouterr().out
        assert "CLAUDE.md" in output
