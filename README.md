# Learn with Dheeru

A React-based web application for mastering English vocabulary with pronunciation, meanings, Hindi translations, and examples. Perfect for students preparing for competitive exams and language proficiency tests.

## 🎯 Features

- 📚 **Vocabulary Management**: Add and store vocabulary words with detailed information
- 🎤 **Text-to-Speech**: Pronounce words in English and Hindi using the browser's speech synthesis API
- 📝 **Markdown Support**: Store vocabulary in Markdown format for easy management
- 💾 **Download**: Export your vocabulary as a Markdown file
- ➕ **Add Words**: Scrape/add new words to your vocabulary list
- 📱 **Responsive Design**: Works seamlessly on desktop, tablet, and mobile devices
- 🌐 **GitHub Pages Ready**: Pre-configured for deployment to GitHub Pages

## 📦 Installation

### 1. Clone the Repository
```bash
git clone https://github.com/manindragautam/english-grammar.git
cd english-grammar
```

### 2. Install Dependencies
```bash
npm install
```

Or use the setup script:
```bash
bash setup.sh
```

## 🚀 Development

### Start the Development Server
```bash
npm start
```
This will open the app at `http://localhost:3000` in your browser.

### Build for Production
```bash
npm run build
```
Creates an optimized production build in the `build/` directory.

## 📋 Project Structure

```
english-grammar/
├── public/
│   ├── index.html              # Main HTML file
│   └── markdown/
│       └── vocab.md            # Vocabulary data file
├── src/
│   ├── components/
│   │   ├── VocabList.js        # Display vocabulary
│   │   ├── ScraperButton.js    # Add new words
│   │   └── SpeakButton.js      # Text-to-speech functionality
│   ├── App.js                  # Main app component
│   ├── App.css                 # App styling
│   └── index.js                # React entry point
├── package.json                # Dependencies and scripts
└── setup.sh                    # Setup script
```

## 🛠️ Available Scripts

- `npm start` - Start development server
- `npm build` - Build for production
- `npm test` - Run tests
- `npm run deploy` - Deploy to GitHub Pages
- `npm run predeploy` - Build before deployment (runs automatically)

## 🌍 Deployment to GitHub Pages

### Step 1: Ensure Git Remote is Configured
```bash
git remote add origin https://github.com/manindragautam/english-grammar.git
```

### Step 2: Commit Your Code
```bash
git add .
git commit -m "Add vocabulary app implementation"
git push -u origin main
```

### Step 3: Deploy
```bash
npm run deploy
```

This will:
1. Build the React app
2. Push the build to the `gh-pages` branch
3. Make it available at: `https://manindragautam.github.io/english-grammar`

### Step 4: Enable GitHub Pages (One-time setup)
1. Go to your repository on GitHub
2. Navigate to **Settings** → **Pages**
3. Under "Build and deployment", select:
   - **Source**: Deploy from a branch
   - **Branch**: `gh-pages` and folder `/root`
4. Click **Save**

## 📱 Usage

### Adding Words
1. Click the **➕ Add New Word** button
2. The app will add a random word to your vocabulary
3. You can customize words by editing the `public/markdown/vocab.md` file

### Pronouncing Words
- Words are typically pronounced using the **🔉** button (if implemented in components)
- Supports both English (🇬🇧) and Hindi (🇮🇳) pronunciation

### Downloading Vocabulary
1. Click the **💾 Download Vocabulary** button
2. Your vocabulary list will be downloaded as `vocab.md`

### Editing Vocabulary
- Edit `public/markdown/vocab.md` directly
- Restart the app to see changes (in development mode)
- Or re-deploy for production changes

## 📝 Vocabulary Format

Vocabulary entries follow this Markdown format:

```markdown
## Word: YourWord
- **Dissection:** [phonetic-breakdown]
- **Meaning:** Clear definition
- **Hindi:** Hindi translation
- **Examples:**
  1. Example sentence 1.
  2. Example sentence 2.
```

## 🎨 Customization

### Styling
Edit `src/App.css` to customize the appearance. The app uses CSS variables for easy theming:
```css
--primary-color: #2c3e50;
--secondary-color: #3498db;
--accent-color: #e74c3c;
--success-color: #27ae60;
```

### Adding More Sample Words
Edit `src/components/ScraperButton.js` and add words to the `SAMPLE_WORDS` array.

## 🔧 Technologies Used

- **React 18**: UI library
- **React Markdown**: Render Markdown content
- **Gray Matter**: Parse Markdown front matter
- **Showdown**: Markdown to HTML converter
- **CSS3**: Styling and animations
- **Web Speech API**: Text-to-speech functionality
- **gh-pages**: GitHub Pages deployment

## 🌐 Browser Support

- Chrome/Edge 90+
- Firefox 88+
- Safari 14+
- Opera 76+

## 📄 License

This project is open source and available under the MIT License.

## 👤 Author

**Manindra Gautam**
- GitHub: [@manindragautam](https://github.com/manindragautam)

## 🤝 Contributing

Contributions are welcome! Feel free to open issues and pull requests.

## 📞 Support

For issues, questions, or suggestions, please open an GitHub issue on the repository.

---

**Happy Learning! 📚✨**
