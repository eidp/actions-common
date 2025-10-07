# Unit tests for check_status.py
import os
import sys
import json
import tempfile
from unittest import mock
import check_status


# Test: Dynamic job discovery with multiple jobs
def test_dynamic_job_discovery():
    def test_fetch_json(url, token):
        if "actions/runs" in url and "jobs" in url:
            return {"jobs": [
                {"name": "check-workflow-status", "conclusion": None},
                {"name": "build", "conclusion": "success"},
                {"name": "test", "conclusion": "success"},
                {"name": "lint", "conclusion": "success"}
            ]}
        return {}

    with mock.patch("check_status.fetch_json", side_effect=test_fetch_json):
        with mock.patch("time.sleep"):
            result = check_status.check_status(
                github_token="dummy_token",
                repo="eidp/actions-common",
                run_id="1",
                initial_wait_seconds=0,
            )

    assert result is True, f"Expected all jobs to succeed, got {result}"


# Test: Job appears dynamically during execution
def test_dynamic_job_appearance():
    call_count = [0]

    def test_fetch_json(url, token):
        if "actions/runs" in url and "jobs" in url:
            call_count[0] += 1
            # First call: only check-workflow-status job
            if call_count[0] == 1:
                return {"jobs": [
                    {"name": "check-workflow-status", "conclusion": None},
                ]}
            # Second call: test job appears
            elif call_count[0] == 2:
                return {"jobs": [
                    {"name": "check-workflow-status", "conclusion": None},
                    {"name": "test", "conclusion": None},
                ]}
            # Third call: test job completes
            else:
                return {"jobs": [
                    {"name": "check-workflow-status", "conclusion": None},
                    {"name": "test", "conclusion": "success"},
                ]}
        return {}

    with mock.patch("check_status.fetch_json", side_effect=test_fetch_json):
        with mock.patch("time.sleep"):
            result = check_status.check_status(
                github_token="dummy_token",
                repo="eidp/actions-common",
                run_id="1",
                initial_wait_seconds=2,  # Need a few polls for job to appear
            )

    assert result is True, f"Expected job to be discovered and succeed, got {result}"


# Test: Current job is excluded from checks
def test_current_job_excluded():
    def test_fetch_json(url, token):
        if "actions/runs" in url and "jobs" in url:
            return {"jobs": [
                {"name": "check-workflow-status", "conclusion": None},  # This is the current job
                {"name": "test", "conclusion": "success"},
            ]}
        return {}

    with mock.patch("check_status.fetch_json", side_effect=test_fetch_json):
        with mock.patch("time.sleep"):
            result = check_status.check_status(
                github_token="dummy_token",
                repo="eidp/actions-common",
                run_id="1",
                initial_wait_seconds=0,
            )

    assert result is True, f"Expected success (current job excluded), got {result}"


# Test: Skipped jobs with skipped_jobs_succeed=True
def test_skipped_jobs_succeed_true():
    def test_fetch_json(url, token):
        if "actions/runs" in url and "jobs" in url:
            return {"jobs": [
                {"name": "check-workflow-status", "conclusion": None},
                {"name": "test", "conclusion": "skipped"},
            ]}
        return {}

    with mock.patch("check_status.fetch_json", side_effect=test_fetch_json):
        with mock.patch("time.sleep"):
            result = check_status.check_status(
                github_token="dummy_token",
                repo="eidp/actions-common",
                run_id="1",
                initial_wait_seconds=0,
            )

    assert result is True, f"Expected skipped job to succeed, got {result}"


# Test: Skipped jobs with skipped_jobs_succeed=False
def test_skipped_jobs_succeed_false():
    def test_fetch_json(url, token):
        if "actions/runs" in url and "jobs" in url:
            return {"jobs": [
                {"name": "check-workflow-status", "conclusion": None},
                {"name": "test", "conclusion": "skipped"},
            ]}
        return {}

    with mock.patch("check_status.fetch_json", side_effect=test_fetch_json):
        with mock.patch("time.sleep"):
            result = check_status.check_status(
                github_token="dummy_token",
                repo="eidp/actions-common",
                run_id="1",
                initial_wait_seconds=0,
                skipped_jobs_succeed=False,
            )

    assert result is False, f"Expected skipped job to fail, got {result}"


# Test: Job failure causes immediate failure
def test_job_failure_immediate():
    def test_fetch_json(url, token):
        if "actions/runs" in url and "jobs" in url:
            return {"jobs": [
                {"name": "check-workflow-status", "conclusion": None},
                {"name": "test", "conclusion": "failure"},
                {"name": "build", "conclusion": None},  # Still in progress
            ]}
        return {}

    with mock.patch("check_status.fetch_json", side_effect=test_fetch_json):
        with mock.patch("time.sleep"):
            result = check_status.check_status(
                github_token="dummy_token",
                repo="eidp/actions-common",
                run_id="1",
                initial_wait_seconds=0,
            )

    assert result is False, f"Expected failure due to failed job, got {result}"


# Test: Overall timeout exceeded
def test_overall_timeout():
    def test_fetch_json(url, token):
        if "actions/runs" in url and "jobs" in url:
            return {"jobs": [
                {"name": "check-workflow-status", "conclusion": None},
                {"name": "test", "conclusion": None},  # Never completes
            ]}
        return {}

    # Mock time to simulate timeout
    start_time = 1000.0
    elapsed = [0]

    def mock_time():
        return start_time + elapsed[0]

    def mock_sleep(seconds):
        elapsed[0] += 60  # Fast-forward by 1 minute each sleep

    with mock.patch("check_status.fetch_json", side_effect=test_fetch_json):
        with mock.patch("time.time", side_effect=mock_time):
            with mock.patch("time.sleep", side_effect=mock_sleep):
                result = check_status.check_status(
                    github_token="dummy_token",
                    repo="eidp/actions-common",
                    run_id="1",
                    initial_wait_seconds=0,
                    timeout_minutes=1,
                )

    assert result is False, f"Expected timeout failure, got {result}"


# Test: No jobs found after initial wait
def test_no_jobs_found():
    def test_fetch_json(url, token):
        if "actions/runs" in url and "jobs" in url:
            return {"jobs": [
                {"name": "check-workflow-status", "conclusion": None},  # Only current job
            ]}
        return {}

    # Mock time for initial wait
    start_time = 1000.0
    elapsed = [0]

    def mock_time():
        return start_time + elapsed[0]

    def mock_sleep(seconds):
        elapsed[0] += seconds

    with mock.patch("check_status.fetch_json", side_effect=test_fetch_json):
        with mock.patch("time.time", side_effect=mock_time):
            with mock.patch("time.sleep", side_effect=mock_sleep):
                result = check_status.check_status(
                    github_token="dummy_token",
                    repo="eidp/actions-common",
                    run_id="1",
                    initial_wait_seconds=2,
                )

    assert result is False, f"Expected failure (no jobs found), got {result}"


# Test: Excluded jobs with exact match
def test_excluded_jobs_exact():
    def test_fetch_json(url, token):
        if "actions/runs" in url and "jobs" in url:
            return {"jobs": [
                {"name": "check-workflow-status", "conclusion": None},
                {"name": "build", "conclusion": "success"},
                {"name": "deploy-staging", "conclusion": "failure"},  # Excluded
                {"name": "test", "conclusion": "success"},
            ]}
        return {}

    with mock.patch("check_status.fetch_json", side_effect=test_fetch_json):
        with mock.patch("time.sleep"):
            result = check_status.check_status(
                github_token="dummy_token",
                repo="eidp/actions-common",
                run_id="1",
                initial_wait_seconds=0,
                excluded_jobs="deploy-staging",
            )

    assert result is True, f"Expected success (deploy-staging excluded), got {result}"


# Test: Excluded jobs with glob pattern
def test_excluded_jobs_glob():
    def test_fetch_json(url, token):
        if "actions/runs" in url and "jobs" in url:
            return {"jobs": [
                {"name": "check-workflow-status", "conclusion": None},
                {"name": "build", "conclusion": "success"},
                {"name": "deploy-dev", "conclusion": "failure"},  # Excluded by deploy-*
                {"name": "deploy-staging", "conclusion": "failure"},  # Excluded by deploy-*
                {"name": "test", "conclusion": "success"},
            ]}
        return {}

    with mock.patch("check_status.fetch_json", side_effect=test_fetch_json):
        with mock.patch("time.sleep"):
            result = check_status.check_status(
                github_token="dummy_token",
                repo="eidp/actions-common",
                run_id="1",
                initial_wait_seconds=0,
                excluded_jobs="deploy-*",
            )

    assert result is True, f"Expected success (deploy-* excluded), got {result}"


# Test: Excluded jobs with multiple patterns
def test_excluded_jobs_multiple():
    def test_fetch_json(url, token):
        if "actions/runs" in url and "jobs" in url:
            return {"jobs": [
                {"name": "check-workflow-status", "conclusion": None},
                {"name": "build", "conclusion": "success"},
                {"name": "deploy-prod", "conclusion": "failure"},  # Excluded by deploy-*
                {"name": "test-optional", "conclusion": "failure"},  # Excluded by *-optional
                {"name": "test-required", "conclusion": "success"},
            ]}
        return {}

    with mock.patch("check_status.fetch_json", side_effect=test_fetch_json):
        with mock.patch("time.sleep"):
            result = check_status.check_status(
                github_token="dummy_token",
                repo="eidp/actions-common",
                run_id="1",
                initial_wait_seconds=0,
                excluded_jobs="deploy-*,*-optional",
            )

    assert result is True, f"Expected success (deploy-* and *-optional excluded), got {result}"


# Test: Non-excluded job fails
def test_excluded_jobs_non_excluded_fails():
    def test_fetch_json(url, token):
        if "actions/runs" in url and "jobs" in url:
            return {"jobs": [
                {"name": "check-workflow-status", "conclusion": None},
                {"name": "build", "conclusion": "failure"},  # NOT excluded, should fail
                {"name": "deploy-staging", "conclusion": "failure"},  # Excluded
            ]}
        return {}

    with mock.patch("check_status.fetch_json", side_effect=test_fetch_json):
        with mock.patch("time.sleep"):
            result = check_status.check_status(
                github_token="dummy_token",
                repo="eidp/actions-common",
                run_id="1",
                initial_wait_seconds=0,
                excluded_jobs="deploy-*",
            )

    assert result is False, f"Expected failure (build failed), got {result}"


def main():
    print("Testing dynamic job discovery...")
    test_dynamic_job_discovery()

    print("Testing dynamic job appearance...")
    test_dynamic_job_appearance()

    print("Testing current job exclusion...")
    test_current_job_excluded()

    print("Testing skipped jobs (succeed=true)...")
    test_skipped_jobs_succeed_true()

    print("Testing skipped jobs (succeed=false)...")
    test_skipped_jobs_succeed_false()

    print("Testing job failure...")
    test_job_failure_immediate()

    print("Testing overall timeout...")
    test_overall_timeout()

    print("Testing no jobs found...")
    test_no_jobs_found()

    print("All tests passed.")

if __name__ == "__main__":
    main()
