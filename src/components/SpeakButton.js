import React, { useState } from "react";

export default function SpeakButton({ word, lang = "en-US" }) {
  const [isSpeaking, setIsSpeaking] = useState(false);

  const handleSpeak = () => {
    // Cancel any ongoing speech
    speechSynthesis.cancel();

    const utterance = new SpeechSynthesisUtterance(word);
    utterance.lang = lang; // 'en-US' for English, 'hi-IN' for Hindi
    utterance.rate = 0.95;
    utterance.pitch = 1;

    utterance.onstart = () => setIsSpeaking(true);
    utterance.onend = () => setIsSpeaking(false);
    utterance.onerror = () => setIsSpeaking(false);

    speechSynthesis.speak(utterance);
  };

  const langDisplay = lang === "en-US" ? "English" : "Hindi";
  const flag = lang === "en-US" ? "🇬🇧" : "🇮🇳";
  const label = lang === "en-US" ? "EN" : "HI";

  return (
    <button
      onClick={handleSpeak}
      disabled={isSpeaking}
      className={`speak-btn ${isSpeaking ? "active-speaking" : ""}`}
      title={`Pronounce in ${langDisplay}`}
    >
      <span>{flag}</span>
      <span>{isSpeaking ? "Speaking..." : label}</span>
    </button>
  );
}
