import React, { useState } from "react";

export function UploadForm({ onSubmit, loading }) {
  const [file, setFile] = useState(null);
  const [description, setDescription] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!file) return;
    onSubmit(file, description);
  };

  return (
    <form className="card upload-card" onSubmit={handleSubmit}>
      <h2>1. Add your plate</h2>

      <p className="section-subtitle">
        Upload a clear photo of a single plate. Mention portions like
        <strong> “1 cup dal, 1.5 cups rice, 1 chapati”</strong>.
      </p>

      <div className="plate-hero">
        <div className="plate">
          <div className="plate-inner">
            <span className="plate-chip plate-carb">🍚</span>
            <span className="plate-chip plate-protein">🥘</span>
            <span className="plate-chip plate-veggie">🥦</span>
          </div>
        </div>
      </div>

      <label className="file-input-label">
        <span className="file-label-text">
          {file ? file.name : "Choose a meal photo"}
        </span>
        <input
          type="file"
          accept="image/*"
          onChange={(e) => setFile(e.target.files?.[0] || null)}
        />
      </label>

      <textarea
        className="description-input"
        placeholder="Example: 2 paneer parathas with butter, ½ cup raita, small salad"
        value={description}
        onChange={(e) => setDescription(e.target.value)}
        rows={3}
      />

      <button
        type="submit"
        className="primary-btn"
        disabled={loading || !file}
      >
        {loading ? "Cooking up your estimate..." : "Estimate Calories"}
      </button>

      {!file && (
        <p className="small-hint">
          Tip: avoid multiple plates in one photo so the AI can focus on a
          single meal.
        </p>
      )}
    </form>
  );
}
