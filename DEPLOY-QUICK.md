# 🚀 Learn with Dheeru - Quick Deploy Guide

## One-Command Deployment

Copy and paste this into your terminal:

```bash
cd /workspaces/english-grammar && npm install && npm run build && git add . && git commit -m "Deploy Learn with Dheeru" && git push origin main && npm run deploy
```

---

## Step-by-Step Deployment

If you prefer to deploy step by step:

### Step 1: Install Dependencies
```bash
cd /workspaces/english-grammar
npm install
```
**Expected**: Takes 1-2 minutes. Wait for "added X packages" message.

---

### Step 2: Build the App
```bash
npm run build
```
**Expected**: Creates a `build/` folder with optimized production files.

---

### Step 3: Verify Build (Optional)
```bash
ls -la build/
```
**Expected**: Should show `index.html`, `static/` folder, and other files.

---

### Step 4: Commit Changes to GitHub
```bash
git add .
git commit -m "Deploy Learn with Dheeru - Vocabulary app with speak functionality"
git push origin main
```
**Expected**: Changes pushed to GitHub main branch.

---

### Step 5: Deploy to GitHub Pages
```bash
npm run deploy
```
**Expected**: 
- Shows "Deploying..." messages
- Creates `gh-pages` branch automatically
- Displays success message

---

## ✅ Verify Deployment

After running deployment, visit:

🌐 **https://manindragautam.github.io/english-grammar**

### Test these features:
- [ ] Header displays "📚 Learn with Dheeru"
- [ ] Vocabulary words are visible (Serendipity, Ephemeral, etc.)
- [ ] Click 🇬🇧 button - should hear English pronunciation
- [ ] Click 🇮🇳 button - should hear Hindi pronunciation
- [ ] Click "➕ Add New Word" - adds a random word
- [ ] Click "💾 Download" - downloads vocab.md file
- [ ] App looks good on mobile (try DevTools)

---

## 🆘 Troubleshooting

### Issue: "npm command not found"
**Solution**: Install Node.js from https://nodejs.org

### Issue: Build fails with errors
**Solution**:
```bash
rm -rf node_modules package-lock.json
npm install
npm run build
```

### Issue: Can't push to GitHub
**Solution**: 
```bash
git config user.email "your-email@example.com"
git config user.name "Your Name"
git push origin main
```

### Issue: GitHub Pages not updating
**Solution**:
1. Go to: https://github.com/manindragautam/english-grammar/settings/pages
2. Verify branch is set to `gh-pages`
3. Clear browser cache (Ctrl+Shift+Del)
4. Wait 2-3 minutes for GitHub to rebuild

### Issue: Speak button not working
**Solution**: 
- Check if browser supports Web Speech API (Chrome, Firefox, Safari, Edge)
- Enable microphone permissions
- Try refreshing the page
- Test in a different browser

---

## 📊 What Gets Deployed

```
github-pages branch:
└── build/
    ├── index.html
    ├── static/css/
    ├── static/js/
    ├── favicon.ico
    └── manifest.json
```

The React app is compiled and bundled into static files, then hosted on GitHub Pages.

---

## ✨ Features Deployed

| Feature | Status | How to Use |
|---------|--------|-----------|
| 📚 Display Vocab | ✅ Live | Loads from markdown |
| 🔉 Speak English | ✅ Live | Click 🇬🇧 button |
| 🔉 Speak Hindi | ✅ Live | Click 🇮🇳 button |
| ➕ Add Words | ✅ Live | Click "Add New Word" button |
| 💾 Download | ✅ Live | Click "Download" button |
| 📱 Mobile | ✅ Live | Responsive design |
| 🌐 GitHub Pages | ✅ Live | Auto-deployed |

---

## 🔄 Updating the App After Deployment

If you want to add more words or make changes:

1. **Edit vocabulary**
   ```bash
   nano /workspaces/english-grammar/public/markdown/vocab.md
   ```

2. **Make any code changes** to `/src/` files

3. **Re-deploy**
   ```bash
   npm run deploy
   ```

That's it! Changes go live in seconds.

---

## 📞 Need Help?

1. Check the full [DEPLOYMENT.md](./DEPLOYMENT.md)
2. Check [README.md](./README.md) for project info
3. Verify all files exist:
   - `/src/App.js` ✓
   - `/src/components/SpeakButton.js` ✓
   - `/public/markdown/vocab.md` ✓
   - `/package.json` ✓

---

**Ready? Run this:**

```bash
cd /workspaces/english-grammar && npm run deploy
```

**That's all you need!** Your app will be live at:
🌐 https://manindragautam.github.io/english-grammar
