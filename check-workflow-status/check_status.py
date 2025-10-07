import os
import sys
import time
import urllib.request
import json
import fnmatch


def get_env(name, required=True, default=None):
    value = os.environ.get(name, default)
    if required and value is None:
        raise ValueError(f"Missing required environment variable: {name}")
    return value

def fetch_json(url, token):
    req = urllib.request.Request(url)
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("Accept", "application/vnd.github+json")
    with urllib.request.urlopen(req) as resp:
        if resp.status != 200:
            raise RuntimeError(f"Failed to fetch {url} (HTTP {resp.status})\nResponse: {resp.read().decode()}")
        return json.load(resp)


def check_status(
    github_token,
    repo,
    run_id,
    excluded_jobs="",
    timeout_minutes=30,
    initial_wait_seconds=10,
    skipped_jobs_succeed=True,
    poll_interval_seconds=5,
    current_job_name="check-workflow-status",
):
    start_time = time.time()
    timeout_seconds = timeout_minutes * 60

    # Parse excluded job patterns
    excluded_patterns = [p.strip() for p in excluded_jobs.split(",") if p.strip()]

    def is_excluded(job_name):
        """Check if a job name matches any excluded pattern."""
        return any(fnmatch.fnmatch(job_name, pattern) for pattern in excluded_patterns)

    if excluded_patterns:
        print(f"Excluding jobs matching patterns: {excluded_patterns}")

    # Phase 1: Wait the full initial wait period for jobs to appear
    jobs_api_url = f"https://api.github.com/repos/{repo}/actions/runs/{run_id}/jobs"
    print(f"Waiting {initial_wait_seconds}s for all jobs to appear (excluding current job: '{current_job_name}')...")

    initial_wait_end = start_time + initial_wait_seconds
    other_jobs_found = False
    all_jobs = []
    other_jobs = []

    # Always fetch jobs at least once, then continue polling until initial_wait_seconds
    while True:
        if time.time() - start_time > timeout_seconds:
            print(f"Overall timeout of {timeout_minutes} minutes exceeded.", file=sys.stderr)
            return False

        jobs_response = fetch_json(jobs_api_url, github_token)
        all_jobs = jobs_response.get("jobs", [])
        other_jobs = [j for j in all_jobs if j["name"] != current_job_name and not is_excluded(j["name"])]

        if other_jobs:
            other_jobs_found = True

        # Check if we've waited long enough
        if time.time() >= initial_wait_end:
            break

        time.sleep(1)

    if not other_jobs_found:
        print(f"No jobs found after {initial_wait_seconds}s initial wait period.", file=sys.stderr)
        print(f"Current job name: '{current_job_name}'", file=sys.stderr)
        all_job_names = [j["name"] for j in all_jobs]
        print(f"All jobs in workflow: {all_job_names}", file=sys.stderr)
        return False

    print(f"Initial wait complete. Found {len(other_jobs)} job(s) to monitor.")

    # Phase 2: Monitor all jobs until completion or timeout
    print(f"Monitoring jobs (polling every {poll_interval_seconds}s, timeout: {timeout_minutes} minutes)...")
    discovered_jobs = set()
    completed_jobs = {}

    while True:
        elapsed = time.time() - start_time
        if elapsed > timeout_seconds:
            print(f"Overall timeout of {timeout_minutes} minutes exceeded.", file=sys.stderr)
            print(f"Completed jobs: {len(completed_jobs)}/{len(discovered_jobs)}", file=sys.stderr)
            incomplete = discovered_jobs - set(completed_jobs.keys())
            if incomplete:
                print(f"Incomplete jobs: {sorted(incomplete)}", file=sys.stderr)
            return False

        jobs_response = fetch_json(jobs_api_url, github_token)
        all_jobs = jobs_response.get("jobs", [])
        other_jobs = [j for j in all_jobs if j["name"] != current_job_name and not is_excluded(j["name"])]

        # Track all discovered jobs
        for job in other_jobs:
            job_name = job["name"]
            if job_name not in discovered_jobs:
                discovered_jobs.add(job_name)
                print(f"Discovered job: '{job_name}'")

        # Check completion status
        for job in other_jobs:
            job_name = job["name"]
            conclusion = job.get("conclusion")

            if conclusion is not None and job_name not in completed_jobs:
                completed_jobs[job_name] = conclusion

                if conclusion == "success":
                    print(f"✓ Job '{job_name}' completed successfully.")
                elif conclusion == "skipped":
                    if skipped_jobs_succeed:
                        print(f"✓ Job '{job_name}' was skipped (treated as success).")
                    else:
                        print(f"✗ Job '{job_name}' was skipped (treated as failure).", file=sys.stderr)
                        return False
                elif conclusion in ("failure", "cancelled"):
                    print(f"✗ Job '{job_name}' {conclusion}.", file=sys.stderr)
                    return False
                else:
                    print(f"✗ Job '{job_name}' has unexpected conclusion: {conclusion}.", file=sys.stderr)
                    return False

        # Check if all discovered jobs are complete
        if len(completed_jobs) == len(discovered_jobs) and len(discovered_jobs) > 0:
            print(f"All {len(discovered_jobs)} job(s) completed successfully in {elapsed:.1f}s.")
            return True

        # Show progress
        in_progress = discovered_jobs - set(completed_jobs.keys())
        if in_progress:
            print(f"In progress ({len(completed_jobs)}/{len(discovered_jobs)} complete): {sorted(in_progress)}")

        time.sleep(poll_interval_seconds)

def main():
    try:
        github_token = get_env("INPUT_GITHUB_TOKEN")
        repo = get_env("GITHUB_REPOSITORY")
        run_id = get_env("GITHUB_RUN_ID")
        current_job_name = get_env("GITHUB_JOB")

        # Parse optional configuration (with defaults in check_status function)
        kwargs = {}
        if get_env("INPUT_TIMEOUT_MINUTES", required=False):
            kwargs["timeout_minutes"] = int(get_env("INPUT_TIMEOUT_MINUTES", required=False))
        if get_env("INPUT_INITIAL_WAIT_SECONDS", required=False):
            kwargs["initial_wait_seconds"] = int(get_env("INPUT_INITIAL_WAIT_SECONDS", required=False))
        if get_env("INPUT_SKIPPED_JOBS_SUCCEED", required=False):
            kwargs["skipped_jobs_succeed"] = get_env("INPUT_SKIPPED_JOBS_SUCCEED", required=False).lower() == "true"
        if get_env("INPUT_POLL_INTERVAL_SECONDS", required=False):
            kwargs["poll_interval_seconds"] = int(get_env("INPUT_POLL_INTERVAL_SECONDS", required=False))
        if get_env("INPUT_EXCLUDED_JOBS", required=False):
            kwargs["excluded_jobs"] = get_env("INPUT_EXCLUDED_JOBS", required=False)
    except Exception as e:
        print(str(e), file=sys.stderr)
        sys.exit(1)

    result = check_status(
        github_token=github_token,
        repo=repo,
        run_id=run_id,
        current_job_name=current_job_name,
        **kwargs
    )
    sys.exit(0 if result else 1)

if __name__ == "__main__":
    main()
