import React, { useEffect, useState } from "react";
import axios from "axios";
import {
  PieChart, Pie, Cell, Tooltip, Legend,
  BarChart, Bar, XAxis, YAxis, CartesianGrid,
  LineChart, Line, ResponsiveContainer
} from "recharts";

// ...existing code...
const COLORS = [
  "#1C398E",  // Bleu profond (Couleur principale de la marque)
  "#9F0712",  // Rouge profond (Couleur secondaire de la marque)
  "#62748E",  // Bleu acier
  "#2C3E50",  // Gris bleu foncé
  "#34495E",  // Gris bleu
  "#516A8B"   // Bleu atténué
];
const STATIC_STATS = {
  total_recommendations: 85,
  accepted: 35,
  refused: 28,
  purchased: 22,
  status_counts: {
    accepted: 35,
    refused: 28,
    purchased: 22,
  },
  product_counts: {
    Auto: 25,
    Santé: 20,
    Vie: 15,
    Habitation: 12,
    
  },
  by_date: {
    "2024-08-01": 8,
    "2024-08-02": 12,
    "2024-08-03": 15,
    "2024-08-04": 10,
    "2024-08-05": 18,
    "2024-08-06": 14,
    "2024-08-07": 8
  }

};

export default function Dashboard() {
  const [stats, setStats] = useState(null);

  useEffect(() => {
    // Garder les données de test statiques (inchangées)
    setStats(STATIC_STATS);
    // axios.get("/api/recommendation-stats").then(res => setStats(res.data));
  }, []);

  if (!stats) {
    return <div className="flex items-center justify-center h-screen bg-slate-50">Chargement...</div>;
  }

  const statusData = Object.entries(stats.status_counts).map(([name, value]) => ({ 
    name: name === 'accepted' ? 'Acceptées' : name === 'refused' ? 'Refusées' : 'Achetées', 
    value 
  }));
  const productData = Object.entries(stats.product_counts).map(([name, value]) => ({ name, value }));
  const dateData = Object.entries(stats.by_date).map(([date, value]) => ({ date, value }));

  return (
    <div className="min-h-screen bg-slate-100 p-6">
      <div className="max-w-[1200px] mx-auto">
        <div className="bg-white rounded-2xl shadow-lg overflow-hidden">
          <div className="flex">
           

            {/* Contenu principal */}
            <main className="flex-1 p-6">
              {/* En-tête */}
              <header className="flex items-center justify-between mb-6">
                <div className="flex items-center gap-4">
                  <input placeholder="Rechercher des recommandations..." className="pl-4 pr-3 py-2 rounded-lg border border-slate-200 bg-slate-50 text-sm w-80 focus:outline-none" />
                  <div className="text-sm text-slate-500">Aperçu</div>
                </div>
                <div className="flex items-center gap-4">
                  <button className="px-4 py-2 rounded-full border border-slate-200 bg-white text-slate-700 text-sm">Exporter</button>
                  <div className="flex items-center gap-3">
                    <div className="text-sm text-slate-600">Administrateur</div>
                    <div className="w-9 h-9 rounded-full bg-indigo-600 flex items-center justify-center text-white">A</div>
                  </div>
                </div>
              </header>

              {/* Indicateurs clés */}
              <section className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-6 mb-6">
                <CardKPI title="Total des recommandations" value={stats.total_recommendations} hint="+12% cette semaine" color="bg-slate-800" />
                <CardKPI title="Acceptées" value={stats.accepted} hint="Taux de conversion" color="bg-blue-900" />
                <CardKPI title="Refusées" value={stats.refused} hint="Nécessite une révision" color="bg-red-800" />
                <CardKPI title="Achetées" value={stats.purchased} hint="Revenus" color="bg-slate-500" />
              </section>

              {/* Grille des graphiques */}
              <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              

                {/* Gauche : Graphique circulaire + graphiques inférieurs */}
                <div className="lg:col-span-2 flex flex-col gap-6">
                  {/* Ligne supérieure : Graphique circulaire */}
                  <div className="bg-white border border-slate-100 rounded-2xl p-5 shadow-sm flex-1">
                    <div className="flex items-center justify-between mb-3">
                      <h3 className="text-lg font-semibold text-slate-800">Statut des recommandations</h3>
                      <div className="text-sm text-slate-400">7 derniers jours</div>
                    </div>
                    <ResponsiveContainer width="100%" height={350}>
                      <PieChart>
                        <Pie
                          data={statusData}
                          dataKey="value"
                          nameKey="name"
                          cx="50%"
                          cy="50%"
                          outerRadius="70%"
                          label
                        >
                          {statusData.map((entry, idx) => (
                            <Cell key={idx} fill={COLORS[idx % COLORS.length]} />
                          ))}
                        </Pie>
                        <Tooltip />
                        <Legend verticalAlign="bottom" height={36} />
                      </PieChart>
                    </ResponsiveContainer>
                  </div>

                  
                </div>
                          
                {/* Colonne droite : widgets empilés, correspondant à la hauteur de gauche */}
                <div className="flex flex-col gap-6">
                  <div className="bg-white border border-slate-100 rounded-2xl p-4 shadow-sm">
                    <div className="text-sm text-slate-500 mb-2">Rappels</div>
                    <div className="font-medium text-slate-800">Réunion avec l'équipe produit</div>
                    <div className="text-xs text-slate-400 mt-1">Aujourd'hui 15:00</div>
                  </div>

                  <div className="bg-white border border-slate-100 rounded-2xl p-4 shadow-sm flex-1">
                    <div className="flex items-center justify-between mb-3">
                      <div className="text-sm text-slate-500">Meilleures recommandations</div>
                      <div className="text-xs text-slate-400">Cette semaine</div>
                    </div>
                    <ul className="space-y-2">
                      {productData.slice(0, 5).map((p, i) => (
                        <li key={i} className="flex items-center justify-between">
                          <div className="text-sm text-slate-700">{p.name}</div>
                          <div className="text-sm font-semibold text-slate-900">{p.value}</div>
                        </li>
                      ))}
                    </ul>
                  </div>

                  <div className="bg-white border border-slate-100 rounded-2xl p-4 shadow-sm flex-1">
                    <div className="text-sm text-slate-500 mb-2">Progrès</div>
                    <div className="h-3 bg-slate-100 rounded-full overflow-hidden">
                      <div
                        style={{
                          width: `${Math.min(
                            100,
                            (stats.purchased / Math.max(1, stats.total_recommendations)) * 100
                          )}%`,
                        }}
                        className="h-full bg-sky-900"
                      />
                    </div>
                    <div className="flex justify-between text-xs text-slate-400 mt-3">
                      <div>Taux d'achat</div>
                      <div>
                        {Math.round(
                          (stats.purchased / Math.max(1, stats.total_recommendations)) * 100
                        )}
                        %
                      </div>
                    </div>
                  </div>
                </div>
                {/* Ligne inférieure : deux graphiques occupant toute la largeur */}
                  <div className="grid grid-cols-2 lg:col-span-3 gap-6 flex-1">
                    
                    <div className="bg-white border border-slate-100 rounded-2xl p-5 shadow-sm w-full">
                      <h4 className="text-md font-semibold mb-3 text-slate-800">Meilleurs produits</h4>
                      <div className="w-full h-64">
                        <ResponsiveContainer width="100%" height="100%">
                          <BarChart data={productData} margin={{ left: -10 }}>
                            <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
                            <XAxis dataKey="name" stroke="#475569" />
                            <YAxis allowDecimals={false} stroke="#475569" />
                            <Tooltip />
                            <Bar dataKey="value" fill="#1C398E" radius={[6, 6, 0, 0]} />
                          </BarChart>
                        </ResponsiveContainer>
                      </div>
                    </div>

                    <div className="bg-white border border-slate-100 rounded-2xl p-5 shadow-sm w-full">
                      <h4 className="text-md font-semibold mb-3 text-slate-800">Tendances par date</h4>
                      <div className="w-full h-64">
                        <ResponsiveContainer width="100%" height="100%">
                          <LineChart data={dateData}>
                            <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
                            <XAxis dataKey="date" stroke="#475569" />
                            <YAxis allowDecimals={false} stroke="#475569" />
                            <Tooltip />
                            <Line
                              type="monotone"
                              dataKey="value"
                              stroke="#024A71"
                              strokeWidth={3}
                              dot={{ r: 3 }}
                            />
                          </LineChart>
                        </ResponsiveContainer>
                      </div>
                    </div>
                  </div>
              </div>

              <footer className="mt-6 text-xs text-slate-400">© NEXT_BH Échantillon de tableau de bord</footer>
            </main>
          </div>
        </div>
      </div>
    </div>
  );
}

// ...existing code...
function CardKPI({ title, value, hint, color }) {
  return (
    <div className={`rounded-2xl p-5 text-white shadow ${color}`}>
      <div className="text-sm text-white/80">{title}</div>
      <div className="mt-3 flex items-baseline justify-between">
        <div className="text-2xl font-extrabold">{value}</div>
        {hint && <div className="text-xs text-white/80">{hint}</div>}
      </div>
    </div>
  );
}