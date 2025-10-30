<!-- NOTE: This file's contents are automatically generated. Do not edit manually. -->
# Commit SHA (Action)

Set the source commit SHA for a workflow as output variable. Regardless of whether the workflow is triggered by a push or a pull request, this action will provide the actual source commit SHA.

## 🔧 Inputs

|Name                      |Description                    |Required|Default|
|--------------------------|-------------------------------|--------|-------|
|`commit-short-sha-length` |Length of the short commit SHA |No      |`7`    |

## 📤 Outputs

|Name        |Description                           |
|------------|--------------------------------------|
|`sha`       |The commit SHA used as source commit  |
|`short-sha` |The short commit SHA as source commit |

## 🚀 Usage

```yaml
- name: Commit SHA
  uses: eidp/actions-common/commit-sha@v0
  with:
    # your inputs here
```
