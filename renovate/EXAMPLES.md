## 📚 Examples

### Basic Usage with All Secrets

The simplest way to use this action is to pass all your secrets using `toJSON(secrets)`:

```yaml
- name: Run Renovate
  uses: eidp/actions-common/renovate@v1
  with:
    github-app-id: ${{ secrets.RENOVATE_APP_ID }}
    github-app-pem: ${{ secrets.RENOVATE_APP_PEM }}
    all-secrets: ${{ toJSON(secrets) }}
```

### Manual Secrets Configuration

You can also manually specify which secrets to pass. Only secrets with keys starting with `RENOVATE_` will be used:

```yaml
- name: Run Renovate
  uses: eidp/actions-common/renovate@v1
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
  uses: eidp/actions-common/renovate@v1
  with:
    github-app-id: ${{ secrets.RENOVATE_APP_ID }}
    github-app-pem: ${{ secrets.RENOVATE_APP_PEM }}
    all-secrets: ${{ toJSON(secrets) }}
    renovate-config-file-path: 'config/renovate.json'
    renovate-version: '41'
    log-level: 'info'
    repository: 'my-org/my-repo'
```
