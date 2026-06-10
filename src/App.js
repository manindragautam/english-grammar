import React, { useState, useEffect, useMemo, useRef } from "react";
import VocabList from "./components/VocabList";
import "./App.css";

const PAGE_SIZE = 20;
const LETTERS = ["All", ...Array.from({ length: 26 }, (_, i) => String.fromCharCode(65 + i))];

export default function App() {
  const [currentLetter, setCurrentLetter] = useState("All");
  const [letterEntries, setLetterEntries] = useState({});
  const [fetchedEntries, setFetchedEntries] = useState([]);
  const [visibleCount, setVisibleCount] = useState(PAGE_SIZE);
  const [loadingLetter, setLoadingLetter] = useState(false);
  const [theme, setTheme] = useState("light");
  const [searchQuery, setSearchQuery] = useState("");
  const [viewMode, setViewMode] = useState("list"); // "list" or "flashcard"
  const listRef = useRef(null);

  useEffect(() => {
    document.body.classList.toggle("dark", theme === "dark");
  }, [theme]);

  useEffect(() => {
    setFetchedEntries([]);
    
    const loadAllInitial = async () => {
      setLoadingLetter(true);
      try {
        const lettersList = Array.from({ length: 26 }, (_, i) => String.fromCharCode(65 + i));
        const results = await Promise.all(
          lettersList.map((L) =>
            fetch(`${process.env.PUBLIC_URL}/markdown/${L}.md`)
              .then((res) => (res.ok ? res.text() : ""))
              .catch(() => "")
          )
        );
        
        const allEntries = results
          .map((text) => parseMarkdownToEntries(text || ""))
          .reduce((acc, arr) => acc.concat(arr), [])
          .filter(Boolean);

        // Fisher-Yates shuffle
        for (let i = allEntries.length - 1; i > 0; i--) {
          const j = Math.floor(Math.random() * (i + 1));
          [allEntries[i], allEntries[j]] = [allEntries[j], allEntries[i]];
        }

        setLetterEntries((prev) => ({ ...prev, All: allEntries }));
      } catch (err) {
        setLetterEntries((prev) => ({ ...prev, All: [] }));
      } finally {
        setLoadingLetter(false);
      }
    };

    loadAllInitial();
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
        const lettersList = Array.from({ length: 26 }, (_, i) => String.fromCharCode(65 + i));
        const results = await Promise.all(
          lettersList.map((L) =>
            fetch(`${process.env.PUBLIC_URL}/markdown/${L}.md`)
              .then((res) => (res.ok ? res.text() : ""))
              .catch(() => "")
          )
        );
        
        const allEntries = results
          .map((text) => parseMarkdownToEntries(text || ""))
          .reduce((acc, arr) => acc.concat(arr), [])
          .filter(Boolean);

        // Fisher-Yates shuffle
        for (let i = allEntries.length - 1; i > 0; i--) {
          const j = Math.floor(Math.random() * (i + 1));
          [allEntries[i], allEntries[j]] = [allEntries[j], allEntries[i]];
        }

        setLetterEntries((prev) => ({ ...prev, [letter]: allEntries }));
        setCurrentLetter(letter);
        setVisibleCount(PAGE_SIZE);
        setSearchQuery(""); // Clear search on letter change
        scrollToTop();
      } else {
        const res = await fetch(`${process.env.PUBLIC_URL}/markdown/${letter}.md`);
        if (!res.ok) throw new Error("Letter file not found");
        const text = await res.text();
        const entries = parseMarkdownToEntries(text);
        setLetterEntries((prev) => ({ ...prev, [letter]: entries }));
        setCurrentLetter(letter);
        setVisibleCount(PAGE_SIZE);
        setSearchQuery(""); // Clear search on letter change
        scrollToTop();
      }
    } catch (err) {
      setLetterEntries((prev) => ({ ...prev, [letter]: [] }));
      setCurrentLetter(letter);
      setVisibleCount(PAGE_SIZE);
      setSearchQuery("");
      scrollToTop();
    } finally {
      setLoadingLetter(false);
    }
  };

  const currentLetterEntries = useMemo(
    () => letterEntries[currentLetter] || [],
    [letterEntries, currentLetter]
  );

  const fetchedForLetter = useMemo(() => {
    if (currentLetter === "All") return fetchedEntries;
    return fetchedEntries.filter((e) => e.word[0]?.toUpperCase() === currentLetter);
  }, [fetchedEntries, currentLetter]);

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

  // Apply search query filter
  const filteredEntries = useMemo(() => {
    if (!searchQuery.trim()) return combinedEntries;
    const query = searchQuery.toLowerCase().trim();
    return combinedEntries.filter(
      (e) =>
        e.word.toLowerCase().includes(query) ||
        (e.meaning && e.meaning.toLowerCase().includes(query)) ||
        (e.hindi && e.hindi.toLowerCase().includes(query))
    );
  }, [combinedEntries, searchQuery]);

  const visibleEntries = useMemo(
    () => filteredEntries.slice(0, visibleCount),
    [filteredEntries, visibleCount]
  );

  useEffect(() => {
    const node = listRef.current;
    if (!node) return;
    const handleScroll = () => {
      if (node.scrollTop + node.clientHeight >= node.scrollHeight - 80) {
        setVisibleCount((prev) => {
          if (prev >= filteredEntries.length) return prev;
          const next = prev + PAGE_SIZE;
          return next > filteredEntries.length ? filteredEntries.length : next;
        });
      }
    };
    node.addEventListener("scroll", handleScroll);
    return () => node.removeEventListener("scroll", handleScroll);
  }, [filteredEntries.length]);

  return (
    <div className={`app-container ${theme}`}>
      {/* Premium Header */}
      <header className="app-header glass-panel">
        <div className="app-title-group">
          <h1>📚 Learn with Dheeru</h1>
          <p>Master English vocabulary with pronunciation, meanings & examples</p>
        </div>
        
        <div className="header-actions">
          {/* Dynamic Text Search */}
          <div className="search-wrapper">
            <span className="search-icon">🔍</span>
            <input
              type="text"
              className="search-input"
              placeholder={`Search in "${currentLetter}" words...`}
              value={searchQuery}
              onChange={(e) => {
                setSearchQuery(e.target.value);
                setVisibleCount(PAGE_SIZE); // reset pagination when search changes
              }}
            />
          </div>

          {/* View Mode Switcher */}
          <div className="view-mode-toggle">
            <button
              className={`mode-btn ${viewMode === "list" ? "active" : ""}`}
              onClick={() => setViewMode("list")}
              title="List View"
            >
              📝 List
            </button>
            <button
              className={`mode-btn ${viewMode === "flashcard" ? "active" : ""}`}
              onClick={() => setViewMode("flashcard")}
              title="Flashcard Study Mode"
            >
              🎴 Study
            </button>
          </div>

          {/* Theme Switcher */}
          <button
            className="theme-toggle"
            onClick={() => setTheme((prev) => (prev === "light" ? "dark" : "light"))}
            aria-label="Toggle theme"
          >
            {theme === "light" ? "🌙 Dark" : "☀️ Light"}
          </button>
        </div>
      </header>

      {/* Main Grid Body */}
      <main className="app-body">
        {/* Sticky A-Z Letter Sidebar */}
        <aside className="letter-sidebar glass-panel">
          <h2 className="sidebar-title">Categories</h2>
          <div className="letter-grid">
            {LETTERS.map((letter) => (
              <button
                key={letter}
                className={`letter-btn ${letter === "All" ? "all-btn" : ""} ${currentLetter === letter ? "active" : ""}`}
                onClick={() => loadLetter(letter)}
                disabled={loadingLetter && currentLetter !== letter}
              >
                {letter}
              </button>
            ))}
          </div>
        </aside>

        {/* Content Area */}
        <section className="vocab-section">
          {/* Metadata Statistics Strip */}
          <div className="section-meta-bar glass-panel">
            <div className="meta-info">
              <span className="meta-badge">{currentLetter}</span>
              <span className="meta-stats">
                Showing {filteredEntries.length} of {combinedEntries.length} words
                {searchQuery.trim() && " (Filtered)"}
              </span>
            </div>
          </div>

          {/* Main List/Card Area */}
          <div className="vocab-wrapper" ref={listRef}>
            <VocabList 
              entries={viewMode === "list" ? visibleEntries : filteredEntries} 
              viewMode={viewMode}
            />
          </div>

          {/* Pagination Scroll Hint */}
          {viewMode === "list" && visibleCount < filteredEntries.length && (
            <div className="scroll-hint glass-panel">
              Scroll down to discover more vocabulary...
            </div>
          )}
        </section>
      </main>
    </div>
  );
}

// Helper to parse markdown contents into JSON objects
function parseMarkdownToEntries(md) {
  const sections = md.split(/^##\s+/m).map((s) => s.trim()).filter(Boolean);
  const entries = sections.map((sec) => {
    const lines = sec.split("\n").map((l) => l.trim());
    const header = lines[0] || "";
    const word = header.replace(/^[0-9]+:\s*/g, "").replace(/^Word:\s*/i, "").trim();
    const obj = { word, dissection: "", meaning: "", hindi: "", examples: [] };
    for (const line of lines.slice(1)) {
      if (line.startsWith("- **Dissection:**")) {
        obj.dissection = line.replace("- **Dissection:**", "").trim();
      } else if (line.startsWith("- **Meaning:**")) {
        obj.meaning = line.replace("- **Meaning:**", "").trim();
      } else if (line.startsWith("- **Hindi:**")) {
        obj.hindi = line.replace("- **Hindi:**", "").trim();
      } else if (/^\d+\./.test(line)) {
        obj.examples.push(line.replace(/^\d+\.\s*/, "").trim());
      }
    }
    return obj;
  });
  return entries;
}
