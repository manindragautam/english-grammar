import React, { useState } from "react";

const SAMPLE_WORDS = [
  {
    word: "Ephemeral",
    dissection: "[e-phe-mer-al]",
    meaning: "Lasting for a very short time.",
    hindi: "क्षणकालिक",
  },
  {
    word: "Eloquent",
    dissection: "[el-o-kwent]",
    meaning: "Fluent or persuasive in speaking or writing.",
    hindi: "वाक्पटु",
  },
  {
    word: "Meticulous",
    dissection: "[me-tic-u-lous]",
    meaning: "Showing great attention to detail; very careful and precise.",
    hindi: "बेहद सावधान",
  },
  {
    word: "Pragmatic",
    dissection: "[prag-mat-ic]",
    meaning: "Dealing with things in a sensible, realistic way based on actual circumstances rather than theory.",
    hindi: "व्यावहारिक",
  },
  {
    word: "Ubiquitous",
    dissection: "[u-biq-ui-tous]",
    meaning: "Present, appearing, or found everywhere.",
    hindi: "सर्वत्र विद्यमान",
  },
];

export default function ScraperButton({ setMarkdown, currentMarkdown }) {
  const [loading, setLoading] = useState(false);

  const handleScrape = async () => {
    setLoading(true);
    
    // Simulate API delay
    await new Promise((resolve) => setTimeout(resolve, 1000));

    // Get a random word from sample words
    const randomWord = SAMPLE_WORDS[Math.floor(Math.random() * SAMPLE_WORDS.length)];

    const scrapedData = `## Word: ${randomWord.word}
- **Dissection:** ${randomWord.dissection}
- **Meaning:** ${randomWord.meaning}
- **Hindi:** ${randomWord.hindi}
- **Examples:**
  1. Example sentence using ${randomWord.word.toLowerCase()}.
  2. Another example with ${randomWord.word.toLowerCase()}.

`;

    setMarkdown((prevMarkdown) => prevMarkdown + "\n" + scrapedData);
    setLoading(false);

    alert(`✅ Added "${randomWord.word}" to vocabulary!`);
  };

  return (
    <button onClick={handleScrape} disabled={loading} className="scrape-btn">
      {loading ? "⏳ Scraping..." : "➕ Add New Word"}
    </button>
  );
}
