#!/bin/bash
# Post-creation setup script for pfSensible HAProxy devcontainer
# This script runs after the container is created to set up the development environment

set -e

echo "========================================="
echo "pfSensible HAProxy DevContainer Setup"
echo "========================================="
echo ""

# Install system dependencies
echo "📦 Installing system dependencies..."
sudo apt-get update -qq && sudo apt-get install -y -qq shellcheck
echo "✓ System dependencies installed"
echo ""

# Install Python requirements
echo "📦 Installing Python requirements..."
pip install --quiet --upgrade pip
pip install --quiet -r .devcontainer/requirements.txt
echo "✓ Python packages installed"
echo ""

# Install Ansible collections
echo "📦 Installing Ansible collections..."
ansible-galaxy collection install community.internal_test_tools
# Install pfsensible.core into the workspace collection root so ansible-test can find it
ansible-galaxy collection install -p /workspaces/ansible_collections git+https://github.com/pfsensible/core.git
echo "✓ Ansible collections installed"
echo ""

# Verify we're in the correct directory structure
echo "📂 Verifying collection directory structure..."
if [[ "$(pwd)" == "/workspaces/ansible_collections/pfsensible/haproxy" ]]; then
    echo "✓ Workspace is correctly structured at: $(pwd)"
else
    echo "⚠️  Warning: Workspace path is $(pwd)"
    echo "   Expected: /workspaces/ansible_collections/pfsensible/haproxy"
fi
echo ""

# Display environment information
echo "========================================="
echo "✓ DevContainer setup complete!"
echo "========================================="
echo ""
echo "Environment information:"
echo "  Python version: $(python --version)"
echo "  Ansible version: $(ansible --version | head -n 1)"
echo "  Pytest version: $(pytest --version)"
echo ""
echo "Useful commands:"
echo "  • Run sanity tests:"
echo "    ansible-test sanity --requirements --python 3.10"
echo ""
echo "  • Run unit tests:"
echo "    ansible-test units --requirements --python 3.10"
echo ""
echo "  • Run pycodestyle linting:"
echo "    pycodestyle plugins/ tests/"
echo ""
echo "  • Test with different Ansible version:"
echo "    pip install ansible-core==2.15.*"
echo ""
echo "Happy coding!"
echo ""
