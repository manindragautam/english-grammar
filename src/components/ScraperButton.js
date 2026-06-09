import React, { useState } from "react";

export default function ScraperButton({ onFetch, fetchedCount = 0, totalStored = 0, maxStored = 1000 }) {
  const [loading, setLoading] = useState(false);

  const handleFetch = async () => {
    if (!onFetch) return;
    setLoading(true);
    await onFetch();
    setLoading(false);
  };

  const isDailyLimitReached = fetchedCount >= 10;
  const isStorageFull = totalStored >= maxStored;

  return (
    <button
      onClick={handleFetch}
      disabled={loading || isDailyLimitReached || isStorageFull}
      className="scrape-btn"
      title={
        isStorageFull
          ? "Storage limit reached. Clear old fetched entries first."
          : isDailyLimitReached
          ? "Daily fetch limit reached. Try again tomorrow."
          : "Fetch 10 new vocab entries"
      }
    >
      {loading
        ? "⏳ Fetching 10 vocab..."
        : isStorageFull
        ? "Storage Full"
        : isDailyLimitReached
        ? "Daily Limit Reached"
        : "➕ Fetch 10 New Vocab"}
    </button>
  );
}
