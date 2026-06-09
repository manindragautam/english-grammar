import React from "react";
import SpeakButton from "./SpeakButton";

export default function VocabList({ entries = [] }) {
  return (
    <div className="vocab-list">
      <div className="vocab-content">
        <h1>Vocabulary</h1>
        {entries.map((e, idx) => (
          <section key={e.word + idx}>
            <div className="word-header">
              <h2>{idx + 1}. {e.word}</h2>
              <div className="speak-buttons">
                <SpeakButton word={e.word} lang="en-US" />
                <SpeakButton word={e.word} lang="hi-IN" />
              </div>
            </div>

            <ul>
              {e.dissection && (
                <li>
                  <strong>Dissection:</strong> {e.dissection}
                </li>
              )}
              {e.meaning && (
                <li>
                  <strong>Meaning:</strong> {e.meaning}
                </li>
              )}
              {e.hindi && (
                <li>
                  <strong>Hindi:</strong> {e.hindi}
                </li>
              )}
              {e.examples && e.examples.length > 0 && (
                <li>
                  <strong>Examples:</strong>
                  <ol>
                    {e.examples.map((ex, i) => (
                      <li key={i}>{ex}</li>
                    ))}
                  </ol>
                </li>
              )}
              {e.dateFetched && (
                <li>
                  <small>Fetched: {e.dateFetched}</small>
                </li>
              )}
            </ul>
          </section>
        ))}
      </div>
    </div>
  );
}
