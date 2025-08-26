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

const DARK_COLORS = [
  "#4F7FFF",  // Bleu clair pour le mode sombre
  "#FF6B6B",  // Rouge clair pour le mode sombre
  "#6B9BFF",  // Bleu acier clair
  "#7FB3FF",  // Gris bleu clair
  "#8FB8FF",  // Gris bleu plus clair
  "#A0C2FF"   // Bleu atténué clair
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
  const [darkMode, setDarkMode] = useState(false);
  
  useEffect(() => {
    // Vérifier la préférence de thème dans le localStorage
    const isDarkMode = localStorage.getItem('darkMode') === 'true';
    setDarkMode(isDarkMode);
    
    // Garder les données de test statiques (inchangées)
    setStats(STATIC_STATS);
    // axios.get("/api/recommendation-stats").then(res => setStats(res.data));
  }, []);

  // Basculer entre les modes clair et sombre
  const toggleDarkMode = () => {
    const newDarkMode = !darkMode;
    setDarkMode(newDarkMode);
    localStorage.setItem('darkMode', newDarkMode);
  };
  
  if (!stats) {
    return <div className="flex items-center justify-center h-screen bg-slate-50 dark:bg-slate-900">Chargement...</div>;
  }
  
  const statusData = Object.entries(stats.status_counts).map(([name, value]) => ({ 
    name: name === 'accepted' ? 'Acceptées' : name === 'refused' ? 'Refusées' : 'Achetées', 
    value 
  }));
  const productData = Object.entries(stats.product_counts).map(([name, value]) => ({ name, value }));
  const dateData = Object.entries(stats.by_date).map(([date, value]) => ({ date, value }));
  
  // Appliquer les classes de thème en fonction du mode
  const bgClass = darkMode ? "bg-gradient-to-br from-slate-900 to-slate-700" : "bg-gradient-to-br from-slate-50 to-slate-100";
  const cardClass = darkMode ? "bg-slate-800 border-slate-600 border-2 " : "bg-white border-slate-100";
  const textClass = darkMode ? "text-slate-100" : "text-slate-800";
  const textSecondaryClass = darkMode ? "text-slate-300" : "text-slate-600";
  const inputClass = darkMode ? "bg-slate-700 border-slate-600 text-slate-100" : "bg-slate-50 border-slate-200 text-slate-800";
  const badgeClass = darkMode ? "bg-slate-700 text-slate-300" : "bg-slate-100 text-slate-600";
  const footerClass = darkMode ? "text-slate-500 border-slate-700" : "text-slate-400 border-slate-100";
  
  // Couleurs adaptées au mode
  const chartColors = darkMode ? DARK_COLORS : COLORS;
  
  return (
    <div className={`min-h-screen ${bgClass} p-6 transition-colors duration-300`}>
      <div className="max-w-[1200px] mx-auto">
        <div className={`${cardClass} rounded-2xl shadow-xl overflow-hidden border transition-colors duration-300`}>
          <div className="flex">
            {/* Contenu principal */}
            <main className="flex-1 p-6">
              {/* En-tête avec sélecteur de thème */}
              <header className="flex items-center justify-between mb-8">
                <div className="flex items-center gap-4">
                  <div className="relative">
                    <input 
                      placeholder="Rechercher des recommandations..." 
                      className={`pl-10 pr-4 py-3 rounded-xl border ${inputClass} text-sm w-80 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200`} 
                    />
                    <div className="absolute left-3 top-1/2 transform -translate-y-1/2 text-slate-400">
                      <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                      </svg>
                    </div>
                  </div>
                  <div className={`text-sm font-medium ${badgeClass} px-3 py-1 rounded-full`}>Aperçu</div>
                </div>
                <div className="flex items-center gap-4">
                  <button className={`px-4 py-2 rounded-full border ${darkMode ? 'border-slate-600 bg-slate-700 text-slate-200' : 'border-slate-200 bg-white text-slate-700'} text-sm font-medium hover:bg-slate-50 dark:hover:bg-slate-700 transition-colors duration-200 shadow-sm`}>
                    Exporter
                  </button>
                  
                  {/* Sélecteur de thème */}
                  <button 
                    onClick={toggleDarkMode}
                    className={`p-2 rounded-full ${darkMode ? 'bg-cyan-50 text-slate-900' : 'bg-slate-800 text-yellow-300'}`}
                    aria-label="Basculer le thème"
                  >
                    {darkMode ? (
                      <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
                      </svg>
                    ) : (
                      <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
                      </svg>
                    )}
                  </button>
                </div>
              </header>
              
              {/* Indicateurs clés */}
              <section className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-6 mb-8">
                <CardKPI title="Total des recommandations" value={stats.total_recommendations} hint="+12% cette semaine" color="bg-gradient-to-br from-slate-800 to-slate-900" darkMode={darkMode} />
                <CardKPI title="Acceptées" value={stats.accepted} hint="Taux de conversion" color="bg-gradient-to-br from-blue-800 to-blue-900" darkMode={darkMode} />
                <CardKPI title="Refusées" value={stats.refused} hint="Nécessite une révision" color="bg-gradient-to-br from-red-700 to-red-800" darkMode={darkMode} />
                <CardKPI title="Achetées" value={stats.purchased} hint="Revenus" color="bg-gradient-to-br from-slate-600 to-slate-700" darkMode={darkMode} />
              </section>
              
              {/* Grille des graphiques */}
              <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                {/* Gauche : Graphique circulaire + graphiques inférieurs */}
                <div className="lg:col-span-2 flex flex-col gap-6">
                  {/* Ligne supérieure : Graphique circulaire */}
                  <div className={`${cardClass} border-2 rounded-2xl p-6 shadow-md flex-1 hover:shadow-lg transition-shadow duration-300`}>
                    <div className="flex items-center justify-between mb-4">
                      <h3 className={`text-lg font-bold ${textClass}`}>Statut des recommandations</h3>
                      <div className={`text-sm font-medium ${badgeClass} px-3 py-1 rounded-full`}>7 derniers jours</div>
                    </div>
                    <div className="h-80">
                      <ResponsiveContainer width="100%" height="100%">
                        <PieChart>
                          <Pie
                            data={statusData}
                            dataKey="value"
                            nameKey="name"
                            cx="50%"
                            cy="50%"
                            outerRadius="70%"
                            innerRadius={40}
                            paddingAngle={2}
                            label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
                            labelLine={false}
                          >
                            {statusData.map((entry, idx) => (
                              <Cell key={idx} fill={chartColors[idx % chartColors.length]} stroke={darkMode ? "#1e293b" : "#fff"} strokeWidth={2} />
                            ))}
                          </Pie>
                          <Tooltip 
                            formatter={(value) => [`${value}`, 'Nombre']}
                            contentStyle={{ 
                              borderRadius: '8px', 
                              border: darkMode ? '1px solid #334155' : '1px solid #e2e8f0',
                              backgroundColor: darkMode ? '#1e293b' : '#fff',
                              color: darkMode ? '#f1f5f9' : '#1e293b',
                              boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)'
                            }}
                          />
                          <Legend 
                            layout="horizontal" 
                            verticalAlign="bottom" 
                            align="center"
                            wrapperStyle={{ paddingTop: '20px' }}
                          />
                        </PieChart>
                      </ResponsiveContainer>
                    </div>
                  </div>
                </div>
                
                {/* Colonne droite : widgets empilés */}
                <div className="flex flex-col gap-6">
                  <div className={`${cardClass} rounded-2xl p-5 shadow-sm hover:shadow-md transition-shadow duration-300 flex-1`}>
                    <div className="flex items-center justify-between mb-4">
                      <div className="flex items-center gap-2">
                        <div className="w-3 h-3 rounded-full bg-green-500"></div>
                        <div className={`text-sm font-semibold ${textClass}`}>Meilleures recommandations</div>
                      </div>
                      <div className={`text-xs font-medium ${badgeClass} px-2 py-1 rounded-full`}>Cette semaine</div>
                    </div>
                    <ul className="space-y-3">
                      {productData.slice(0, 5).map((p, i) => (
                        <li key={i} className={`flex items-center justify-between p-2 rounded-lg transition-colors duration-200 ${darkMode ? 'hover:bg-slate-700' : 'hover:bg-slate-50'}`}>
                          <div className={`text-sm font-medium ${textClass}`}>{p.name}</div>
                          <div className={`text-sm font-bold ${badgeClass} px-2 py-1 rounded-md`}>{p.value}</div>
                        </li>
                      ))}
                    </ul>
                  </div>
                  
                  <div className={`${cardClass} rounded-2xl p-5 shadow-sm hover:shadow-md transition-shadow duration-300 flex-1`}>
                    <div className="flex items-center gap-2 mb-3">
                      <div className="w-3 h-3 rounded-full bg-purple-500"></div>
                      <div className={`text-sm font-semibold ${textClass}`}>Progrès</div>
                    </div>
                    <div className="mb-2">
                      <div className={`flex justify-between text-xs ${textSecondaryClass} mb-1`}>
                        <div>Taux d'achat</div>
                        <div className="font-bold">
                          {Math.round(
                            (stats.purchased / Math.max(1, stats.total_recommendations)) * 100
                          )}
                          %
                        </div>
                      </div>
                      <div className={`h-4 ${darkMode ? 'bg-slate-700' : 'bg-slate-100'} rounded-full overflow-hidden`}>
                        <div
                          style={{
                            width: `${Math.min(
                              100,
                              (stats.purchased / Math.max(1, stats.total_recommendations)) * 100
                            )}%`,
                          }}
                          className="h-full bg-gradient-to-r from-sky-600 to-sky-800 rounded-full transition-all duration-1000 ease-out"
                        />
                      </div>
                    </div>
                  </div>
                </div>
                
                {/* Ligne inférieure : deux graphiques occupant toute la largeur */}
                <div className="grid grid-cols-2 lg:col-span-3 gap-6 flex-1">
                  <div className={`${cardClass} rounded-2xl p-5 shadow-sm hover:shadow-md transition-shadow duration-300 w-full`}>
                    <div className="flex items-center gap-2 mb-4">
                      <div className="w-3 h-3 rounded-full bg-indigo-500"></div>
                      <h4 className={`text-md font-bold ${textClass}`}>Meilleurs produits</h4>
                    </div>
                    <div className="w-full h-64">
                      <ResponsiveContainer width="100%" height="100%">
                        <BarChart data={productData} margin={{ left: -10 }}>
                          <CartesianGrid strokeDasharray="3 3" stroke={darkMode ? "#334155" : "#f1f5f9"} vertical={false} />
                          <XAxis dataKey="name" stroke={darkMode ? "#94a3b8" : "#64748b"} tick={{ fontSize: 12 }} />
                          <YAxis allowDecimals={false} stroke={darkMode ? "#94a3b8" : "#64748b"} tick={{ fontSize: 12 }} />
                          <Tooltip 
                            contentStyle={{ 
                              borderRadius: '8px', 
                              border: darkMode ? '1px solid #334155' : '1px solid #e2e8f0',
                              backgroundColor: darkMode ? '#1e293b' : '#fff',
                              color: darkMode ? '#f1f5f9' : '#1e293b',
                              boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)'
                            }}
                          />
                          <Bar 
                            dataKey="value" 
                            fill="url(#colorGradient)" 
                            radius={[6, 6, 0, 0]} 
                            barSize={30}
                          />
                          <defs>
                            <linearGradient id="colorGradient" x1="0" y1="0" x2="0" y2="1">
                              <stop offset="5%" stopColor="#1C398E" stopOpacity={0.9}/>
                              <stop offset="95%" stopColor="#1C398E" stopOpacity={0.6}/>
                            </linearGradient>
                          </defs>
                        </BarChart>
                      </ResponsiveContainer>
                    </div>
                  </div>
                  
                  <div className={`${cardClass} rounded-2xl p-5 shadow-sm hover:shadow-md transition-shadow duration-300 w-full`}>
                    <div className="flex items-center gap-2 mb-4">
                      <div className="w-3 h-3 rounded-full bg-teal-500"></div>
                      <h4 className={`text-md font-bold ${textClass}`}>Tendances par date</h4>
                    </div>
                    <div className="w-full h-64">
                      <ResponsiveContainer width="100%" height="100%">
                        <LineChart data={dateData}>
                          <CartesianGrid strokeDasharray="3 3" stroke={darkMode ? "#334155" : "#f1f5f9"} vertical={false} />
                          <XAxis dataKey="date" stroke={darkMode ? "#94a3b8" : "#64748b"} tick={{ fontSize: 12 }} />
                          <YAxis allowDecimals={false} stroke={darkMode ? "#94a3b8" : "#64748b"} tick={{ fontSize: 12 }} />
                          <Tooltip 
                            contentStyle={{ 
                              borderRadius: '8px', 
                              border: darkMode ? '1px solid #334155' : '1px solid #e2e8f0',
                              backgroundColor: darkMode ? '#1e293b' : '#fff',
                              color: darkMode ? '#f1f5f9' : '#1e293b',
                              boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)'
                            }}
                          />
                          <Line
                            type="monotone"
                            dataKey="value"
                            stroke="#024A71"
                            strokeWidth={3}
                            dot={{ r: 4, fill: "#024A71", strokeWidth: 2, stroke: darkMode ? "#1e293b" : "#fff" }}
                            activeDot={{ r: 6, fill: darkMode ? "#1e293b" : "#fff", stroke: "#024A71", strokeWidth: 2 }}
                          />
                        </LineChart>
                      </ResponsiveContainer>
                    </div>
                  </div>
                </div>
              </div>
              
              <footer className={`mt-8 text-xs ${footerClass} text-center py-4 border-t transition-colors duration-300`}>
                © NEXT_BH Échantillon de tableau de bord
              </footer>
            </main>
          </div>
        </div>
      </div>
    </div>
  );
}

function CardKPI({ title, value, hint, color, darkMode }) {
  return (
    <div className={`rounded-2xl p-5 text-white shadow-lg hover:shadow-xl transition-all duration-300 transform hover:-translate-y-1 ${color}`}>
      <div className="text-sm font-medium text-white/90 mb-1">{title}</div>
      <div className="mt-3 flex items-baseline justify-between">
        <div className="text-3xl font-extrabold">{value}</div>
        {hint && <div className="text-xs font-medium text-white/80 bg-white/20 px-2 py-1 rounded-full">{hint}</div>}
      </div>
    </div>
  );
}