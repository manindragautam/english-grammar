import React, { useState, useEffect, useMemo, useRef } from "react";
import VocabList from "./components/VocabList";
import "./App.css";

const PAGE_SIZE = 20;
const MAX_FETCHED_ENTRIES = 1000;
const LETTERS = ["All", ...Array.from({ length: 26 }, (_, i) => String.fromCharCode(65 + i))];

function todayString() {
  return new Date().toISOString().slice(0, 10);
}

export default function App() {
  const [currentLetter, setCurrentLetter] = useState("All");
  const [letterEntries, setLetterEntries] = useState({});
  const [letterMarkdown, setLetterMarkdown] = useState({});
  const [fetchedEntries, setFetchedEntries] = useState([]);
  const [visibleCount, setVisibleCount] = useState(PAGE_SIZE);
  const [loadingLetter, setLoadingLetter] = useState(false);
  const [theme, setTheme] = useState("light");
  const listRef = useRef(null);

  useEffect(() => {
    document.body.classList.toggle("dark", theme === "dark");
  }, [theme]);

  useEffect(() => {
    // do not read or persist fetched entries in localStorage for now
    setFetchedEntries([]);
    loadLetter("All");
  }, []);

  const loadLetter = async (letter) => {
    if (letter === currentLetter && letterEntries[letter]) return;
    setLoadingLetter(true);

    const scrollToTop = () => {
      setTimeout(() => {
        const node = listRef.current;
        if (node) node.scrollTop = 0;
      }, 0);
    };

    try {
      if (letter === "All") {
        // fetch all letter files in parallel
        const letters = Array.from({ length: 26 }, (_, i) => String.fromCharCode(65 + i));
        const results = await Promise.all(
          letters.map((L) =>
            fetch(`${process.env.PUBLIC_URL}/markdown/${L}.md`).then((res) => (res.ok ? res.text() : "")).catch(() => "")
          )
        );
        const allEntries = results
          .map((text) => parseMarkdownToEntries(text || ""))
          .reduce((acc, arr) => acc.concat(arr), [])
          .filter(Boolean);
        // randomize order
        for (let i = allEntries.length - 1; i > 0; i--) {
          const j = Math.floor(Math.random() * (i + 1));
          [allEntries[i], allEntries[j]] = [allEntries[j], allEntries[i]];
        }
        setLetterEntries((prev) => ({ ...prev, [letter]: allEntries }));
        setLetterMarkdown((prev) => ({ ...prev, [letter]: results.join("\n\n") }));
        setCurrentLetter(letter);
        setVisibleCount(PAGE_SIZE);
        scrollToTop();
      } else {
        const res = await fetch(`${process.env.PUBLIC_URL}/markdown/${letter}.md`);
        if (!res.ok) throw new Error("Letter file not found");
        const text = await res.text();
        const entries = parseMarkdownToEntries(text);
        setLetterEntries((prev) => ({ ...prev, [letter]: entries }));
        setLetterMarkdown((prev) => ({ ...prev, [letter]: text }));
        setCurrentLetter(letter);
        setVisibleCount(PAGE_SIZE);
        scrollToTop();
      }
    } catch (err) {
      setLetterEntries((prev) => ({ ...prev, [letter]: [] }));
      setLetterMarkdown((prev) => ({ ...prev, [letter]: "" }));
      setCurrentLetter(letter);
      setVisibleCount(PAGE_SIZE);
      scrollToTop();
    } finally {
      setLoadingLetter(false);
    }
  };

  const currentLetterEntries = letterEntries[currentLetter] || [];
  const currentMarkdown = letterMarkdown[currentLetter] || "";

  const fetchedForLetter = useMemo(
    () => fetchedEntries.filter((e) => e.word[0]?.toUpperCase() === currentLetter),
    [fetchedEntries, currentLetter]
  );

  const combinedEntries = useMemo(() => {
    const seen = new Set();
    const combined = [];
    for (const entry of [...fetchedForLetter, ...currentLetterEntries]) {
      if (!seen.has(entry.word)) {
        seen.add(entry.word);
        combined.push(entry);
      }
    }
    return combined;
  }, [currentLetterEntries, fetchedForLetter]);

  const visibleEntries = useMemo(
    () => combinedEntries.slice(0, visibleCount),
    [combinedEntries, visibleCount]
  );

  useEffect(() => {
    const node = listRef.current;
    if (!node) return;
    const handleScroll = () => {
      if (node.scrollTop + node.clientHeight >= node.scrollHeight - 80) {
        // only increase if there are more entries to show
        setVisibleCount((prev) => {
          if (prev >= combinedEntries.length) return prev;
          const next = prev + PAGE_SIZE;
          return next > combinedEntries.length ? combinedEntries.length : next;
        });
      }
    };
    node.addEventListener("scroll", handleScroll);
    return () => node.removeEventListener("scroll", handleScroll);
  }, [combinedEntries.length]);

  // legacy fetch/clear handlers removed — entries come from markdown

  return (
    <div className={`app-container ${theme}`}>
      <header className="app-header">
        <div className="app-title-group">
          <div>
            <h1>📚 Learn with Dheeru</h1>
            <p>Master English vocabulary with pronunciation, meanings & examples</p>
          </div>
          <button
            className="theme-toggle"
            onClick={() => setTheme((prev) => (prev === "light" ? "dark" : "light"))}
            aria-label="Toggle theme"
          >
            {theme === "light" ? "🌙 Dark mode" : "☀️ Light mode"}
          </button>
        </div>
      </header>

      <div className="app-body">
        <div className="letter-strip">
          {LETTERS.map((letter) => (
            <button
              key={letter}
              className={`letter-btn ${currentLetter === letter ? "active" : ""}`}
              onClick={() => loadLetter(letter)}
              disabled={loadingLetter && currentLetter !== letter}
            >
              {letter}
            </button>
          ))}
        </div>

        <div className="vocab-wrapper" ref={listRef}>
          <VocabList entries={visibleEntries} />
        </div>

      {visibleCount < combinedEntries.length && (
        <div className="scroll-hint">Scroll to load more vocab...</div>
      )}
    </div>
  </div>
  );
}

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
  {
    word: "Loquacious",
    dissection: "[lo-qua-cious]",
    meaning: "Tending to talk a great deal; talkative.",
    hindi: "बोलीवाला",
  },
  {
    word: "Obscure",
    dissection: "[ob-scure]",
    meaning: "Not discovered or known about; uncertain.",
    hindi: "अस्पष्ट",
  },
  {
    word: "Resilient",
    dissection: "[re-sil-ient]",
    meaning: "Able to withstand or recover quickly from difficult conditions.",
    hindi: "लचीला",
  },
  {
    word: "Candid",
    dissection: "[can-did]",
    meaning: "Truthful and straightforward; frank.",
    hindi: "ईमानदार",
  },
  {
    word: "Apathetic",
    dissection: "[a-pa-thet-ic]",
    meaning: "Showing or feeling no interest, enthusiasm, or concern.",
    hindi: "उदासीन",
  },
];

// parse markdown text into entry objects
function parseMarkdownToEntries(md) {
  const sections = md.split(/^##\s+/m).map((s) => s.trim()).filter(Boolean);
  const entries = sections.map((sec) => {
    const lines = sec.split("\n").map((l) => l.trim());
    const header = lines[0] || "";
    const word = header.replace(/^[0-9]+:\s*/g, "").replace(/^Word:\s*/i, "").trim();
    const obj = { word, dissection: "", meaning: "", hindi: "", examples: [] };
    for (const line of lines.slice(1)) {
      if (line.startsWith("- **Dissection:**")) obj.dissection = line.replace("- **Dissection:**", "").trim();
      else if (line.startsWith("- **Meaning:**")) obj.meaning = line.replace("- **Meaning:**", "").trim();
      else if (line.startsWith("- **Hindi:**")) obj.hindi = line.replace("- **Hindi:**", "").trim();
      else if (/^\d+\./.test(line)) obj.examples.push(line.replace(/^\d+\.\s*/, "").trim());
    }
    return obj;
  });
  return entries;
}
