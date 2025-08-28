# Unit test to make sure that check_status.py correctly handles requires_files_changed patterns
import os
import sys
import json
import tempfile
from unittest import mock
import check_status

pr_event = {
    "number": 123,
}

def write_temp_json(data):
    fd, path = tempfile.mkstemp(suffix=".json")
    with os.fdopen(fd, "w") as f:
        json.dump(data, f)
    return path

def mock_fetch_json(url, token):
    # This will be overridden in each test
    return {}

def run_test(patterns, changed_files_list, should_match):
    event_path = write_temp_json(pr_event)
    
    def test_fetch_json(url, token):
        if "pulls" in url and "files" in url:
            return changed_files_list
        elif "actions/runs" in url and "jobs" in url:
            return {"jobs": [{"name": "dummy", "conclusion": "success"}]}
        else:
            return {}

    with mock.patch("check_status.fetch_json", side_effect=test_fetch_json):
        result = check_status.check_status(
            jobs=["dummy"],
            github_token="dummy_token",
            requires_files_changed=patterns,
            event_name="pull_request",
            repo="eidp/actions-common",
            run_id="1",
            event_path=event_path,
        )

    os.unlink(event_path)
    
    if should_match:
        assert result is True, f"Expected match (True), got {result}"
    else:
        assert result is True, f"Expected no match but successful exit (True), got {result}"

def main():
    # Should match: pattern matches a file
    run_test("src/foo/*.py", [{"filename": "src/foo/bar.py"}], True)
    # Should not match: pattern does not match any file
    run_test("src/baz/*.py", [{"filename": "src/foo/bar.py"}], False)
    # Should match: multiple patterns, one matches
    run_test("src/baz/*.py,src/foo/*.py", [{"filename": "src/foo/bar.py"}], True)
    # Should not match: multiple patterns, none match
    run_test("src/baz/*.py,docs/*.txt", [{"filename": "src/foo/bar.py"}], False)
    print("All tests passed.")

if __name__ == "__main__":
    main()
