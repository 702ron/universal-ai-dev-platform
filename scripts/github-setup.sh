#!/bin/bash
# GitHub Repository Setup Script
# Run this after creating the repository on GitHub

set -e

# Configuration
GITHUB_USERNAME="702ron"
REPO_NAME="universal-ai-dev-platform"
REPO_URL="https://github.com/${GITHUB_USERNAME}/${REPO_NAME}.git"

echo "🚀 Setting up Universal AI Development Platform on GitHub"
echo "=================================================="

# Check if we're in the right directory
if [ ! -f "pyproject.toml" ] || [ ! -d "src/universal_ai_dev_platform" ]; then
    echo "❌ Error: Please run this script from the universal-ai-dev-platform root directory"
    exit 1
fi

# Check git status
echo "📊 Checking git status..."
git status

# Add remote if it doesn't exist
if ! git remote get-url origin >/dev/null 2>&1; then
    echo "🔗 Adding GitHub remote..."
    git remote add origin "$REPO_URL"
else
    echo "✅ GitHub remote already exists"
fi

# Push to GitHub
echo "📤 Pushing to GitHub..."
git push -u origin main

# Create and push tags
echo "🏷️ Creating release tag..."
git tag -a v0.1.0 -m "Universal AI Development Platform Phase 1 Release - Complete adaptive AI development platform with CLI, project analysis, agent orchestration, and industry adaptation capabilities"
git push origin v0.1.0

echo ""
echo "✅ Repository successfully set up on GitHub!"
echo "🌐 Repository URL: https://github.com/${GITHUB_USERNAME}/${REPO_NAME}"
echo "📋 Next steps:"
echo "   1. Visit the repository on GitHub"
echo "   2. Add repository description and topics"
echo "   3. Enable Issues and Discussions"
echo "   4. Set up branch protection rules"
echo "   5. Create a release from the v0.1.0 tag"
echo ""
echo "🧪 Test the installation:"
echo "   git clone ${REPO_URL}"
echo "   cd ${REPO_NAME}"
echo "   pip install -e ."
echo "   uai --help"