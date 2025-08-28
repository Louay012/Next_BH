import React, { useEffect, useState } from "react";
import axios from "axios";
import {
  PieChart, Pie, Cell, Tooltip, Legend,
  BarChart, Bar, XAxis, YAxis, CartesianGrid,
  LineChart, Line, ResponsiveContainer
} from "recharts";



// Modern color palette with better gradients
// Light mode color palette (harmonious & elegant)
const COLORS = [
  "#6EE7B7", 
   // Emerald Green - Accepted
  "#8B5CF6",  // Purple - Refused
  "#BCB3D8FF",  // Lavender - On Hold / Review
  "#10B981",  // Soft Mint Green - Pending / In Progress
  "#C084FC",  // Muted Magenta - Canceled / Error
  "#3B82F6",  // Soft Blue - Neutral / Info
  "#818CF8",  // Light Indigo - Total / Other stats
  "#22D3EE",  // Light Cyan - Complementary
];

// Dark mode color palette (better contrast, same harmony)
const DARK_COLORS = [
  "#34D399",  // Emerald Light - Accepted
  "#A78BFA",  // Purple Light - Refused
  "#D8B4FE",  // Lavender Light - On Hold / Review
  "#86EFAC",  // Mint Light - Pending / In Progress
  "#E0AAFF",  // Muted Magenta Light - Canceled / Error
  "#60A5FA",  // Soft Blue Light - Neutral / Info
  "#818CF8",  // Light Indigo - Total / Other stats
  "#22D3EE",  // Light Cyan - Complementary
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
    const isDarkMode = localStorage.getItem('darkMode') === 'true';
    setDarkMode(isDarkMode);
    setStats(STATIC_STATS);
  }, []);
  
  const toggleDarkMode = () => {
    const newDarkMode = !darkMode;
    setDarkMode(newDarkMode);
    localStorage.setItem('darkMode', newDarkMode);
  };
  
  if (!stats) {
    return (
      <div  className="flex items-center justify-center h-screen bg-gradient-to-br from-slate-50 to-slate-100 dark:from-slate-900 dark:to-slate-800">
        <div className="flex flex-col items-center">
          <div className="relative">
            <div className="w-16 h-16 rounded-full border-4 border-indigo-200"></div>
            <div className="w-16 h-16 rounded-full border-4 border-indigo-600 border-t-transparent animate-spin absolute top-0 left-0"></div>
          </div>
          <p className="mt-4 text-lg font-medium text-slate-600 dark:text-slate-300">Chargement...</p>
        </div>
      </div>
    );
  }
  
  const statusData = Object.entries(stats.status_counts).map(([name, value]) => ({ 
    name: name === 'accepted' ? 'Acceptées' : name === 'refused' ? 'Refusées' : 'En cours', 
    value 
  }));
  const productData = Object.entries(stats.product_counts).map(([name, value]) => ({ name, value }));
  const dateData = Object.entries(stats.by_date).map(([date, value]) => ({ date, value }));
  
          // Modern theme classes
          const bgClass = darkMode 
            ? "bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900" 
            : "bg-gradient-to-br from-slate-50 via-slate-100 to-slate-200";
          const cardClass = darkMode 
            ? "bg-slate-700/80 backdrop-blur-sm border-slate-700/50 shadow-lg" 
            : "bg-white/90 backdrop-blur-sm border-slate-200/50 shadow-md";
          const mainCardClass = darkMode 
            ? "bg-slate-800/80 backdrop-blur-sm border-slate-700/50 shadow-lg" 
            : "bg-white/90 backdrop-blur-sm border-slate-200/50 shadow-md";
          const textClass = darkMode ? "text-slate-100" : "text-slate-800";
          const textSecondaryClass = darkMode ? "text-slate-300" : "text-slate-600";
          const inputClass = darkMode 
            ? "bg-slate-700/80 border-slate-600 text-slate-100 placeholder-slate-400" 
            : "bg-slate-50 border-slate-200 text-slate-800 placeholder-slate-400";
          const badgeClass = darkMode 
            ? "bg-slate-700/60 text-slate-300" 
    : "bg-slate-100 text-slate-600";
  const footerClass = darkMode 
    ? "text-slate-500 border-slate-700/50" 
    : "text-slate-400 border-slate-100/50";
  
  // Colors adapted to theme
  const chartColors = darkMode ? DARK_COLORS : COLORS;
  
  return (
    <div  className={`min-h-screen ${bgClass} p-8 transition-all duration-500`}>
      <div className="max-w-[1400px] mx-auto">
        <div className={`${mainCardClass} rounded-3xl overflow-hidden border transition-all duration-300 hover:shadow-2xl`}>
          <div className="flex flex-col lg:flex-row">
            {/* Main content */}
            <main className="flex-1 p-6">
              {/* Header with theme selector */}
              <header className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 mb-8">
                <div className="flex flex-col sm:flex-row items-start sm:items-center gap-4 w-full">
                  <div className="relative w-full sm:w-auto">
                    <input 
                      placeholder="Rechercher des recommandations..." 
                      className={`pl-12 pr-4 py-3 rounded-2xl border ${inputClass} text-sm w-full sm:w-96 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all duration-300 shadow-sm`} 
                    />
                    <div className="absolute left-4 top-1/2 transform -translate-y-1/2 text-slate-400">
                      <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                      </svg>
                    </div>
                  </div>
                  <div className={`text-sm font-medium ${badgeClass} px-4 py-2 rounded-full flex items-center gap-2`}>
                    <div className="w-2 h-2 rounded-full bg-green-500"></div>
                    Aperçu
                  </div>
                </div>
                <div className="flex items-center gap-4">
                  <button className={`px-5 py-2.5 cursor-pointer rounded-2xl border ${darkMode ? 'border-slate-600 bg-slate-700/50 text-slate-200' : 'border-slate-200 bg-white text-slate-700'} text-sm font-medium hover:bg-slate-50 dark:hover:bg-slate-700/50 transition-all duration-300 shadow-sm flex items-center gap-2`}>
                   
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
                    </svg>
                    Exporter
                  </button>
                  
                  {/* Theme selector */}
                  <button 
                    onClick={toggleDarkMode}
                    className={`p-3 rounded-full ${darkMode ? 'bg-gradient-to-br from-amber-200 to-gray-200 text-slate-900' : 'bg-gradient-to-br from-slate-800 to-slate-900 text-amber-200'} transition-all duration-300 shadow-lg hover:shadow-xl transform hover:scale-105`}
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
              
              {/* Key indicators */}
              <section className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-10">
              <CardKPI 
                title="Total des recommandations" 
                value={stats.total_recommendations} 
                hint="+12% cette semaine" 
                color="bg-gradient-to-br from-indigo-600 to-indigo-800" 
                darkMode={darkMode} 
              />
              <CardKPI 
                title="Acceptées" 
                value={stats.accepted} 
                hint="Taux de conversion" 
                color="bg-gradient-to-br from-emerald-300 to-emerald-500" 
                darkMode={darkMode} 
              />
              <CardKPI 
                title="Refusées" 
                value={stats.refused} 
                hint="Nécessite une révision" 
                color="bg-gradient-to-br from-purple-500 to-purple-700" 
                darkMode={darkMode} 
              />
              <CardKPI 
                title="En cours" 
                value={stats.purchased} 
                hint="Revenus" 
                color="bg-gradient-to-br from-gray-300 to-gray-500" 
                darkMode={darkMode} 
              />
            </section>

              
              {/* Charts grid */}
              <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                {/* Top row with equal height */}
                <div className="lg:col-span-3 flex flex-col lg:flex-row gap-6">
                  {/* Pie chart */}
                  <div className="flex-1">
                    <div className={`${cardClass} rounded-3xl p-6 shadow-lg hover:shadow-xl transition-all duration-300 transform hover:-translate-y-1 h-full`}>
                      <div className="flex items-center justify-between mb-6">
                        <h3 className={`text-xl font-bold ${textClass}`}>Statut des recommandations</h3>
                        <div className={`text-sm font-medium ${badgeClass} px-4 py-2 rounded-full flex items-center gap-2`}>
                          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                          </svg>
                          7 derniers jours
                        </div>
                      </div>
                      <div className="h-[calc(100%-80px)]">
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
                                borderRadius: '12px', 
                                border: darkMode ? '1px solid #334155' : '1px solid #e2e8f0',
                                backgroundColor: darkMode ? '#1e293b' : '#fff',
                                color: darkMode ? '#f1f5f9' : '#1e293b',
                                boxShadow: '0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)',
                                backdropFilter: 'blur(4px)'
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
                  
                  {/* Right widgets */}
                  <div className="flex-1 flex flex-col gap-6">
                    <div className={`${cardClass} rounded-3xl p-5 shadow-lg hover:shadow-xl transition-all duration-300 transform hover:-translate-y-1 flex-1`}>
                      <div className="flex items-center justify-between mb-4">
                        <div className="flex items-center gap-2">
                          <div className="w-3 h-3 rounded-full bg-emerald-500"></div>
                          <div className={`text-sm font-semibold ${textClass}`}>Meilleures recommandations</div>
                        </div>
                        <div className={`text-xs font-medium ${badgeClass} px-3 py-1.5 rounded-full flex items-center gap-1`}>
                          <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                          </svg>
                          Cette semaine
                        </div>
                      </div>
                      <ul className="space-y-3">
                        {productData.slice(0, 5).map((p, i) => (
                          <li key={i} className={`flex items-center justify-between p-3 rounded-xl transition-all duration-300 ${darkMode ? 'hover:bg-slate-700/50' : 'hover:bg-slate-50'}`}>
                            <div className={`text-sm font-medium ${textClass}`}>{p.name}</div>
                            <div className={`text-sm font-bold ${badgeClass} px-3 py-1.5 rounded-xl flex items-center gap-1`}>
                              <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                              </svg>
                              {p.value}
                            </div>
                          </li>
                        ))}
                      </ul>
                    </div>
                    
                    <div className={`${cardClass} rounded-3xl p-5 shadow-lg hover:shadow-xl transition-all duration-300 transform hover:-translate-y-1 flex-1`}>
                      <div className="flex items-center gap-2 mb-3">
                        <div className="w-3 h-3 rounded-full bg-violet-500"></div>
                        <div className={`text-sm font-semibold ${textClass}`}>Progrès</div>
                      </div>
                      <div className="mb-3">
                        <div className={`flex justify-between text-xs ${textSecondaryClass} mb-2`}>
                          <div>Taux d'achat</div>
                          <div className="font-bold">
                            {Math.round(
                              (stats.purchased / Math.max(1, stats.total_recommendations)) * 100
                            )}
                            %
                          </div>
                        </div>
                        <div className={`h-3 ${darkMode ? 'bg-slate-700/50' : 'bg-slate-100'} rounded-full overflow-hidden`}>
                          <div
                            style={{
                              width: `${Math.min(
                                100,
                                (stats.purchased / Math.max(1, stats.total_recommendations)) * 100
                              )}%`,
                            }}
                            className="h-full bg-gradient-to-r from-violet-600 to-indigo-600 rounded-full transition-all duration-1000 ease-out"
                          />
                        </div>
                      </div>
                      <div className="flex justify-between mt-4">
                        <div className={`text-xs ${textSecondaryClass}`}>Objectif: 40%</div>
                        <div className={`text-xs font-medium ${textClass}`}>
                          {Math.round(
                            (stats.purchased / Math.max(1, stats.total_recommendations)) * 100
                          ) >= 40 ? (
                            <span className="text-emerald-500 flex items-center gap-1">
                              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                              </svg>
                              Atteint
                            </span>
                          ) : (
                            <span className="text-amber-500 flex items-center gap-1">
                              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                              </svg>
                              En cours
                            </span>
                          )}
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
                
                {/* Bottom row: two charts spanning full width */}
                <div className=" lg:col-span-3 grid grid-cols-1 lg:grid-cols-2 gap-6">
                  <div className={`${cardClass} rounded-3xl p-5 shadow-lg hover:shadow-xl transition-all duration-300 transform hover:-translate-y-1 w-full`}>
                    <div className="flex items-center gap-2 mb-4">
                      <div className="w-3 h-3 rounded-full bg-indigo-500"></div>
                      <h4 className={`text-md font-bold ${textClass}`}>Meilleurs produits</h4>
                    </div>
                    <div className="w-full h-64">
                      <ResponsiveContainer width="100%" height="100%">
                        <BarChart data={productData} margin={{ left: -10 }}>
                          <CartesianGrid strokeDasharray="3 3" stroke={darkMode ? "#334155/30" : "#f1f5f9/50"} vertical={false} />
                          <XAxis dataKey="name" stroke={darkMode ? "#94a3b8" : "#64748b"} tick={{ fontSize: 12 }} />
                          <YAxis allowDecimals={false} stroke={darkMode ? "#94a3b8" : "#64748b"} tick={{ fontSize: 12 }} />
                          <Tooltip 
                            contentStyle={{ 
                              borderRadius: '12px', 
                              border: darkMode ? '1px solid #334155' : '1px solid #e2e8f0',
                              backgroundColor: darkMode ? '#1e293b' : '#fff',
                              color: darkMode ? '#f1f5f9' : '#1e293b',
                              boxShadow: '0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)',
                              backdropFilter: 'blur(4px)'
                            }}
                          />
                          <Bar 
                            dataKey="value" 
                            fill="url(#colorGradient)" 
                            radius={[8, 8, 0, 0]} 
                            barSize={30}
                            animationDuration={1500}
                          >
                            {productData.map((entry, index) => (
                              <Cell key={`cell-${index}`} fill={chartColors[index % chartColors.length]} />
                            ))}
                          </Bar>
                        </BarChart>
                      </ResponsiveContainer>
                    </div>
                  </div>
                  
                  <div className={`${cardClass} rounded-3xl p-5 shadow-lg hover:shadow-xl transition-all duration-300 transform hover:-translate-y-1 w-full`}>
                    <div className="flex items-center gap-2 mb-4">
                      <div className="w-3 h-3 rounded-full bg-teal-500"></div>
                      <h4 className={`text-md font-bold ${textClass}`}>Tendances par date</h4>
                    </div>
                    <div className="w-full h-64">
                      <ResponsiveContainer width="100%" height="100%">
                        <LineChart data={dateData}>
                          <CartesianGrid strokeDasharray="3 3" stroke={darkMode ? "#334155/30" : "#f1f5f9/50"} vertical={false} />
                          <XAxis dataKey="date" stroke={darkMode ? "#94a3b8" : "#64748b"} tick={{ fontSize: 12 }} />
                          <YAxis allowDecimals={false} stroke={darkMode ? "#94a3b8" : "#64748b"} tick={{ fontSize: 12 }} />
                          <Tooltip 
                            contentStyle={{ 
                              borderRadius: '12px', 
                              border: darkMode ? '1px solid #334155' : '1px solid #e2e8f0',
                              backgroundColor: darkMode ? '#1e293b' : '#fff',
                              color: darkMode ? '#f1f5f9' : '#1e293b',
                              boxShadow: '0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)',
                              backdropFilter: 'blur(4px)'
                            }}
                          />
                          <Line
                            type="monotone"
                            dataKey="value"
                            stroke="url(#lineGradient)"
                            strokeWidth={3}
                            dot={{ r: 5, fill: darkMode ? "#0f172a" : "#fff", strokeWidth: 2, stroke: "#0ea5e9" }}
                            activeDot={{ r: 7, fill: "#0ea5e9", stroke: darkMode ? "#0f172a" : "#fff", strokeWidth: 2 }}
                            animationDuration={1500}
                          />
                          <defs>
                            <linearGradient id="lineGradient" x1="0" y1="0" x2="1" y2="0">
                              <stop offset="5%" stopColor="#0ea5e9" stopOpacity={0.9}/>
                              <stop offset="95%" stopColor="#06b6d4" stopOpacity={0.9}/>
                            </linearGradient>
                          </defs>
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
    <div className={`rounded-3xl p-6 text-white shadow-xl hover:shadow-2xl transition-all duration-500 transform hover:-translate-y-2 ${color} overflow-hidden relative`}>
      {/* Decorative elements */}
      <div className="absolute top-0 right-0 w-32 h-32 bg-white/10 rounded-full -mr-16 -mt-16"></div>
      <div className="absolute bottom-0 left-0 w-24 h-24 bg-white/10 rounded-full -ml-12 -mb-12"></div>
      
      <div className="text-md font-medium text-white/90 mb-2 relative z-10">{title}</div>
      <div className="mt-3 flex items-baseline justify-between relative z-10">
        <div className="text-4xl font-extrabold">{value}</div>
        {hint && (
          <div className="text-xs font-medium text-white/80 bg-white/20 px-3 py-1.5 rounded-full backdrop-blur-sm">
            {hint}
          </div>
        )}
      </div>
      
      {/* Icon */}
      <div className="absolute bottom-4 right-4 opacity-20">
        <svg className="w-12 h-12" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
        </svg>
      </div>
    </div>
  );
}