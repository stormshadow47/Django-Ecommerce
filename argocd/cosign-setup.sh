#!/bin/bash

# Cosign Image Signing Setup (Optional)
# This script sets up keyless image signing using GitHub OIDC

set -e

echo "Setting up Cosign for image signing..."

# Install Cosign
if ! command -v cosign &> /dev/null; then
    echo "Installing Cosign..."
    go install github.com/sigstore/cosign/v2/cmd/cosign@latest
fi

# Verify installation
cosign version

echo "Cosign installed successfully!"
echo ""
echo "To sign images with GitHub OIDC:"
echo "1. Ensure you have GitHub Actions OIDC enabled"
echo "2. Add this to your CI/CD pipeline:"
echo ""
echo "   cosign sign --yes \"\${DOCKER_IMAGE}:\${DOCKER_TAG}\""
echo ""
echo "To verify signed images:"
echo "   cosign verify \"\${DOCKER_IMAGE}:\${DOCKER_TAG}\""
echo ""
echo "For Kubernetes policy enforcement, add this to your deployment:"
echo "   annotations:"
echo "     cosign.sigstore.dev/image: \"\${DOCKER_IMAGE}:\${DOCKER_TAG}\""
