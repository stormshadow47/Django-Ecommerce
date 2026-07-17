#!/bin/bash

# ArgoCD Installation Script for EKS

set -e

echo "Installing ArgoCD on EKS cluster..."

# Create ArgoCD namespace
kubectl create namespace argocd --dry-run=client -o yaml | kubectl apply -f -

# Install ArgoCD using kubectl create to avoid CRD annotation issues
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml --server-side=true

# Wait for ArgoCD to be ready
echo "Waiting for ArgoCD pods to be ready..."
kubectl wait --for=condition=ready pod -l app.kubernetes.io/name=argocd-server -n argocd --timeout=5m

# Get ArgoCD initial password
ARGOCD_PASSWORD=$(kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d)

echo "ArgoCD installed successfully!"
echo "Initial admin password: $ARGOCD_PASSWORD"
echo "Access ArgoCD UI: kubectl port-forward svc/argocd-server -n argocd 8090:443"
