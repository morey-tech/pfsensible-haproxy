#!/bin/bash
# Post-creation setup script for pfSensible HAProxy devcontainer
# This script runs after the container is created to set up the development environment

set -e

echo "========================================="
echo "pfSensible HAProxy DevContainer Setup"
echo "========================================="
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
ansible-galaxy collection install git+https://github.com/pfsensible/core.git
echo "✓ Ansible collections installed"
echo ""

# Set up collection directory structure for testing
# This matches the structure expected by ansible-test
echo "🔗 Setting up collection directory structure..."
mkdir -p ~/.ansible/collections/ansible_collections/pfsensible
ln -sf "$(pwd)" ~/.ansible/collections/ansible_collections/pfsensible/haproxy
echo "✓ Collection symlink created at ~/.ansible/collections/ansible_collections/pfsensible/haproxy"
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
echo "    cd ~/.ansible/collections/ansible_collections/pfsensible/haproxy"
echo "    ansible-test sanity --requirements --python 3.10"
echo ""
echo "  • Run unit tests:"
echo "    cd ~/.ansible/collections/ansible_collections/pfsensible/haproxy"
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
