#!/bin/bash

# Test script to verify the app builds correctly

echo "🧪 Testing Learn with Dheeru App..."
echo ""

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies first..."
    npm install
fi

# Build the app
echo "🔨 Building app..."
npm run build > /tmp/build.log 2>&1

if [ $? -eq 0 ]; then
    echo "✅ Build Successful!"
    echo ""
    echo "📊 Build Statistics:"
    echo "- Build directory size: $(du -sh build/ | cut -f1)"
    echo "- Main files created:"
    ls -1 build/ | head -10
    echo ""
    echo "✨ App is ready for deployment!"
    echo "Run: npm run deploy"
else
    echo "❌ Build failed! Error log:"
    cat /tmp/build.log
    exit 1
fi
