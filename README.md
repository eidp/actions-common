# Common Actions and Workflows

This repository contains common GitHub Actions and shared workflows.

<!-- BEGIN ACTIONS -->

## 🛠️ GitHub Actions

The following GitHub Actions are available in this repository:

- [commit-sha](commit-sha/README.md)
- [check-workflow-status](check-workflow-status/README.md)
- [renovate](renovate/README.md)

<!-- END ACTIONS -->

<!-- BEGIN SHARED WORKFLOWS -->

## 📚 Shared Workflows

The following reusable workflows are available in this repository:

- [common](./.github/workflows/README.md#common-workflow)

<!-- END SHARED WORKFLOWS -->

## GitHub self-hosted actions runner tool cache

This repository contains a workflow that sets up a self-hosted GitHub Actions runner tool cache and publishes it to an S3 bucket.
The tool cache is used to speed up the execution of GitHub Actions by caching tools and dependencies that are commonly used in workflows.
The workflow is located in the `.github/workflows/tool-cache.yml` file.

## Development

### Pre-commit hooks

To ensure code quality and consistency, this repository uses [pre-commit](https://pre-commit.com/) hooks. Make sure to
install the pre-commit hooks by running:

```bash
pre-commit install
```
