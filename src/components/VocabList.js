import React from "react";

export default function VocabList({ markdown }) {
  return (
    <div className="vocab-list">
      <div className="vocab-content">
        {markdown}
      </div>
    </div>
  );
}
