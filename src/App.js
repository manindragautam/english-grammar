import React, { useState, useEffect } from "react";
import ReactMarkdown from "react-markdown";
import ScraperButton from "./components/ScraperButton";
import SpeakButton from "./components/SpeakButton";
import "./App.css";

export default function App() {
  const [markdown, setMarkdown] = useState("");

  useEffect(() => {
    // Fetch the vocab.md file from public folder
    fetch(process.env.PUBLIC_URL + "/markdown/vocab.md")
      .then((res) => res.text())
      .then((text) => setMarkdown(text))
      .catch((err) => {
        console.log("Loading default vocabulary...");
        setMarkdown(getDefaultVocab());
      });
  }, []);

  const getDefaultVocab = () => {
    return `# English Grammar Vocabulary

## Word: Serendipity
- **Dissection:** [se-ren-di-pi-ty]
- **Meaning:** The occurrence of events by chance in a happy or beneficial way.
- **Hindi:** संयोगवश
- **Examples:**
  1. Discovering that bookshop was pure serendipity.
  2. Meeting her again in Paris was a serendipity.

## Word: Ephemeral
- **Dissection:** [e-phe-mer-al]
- **Meaning:** Lasting for a very short time.
- **Hindi:** क्षणकालिक
- **Examples:**
  1. The ephemeral beauty of flowers is captivating.
  2. Life itself is ephemeral.
`;
  };

  const handleSaveMarkdown = () => {
    const blob = new Blob([markdown], { type: "text/markdown" });
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = "vocab.md";
    link.click();
  };

  return (
    <div className="app-container">
      <header className="app-header">
        <h1>📚 Learn with Dheeru</h1>
        <p>Master English vocabulary with pronunciation, meanings & examples</p>
      </header>

      <div className="button-group">
        <ScraperButton setMarkdown={setMarkdown} currentMarkdown={markdown} />
        <button onClick={handleSaveMarkdown} className="save-btn">
          💾 Download Vocabulary
        </button>
      </div>

      <main className="vocab-content">
        <ReactMarkdown
          components={{
            h2: ({ node, ...props }) => {
              // Extract word from heading
              const text = props.children[0];
              const match = text.match(/Word:\s*(.+)/);
              const word = match ? match[1] : text;

              return (
                <div className="word-header">
                  <h2 {...props} />
                  <div className="speak-buttons">
                    <SpeakButton word={word} lang="en-US" />
                    <SpeakButton word={word} lang="hi-IN" />
                  </div>
                </div>
              );
            },
          }}
        >
          {markdown}
        </ReactMarkdown>
      </main>
    </div>
  );
}
