#!/bin/bash

# Complete Build, Test, and Deploy Script for Learn with Dheeru
# This script will install dependencies, test the app, commit, and deploy to GitHub Pages

set -e

echo "======================================"
echo "🚀 Learn with Dheeru - Build & Deploy"
echo "======================================"
echo ""

# Step 1: Install Dependencies
echo "📦 Step 1: Installing dependencies..."
npm install
echo "✅ Dependencies installed!"
echo ""

# Step 2: Build the project
echo "🔨 Step 2: Building the React app..."
npm run build
echo "✅ Build successful!"
echo ""

# Step 3: Display build info
echo "📊 Build output:"
ls -lh build/ | tail -10
echo ""

# Step 4: Git operations
echo "📝 Step 3: Committing changes to GitHub..."
git config user.email "github-actions[bot]@users.noreply.github.com" || true
git config user.name "GitHub Actions" || true
git add .
git commit -m "Add Learn with Dheeru vocabulary app with speak functionality" || echo "No changes to commit"
git push -u origin main
echo "✅ Changes pushed to GitHub!"
echo ""

# Step 5: Deploy to GitHub Pages
echo "🌐 Step 4: Deploying to GitHub Pages..."
npm run deploy
echo "✅ Deployment successful!"
echo ""

echo "======================================"
echo "🎉 Deployment Complete!"
echo "======================================"
echo ""
echo "📱 Your app is now live at:"
echo "https://manindragautam.github.io/english-grammar"
echo ""
echo "📋 Next steps:"
echo "1. Visit the URL above to see your app"
echo "2. Test the 'Add New Word' button"
echo "3. Test the speak buttons (🔉 English & 🇮🇳 Hindi)"
echo "4. Test the 'Download Vocabulary' button"
echo ""
