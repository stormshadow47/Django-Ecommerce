#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

ENV_FILE="$PROJECT_ROOT/.env.secrets"
OUTPUT_FILE="$PROJECT_ROOT/k8s/django-secrets.sealed.yaml"

if [[ ! -f "$ENV_FILE" ]]; then
    echo ".env.secrets is missing; copy .env.secrets.example and fill it locally."
    exit 1
fi

mkdir -p "$PROJECT_ROOT/k8s"

kubectl create secret generic django-secrets \
  --namespace default \
  --from-env-file="$ENV_FILE" \
  --dry-run=client \
  --output yaml |
kubeseal \
  --controller-name sealed-secrets\
  --controller-namespace kube-system \
  --format yaml \
  > "$OUTPUT_FILE"

echo "Wrote $OUTPUT_FILE. Review and commit that file; never commit .env.secrets."