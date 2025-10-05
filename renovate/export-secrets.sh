#!/bin/bash
set -euo pipefail

# Script to export RENOVATE_* secrets to GITHUB_ENV
# Usage: export-secrets.sh
# Note: Expects SECRETS_JSON environment variable to be set

echo "🔧 Exporting RENOVATE_* secrets to GITHUB_ENV..."
echo ""

# Validate that SECRETS_JSON is set
if [ -z "${SECRETS_JSON:-}" ]; then
  echo "❌ Error: SECRETS_JSON environment variable is not set"
  exit 1
fi

# Clean and validate the JSON using jq
echo "🔍 Validating JSON..."
CLEANED_JSON=$(echo "$SECRETS_JSON" | jq -c . 2>&1) || {
  echo "❌ Error: Invalid JSON in SECRETS_JSON"
  exit 1
}

echo "✅ JSON validated"

# Track count of exported secrets
EXPORTED_COUNT=0

# Export each RENOVATE_* secret to GITHUB_ENV
while IFS='=' read -r key value; do
  if [ -n "$key" ] && [ -n "$value" ]; then
    echo "$key=$value" >> "$GITHUB_ENV"
    EXPORTED_COUNT=$((EXPORTED_COUNT + 1))
  fi
done < <(echo "$CLEANED_JSON" | jq -r 'to_entries[] | select(.key | startswith("RENOVATE_")) | "\(.key)=\(.value)"')

echo ""
echo "✅ Exported $EXPORTED_COUNT RENOVATE_* secrets to GITHUB_ENV"
echo ""
