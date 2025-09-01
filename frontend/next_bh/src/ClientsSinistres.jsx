import React, { useState } from "react";
import axios from "axios";

const ClientSinistres = () => {
  const [clientRef, setClientRef] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setResult(null);
    setError("");
    setLoading(true);
    try {
      // Adapte l'URL selon ton backend (FastAPI, Flask, Next.js API route, etc.)
      const response = await axios.post("/", { client_ref: clientRef });
      setResult(response.data.data || response.data);
    } catch (err) {
      setError(
        err.response?.data?.message ||
        err.message ||
        "Erreur lors de la récupération des sinistres."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: 700, margin: "auto", padding: 24 }}>
      <h2>Analyse des sinistres d'un client</h2>
      <form onSubmit={handleSubmit} style={{ marginBottom: 24 }}>
        <label>
          Référence client :{" "}
          <input
            type="text"
            value={clientRef}
            onChange={(e) => setClientRef(e.target.value)}
            required
            style={{ marginRight: 8 }}
          />
        </label>
        <button type="submit" disabled={loading}>
          {loading ? "Analyse en cours..." : "Analyser"}
        </button>
      </form>

      {error && (
        <div style={{ color: "red", marginBottom: 16 }}>
          <b>Erreur :</b> {error}
        </div>
      )}

      {result && (
        <div style={{ background: "#f8f8f8", padding: 16, borderRadius: 8 }}>
          <h3>Résultat de l'analyse</h3>
          {result.analyse && (
            <>
              <b>Analyse :</b>
              <div style={{ whiteSpace: "pre-line", marginBottom: 8 }}>
                {result.analyse}
              </div>
            </>
          )}
          {result.causes_probables && (
            <>
              <b>Causes probables :</b>
              <div style={{ whiteSpace: "pre-line", marginBottom: 8 }}>
                {result.causes_probables}
              </div>
            </>
          )}
          {result.conseils_prevention && (
            <>
              <b>Conseils de prévention :</b>
              <div style={{ whiteSpace: "pre-line", marginBottom: 8 }}>
                {result.conseils_prevention}
              </div>
            </>
          )}
          {result.donnees_manquantes && result.donnees_manquantes !== "" && (
            <>
              <b>Données manquantes :</b>
              <div style={{ whiteSpace: "pre-line", marginBottom: 8 }}>
                {result.donnees_manquantes}
              </div>
            </>
          )}
          {result.errors && result.errors !== "" && (
            <>
              <b>Erreurs :</b>
              <div style={{ whiteSpace: "pre-line", marginBottom: 8 }}>
                {result.errors}
              </div>
            </>
          )}
          {result.email && (
            <>
              <b>Email généré pour le client :</b>
              <div
                style={{
                  background: "#fff",
                  border: "1px solid #ddd",
                  padding: 12,
                  borderRadius: 6,
                  marginTop: 8,
                  whiteSpace: "pre-line",
                }}
              >
                {result.email}
              </div>
            </>
          )}
        </div>
      )}
    </div>
  );
};

export default ClientSinistres;