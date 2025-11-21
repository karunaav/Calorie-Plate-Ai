import React from "react";

export function ResultCard({ result }) {
  const {
    image_features,
    total_calories,
    macros,
    reasoning,
    suggestions,
    model_name,
  } = result;

  return (
    <div className="card result-card">
      <h2>2. Meal breakdown</h2>
      <p className="model-chip">AI estimate · {model_name}</p>

      <div className="result-grid">
        <div className="result-main">
          <p className="calories-text">
            {total_calories
              ? `${Math.round(total_calories)} kcal (approx.)`
              : "Calories: not available (model returned free-form text)."}
          </p>

          <p className="calories-caption">
            For accuracy, treat this as a ballpark estimate – real portions and
            recipes can vary.
          </p>

          {macros && (
            <ul className="macro-list">
              <li className="macro macro-protein">
                <div className="macro-label">
                  <span>Protein</span>
                  <span className="macro-tag">muscle</span>
                </div>
                <div className="macro-value">
                  {macros.protein_g != null
                    ? `${Math.round(macros.protein_g)} g`
                    : "n/a"}
                </div>
              </li>
              <li className="macro macro-carbs">
                <div className="macro-label">
                  <span>Carbs</span>
                  <span className="macro-tag">energy</span>
                </div>
                <div className="macro-value">
                  {macros.carbs_g != null
                    ? `${Math.round(macros.carbs_g)} g`
                    : "n/a"}
                </div>
              </li>
              <li className="macro macro-fats">
                <div className="macro-label">
                  <span>Fats</span>
                  <span className="macro-tag">satiety</span>
                </div>
                <div className="macro-value">
                  {macros.fats_g != null
                    ? `${Math.round(macros.fats_g)} g`
                    : "n/a"}
                </div>
              </li>
            </ul>
          )}
        </div>

        <div className="result-side">
          <h3>How the plate looks</h3>
          <ul className="feature-list">
            <li>
              Photo size: {image_features.width} × {image_features.height}px
            </li>
            <li>Brightness: {image_features.brightness.toFixed(3)}</li>
            <li>AI hint: {image_features.dish_hint}</li>
          </ul>

          <div className="meal-tags">
            <span className="tag-chip">🍽️ Portion sizing</span>
            <span className="tag-chip">🌶️ Dish type guess</span>
          </div>
        </div>
      </div>

      {reasoning && (
        <div className="section">
          <h3>Why this estimate?</h3>
          <p>{reasoning}</p>
        </div>
      )}

      {suggestions && (
        <div className="section">
          <h3>Gentle tweaks</h3>
          {Array.isArray(suggestions) ? (
            <ul className="suggestion-list">
              {suggestions.map((s, idx) => (
                <li key={idx}>{s}</li>
              ))}
            </ul>
          ) : (
            <p>{suggestions}</p>
          )}
        </div>
      )}
    </div>
  );
}
