# 📋 Step-by-Step Deployment Guide - Option 2

## Run These Commands in Order

Copy and paste each command one at a time into your terminal.

---

## Step 1️⃣: Navigate to Project
```bash
cd /workspaces/english-grammar
```
**What it does**: Changes to the project directory  
**Expected output**: Command prompt changes to show you're in the right folder

---

## Step 2️⃣: Install Dependencies
```bash
npm install
```
**What it does**: Downloads all packages needed (React, gh-pages, etc.)  
**Expected output**: 
- Shows downloading packages
- Takes 1-2 minutes
- Ends with "added X packages" or "up to date"

---

## Step 3️⃣: Stage All Changes
```bash
git add .
```
**What it does**: Marks all files to be committed  
**Expected output**: No output (that's normal)

---

## Step 4️⃣: Commit Changes Locally
```bash
git commit -m "Deploy Learn with Dheeru with speak functionality"
```
**What it does**: Creates a checkpoint with a message  
**Expected output**: Shows which files changed (something like):
```
[main abc123] Deploy Learn with Dheeru with speak functionality
 X files changed, Y insertions(+)
```

---

## Step 5️⃣: Push to GitHub
```bash
git push origin main
```
**What it does**: Uploads your code to GitHub  
**Expected output**: Shows upload progress, ends with:
```
✓ Your commits have been pushed to GitHub
```

---

## Step 6️⃣: Deploy to GitHub Pages ⭐
```bash
npm run deploy
```
**What it does**: **THIS IS THE DEPLOYMENT** - Builds the app and pushes to GitHub Pages  
**Expected output**:
```
> npm run deploy

...building...
Published to gh-pages branch
Success! Your app is now live at:
https://manindragautam.github.io/english-grammar
```

---

## ✅ After All Steps Complete

Your app will be live at:
🌐 **https://manindragautam.github.io/english-grammar**

---

## 🧪 Test Your Deployment

Visit the URL and check:
- [ ] Page loads with "📚 Learn with Dheeru" header
- [ ] Click 🇬🇧 button → Should hear English pronunciation
- [ ] Click 🇮🇳 button → Should hear Hindi pronunciation
- [ ] Click ➕ button → Should add a new word
- [ ] Click 💾 button → Should download vocab.md file
- [ ] Try on mobile → Should be responsive

---

## ⏱️ Time Breakdown

| Step | Command | Time |
|------|---------|------|
| 1 | `cd` | <1 sec |
| 2 | `npm install` | 1-2 min |
| 3 | `git add .` | <1 sec |
| 4 | `git commit` | <1 sec |
| 5 | `git push` | 10-30 sec |
| 6 | `npm run deploy` | 30-60 sec |
| **TOTAL** | - | **~3-5 minutes** |

---

## 🆘 If You Get Errors

### Error: "npm: command not found"
- Install Node.js from https://nodejs.org/
- Restart terminal
- Try again

### Error: "git: command not found"
- Install Git from https://git-scm.com/
- Restart terminal
- Try again

### Error: "nothing to commit" at Step 4
- Files might already be committed
- That's okay! Skip to Step 5

### Error at `git push` - "Permission denied"
- Make sure you have GitHub CLI or SSH keys configured
- Or use HTTPS with Personal Access Token
- Run: `git config --global user.email "your-email@example.com"`

### Error at `npm run deploy` - "Build failed"
```bash
rm -rf node_modules package-lock.json
npm install
npm run deploy
```

---

## ✨ What Gets Deployed

Your entire React app is:
1. ✅ Built into optimized files
2. ✅ Pushed to `gh-pages` branch
3. ✅ Hosted on GitHub Pages servers
4. ✅ Available globally at the URL

---

## 📱 Live App Features

Once deployed, your app has:
- 🎤 Text-to-Speech (English & Hindi)
- ➕ Add random words
- 💾 Download vocabulary
- 📱 Mobile responsive
- ⚡ Fast loading
- 🌐 Always online

---

## 🔄 After Deployment - Updating Content

To add more words later:

1. Edit vocabulary file:
   ```bash
   nano /workspaces/english-grammar/public/markdown/vocab.md
   ```

2. Add new words following the format:
   ```markdown
   ## Word: NewWord
   - **Dissection:** [pho-net-ic]
   - **Meaning:** Definition
   - **Hindi:** हिंदी
   - **Examples:**
     1. Example 1
     2. Example 2
   ```

3. Redeploy:
   ```bash
   npm run deploy
   ```

Changes go live in ~30 seconds!

---

## 🎯 Ready?

Copy this and paste into terminal:

```bash
cd /workspaces/english-grammar && npm install && git add . && git commit -m "Deploy Learn with Dheeru" && git push origin main && npm run deploy
```

Or run the 6 steps one by one as shown above.

---

**You're all set! 🚀**

After deployment, visit:
🌐 https://manindragautam.github.io/english-grammar
