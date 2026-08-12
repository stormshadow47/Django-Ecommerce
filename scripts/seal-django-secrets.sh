#!/usr/bin/env bash
set -euo pipefail

# Requires kubectl access to the target cluster, kubeseal, and .env.secrets.
# The result is safe to commit because it can only be decrypted by this cluster's controller.
if [[ ! -f .env.secrets ]]; then
  echo ".env.secrets is missing; copy env.secrets.example and fill it locally." >&2
  exit 1
fi

kubectl create secret generic django-secrets \
  --namespace default \
  --from-env-file=.env.secrets \
  --dry-run=client \
  --output yaml \
  | kubeseal \
      --controller-name sealed-secrets-controller \
      --controller-namespace kube-system \
      --format yaml \
  > k8s/django-secrets.sealed.yaml

echo "Wrote k8s/django-secrets.sealed.yaml. Review and commit that file; never commit .env.secrets."
