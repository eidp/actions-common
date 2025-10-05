<!-- NOTE: This file's contents are automatically generated. Do not edit manually. -->
# Renovate with Dynamic Secrets (Action)

Run Renovate with auto-detected RENOVATE_* secrets from GitHub Secrets.
Renovate - http://renovatebot.com - is an open-source tool that automates dependency updates across your projects. It helps keep your dependencies up-to-date by creating pull requests when new versions are available, reducing technical debt and security vulnerabilities.
Key features of this action: - Dynamic secret detection: Automatically detects and passes all RENOVATE_*
  secrets from your GitHub Secrets as environment variables. Existing environment variables
  will be overwritten if they conflict.
- GitHub App authentication: Uses a GitHub App for improved API rate limits
  and better permission control
- Flexible configuration: Supports custom Renovate configs, Docker images,
  and repository targeting
- Registry authentication: Automatically configures authentication for npm,
  Docker, and other registries using your secrets

## 🔧 Inputs

|            Name           |                                                            Description                                                            |Required|                                                     Default                                                    |
|---------------------------|-----------------------------------------------------------------------------------------------------------------------------------|--------|----------------------------------------------------------------------------------------------------------------|
|      `github-app-id`      |                                             The ID of the GitHub App used for Renovate                                            |   Yes  |                                                                                                                |
|      `github-app-pem`     |                                The private key (in PEM format) of the GitHub App used for Renovate                                |   Yes  |                                                                                                                |
|       `all-secrets`       |JSON string of all secrets (use toJSON(secrets)) or a manually specified JSON object with RENOVATE_* keys. See README for examples.|   Yes  |                                                                                                                |
|`renovate-config-file-path`|                               The full path to the Renovate configuration file, relative to the root                              |   No   |                                                 `renovate.json`                                                |
|      `renovate-image`     |                       The Renovate Docker image name to use. If omitted, uses ghcr.io/renovatebot/renovate.                       |   No   |                                           `ghcr.io/renovate/renovate`                                          |
|     `renovate-version`    |                           The Renovate version to use. If omitted, uses the default version Docker tag.                           |   No   |                                                       ``                                                       |
|        `log-level`        |                                           Renovate log level (debug, info, warn, error)                                           |   No   |                                                     `debug`                                                    |
|        `repository`       |                 Repository to run Renovate on. Format: owner/repo Defaults to current repository if not specified.                |   No   |                                                       ``                                                       |
|    `onboarding-config`    |                               Onboarding config to use when generating a onboarding PR for Renovate.                              |   No   |`{ "$schema": "https://docs.renovatebot.com/renovate-schema.json", "extends": ["github>eidp/renovate-config"] }`|

## 📤 Outputs

_None_

## 🚀 Usage

```yaml
- name: Renovate with Dynamic Secrets
  uses: eidp/actions-common/renovate@v0
  with:
    # your inputs here
```


## 📚 Examples

### Basic Usage with All Secrets

The simplest way to use this action is to pass all your secrets using `toJSON(secrets)`:

```yaml
- name: Run Renovate
  uses: eidp/actions-common/renovate@v0
  with:
    github-app-id: ${{ secrets.RENOVATE_APP_ID }}
    github-app-pem: ${{ secrets.RENOVATE_APP_PEM }}
    all-secrets: ${{ toJSON(secrets) }}
```

### Manual Secrets Configuration

You can also manually specify which secrets to pass. Only secrets with keys starting with `RENOVATE_` will be used:

```yaml
- name: Run Renovate
  uses: eidp/actions-common/renovate@v0
  with:
    github-app-id: ${{ secrets.RENOVATE_APP_ID }}
    github-app-pem: ${{ secrets.RENOVATE_APP_PEM }}
    all-secrets: |
      {
        "RENOVATE_DOCKER_USERNAME": "${{ secrets.RENOVATE_DOCKER_USERNAME }}",
        "RENOVATE_DOCKER_PASSWORD": "${{ secrets.RENOVATE_DOCKER_PASSWORD }}",
        "RENOVATE_NPM_TOKEN": "${{ secrets.RENOVATE_NPM_TOKEN }}"
      }
```

### Custom Configuration

You can customize the Renovate execution with additional inputs:

```yaml
- name: Run Renovate
  uses: eidp/actions-common/renovate@v0
  with:
    github-app-id: ${{ secrets.RENOVATE_APP_ID }}
    github-app-pem: ${{ secrets.RENOVATE_APP_PEM }}
    all-secrets: ${{ toJSON(secrets) }}
    renovate-config-file-path: 'config/renovate.json'
    renovate-version: '41'
    log-level: 'info'
    repository: 'my-org/my-repo'
```
