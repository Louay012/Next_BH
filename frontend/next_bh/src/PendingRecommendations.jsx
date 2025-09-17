import React, { useEffect, useState } from "react";

function PendingRecommendations() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("http://127.0.0.1:5000/list_pending")
      .then((res) => res.json())
      .then((resData) => {
        setData(resData);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Erreur API:", err);
        setLoading(false);
      });
  }, []);

  if (loading) return <p className="text-center p-5">⏳ Chargement...</p>;
  if (!data) return <p className="text-center p-5">❌ Erreur de chargement</p>;

  return (
    <div className="p-6 bg-gray-100 min-h-screen mt-20">
      <h1 className="text-2xl font-bold mb-4 text-center">
        ⏳ Recommandations En Attente
      </h1>

      <div className="bg-white shadow-md rounded-lg p-4 mb-6">
        <p className="text-lg font-semibold text-gray-700">
          ⏳ Total En Attente :{" "}
          <span className="text-yellow-600">{data.total_pending}</span>
        </p>
      </div>

      <div className="bg-white shadow-md rounded-lg p-4">
        <h2 className="text-xl font-semibold mb-3">📋 Détails</h2>
        <table className="w-full border-collapse border border-gray-300">
          <thead>
            <tr className="bg-gray-200 text-gray-700">
              <th className="border p-2">#</th>
              <th className="border p-2">Client Ref</th>
              <th className="border p-2">Produit Recommandé</th>
              <th className="border p-2">Date Création</th>
            </tr>
          </thead>
          <tbody>
            {data.pending_list.map((rec, index) => (
              <tr key={index} className="hover:bg-blue-200">
                <td className="border p-2 text-center">{index + 1}</td>
                <td className="border p-2">{rec.client_ref}</td>
                <td className="border p-2">{rec["recommendation.produit_recommande"]}</td>
                <td className="border p-2">
                  {new Date(rec.created_at).toLocaleString("fr-FR")}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default PendingRecommendations;
