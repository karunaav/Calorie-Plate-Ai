import React, { useState } from "react";
import { UploadForm } from "./components/UploadForm";
import { ResultCard } from "./components/ResultCard";

const API_BASE = "http://localhost:8000";

function App() {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  const handleSubmit = async (file, description) => {
    setLoading(true);
    setError("");
    setResult(null);
    try {
      const formData = new FormData();
      formData.append("file", file);
      if (description) {
        formData.append("description", description);
      }

      const res = await fetch(`${API_BASE}/api/calc-image`, {
        method: "POST",
        body: formData,
      });

      if (!res.ok) {
        const data = await res.json().catch(() => ({}));
        throw new Error(data.detail || "Request failed");
      }

      const data = await res.json();
      setResult(data);
    } catch (err) {
      setError(err.message || "Something went wrong");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-root">
      <div className="bg-orbit"></div>
      <div className="bg-orbit bg-orbit-secondary"></div>
      <main className="app-shell">
        <header className="app-header">
          <h1>Calorie Plate AI</h1>
          <p>
            Snap a photo of your meal and add a few details. A tiny vision module
            reads the plate, and Gemini estimates calories &amp; macros so you can
            keep your food diary feeling realistic, not restrictive.
          </p>

          <div className="pill-row">
            <span className="pill pill-green">🍛 Indian thali</span>
            <span className="pill pill-orange">🥗 Salad bowls</span>
            <span className="pill pill-yellow">🍔 Cheat meals</span>
          </div>
        </header>

        <section className="app-content">
          <UploadForm onSubmit={handleSubmit} loading={loading} />
          <div className="app-results">
            {error && <div className="error-banner">{error}</div>}
            {result && <ResultCard result={result} />}
            {!result && !error && !loading && (
              <p className="hint-text">
                Tip: clear, top-down photos with a short description (e.g.,{" "}
                &quot;1 cup dal, 1 cup rice, 1 chapati&quot;) give better estimates.
              </p>
            )}
          </div>
        </section>

        <footer className="app-footer">
          <p>
            Demo only – not medical advice. Calorie estimates are approximate and may
            be inaccurate.
          </p>
        </footer>
      </main>
    </div>
  );
}

export default App;

