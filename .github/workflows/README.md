# Common shared workflows

## Common workflow (Workflow)

This workflow runs a number of very common tasks that are useful in many repositories.

The tasks include:
- labelling pull requests based on commit messages using the conventional commits standard.

This workflow requires the following GitHub permissions:
```yaml
permissions:
  pull-requests: write
```

<!-- BEGIN WORKFLOW INPUT DOCS: common -->

### 🔧 Inputs

|Name      |Description                                                                                                            |Required|Type   |Default         |
|----------|-----------------------------------------------------------------------------------------------------------------------|--------|-------|----------------|
|`runs-on` |The type of runner to use for the workflow. Defaults to 'ubuntu-latest'. You can specify a different runner if needed. |No      |string |`ubuntu-latest` |

### 🔐 Secrets

_None_

### 📤 Outputs

_None_

<!-- END WORKFLOW INPUT DOCS -->

### Example Usage

```yaml
name: 'Common PR workflow'

on:
  pull_request:
    branches:
      - main

jobs:
  common:
    uses: eidp/actions-common/.github/workflows/common.yml@v0
    secrets:
      GITHUB_SECRET: ${{ secrets.GITHUB_SECRET }}
```

## Renovate workflow (Workflow)

This reusable workflow is runs [Renovate](https://www.renovatebot.com/) self-hosted as part of a GitHub actions pipeline.
It can load the "global" Renovate configuration from a separate repository.

Under the hood this workflow uses the [Renovate GitHub action](https://github.com/renovatebot/github-action?tab=readme-ov-file)

It is best to trigger this workflow on a schedule, for example, every half hour.
```yaml
on:
  schedule:
    - cron: '0,30 * * * *'
```

This workflow requires a GitHub app that is set up with the permissions as is stated in the [Renovate documentation](https://docs.renovatebot.com/modules/platform/github/#running-as-a-github-app).

<!-- BEGIN WORKFLOW INPUT DOCS: renovate -->

### 🔧 Inputs

|Name                        |Description                                                                                                                                                                                                                                   |Required|Type   |Default                                         |
|----------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------|-------|------------------------------------------------|
|`runs-on`                   |The type of runner to use for the workflow. You can specify a different runner if needed.                                                                                                                                                     |No      |string |`ubuntu-latest`                                 |
|`renovate-config-repo`      |The repository where the Renovate configuration is stored.  This must be the repository name **without** the owner, e.g., `renovate-config`.                                                                                                  |No      |string |`${{ github.event.repository.name }}`           |
|`renovate-config-repo-ref`  |The branch or tag of the Renovate configuration repository to use.                                                                                                                                                                            |No      |string |`${{ github.event.repository.default_branch }}` |
|`renovate-config-file-path` |The full path to the Renovate configuration file, relative to the root.                                                                                                                                                                       |No      |string |`renovate-config/renovate.js`                   |
|`renovate-image`            |The Renovate Docker image name to use.  If omitted the action will use the `ghcr.io/renovatebot/renovate:<renovate-version>` Docker image name otherwise. If a Docker image name is defined, the action will use that name to pull the image. |No      |string |                                                |
|`renovate-version`          |The Renovate version to use. If omitted the action will use the default version Docker tag.  Check [the available tags on Docker Hub](https://hub.docker.com/r/renovate/renovate/tags).                                                       |No      |string |                                                |

### 🔐 Secrets

|Name                  |Description                                                                    |Required|
|----------------------|-------------------------------------------------------------------------------|--------|
|`GITHUB_APP_ID`       |The ID of the GitHub App used for Renovate. This should be stored as a secret. |Yes     |
|`GITHUB_APP_PEM_FILE` |The private key (in PEM format) of the GitHub App used for Renovate.           |Yes     |

### 📤 Outputs

_None_

<!-- END WORKFLOW INPUT DOCS -->
