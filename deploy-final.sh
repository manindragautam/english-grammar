#!/bin/bash
# Deploy Learn with Dheeru to GitHub Pages
# Run this script from the project root directory

set -e

echo "🚀 Starting deployment of Learn with Dheeru..."
echo ""

# Step 1: Install dependencies
echo "📦 Step 1: Installing dependencies..."
npm install
echo "✅ Dependencies installed!"
echo ""

# Step 2: Build the React app
echo "🔨 Step 2: Building React app..."
npm run build
BUILD_STATUS=$?

if [ $BUILD_STATUS -ne 0 ]; then
    echo "❌ Build failed!"
    exit 1
fi
echo "✅ Build successful!"
echo ""

# Step 3: Verify build
echo "📊 Build artifacts created:"
du -sh build/ 2>/dev/null || echo "Build directory created"
echo ""

# Step 4: Configure git (if needed)
echo "📝 Step 3: Configuring git..."
git config user.email "github-actions[bot]@users.noreply.github.com" 2>/dev/null || true
git config user.name "Deploy Bot" 2>/dev/null || true
echo ""

# Step 5: Commit changes
echo "📝 Step 4: Committing changes to GitHub..."
git add .
git commit -m "Deploy Learn with Dheeru - React vocabulary app with speak functionality" || echo "ℹ️  No new changes to commit"
echo ""

# Step 6: Push to main
echo "📤 Step 5: Pushing to main branch..."
git push origin main
echo "✅ Changes pushed!"
echo ""

# Step 7: Deploy to GitHub Pages
echo "🌐 Step 6: Deploying to GitHub Pages..."
npm run deploy
DEPLOY_STATUS=$?

if [ $DEPLOY_STATUS -eq 0 ]; then
    echo ""
    echo "======================================"
    echo "✨ DEPLOYMENT SUCCESSFUL! ✨"
    echo "======================================"
    echo ""
    echo "🎉 Your app is now live at:"
    echo "📍 https://manindragautam.github.io/english-grammar"
    echo ""
    echo "📋 What to test:"
    echo "  ✓ App loads with 'Learn with Dheeru' header"
    echo "  ✓ Click 🇬🇧 to hear English pronunciation"
    echo "  ✓ Click 🇮🇳 to hear Hindi pronunciation"
    echo "  ✓ Click ➕ to add new words"
    echo "  ✓ Click 💾 to download vocabulary"
    echo ""
else
    echo "❌ Deployment failed!"
    exit 1
fi
