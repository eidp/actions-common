import os
import sys
import time
import urllib.request
import json
import fnmatch

def get_env(name, required=True, default=None):
    value = os.environ.get(name, default)
    if required and value is None:
        print(f"Missing required environment variable: {name}", file=sys.stderr)
        sys.exit(1)
    return value

def fetch_json(url, token):
    req = urllib.request.Request(url)
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("Accept", "application/vnd.github+json")
    try:
        with urllib.request.urlopen(req) as resp:
            if resp.status != 200:
                print(f"Failed to fetch {url} (HTTP {resp.status})", file=sys.stderr)
                print(f"Response: {resp.read().decode()}", file=sys.stderr)
                sys.exit(1)
            return json.load(resp)
    except Exception as e:
        print(f"Error fetching {url}: {e}", file=sys.stderr)
        sys.exit(1)

def main():
    jobs = [j.strip() for j in get_env("INPUT_JOBS").split(",") if j.strip()]
    github_token = get_env("INPUT_GITHUB_TOKEN")
    requires_files_changed = get_env("INPUT_REQUIRES_FILES_CHANGED", required=False, default="")
    event_name = get_env("GITHUB_EVENT_NAME")
    repo = get_env("GITHUB_REPOSITORY")
    run_id = get_env("GITHUB_RUN_ID")
    event_path = get_env("GITHUB_EVENT_PATH")

    # Check for required files changed on PRs
    if requires_files_changed and event_name == "pull_request":
        print(f"Checking if PR has changed files matching patterns: {requires_files_changed}")
        with open(event_path, "r") as f:
            event = json.load(f)
        pr_number = event["number"]
        api_url = f"https://api.github.com/repos/{repo}/pulls/{pr_number}/files"
        files = fetch_json(api_url, github_token)
        if not isinstance(files, list):
            print("No changed files found in API response. Check permissions, token, and run ID.", file=sys.stderr)
            sys.exit(1)
        changed_files = [f["filename"] for f in files]
        patterns = [p.strip() for p in requires_files_changed.split(",") if p.strip()]
        match_found = any(
            any(fnmatch.fnmatch(file, pattern) for pattern in patterns)
            for file in changed_files
        )
        if not match_found:
            print("No changed files match the required patterns. Exiting successfully.")
            sys.exit(0)
        print("Found matching files. Proceeding with workflow status check.")

    # Check job statuses
    jobs_api_url = f"https://api.github.com/repos/{repo}/actions/runs/{run_id}/jobs"
    max_attempts = 10
    for job in jobs:
        attempt = 1
        job_found = False
        while attempt <= max_attempts:
            jobs_response = fetch_json(jobs_api_url, github_token)
            job_obj = next((j for j in jobs_response.get("jobs", []) if j["name"] == job), None)
            if job_obj:
                job_found = True
                break
            print(f"Job '{job}' not found. Attempt {attempt}/{max_attempts}. Waiting...")
            time.sleep(2)
            attempt += 1
        if not job_found:
            found_names = [j["name"] for j in jobs_response.get("jobs", [])]
            print(f"Jobs found: {', '.join(found_names)}")
            print(f"Job '{job}' does not exist after {max_attempts} attempts.", file=sys.stderr)
            sys.exit(1)
        # Wait for job to finish
        while True:
            conclusion = job_obj.get("conclusion")
            if conclusion is None:
                print(f"Job '{job}' is still in progress. Waiting...")
                time.sleep(1)
                jobs_response = fetch_json(jobs_api_url, github_token)
                job_obj = next((j for j in jobs_response.get("jobs", []) if j["name"] == job), None)
                continue
            if conclusion == "success":
                print(f"Job '{job}' completed successfully.")
            elif conclusion in ("failure", "cancelled"):
                print(f"Job '{job}' failed or was cancelled.", file=sys.stderr)
                sys.exit(1)
            break

if __name__ == "__main__":
    main()
