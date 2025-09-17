// src/AssistantRecommandation.jsx
import React, { useState } from "react";
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from "chart.js";
import { Doughnut } from "react-chartjs-2";
import { Shield, BriefcaseMedical, Send, Edit } from "lucide-react"; // Icônes modernes
import NavbarSection from "./NavbarSection";

ChartJS.register(ArcElement, Tooltip, Legend);

export default function AssistantRecommandation() {
  const [refClient, setRefClient] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [result, setResult] = useState(null);
  const [editing, setEditing] = useState(false);
  const [pitch, setPitch] = useState("");
  const [successMsg, setSuccessMsg] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    setResult(null);
    setSuccessMsg("");

    try {
      // Ici tu appelles ton API backend
    const formData = new FormData();
    formData.append("ref_client", refClient);  // nom identique à Flask

    const res = await fetch("http://127.0.0.1:5000/get_recommendation", {
      method: "POST",
      body: formData,
    });
    if (!res.ok) throw new Error("Erreur lors de la récupération des données");

      const data1 = await res.json();
      const data = data1.data; // Accéder à l'objet 'data'

      setResult(data);
      setPitch(data.pitch || "");
    } catch (err) {
      setError(err.message || "Erreur inconnue");
    } finally {
      setLoading(false);
    }
  };

  const handleSendPitch = () => {
    setSuccessMsg("✅ Pitch envoyé avec succès !");
    setEditing(false);
  };

  return (
    <div className="min-h-screen bg-gray-50 py-12 px-6">
      
      {/* Titre */}
{/* Titre */}


      {/* Formulaire */}
      <div className="max-w-3xl mx-auto bg-white rounded-2xl shadow-lg p-6 mb-12 pt-10 mt-8">
        <form
          onSubmit={handleSubmit}
          className="flex flex-col md:flex-row gap-4"
        >
          <input
            type="text"
            value={refClient}
            onChange={(e) => setRefClient(e.target.value)}
            placeholder="Entrez la référence client"
            className="flex-grow p-4 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <button
            type="submit"
            className="px-6 py-3 rounded-xl text-sm font-semibold transition-all duration-300
               hover:scale-105 hover:shadow-md
               bg-gradient-to-r from-blue-600 to-blue-400 text-white"
          >
            Obtenir la recommandation
          </button>
        </form>
      </div>

      {/* Loading */}
      {loading && (
        <div className="text-center text-blue-700">
          <div className="inline-block animate-spin rounded-full h-10 w-10 border-t-2 border-b-2 border-blue-500 mb-2"></div>
          <p>Analyse du profil client en cours...</p>
        </div>
      )}

      {/* Erreur */}
      {error && (
        <div className="max-w-3xl mx-auto bg-red-100 border-l-4 border-red-500 text-red-700 p-4 mb-8 rounded">
          <p>{error}</p>
        </div>
      )}

      {/* Résultats */}
      {result && (
        <div className="max-w-6xl mx-auto space-y-8">
          {/* Dashboard */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            {/* Produit */}
            <div className="bg-white rounded-2xl shadow-lg p-6 text-center hover:shadow-xl transition">
              <h2 className="text-xl font-semibold text-blue-800 mb-4">
                Produit Recommandé
              </h2>
              <div className="flex flex-col items-center">
                <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mb-3">
                  <Shield className="w-8 h-8 text-blue-600" />
                </div>
                <h3 className="text-lg font-medium">{result.produit_recommande}</h3>
                <p className="text-gray-600 text-sm">{result.branche}</p>
              </div>
            </div>

            {/* Score */}
            <div className="bg-white rounded-2xl shadow-lg p-6 text-center hover:shadow-xl transition">
              <h2 className="text-xl font-semibold text-blue-800 mb-4">
                Score de Pertinence
              </h2>
              <div className="flex flex-col items-center">
                <div className="relative w-32 h-32 mb-3">
                  <Doughnut
                    data={{
                      labels: ["Pertinence", "Reste"],
                      datasets: [
                        {
                          data: [result.score_pertinence, 100 - result.score_pertinence],
                          backgroundColor: ["#2563eb", "#e5e7eb"],
                          borderWidth: 0,
                        },
                      ],
                    }}
                    options={{ cutout: "70%" }}
                  />
                </div>
                <p className="text-lg font-semibold text-blue-700">
                  {result.score_pertinence}%
                </p>
              </div>
            </div>

            {/* Branche */}
            <div className="bg-white rounded-2xl shadow-lg p-6 text-center hover:shadow-xl transition">
              <h2 className="text-xl font-semibold text-blue-800 mb-4">
                Branche d'Assurance
              </h2>
              <div className="flex flex-col items-center">
                <div className="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mb-3">
                  <BriefcaseMedical className="w-8 h-8 text-blue-600" />
                </div>
                <p className="text-lg font-medium">{result.branche}</p>
              </div>
            </div>
          </div>

          {/* Raisonnement & Pitch */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            {/* Raisonnement */}
            <div className="bg-white rounded-2xl shadow-lg p-6">
              <h2 className="text-xl font-semibold text-blue-800 mb-4">
                Analyse et Raisonnement
              </h2>
              <div className="text-gray-700">{result.raisonnement}</div>
            </div>

            {/* Pitch */}
            <div className="bg-white rounded-2xl shadow-lg p-6">
              <h2 className="text-xl font-semibold text-blue-800 mb-4">
                Pitch Commercial
              </h2>
              {!editing ? (
                <div className="text-gray-700">{pitch}</div>
              ) : (
                <textarea
                  value={pitch}
                  onChange={(e) => setPitch(e.target.value)}
                  className="w-full p-4 border rounded-lg min-h-[100px]"
                />
              )}
              <div className="mt-4 flex gap-3">
                <button
                  onClick={() => setEditing(!editing)}
                  className="flex items-center gap-2 px-4 py-2 rounded-xl bg-blue-500 text-white font-semibold hover:bg-blue-600 transition"
                >
                  <Edit size={18} />
                  {editing ? "Annuler" : "Modifier"}
                </button>
                <button
                  onClick={handleSendPitch}
                  disabled={!pitch}
                  className="flex items-center gap-2 px-4 py-2 rounded-xl bg-green-500 text-white font-semibold hover:bg-green-600 transition"
                >
                  <Send size={18} />
                  Envoyer
                </button>
              </div>
              {successMsg && (
                <div className="text-green-600 font-semibold mt-3 animate-pulse">
                  {successMsg}
                </div>
              )}
            </div>
          </div>

          {/* Conditions Générales */}
          <div className="bg-white rounded-2xl shadow-lg p-6">
            <h2 className="text-xl font-semibold text-blue-800 mb-4">
              Conditions Générales
            </h2>
            <div className="text-gray-700">{result.conditions_generales}</div>
          </div>
        </div>
      )}
    </div>
  );
}
