import React, { useState } from "react";

export default function SpeakButton({ word, lang = "en-US" }) {
  const [isSpeaking, setIsSpeaking] = useState(false);

  const handleSpeak = () => {
    // Cancel any ongoing speech
    speechSynthesis.cancel();

    const utterance = new SpeechSynthesisUtterance(word);
    utterance.lang = lang; // 'en-US' for English, 'hi-IN' for Hindi
    utterance.rate = 0.9;
    utterance.pitch = 1;

    utterance.onstart = () => setIsSpeaking(true);
    utterance.onend = () => setIsSpeaking(false);
    utterance.onerror = () => setIsSpeaking(false);

    speechSynthesis.speak(utterance);
  };

  const langDisplay = lang === "en-US" ? "English" : "Hindi";
  const emoji = lang === "en-US" ? "🇬🇧" : "🇮🇳";

  return (
    <button
      onClick={handleSpeak}
      disabled={isSpeaking}
      className="speak-btn"
      title={`Pronounce in ${langDisplay}`}
    >
      {isSpeaking ? "🔊 Playing..." : `🔉 ${emoji}`}
    </button>
  );
}
