import React, { useState, useEffect } from "react";
import SpeakButton from "./SpeakButton";

export default function VocabList({ entries = [], viewMode = "list" }) {
  const [currentIdx, setCurrentIdx] = useState(0);
  const [isFlipped, setIsFlipped] = useState(false);

  // Reset flashcard state when the entries list changes (e.g., changing letters or search)
  useEffect(() => {
    setCurrentIdx(0);
    setIsFlipped(false);
  }, [entries]);

  if (entries.length === 0) {
    return (
      <div className="empty-state glass-panel">
        <span className="empty-state-icon">🔍</span>
        <h3>No Vocabulary Found</h3>
        <p>We couldn't find any words matching your search criteria. Try a different letter category or clear your search input.</p>
      </div>
    );
  }

  // --- FLASHCARD / STUDY VIEW ---
  if (viewMode === "flashcard") {
    const currentEntry = entries[currentIdx] || entries[0];

    if (!currentEntry) return null;

    return (
      <div className="flashcard-view-container">
        <div className="flashcard-wrapper">
          <div 
            className={`flashcard ${isFlipped ? "flipped" : ""}`} 
            onClick={() => setIsFlipped(!isFlipped)}
          >
            {/* Front Card Face */}
            <div className="flashcard-face flashcard-front">
              <span className="word-index-badge">Flashcard {currentIdx + 1} of {entries.length}</span>
              <h2 className="card-word">{currentEntry.word}</h2>
              {currentEntry.dissection && (
                <span className="syllable-dissection">{currentEntry.dissection}</span>
              )}
              <div className="flip-hint">
                <span>💡 Tap to Reveal Details</span>
              </div>
            </div>

            {/* Back Card Face */}
            <div 
              className="flashcard-face flashcard-back" 
              onClick={(e) => {
                // Prevent general flip back when clicking inside details,
                // but let them tap outer card parts to flip back.
                if (e.target.tagName !== "BUTTON" && !e.target.closest("button")) {
                  setIsFlipped(false);
                }
              }}
            >
              <div className="card-header">
                <div className="card-title-group">
                  <h2 className="card-word">{currentEntry.word}</h2>
                  {currentEntry.dissection && (
                    <span className="syllable-dissection">{currentEntry.dissection}</span>
                  )}
                </div>
                {/* Audio controls block: stop propagation so clicking buttons doesn't trigger flip */}
                <div className="audio-controls" onClick={(e) => e.stopPropagation()}>
                  <SpeakButton word={currentEntry.word} lang="en-US" />
                  <SpeakButton word={currentEntry.word} lang="hi-IN" />
                </div>
              </div>

              <div className="card-details">
                {currentEntry.meaning && (
                  <div className="detail-row">
                    <span className="detail-label">Meaning</span>
                    <p className="meaning-text">{currentEntry.meaning}</p>
                  </div>
                )}
                {currentEntry.hindi && (
                  <div className="detail-row">
                    <span className="detail-label">Hindi</span>
                    <p className="hindi-text">{currentEntry.hindi}</p>
                  </div>
                )}
                {currentEntry.examples && currentEntry.examples.length > 0 && (
                  <div className="detail-row">
                    <span className="detail-label">Examples</span>
                    <div className="examples-list">
                      {currentEntry.examples.slice(0, 2).map((ex, i) => (
                        <blockquote className="example-item" key={i}>{ex}</blockquote>
                      ))}
                    </div>
                  </div>
                )}
              </div>

              <div className="flip-hint" style={{ marginTop: "12px" }}>
                <span>💡 Tap Card to Hide Details</span>
              </div>
            </div>
          </div>
        </div>

        {/* Card Navigation Controls */}
        <div className="flashcard-navigation">
          <button
            className="nav-btn"
            disabled={currentIdx === 0}
            onClick={() => {
              setIsFlipped(false);
              setCurrentIdx((prev) => Math.max(0, prev - 1));
            }}
          >
            ◀ Previous
          </button>
          <span className="card-counter">
            {currentIdx + 1} / {entries.length}
          </span>
          <button
            className="nav-btn"
            disabled={currentIdx === entries.length - 1}
            onClick={() => {
              setIsFlipped(false);
              setCurrentIdx((prev) => Math.min(entries.length - 1, prev + 1));
            }}
          >
            Next ▶
          </button>
        </div>
      </div>
    );
  }

  // --- STANDARD LIST VIEW ---
  return (
    <div className="vocab-list">
      {entries.map((e, idx) => (
        <article className="vocab-card glass-panel" key={e.word + idx}>
          <div className="card-header">
            <div className="card-title-group">
              <span className="word-index-badge">Vocabulary Word #{idx + 1}</span>
              <h2 className="card-word">{e.word}</h2>
              {e.dissection && (
                <span className="syllable-dissection">{e.dissection}</span>
              )}
            </div>
            <div className="audio-controls">
              <SpeakButton word={e.word} lang="en-US" />
              <SpeakButton word={e.word} lang="hi-IN" />
            </div>
          </div>

          <div className="card-details">
            {e.meaning && (
              <div className="detail-row">
                <span className="detail-label">Meaning</span>
                <p className="meaning-text">{e.meaning}</p>
              </div>
            )}
            {e.hindi && (
              <div className="detail-row">
                <span className="detail-label">Hindi</span>
                <p className="hindi-text">{e.hindi}</p>
              </div>
            )}
            {e.examples && e.examples.length > 0 && (
              <div className="detail-row">
                <span className="detail-label">Examples</span>
                <div className="examples-list">
                  {e.examples.map((ex, i) => (
                    <blockquote className="example-item" key={i}>{ex}</blockquote>
                  ))}
                </div>
              </div>
            )}
          </div>
        </article>
      ))}
    </div>
  );
}
