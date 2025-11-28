import React, { useEffect, useMemo, useState } from "react";
import { generateLook, fetchHistory } from "./api";

const samplePrompt = "tenue pour un mariage en été, budget moyen";

export default function App() {
  const [input, setInput] = useState(samplePrompt);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [data, setData] = useState(null);
  const [history, setHistory] = useState([]);

  const hasLooks = useMemo(() => data && data.looks && data.looks.length > 0, [data]);

  useEffect(() => {
    fetchHistory()
      .then(setHistory)
      .catch(() => {});
  }, []);

  const onSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    try {
      const res = await generateLook(input);
      setData(res);
      const hist = await fetchHistory();
      setHistory(hist);
    } catch (err) {
      setError(err.message || "Erreur lors de la génération");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="page">
      <header className="hero">
        <div>
          <p className="eyebrow">Wardrobe AI</p>
          <h1>Assistant de stylisme</h1>
          <p className="lede">
            Saisis un brief et reçois trois looks classés par budget, avec images générées.
          </p>
        </div>
        <form className="card form" onSubmit={onSubmit}>
          <label htmlFor="input">Brief utilisateur</label>
          <textarea
            id="input"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder={samplePrompt}
            rows={3}
          />
          <button type="submit" disabled={loading || !input.trim()}>
            {loading ? "Génération..." : "Générer 3 looks"}
          </button>
          {error && <p className="error">{error}</p>}
        </form>
      </header>

      <main className="grid">
        <section className="card">
          <div className="section-header">
            <h2>Résultat</h2>
            {hasLooks && <span className="pill">Budget ↑</span>}
          </div>
          {!hasLooks && <p className="muted">Aucun look généré pour l’instant.</p>}
          {hasLooks && (
            <div className="looks">
              {data.looks.map((look) => (
                <article className="look" key={look.id}>
                  {look.image_url && (
                    <img src={look.image_url} alt={look.name} loading="lazy" />
                  )}
                  <div className="look-body">
                    <div className="look-title">
                      <h3>{look.name}</h3>
                      <span className="pill">{look.budget_label}</span>
                    </div>
                    <p className="muted">{look.justification}</p>
                    <ul className="stack">
                      <li>
                        <strong>Haut :</strong> {look.top}
                      </li>
                      <li>
                        <strong>Bas :</strong> {look.bottom}
                      </li>
                      <li>
                        <strong>Chaussures :</strong> {look.shoes}
                      </li>
                      <li>
                        <strong>Accessoires :</strong> {look.accessories}
                      </li>
                    </ul>
                    <div className="score">
                      <span>Score style : {look.style_score}/5</span>
                      <span>Rang budget : {look.budget_rank}</span>
                    </div>
                  </div>
                </article>
              ))}
            </div>
          )}
        </section>

        <section className="card">
          <h2>Historique récent</h2>
          {history.length === 0 && <p className="muted">Pas encore d’historique.</p>}
          <ul className="history">
            {history.map((req) => (
              <li key={req.id}>
                <div>
                  <p>{req.user_input}</p>
                  <span className="muted">
                    {new Date(req.created_at).toLocaleString("fr-FR")}
                  </span>
                </div>
              </li>
            ))}
          </ul>
        </section>
      </main>
    </div>
  );
}
