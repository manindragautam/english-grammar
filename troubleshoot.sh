#!/bin/bash

# Troubleshooting script for Learn with Dheeru deployment

echo "🔍 Troubleshooting npm deploy issue..."
echo ""

# Check 1: Is npm installed?
echo "✓ Checking if npm is installed..."
if command -v npm &> /dev/null; then
    npm_version=$(npm --version)
    echo "  ✅ npm version: $npm_version"
else
    echo "  ❌ npm is NOT installed!"
    echo "  Install Node.js from https://nodejs.org/"
    exit 1
fi

# Check 2: Is node installed?
echo ""
echo "✓ Checking if node is installed..."
if command -v node &> /dev/null; then
    node_version=$(node --version)
    echo "  ✅ Node version: $node_version"
else
    echo "  ❌ Node is NOT installed!"
    echo "  Install Node.js from https://nodejs.org/"
    exit 1
fi

# Check 3: Do node_modules exist?
echo ""
echo "✓ Checking node_modules..."
if [ -d "node_modules" ]; then
    echo "  ✅ node_modules directory exists"
else
    echo "  ⚠️  node_modules missing - installing..."
    npm install
fi

# Check 4: Does build directory exist?
echo ""
echo "✓ Checking build directory..."
if [ -d "build" ]; then
    echo "  ✅ build directory exists"
else
    echo "  ⚠️  build directory missing - building..."
    npm run build
fi

# Check 5: Is gh-pages installed?
echo ""
echo "✓ Checking gh-pages package..."
if [ -d "node_modules/gh-pages" ]; then
    echo "  ✅ gh-pages is installed"
else
    echo "  ⚠️  gh-pages missing - installing..."
    npm install gh-pages --save-dev
fi

# Check 6: Can we run npm?
echo ""
echo "✓ Testing npm commands..."
npm --version > /dev/null 2>&1 && echo "  ✅ npm works"

echo ""
echo "======================================"
echo "✨ All checks passed!"
echo "======================================"
echo ""
echo "Now run:"
echo "npm run deploy"
echo ""
