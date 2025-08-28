// src/App.js
import React, { useState, useEffect } from 'react';
import { BarChart, Bar, PieChart, Pie, Cell, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, RadialBarChart, RadialBar, PolarAngleAxis  } from 'recharts';

import './App.css';
import { IoAddCircleOutline } from "react-icons/io5";

// Modern color palette
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

// Static data (unchanged)
const staticData = {
  client_ref: '1381',
  client_name: 'Jean Dupont',
  client_details: {
    age: 63,
    profession: 'Chauffeur',
    marital_status: 'Marié',
    contracts: ['Automobile', 'Décès temporaire (expiré)']
  },
  recommendations: [
    {
      id: '68a04264bd9cde4606fd0d47',
      client_ref: '1381',
      produit_recommande: 'CG ASSURANCE GROUPE MALADIE',
      branche: 'Assurance Santé',
      score_pertinence: '85/100',
      score_value: 85,
      created_at: '2025-08-16T10:33:40.982Z',
      status: "Accepté",
      raisonnement: "Le client est un chauffeur de 63 ans, marié, avec un contrat automobile résilié et 2 contrats d'assurance décès expirés. Son profil professionnel à risque nécessite une couverture santé adaptée, et son âge avancé justifie une préparation pour la retraite. Le système identifie clairement un manque de produit Santé. L'assurance groupe maladie est la meilleure solution pour couvrir les risques professionnels, protéger sa famille et préparer sa retraite.",
      pitch: "Cher Monsieur,\n\nEn tant que chauffeur expérimenté et marié, vous savez mieux que quiconque l'importance d'une couverture santé solide. Votre métier vous expose à des risques professionnels quotidiens, et à 63 ans, il est essentiel de préparer votre avenir avec sérénité.\n\nNotre assurance groupe maladie CG ASSURANCE GROUPE MALADIE est spécialement conçue pour les professionnels comme vous. Elle offre une couverture complète pour vos besoins de santé, avec des avantages adaptés à votre situation familiale et à votre approche de la retraite.\n\nAvec cette assurance, vous bénéficiez d'un accès aux meilleurs soins médicaux, d'une couverture hospitalière étendue et d'une assistance 24/7. Votre famille est également protégée, vous permettant de voyager l'esprit tranquol.\n\nNe laissez pas les imprévus perturber votre tranquillité familiale. Investissez dès aujourd'hui dans une protection santé qui suivra votre carrière et votre retraite.\n\nJe reste à votre disposition pour discuter plus en détail de cette solution adaptée à votre profil.\n\nCordialement,\n\nVotre conseiller en assurances"
    },
    {
      id: '68a0a1fa0751de4d5f33f94',
      client_ref: '1381',
      produit_recommande: 'CG_RAHMA',
      branche: 'Assurance Vie',
      score_pertinence: '85/100',
      score_value: 85,
      created_at: '2025-08-16T11:06:39.206Z',
      status: "Accepté",
      raisonnement: "Le client, un chauffeur de 63 ans marié, a un historique de contrats d'assurance automobile et temporaire décès. Les opportunités détectées incluent un besoin en assurance Vie et santé. Parmi les produits disponibles, 'CG_RAHMA' (Assurance Vie) est le plus pertinent pour couvrir ses besoins de prévoyance, bien qu'il ne réponde pas complètement aux risques liés à sa profession.",
      pitch: "Bonjour Monsieur, En tant que chauffeur, vous êtes quotidiennement exposé à des risques professionnels. Pour protéger votre famille en cas d'imprévu, nous vous recommandons notre assurance Vie 'CG_RAHMA'. Ce produit vous offre une couverture en cas de décès, ainsi qu'une épargne complémentaire pour sécuriser votre avenir. Combiné à votre assurance automobile, il constitue une protection complète pour vous et vos proches. Nous restons à votre disposition pour en discuter plus en détail. Cordialement,"
    },
    {
      id: '68a078bee1e32ce70fe983aa',
      client_ref: '1381',
      produit_recommande: 'Assurance santé adaptée aux déplacements fréquents',
      branche: 'Santé',
      score_pertinence: '90/100',
      score_value: 90,
      created_at: '2025-08-16T14:25:34.972Z',
      status: "Refusé",
      raisonnement: 'Le client est un chauffeur de 63 ans sans couverture santé ou vie active. Une assurance santé adaptée aux déplacements fréquents est recommandée pour couvrir les risques liés à son métier et à son âge.',
      pitch: "Bonjour Jean Dupont, En tant que chauffeur, vous êtes quotidiennement exposé à des risques liés à votre activité et à vos déplacements. À 63 ans, il est essentiel de protéger votre santé et celle de votre famille. Nous vous recommandons notre assurance santé adaptée aux déplacements fréquents, qui vous offre une couverture complète en cas d'accident ou de problème de santé, où que vous soyez. Cette assurance inclut des prestations médicales étendues, une prise en charge rapide, et des garanties adaptées à votre rythme de vie. Protégez-vous et votre famille dès aujourd'hui en souscrivant à cette solution sur mesure. N'hésitez pas à nous contacter pour plus d'informations ou pour finaliser votre souscription. Cordialement, Votre conseiller en assurance."
    },
    {
      id: '68a0880c2ebe0fafa30e8c93',
      client_ref: '1381',
      produit_recommande: 'ASSURANCE SANTE',
      branche: 'SANTE',
      score_pertinence: '90/100',
      score_value: 90,
      created_at: '2025-08-16T15:30:52.929Z',
      status: "Refusé",
      raisonnement: "Le client est un chauffeur de 63 ans, marié, avec un seul contrat actif (automobile) et des contrats expirés (décès temporaire). Les opportunités détectées incluent l'absence d'assurance santé et d'assurance vie adaptée. En tant que chauffeur, il est exposé à des risques professionnels et de santé. Une assurance santé est recommandée pour couvrir ces risques et répondre à ses besoins de senior.",
      pitch: 'Bonjour, en tant que chauffeur professionnel, votre métier vous expose à des risques spécifiques liés aux déplacements fréquents. À 63 ans, il est également essentiel de prévoir une couverture santé adaptée à vos besoins. Notre assurance santé vous offre une protection complète, incluant les frais médicaux, les hospitalisations et les soins liés aux accidents professionnels. Avec des garanties étendues et des tarifs compétitifs, cette assurance est idéale pour sécuriser votre santé et celle de votre famille. Contactez-nous pour en savoir plus !'
    },
    {
      id: '68a08b116884ad103228aed4',
      client_ref: '1381',
      produit_recommande: 'Assurance Santé',
      branche: 'Santé',
      score_pertinence: '90/100',
      score_value: 90,
      created_at: '2025-08-16T15:43:45.198Z',
      status: "Refusé",
      raisonnement: "Le client est un chauffeur de 63 ans, marié, avec un contrat auto actif mais pas d'assurance santé. Les risques liés à son métier et à son âge justifient une couverture santé adaptée aux déplacements fréquents.",
      pitch: "Bonjour Monsieur Dupont, En tant que chauffeur professionnel, votre métier vous expose quotidiennement à des risques liés à vos déplacements. À 63 ans, il est également essentiel de vous protéger contre les imprévus de santé. Notre assurance santé est spécialement conçue pour les personnes actives comme vous, offrant une couverture complète même en déplacement, des consultations médicales à l'hospitalisation. Avec des garanties adaptées à votre rythme de vie, vous pourrez conduire l'esprit tranquille, sachant que vous et votre famille êtes protégés. N'attendez pas pour sécuriser votre avenir et celui de vos proches. Contactez-nous dès aujourd'hui pour en savoir plus !"
    },
    {
      id: '68a1a7b36e02d805ed273494',
      client_ref: '1381',
      produit_recommande: 'assurance groupe maladie',
      branche: 'santé',
      score_pertinence: '70/100',
      score_value: 70,
      created_at: '2025-08-17T11:58:11.498Z',
      status: "En cours",
      raisonnement: "Le client est un chauffeur de 63 ans, marié, travaillant dans le secteur des services personnels. Il possède actuellement un contrat automobile et a eu dans le passé des contrats d'assurance décès temporaire. Les opportunités détectées indiquent un manque de couverture santé et vie. Étant donné son âge et sa profession, il est crucial de lui proposer une assurance santé pour couvrir les risques médicaux et une assurance vie pour protéger sa famille en cas de décès ou invalidité. Le produit 'assurance groupe maladie' est pertinent pour la couverture santé, bien que l'âge maximal ciblé soit de 60 ans, ce qui pourrait nécessiter une adaptation. L'assurance vie pourrait être complétée par un produit adapté aux personnes de plus de 60 ans.",
      pitch: "Bonjour Monsieur Dupont, En tant que chauffeur professionnel, votre métier expose à des risques spécifiques, et il est essentiel de vous protéger ainsi que votre famille. Nous vous recommandons notre assurance groupe maladie, qui couvre les frais de santé, le décès et l'invalidité. Bien que l'âge cible maximal soit de 60 ans, nous pouvons adapter cette offre pour répondre à vos besoins. Cette assurance vous apportera une tranquillité d'esprit, notamment pour vos déplacements fréquents. N'hésitez pas à nous contacter pour personnaliser cette solution avec vous. Cordialement, Votre conseiller en assurance."
    },
    {
      id: '68a1ae8ca0882520a1464818',
      client_ref: '1381',
      produit_recommande: 'assurance individuelle contre les accidents corporels',
      branche: '4/IARD',
      score_pertinence: '80/100',
      score_value: 80,
      created_at: '2025-08-17T12:27:24.597Z',
      status: "En cours",
      raisonnement: "Le client, un chauffeur de 63 ans, marié, travaillant dans les services personnels, a un historique de contrats automobiles et temporaire décès. Il ne dispose actuellement que d'un contrat automobile résilié et non payé. Les opportunités détectées comprennent l'absence d'assurance santé et d'assurance vie. Compte tenu de son âge et de sa profession, une assurance santé serait pertinente pour couvrir les risques liés à son activité professionnelle, tandis qu'une assurance vie pourrait garantir sa famille en cas de décès ou d'invalidité. Parmi les produits proposés, l'assurance individuelle contre les accidents corporels (IARD) est adaptée à son profil, ainsi que le contrat 'Rahma' (assurance vie) qui propose des garanties en cas de décès ou invalidité.",
      pitch: "Objet : Offre d'assurance adaptée à votre profil professionnel et personnel\n\nCher Monsieur Dupont,\n\nEn tant que chauffeur professionnel, vous êtes exposé quotidiennement à des risques d'accidents corporels, que ce soit sur la route ou dans le cadre de votre activité. Nous avons le plaisir de vous proposer notre assurance individuelle contre les accidents corporels, spécialement conçue pour vous protéger, vous et votre famille, des conséquences financières d'un accident.\n\nCette assurance couvre les frais médicaux, les indemnités en cas d'incapacité temporaire ou permanente, ainsi qu'un capital en cas de décès. Elle vous offre une tranquillité d'esprit, sachant que vous et vos proches êtes protégés en toutes circonstances.\n\nNous vous invitons à nous contacter pour en savoir plus sur les garanties et les modalités de souscription. Nous sommes à votre disposition pour répondre à toutes vos questions et vous accompagner dans le choix des options les plus adaptées à votre situation.\n\nCordialement,\nVotre conseiller en assurance"
    }
  ],
  stats: {
    total_recommendations: 7,
    accepted_count: 2,
    refused_count: 3,
    pending_count: 2,
    avg_score: 84.3,
    branch_distribution: {
      'Assurance Santé': 1,
      'Assurance Vie': 1,
      
  
      '4/IARD': 1
    },
    score_distribution: {
      '0-20': 0,
      '21-40': 0,
      '41-60': 0,
      '61-80': 1,
      '81-100': 6
    },
    timeline_data: [
      { date: '2025-08-16', count: 5 },
      { date: '2025-08-17', count: 2 }
    ]
  }
};

// Custom Tooltip with modern design
const CustomTooltip = ({ active, payload, label, darkMode }) => {
  if (active && payload && payload.length) {
    return (
      <div className={`${darkMode ? 'bg-gray-800 border-gray-700' : 'bg-white border-gray-200'} p-4 shadow-xl rounded-xl border backdrop-blur-sm`}>
        <p className={`font-bold ${darkMode ? 'text-gray-100' : 'text-gray-900'}`}>{label}</p>
        <div className="mt-2">
          {payload.map((entry, index) => (
            <div key={index} className="flex items-center">
              <div className="w-3 h-3 rounded-full mr-2" style={{ backgroundColor: entry.color }}></div>
              <p className={`text-sm ${darkMode ? 'text-gray-300' : 'text-gray-600'}`}>
                {entry.name}: <span className="font-semibold">{entry.value}</span>
              </p>
            </div>
          ))}
        </div>
      </div>
    );
  }
  return null;
};

// Customized label for pie chart
const renderCustomizedLabel = ({ cx, cy, midAngle, innerRadius, outerRadius, percent, index,darkMode }) => {
  const RADIAN = Math.PI / 180;
  const radius = outerRadius + 20; // Position labels outside the pie
  const x = cx + radius * Math.cos(-midAngle * RADIAN);
  const y = cy + radius * Math.sin(-midAngle * RADIAN);

  return (
    <text
      x={x}
      y={y}
      fill={darkMode ? '#f1f5f9' : '#1e293b'} // Dynamic color based on dark mode
      textAnchor={x > cx ? 'start' : 'end'} // Align text based on position
      dominantBaseline="central"
      className="text-sm font-semibold" // Slightly larger and bolder text
      style={{
        backgroundColor: darkMode ? 'rgba(30, 41, 59, 0.7)' : 'rgba(241, 245, 249, 0.7)', // Semi-transparent background
        padding: '2px 6px',
        borderRadius: '4px',
      }}
    >
      {`${(percent * 100).toFixed(0)}%`}
    </text>
  );
};

// Modern Recommendation Modal
const RecommendationModal = ({ recommendation, isOpen, onClose, darkMode }) => {
  if (!isOpen) return null;
  
  return (
    <div className="fixed inset-0 backdrop-blur-md bg-black/30 flex items-center justify-center z-50 p-4">
      <div className={`${darkMode ? 'bg-gray-800' : 'bg-white'} rounded-2xl shadow-2xl max-w-4xl w-full max-h-[90vh] overflow-y-auto transform transition-all duration-300 scale-95 animate-scaleIn`}>
        <div className="p-8">
          <div className="flex justify-between items-start mb-8">
            <div>
              <h2 className={`text-3xl font-bold ${darkMode ? 'text-gray-100' : 'text-gray-900'} mb-2`}>{recommendation.produit_recommande}</h2>
              <div className="flex items-center space-x-3">
                <span className={`px-3 py-1 text-sm font-bold rounded-full ${
                  recommendation.score_value >= 80 ? 'bg-green-100 text-green-800' : 
                  recommendation.score_value >= 60 ? 'bg-yellow-100 text-yellow-800' : 
                  'bg-red-100 text-red-800'
                }`}>
                  Score: {recommendation.score_pertinence}
                </span>
                <span className="px-3 py-1 bg-indigo-100 text-indigo-800 text-sm font-bold rounded-full">
                  {recommendation.branche}
                </span>
              </div>
            </div>
            <button 
              onClick={onClose}
              className={`p-2 rounded-full ${darkMode ? 'bg-gray-700 text-gray-300 hover:bg-gray-600' : 'bg-gray-100 text-gray-500 hover:bg-gray-200'} transition-colors`}
            >
              <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
          
          <div className="mb-8">
            <h3 className={`text-xl font-bold mb-4 flex items-center ${darkMode ? 'text-gray-100' : 'text-gray-900'}`}>
              <div className={`w-8 h-8 rounded-lg flex items-center justify-center mr-3 ${darkMode ? 'bg-indigo-900/30' : 'bg-indigo-100'}`}>
                <svg className={`w-5 h-5 ${darkMode ? 'text-indigo-400' : 'text-indigo-600'}`} fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z"></path>
                </svg>
              </div>
              Raisonnement
            </h3>
            <div className={`${darkMode ? 'bg-gray-700/50 border-gray-600' : 'bg-gray-50 border-gray-200'} p-6 rounded-2xl border backdrop-blur-sm`}>
              <p className={`leading-relaxed ${darkMode ? 'text-gray-300' : 'text-gray-700'}`}>{recommendation.raisonnement}</p>
            </div>
          </div>
          
          <div className="mb-8">
            <h3 className={`text-xl font-bold mb-4 flex items-center ${darkMode ? 'text-gray-100' : 'text-gray-900'}`}>
              <div className={`w-8 h-8 rounded-lg flex items-center justify-center mr-3 ${darkMode ? 'bg-indigo-900/30' : 'bg-indigo-100'}`}>
                <svg className={`w-5 h-5 ${darkMode ? 'text-indigo-400' : 'text-indigo-600'}`} fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z"></path>
                </svg>
              </div>
              Argumentaire de vente
            </h3>
            <div className={`${darkMode ? 'bg-indigo-900/20 border-indigo-700' : 'bg-indigo-50 border-indigo-100'} p-6 rounded-2xl border backdrop-blur-sm`}>
              <p className={`leading-relaxed ${darkMode ? 'text-gray-300' : 'text-gray-700'} whitespace-pre-line`}>{recommendation.pitch}</p>
            </div>
          </div>
          
          <div className="flex justify-end space-x-3">
            <button
              onClick={onClose}
              className={`px-6 py-3 rounded-xl font-medium transition-all ${
                darkMode 
                  ? 'bg-gray-700 text-gray-200 hover:bg-gray-600' 
                  : 'bg-gray-100 text-gray-800 hover:bg-gray-200'
              }`}
            >
              Fermer
            </button>
            <button
              className={`px-6 py-3 rounded-xl font-medium text-white transition-all ${
                darkMode ? 'bg-indigo-600 hover:bg-indigo-500' : 'bg-indigo-600 hover:bg-indigo-700'
              }`}
            >
              Exporter
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

function Client() {
  const [clientId, setClientId] = useState('1381');
  const [dashboard, setDashboard] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [selectedRecommendation, setSelectedRecommendation] = useState(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [darkMode, setdarkMode] = useState(false);
  const [new_recommendations, setNewRecommendations] = useState([]);
  const [menuOpen, setMenuOpen] = useState(false);

  const handleNewRecommendation = async () => {
  setLoading(true); // tu peux afficher un spinner
  
  try {
    //const res = await fetch("http://localhost:5000/api/recommendations");
    const data = staticData.recommendations[0];
    
    // suppose que l’API retourne une seule recommandation
    setSelectedRecommendation(data);
    setIsModalOpen(true); // ouvre le modal
  } catch (error) {
    console.error("Erreur recommandation:", error);
  } finally {
    setLoading(false);
  }
};

  // Initialize dark mode
  useEffect(() => {
    const isDark = localStorage.getItem('darkMode') === 'true' || 
                  (!localStorage.getItem('darkMode') && window.matchMedia('(prefers-color-scheme: dark)').matches);
    setdarkMode(isDark);
  }, []);
  
  // Update dark mode
  useEffect(() => {
    localStorage.setItem('darkMode', darkMode);
    if (darkMode) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  }, [darkMode]);

  const toggledarkMode = () => {
    setdarkMode(!darkMode);
  };

  useEffect(() => {
    setLoading(true);
    setTimeout(() => {
      setDashboard(staticData);
      setLoading(false);
    }, 800);
  }, [clientId]);

  const handleSubmit = (e) => {
    e.preventDefault();
    setLoading(true);
    setTimeout(() => {
      setDashboard(staticData);
      setLoading(false);
    }, 800);
  };

  const openRecommendationModal = (recommendation) => {
    setSelectedRecommendation(recommendation);
    setIsModalOpen(true);
  };

  const closeRecommendationModal = () => {
    setIsModalOpen(false);
    setSelectedRecommendation(null);
  };

  if (loading) return (
    <div className={`flex justify-center items-center h-screen ${darkMode ? 'bg-gray-900' : 'bg-gray-50'}`}>
      <div className="flex flex-col items-center">
        <div className="relative">
          <div className="w-16 h-16 rounded-full border-4 border-indigo-200"></div>
          <div className="w-16 h-16 rounded-full border-4 border-indigo-600 border-t-transparent animate-spin absolute top-0 left-0"></div>
        </div>
        <p className={`mt-6 text-lg font-medium ${darkMode ? 'text-gray-300' : 'text-gray-600'}`}>Chargement des données client...</p>
      </div>
    </div>
  );
  
  if (error) return (
    <div className={`flex justify-center items-center h-screen ${darkMode ? 'bg-gray-900' : 'bg-gray-50'}`}>
      <div className={`${darkMode ? 'bg-gray-800' : 'bg-white'} p-8 rounded-2xl shadow-xl max-w-md w-full`}>
        <div className="flex items-center justify-center w-16 h-16 rounded-full bg-red-100 text-red-600 mx-auto mb-6">
          <svg className="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3,1.732 3z" />
          </svg>
        </div>
        <h3 className={`text-xl font-bold text-center mb-2 ${darkMode ? 'text-gray-100' : 'text-gray-900'}`}>Erreur de chargement</h3>
        <p className={`text-center mb-6 ${darkMode ? 'text-gray-400' : 'text-gray-500'}`}>{error}</p>
        <button 
          onClick={() => setError(null)}
          className={`w-full py-3 px-4 rounded-xl font-medium transition-colors ${
            darkMode 
              ? 'bg-indigo-600 text-white hover:bg-indigo-500' 
              : 'bg-indigo-600 text-white hover:bg-indigo-700'
          }`}
        >
          Réessayer
        </button>
      </div>
    </div>
  );
  
  if (!dashboard) return (
    <div className={`flex justify-center items-center h-screen ${darkMode ? 'bg-gray-900' : 'bg-gray-50'}`}>
      <div className="text-center max-w-md">
        <div className={`w-24 h-24 rounded-2xl flex items-center justify-center mx-auto mb-6 ${darkMode ? 'bg-gray-800' : 'bg-white'}`}>
          <svg className={`w-12 h-12 ${darkMode ? 'text-gray-600' : 'text-gray-400'}`} fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        </div>
        <h3 className={`text-2xl font-bold mb-2 ${darkMode ? 'text-gray-100' : 'text-gray-900'}`}>Aucune donnée client</h3>
        <p className={`mb-6 ${darkMode ? 'text-gray-400' : 'text-gray-500'}`}>Veuillez rechercher un ID client pour commencer.</p>
        <button 
          onClick={() => setClientId('1381')}
          className={`px-6 py-3 rounded-xl font-medium transition-colors ${
            darkMode 
              ? 'bg-indigo-600 text-white hover:bg-indigo-500' 
              : 'bg-indigo-600 text-white hover:bg-indigo-700'
          }`}
        >
          Charger exemple
        </button>
        
      </div>
    </div>
  );

  // Safely destructure with default values
  const { 
    recommendations = [], 
    stats = {}, 
    client_name = '', 
    client_details = {} 
  } = dashboard;

  // Safely get stats with defaults
  const {
    total_recommendations = 0,
    accepted_count = 0,
    refused_count = 0,
    pending_count = 0,
    branch_distribution = {},
    score_distribution = {},
    timeline_data = []
  } = stats;

  // Prepare chart data with fallbacks
  const branchData = Object.entries(branch_distribution).map(([name, value]) => ({ name, value }));
  const scoreData = Object.entries(score_distribution).map(([name, value]) => ({ name, value }));
  const chartColors = darkMode ? DARK_COLORS : COLORS;
// Prepare data for the new status chart (showing actual counts)
// Prepare data for the radial bar chart


  return (
    <div className={`min-h-screen transition-colors duration-300 ${darkMode ? 'bg-gradient-to-br from-slate-800 to-gray-900' : 'bg-gradient-to-br from-teal-50 to-gray-100'}`}>
      {/* Modern Header */}
      
      
      <main className="max-w-7xl mx-auto px-4 py-8 sm:px-6 lg:px-8" >
        {/* Main Content Container */}
        
        <div className={`${darkMode ? 'bg-gray-800' : 'bg-white'} rounded-2xl shadow-lg p-6 mb-8 border ${darkMode ? 'border-gray-700' : 'border-gray-200'} transition-all duration-300 hover:shadow-xl`}>
          <header className={`${darkMode ? 'bg-gray-800' : 'bg-white'}   p-6 mb-2  ${darkMode ? 'border-gray-700' : 'border-gray-200'} transition-all duration-300 `}>
        <div className="max-w-7xl mx-auto px-4 py-4 sm:px-6 lg:px-8 flex flex-col sm:flex-row justify-between items-start sm:items-center space-y-4 sm:space-y-0">
          <div className="flex items-center space-x-4">
            <div className={`w-10 h-10 rounded-xl flex items-center justify-center ${darkMode ? 'bg-indigo-900/30' : 'bg-indigo-100'}`}>
              <svg className={`w-6 h-6 ${darkMode ? 'text-indigo-400' : 'text-indigo-600'}`} fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path>
              </svg>
            </div>
            <div>
              <h1 className={`text-2xl font-bold ${darkMode ? 'text-gray-100' : 'text-gray-900'}`}>Tableau de Bord Client</h1>
              <p className={`text-sm ${darkMode ? 'text-gray-400' : 'text-gray-500'}`}>Recommandations intelligentes</p>
            </div>
          </div>
          <div className="flex items-center space-x-4 w-full sm:w-auto">
            {/* Modern Dark mode toggle */}
            <button
              onClick={toggledarkMode}
              className={`p-2 rounded-xl ${darkMode ? 'bg-gray-700 text-yellow-300' : 'bg-gray-200 text-gray-700'} focus:outline-none transition-colors`}
              aria-label="Toggle dark mode"
            >
              {darkMode ? (
                <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
                  <path fillRule="evenodd" d="M10 2a1 1 0 011 1v1a1 1 0 11-2 0V3a1 1 0 011-1zm4 8a4 4 0 11-8 0 4 4 0 018 0zm-.464 4.95l.707.707a1 1 0 001.414-1.414l-.707-.707a1 1 0 00-1.414 1.414zm2.12-10.607a1 1 0 010 1.414l-.706.707a1 1 0 11-1.414-1.414l.707-.707a1 1 0 011.414 0zM17 11a1 1 0 100-2h-1a1 1 0 100 2h1zm-7 4a1 1 0 011 1v1a1 1 0 11-2 0v-1a1 1 0 011-1zM5.05 6.464A1 1 0 106.465 5.05l-.708-.707a1 1 0 00-1.414 1.414l.707.707zm1.414 8.486l-.707.707a1 1 0 01-1.414-1.414l.707-.707a1 1 0 011.414 1.414zM4 11a1 1 0 100-2H3a1 1 0 000 2h1z" clipRule="evenodd"></path>
                </svg>
              ) : (
                <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
                  <path d="M17.293 13.293A8 8 0 016.707 2.707a8.001 8.001 0 1010.586 10.586z"></path>
                </svg>
              )}
            </button>
            
            <form onSubmit={handleSubmit} className="flex w-full sm:w-auto">
              <div className="relative flex-grow">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <svg className={`h-5 w-5 ${darkMode ? 'text-gray-400' : 'text-gray-400'}`} fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                  </svg>
                </div>
                <input
                  type="text"
                  value={clientId}
                  onChange={(e) => setClientId(e.target.value)}
                  placeholder="ID client"
                  className={`pl-10 pr-4 py-3 w-full rounded-l-xl outline-none 
                    border ${darkMode ? "border-gray-600 bg-gray-700 text-gray-100 placeholder-gray-400" : "border-gray-500 bg-white text-gray-900 placeholder-gray-500"} 
                    focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500`}

                />
              </div>
              <button
                type="submit"
                className={`px-6 py-3 rounded-r-xl font-medium focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 transition-colors whitespace-nowrap ${
                  darkMode 
                    ? 'bg-indigo-600 text-white hover:bg-indigo-500' 
                    : 'bg-indigo-600 text-white hover:bg-indigo-700'
                }`}
              >
                Rechercher
              </button>
            </form>
          </div>
        </div>
        </header>
          
          {/* Modern Client info card */}
          <div className={`${darkMode ? 'bg-gray-700' : 'bg-gray-50'} rounded-2xl p-6 mb-6 transition-all duration-300`}>
            <div className="flex flex-col md:flex-row items-start md:items-center justify-between">
              <div className="flex items-center space-x-5 mb-6 md:mb-0">
                <div className={`relative ${darkMode ? 'bg-indigo-200/30' : 'bg-indigo-100'} w-20 h-20 rounded-2xl flex items-center justify-center`}>
                  <span className={`text-2xl font-bold  ${darkMode ? 'text-indigo-100' : 'text-indigo-700'}`}>
                    {client_name ? client_name.charAt(0) : clientId.charAt(0)}
                  </span>
                  <div className="absolute -bottom-1 -right-1 w-6 h-6 rounded-full bg-green-500 border-2 border-white flex items-center justify-center">
                    <svg className="w-3 h-3 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                    </svg>
                  </div>
                </div>
                <div>
                  <h2 className={`text-2xl font-bold ${darkMode ? 'text-gray-100' : 'text-gray-900'}`}>{client_name || `Client ${clientId}`}</h2>
                  <p className={`text-sm ${darkMode ? 'text-gray-400' : 'text-gray-500'}`}>ID: {clientId}</p>
                </div>
              </div>
              <div className="grid grid-cols-3 gap-6 text-md w-full md:w-auto">
                {client_details && (
                  <>
                    <div className="text-center">
                      <p className={`text-sm font-medium ${darkMode ? 'text-gray-400' : 'text-gray-500'}`}>Âge</p>
                      <p className={`text-lg font-bold ${darkMode ? 'text-gray-100' : 'text-gray-900'}`}>{client_details.age || '-'}</p>
                    </div>
                    <div className="text-center">
                      <p className={`text-sm font-medium ${darkMode ? 'text-gray-400' : 'text-gray-500'}`}>Profession</p>
                      <p className={`text-lg font-bold ${darkMode ? 'text-gray-100' : 'text-gray-900'}`}>{client_details.profession || '-'}</p>
                    </div>
                    <div className="text-center">
                      <p className={`text-sm font-medium ${darkMode ? 'text-gray-400' : 'text-gray-500'}`}>Statut</p>
                      <p className={`text-lg font-bold ${darkMode ? 'text-gray-100' : 'text-gray-900'}`}>{client_details.marital_status || '-'}</p>
                    </div>
                  </>
                )}
              </div>
              <div className='flex items-center space-x-4 mt-4 md:mt-0'>
                <button
                  onClick={handleNewRecommendation}
                  className={`p-2 h-12 flex items-center gap-3 cursor-pointer rounded-2xl ${darkMode ? 'bg-green-400 text-gray-50 hover:bg-green-300' : 'bg-blue-200 text-gray-700 hover:bg-blue-300'} focus:outline-none focus:ring-2 focus:ring-blue-500 transition-colors`}
                >
                  <IoAddCircleOutline className='h-6 w-6'/>
                  New Recommandation
                </button>
                
              </div>
            </div>
          </div>
          
          {/* Modern Stats cards */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-6">
            <div className={`${darkMode ? 'bg-gradient-to-br from-indigo-900/30 to-indigo-800/30 border-indigo-700/50' : 'bg-gradient-to-br from-indigo-50 to-blue-50 border-indigo-100'} rounded-2xl shadow-lg p-6 border transition-all duration-300 hover:shadow-xl hover:scale-[1.02]`}>
              <div className="flex items-center justify-between">
                <div>
                  <h3 className={`text-sm font-medium ${darkMode ? 'text-indigo-300' : 'text-indigo-700'}`}>Total Recommandations</h3>
                  <p className={`text-3xl font-bold mt-2 ${darkMode ? 'text-white' : 'text-indigo-900'}`}>{total_recommendations}</p>
                </div>
                <div className={`w-12 h-12 rounded-xl flex items-center justify-center ${darkMode ? 'bg-indigo-800/50' : 'bg-indigo-100'}`}>
                  <svg className={`w-6 h-6 ${darkMode ? 'text-indigo-300' : 'text-indigo-600'}`} fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                  </svg>
                </div>
              </div>
              <div className="mt-4 flex items-center">
                <svg className="w-4 h-4 text-green-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 15l7-7 7 7" />
                </svg>
                <span className={`text-sm ml-1 ${darkMode ? 'text-green-400' : 'text-green-600'}`}>+12% cette semaine</span>
              </div>
            </div>
            
            <div className={`${darkMode ? 'bg-gradient-to-br from-green-900/30 to-emerald-800/30 border-green-700/50' : 'bg-gradient-to-br from-green-100 to-emerald-200 border-green-100'} rounded-2xl shadow-lg p-6 border transition-all duration-300 hover:shadow-xl hover:scale-[1.02]`}>
              <div className="flex items-center justify-between">
                <div>
                  <h3 className={`text-sm font-medium ${darkMode ? 'text-green-300' : 'text-green-700'}`}>Acceptées</h3>
                  <p className={`text-3xl font-bold mt-2 ${darkMode ? 'text-white' : 'text-green-900'}`}>{accepted_count}</p>
                </div>
                <div className={`w-12 h-12 rounded-xl flex items-center justify-center ${darkMode ? 'bg-green-800/50' : 'bg-green-100'}`}>
                  <svg className={`w-6 h-6 ${darkMode ? 'text-green-300' : 'text-green-600'}`} fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                  </svg>
                </div>
              </div>
              <div className="mt-4">
                <span className={`text-sm ${darkMode ? 'text-gray-400' : 'text-gray-500'}`}>Taux de conversion</span>
              </div>
            </div>
            
            <div className={`${darkMode ? 'bg-gradient-to-br  from-purple-900/30 to-violet-800/30 border-purple-700/50' : 'bg-gradient-to-br from-purple-100 to-purple-200 border-purple-100'} rounded-2xl shadow-lg p-6 border transition-all duration-300 hover:shadow-xl hover:scale-[1.02]`}>
              <div className="flex items-center justify-between">
                <div>
                  <h3 className={`text-sm font-medium ${darkMode ? 'text-purple-300' : 'text-purple-700'}`}>Refusées</h3>
                  <p className={`text-3xl font-bold mt-2 ${darkMode ? 'text-white' : 'text-purple-900'}`}>{refused_count}</p>
                </div>
                <div className={`w-12 h-12 rounded-xl flex items-center justify-center ${darkMode ? 'bg-purple-800/50' : 'bg-ropurplese-100'}`}>
                  <svg className={`w-6 h-6 ${darkMode ? 'text-purple-300' : 'text-purple-600'}`} fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3,1.732 3z" />
                  </svg>
                </div>
              </div>
              <div className="mt-4">
                <span className={`text-sm ${darkMode ? 'text-gray-400' : 'text-gray-500'}`}>À revoir</span>
              </div>
            </div>
            
            <div className={`${darkMode ? 'bg-gradient-to-br from-gray-500/30 to-gray-400/30 border-gray-300/50' : 'bg-gradient-to-br from-gray-50 to-gray-50 border-gray-100'} rounded-2xl shadow-lg p-6 border transition-all duration-300 hover:shadow-xl hover:scale-[1.02]`}>
              <div className="flex items-center justify-between">
                <div>
                  <h3 className={`text-sm font-medium ${darkMode ? 'text-gray-300' : 'text-gray-700'}`}>En cours</h3>
                  <p className={`text-3xl font-bold mt-2 ${darkMode ? 'text-white' : 'text-gray-900'}`}>{pending_count}</p>
                </div>
                <div className={`w-12 h-12 rounded-xl flex items-center justify-center ${darkMode ? 'bg-gray-800/50' : 'bg-gray-100'}`}>
                  <svg className={`w-6 h-6 ${darkMode ? 'text-gray-300' : 'text-gray-600'}`} fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
              </div>
              <div className="mt-4">
                <span className={`text-sm ${darkMode ? 'text-gray-400' : 'text-gray-500'}`}>Revenus générés</span>
              </div>
            </div>
          </div>
          
          {/* Charts Container */}
          <div className={`${darkMode ? 'bg-gray-800' : 'bg-gray-50'} rounded-2xl p-6 mb-6 transition-all duration-300`}>
            <div className="flex items-center justify-between mb-6">
              <h3 className={`text-lg font-bold ${darkMode ? 'text-gray-100' : 'text-gray-900'}`}>Analyse des Recommandations</h3>
              <div className={`px-3 py-1 rounded-full text-xs font-medium ${darkMode ? 'bg-gray-700 text-gray-300' : 'bg-gray-200 text-gray-700'}`}>
                Dernière mise à jour: {new Date().toLocaleDateString('fr-FR')}
              </div>
            </div>
            
            <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
              {/* Left column: Pie chart */}
              <div className="lg:col-span-2 flex flex-col gap-6">
                <div className={`${darkMode ? 'bg-gray-700/50' : 'bg-white'} rounded-2xl p-3 flex-1 border ${darkMode ? 'border-gray-700' : 'border-gray-200'} shadow-sm`}>
                  <div className="flex items-center justify-between mb-4">
                    <h3 className={`text-lg font-bold flex items-center ${darkMode ? 'text-gray-100' : 'text-gray-900'}`}>
                      <div className={`w-6 h-6 rounded-lg flex items-center justify-center mr-2 ${darkMode ? 'bg-indigo-900/30' : 'bg-indigo-100'}`}>
                        <svg className={`w-4 h-4 ${darkMode ? 'text-indigo-400' : 'text-indigo-600'}`} fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 3.055A9.001 9.001 0 1020.945 13H11V3.055z"></path>
                        </svg>
                      </div>
                      Répartition par Branche
                    </h3>
                    <div className={`px-2 py-1 rounded-full text-xs font-medium ${darkMode ? 'bg-gray-700 text-gray-300' : 'bg-gray-200 text-gray-700'}`}>
                      {branchData.length} catégories
                    </div>
                  </div>
                  <div className="h-64">
                    {branchData.length > 0 ? (
                      <ResponsiveContainer width="100%" height="100%">
                        <PieChart>
                          <Pie
                            data={branchData}
                            cx="50%"
                            cy="50%"
                            innerRadius={50}
                            outerRadius={90}
                            paddingAngle={2}
                            dataKey="value"
                            label={renderCustomizedLabel}
                          >
                            {branchData.map((entry, index) => (
                              <Cell key={`cell-${index}`} fill={chartColors[index % chartColors.length]} />
                            ))}
                          </Pie>
                          <Tooltip content={<CustomTooltip darkMode={darkMode} />} />
                          <Legend 
                                  layout="horizontal" 
                                  verticalAlign="bottom" 
                                  align="center"
                                  wrapperStyle={{
                                    paddingTop: '20px',
                                    display: 'flex',
                                    flexWrap: 'wrap',
                                    justifyContent: 'center',
                                    maxWidth: '100%', // Ensure it respects the chart's width
                                    gap: '10px', // Add spacing between wrapped items
                                  }}
                                  formatter={(value) => (
                                    <span className={`text-sm ${darkMode ? 'text-gray-300' : 'text-gray-600'}`} style={{ display: 'inline-block', minWidth: '100px', textAlign: 'center' }}>
                                      {value}
                                    </span>
                                  )}
                                />
                        </PieChart>
                      </ResponsiveContainer>
                    ) : (
                      <div className="flex flex-col items-center justify-center h-full">
                        <div className={`w-16 h-16 rounded-full flex items-center justify-center mb-4 ${darkMode ? 'bg-gray-700' : 'bg-gray-200'}`}>
                          <svg className={`w-8 h-8 ${darkMode ? 'text-gray-500' : 'text-gray-400'}`} fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                          </svg>
                        </div>
                        <p className={darkMode ? 'text-gray-400' : 'text-gray-500'}>Aucune donnée disponible</p>
                      </div>
                    )}
                  </div>
                </div>
                {/* New chart for Acceptance/Refusal percentages - Radial Bar Chart */}
                  <div className={`${darkMode ? 'bg-gray-700/50' : 'bg-white'} rounded-2xl p-5 border ${darkMode ? 'border-gray-700' : 'border-gray-200'} shadow-sm`}>
                    <div className="flex items-center justify-between mb-4">
                      <h3 className={`text-lg font-bold flex items-center ${darkMode ? 'text-gray-100' : 'text-gray-900'}`}>
                        <div className={`w-6 h-6 rounded-lg flex items-center justify-center mr-2 ${darkMode ? 'bg-indigo-900/30' : 'bg-indigo-100'}`}>
                          <svg className={`w-4 h-4 ${darkMode ? 'text-indigo-400' : 'text-indigo-600'}`} fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path>
                          </svg>
                        </div>
                        Taux d'Acceptation, Refus et En Cours
                      </h3>
                    </div>
                    
                    <div className="h-64 flex flex-col justify-center">
                      {accepted_count > 0 || refused_count > 0 || pending_count > 0 ? (
                        <div className="space-y-5">
                          {/* Acceptation Rate */}
                          <div className="flex items-center justify-between">
                            <div className="flex items-center">
                              <div className={`w-3 h-3 rounded-full mr-3 ${darkMode ? 'bg-green-400' : 'bg-green-500'}`}></div>
                              <span className={`text-base font-medium ${darkMode ? 'text-gray-200' : 'text-gray-700'}`}>Acceptées</span>
                            </div>
                            <div className="flex items-center">
                              <span className={`text-xl font-bold mr-2 ${darkMode ? 'text-green-400' : 'text-green-600'}`}>
                                {Math.round((accepted_count / (accepted_count + refused_count + pending_count)) * 100)}%
                              </span>
                              <svg className={`w-5 h-5 ${darkMode ? 'text-green-400' : 'text-green-600'}`} fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 15l7-7 7 7"></path>
                              </svg>
                            </div>
                          </div>
                          
                          {/* Refusal Rate */}
                          <div className="flex items-center justify-between">
                            <div className="flex items-center">
                              <div className={`w-3 h-3 rounded-full mr-3 ${darkMode ? 'bg-purple-400' : 'bg-purple-500'}`}></div>
                              <span className={`text-base font-medium ${darkMode ? 'text-gray-200' : 'text-gray-700'}`}>Refusées</span>
                            </div>
                            <div className="flex items-center">
                              <span className={`text-xl font-bold mr-2 ${darkMode ? 'text-red-400' : 'text-purple-600'}`}>
                                {Math.round((refused_count / (accepted_count + refused_count + pending_count)) * 100)}%
                              </span>
                              <svg className={`w-5 h-5 ${darkMode ? 'text-purple-400' : 'text-purple-600'}`} fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7"></path>
                              </svg>
                            </div>
                          </div>
                          
                          {/* Pending Rate */}
                          <div className="flex items-center justify-between">
                            <div className="flex items-center">
                              <div className={`w-3 h-3 rounded-full mr-3 ${darkMode ? 'bg-gray-400' : 'bg-gray-500'}`}></div>
                              <span className={`text-base font-medium ${darkMode ? 'text-gray-200' : 'text-gray-700'}`}>En cours</span>
                            </div>
                            <div className="flex items-center">
                              <span className={`text-xl font-bold mr-2 ${darkMode ? 'text-gray-400' : 'text-gray-600'}`}>
                                {Math.round((pending_count / (accepted_count + refused_count + pending_count)) * 100)}%
                              </span>
                              <svg className={`w-5 h-5 ${darkMode ? 'text-gray-400' : 'text-gray-600'}`} fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path>
                              </svg>
                            </div>
                          </div>
                          
                          {/* Visual divider */}
                          <div className={`my-3 border-t ${darkMode ? 'border-gray-600' : 'border-gray-200'}`}></div>
                          
                          {/* Total count */}
                          <div className="flex justify-between text-sm">
                            <span className={`${darkMode ? 'text-gray-400' : 'text-gray-500'}`}>Total</span>
                            <span className={`font-medium ${darkMode ? 'text-gray-300' : 'text-gray-700'}`}>
                              {accepted_count + refused_count + pending_count} demandes
                            </span>
                          </div>
                        </div>
                      ) : (
                        <div className="flex flex-col items-center justify-center h-full">
                          <div className={`w-16 h-16 rounded-full flex items-center justify-center mb-4 ${darkMode ? 'bg-gray-700' : 'bg-gray-200'}`}>
                            <svg className={`w-8 h-8 ${darkMode ? 'text-gray-500' : 'text-gray-400'}`} fill="none" viewBox="0 0 24 24" stroke="currentColor">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                            </svg>
                          </div>
                          <p className={darkMode ? 'text-gray-400' : 'text-gray-500'}>Aucune donnée disponible</p>
                        </div>
                      )}
                    </div>
                  </div>
              </div>
              
              {/* Right column: Bar and Line charts */}
              <div className="lg:col-span-2 flex flex-col gap-6">
                {/* Bar chart */}
                <div className={`${darkMode ? 'bg-gray-700/50' : 'bg-white'} rounded-2xl p-5 flex-1 border ${darkMode ? 'border-gray-700' : 'border-gray-200'} shadow-sm`}>
                  <div className="flex items-center justify-between mb-4">
                    <h3 className={`text-lg font-bold flex items-center ${darkMode ? 'text-gray-100' : 'text-gray-900'}`}>
                      <div className={`w-6 h-6 rounded-lg flex items-center justify-center mr-2 ${darkMode ? 'bg-indigo-900/30' : 'bg-indigo-100'}`}>
                        <svg className={`w-4 h-4 ${darkMode ? 'text-indigo-400' : 'text-indigo-600'}`} fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path>
                        </svg>
                      </div>
                      Scores de Pertinence
                    </h3>
                    <div className={`px-2 py-1 rounded-full text-xs font-medium ${darkMode ? 'bg-gray-700 text-gray-300' : 'bg-gray-200 text-gray-700'}`}>
                      {scoreData.length} niveaux
                    </div>
                  </div>
                  <div className="h-64">
                    {scoreData.length > 0 ? (
                      <ResponsiveContainer width="100%" height="100%">
                        <BarChart data={scoreData} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
                          <CartesianGrid strokeDasharray="3 3" stroke={darkMode ? "#374151" : "#f0f0f0"} vertical={false} />
                          <XAxis dataKey="name" tick={{ fontSize: 12, fill: darkMode ? '#9CA3AF' : '#6B7280' }} />
                          <YAxis tick={{ fontSize: 12, fill: darkMode ? '#9CA3AF' : '#6B7280' }} />
                          <Tooltip content={<CustomTooltip darkMode={darkMode} />} />
                          <Bar 
                            dataKey="value" 
                            name="Recommandations" 
                            radius={[6, 6, 0, 0]}
                          >
                            {scoreData.map((entry, index) => (
                              <Cell key={`cell-${index}`} fill={chartColors[index % chartColors.length]} />
                            ))}
                          </Bar>
                        </BarChart>
                      </ResponsiveContainer>
                    ) : (
                      <div className="flex flex-col items-center justify-center h-full">
                        <div className={`w-16 h-16 rounded-full flex items-center justify-center mb-4 ${darkMode ? 'bg-gray-700' : 'bg-gray-200'}`}>
                          <svg className={`w-8 h-8 ${darkMode ? 'text-gray-500' : 'text-gray-400'}`} fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                          </svg>
                        </div>
                        <p className={darkMode ? 'text-gray-400' : 'text-gray-500'}>Aucune donnée disponible</p>
                      </div>
                    )}
                  </div>
                </div>
                
                {/* Line chart */}
                <div className={`${darkMode ? 'bg-gray-700/50' : 'bg-white'} rounded-2xl p-5 flex-1 border ${darkMode ? 'border-gray-700' : 'border-gray-200'} shadow-sm`}>
                  <div className="flex items-center justify-between mb-4">
                    <h3 className={`text-lg font-bold flex items-center ${darkMode ? 'text-gray-100' : 'text-gray-900'}`}>
                      <div className={`w-6 h-6 rounded-lg flex items-center justify-center mr-2 ${darkMode ? 'bg-indigo-900/30' : 'bg-indigo-100'}`}>
                        <svg className={`w-4 h-4 ${darkMode ? 'text-indigo-400' : 'text-indigo-600'}`} fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
                        </svg>
                      </div>
                      Chronologie des Recommandations
                    </h3>
                    <div className={`px-2 py-1 rounded-full text-xs font-medium ${darkMode ? 'bg-gray-700 text-gray-300' : 'bg-gray-200 text-gray-700'}`}>
                      {timeline_data.length} jours
                    </div>
                  </div>
                  <div className="h-64">
                    {timeline_data.length > 0 ? (
                      <ResponsiveContainer width="100%" height="100%">
                        <LineChart data={timeline_data} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
                          <CartesianGrid strokeDasharray="3 3" stroke={darkMode ? "#374151" : "#f0f0f0"} vertical={false} />
                          <XAxis dataKey="date" tick={{ fontSize: 12, fill: darkMode ? '#9CA3AF' : '#6B7280' }} />
                          <YAxis tick={{ fontSize: 12, fill: darkMode ? '#9CA3AF' : '#6B7280' }} />
                          <Tooltip content={<CustomTooltip darkMode={darkMode} />} />
                          <Line 
                            type="monotone" 
                            dataKey="count" 
                            name="Recommandations" 
                            stroke={darkMode ? "#818CF8" : "#6366F1"} 
                            strokeWidth={3} 
                            dot={{ r: 6, fill: darkMode ? "#818CF8" : "#6366F1", strokeWidth: 2, stroke: darkMode ? "#1F2937" : "#fff" }}
                            activeDot={{ r: 8, fill: darkMode ? "#818CF8" : "#6366F1", strokeWidth: 0 }}
                          />
                        </LineChart>
                      </ResponsiveContainer>
                    ) : (
                      <div className="flex flex-col items-center justify-center h-full">
                        <div className={`w-16 h-16 rounded-full flex items-center justify-center mb-4 ${darkMode ? 'bg-gray-700' : 'bg-gray-200'}`}>
                          <svg className={`w-8 h-8 ${darkMode ? 'text-gray-500' : 'text-gray-400'}`} fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                          </svg>
                        </div>
                        <p className={darkMode ? 'text-gray-400' : 'text-gray-500'}>Aucune donnée disponible</p>
                      </div>
                    )}
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          {/* Modern Recommendations table */}
          <div className={`${darkMode ? 'bg-gray-750' : 'bg-gray-50'} rounded-2xl p-6 transition-all duration-300`}>
            <div className={`${darkMode ? 'bg-gray-700/50' : 'bg-white'} rounded-2xl shadow-lg overflow-hidden border ${darkMode ? 'border-gray-700' : 'border-gray-200'} transition-all duration-300 hover:shadow-xl`}>
              <div className={`px-6 py-5 ${darkMode ? 'bg-gray-750' : 'bg-gray-50'} border-b ${darkMode ? 'border-gray-700' : 'border-gray-200'}`}>
                <div className="flex items-center justify-between">
                  <h3 className={`text-lg font-bold flex items-center ${darkMode ? 'text-gray-100' : 'text-gray-900'}`}>
                    <div className={`w-8 h-8 rounded-lg flex items-center justify-center mr-3 ${darkMode ? 'bg-indigo-900/30' : 'bg-indigo-100'}`}>
                      <svg className={`w-5 h-5 ${darkMode ? 'text-indigo-400' : 'text-indigo-600'}`} fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 10h16M4 14h16M4 18h16"></path>
                      </svg>
                    </div>
                    Détails des Recommandations
                  </h3>
                  <div className={`px-3 py-1 rounded-full text-xs font-medium ${darkMode ? 'bg-gray-700/50 text-gray-300' : 'bg-gray-200 text-gray-700'}`}>
                    {recommendations.length} recommandations
                  </div>
                </div>
              </div>
              <div className="overflow-x-auto">
                <table className="min-w-full divide-y divide-gray-200">
                  <thead className={darkMode ? 'bg-gray-700/50' : 'bg-gray-50'}>
                    <tr>
                      <th scope="col" className={`px-6 py-3 text-left text-xs font-bold uppercase tracking-wider ${darkMode ? 'text-gray-400' : 'text-gray-500'}`}>Produit</th>
                      <th scope="col" className={`px-6 py-3 text-left text-xs font-bold uppercase tracking-wider ${darkMode ? 'text-gray-400' : 'text-gray-500'}`}>Branche</th>
                      <th scope="col" className={`px-6 py-3 text-left text-xs font-bold uppercase tracking-wider ${darkMode ? 'text-gray-400' : 'text-gray-500'}`}>Score</th>
                      <th scope="col" className={`px-6 py-3 text-left text-xs font-bold uppercase tracking-wider ${darkMode ? 'text-gray-400' : 'text-gray-500'}`}>Date</th>
                      <th scope="col" className={`px-6 py-3 text-left text-xs font-bold uppercase tracking-wider ${darkMode ? 'text-gray-400' : 'text-gray-500'}`}>Statut</th>
                      <th scope="col" className={`px-6 py-3 text-left text-xs font-bold uppercase tracking-wider ${darkMode ? 'text-gray-400' : 'text-gray-500'}`}>Actions</th>
                    </tr>
                  </thead>
                  <tbody className={`divide-y ${darkMode ? 'divide-gray-700 bg-gray-700/80' : 'divide-gray-200 bg-white'}`}>
                    {recommendations.map((rec) => (
                      <tr 
                        key={rec.id} 
                        className={`transition-colors duration-150 ${darkMode ? 'hover:bg-gray-800' : 'hover:bg-gray-50'}`}
                      >
                        <td className="px-6 py-4 whitespace-nowrap">
                          <div className={`text-sm font-bold ${darkMode ? 'text-gray-100' : 'text-gray-900'}`}>{rec.produit_recommande}</div>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap">
                          <div className={`text-sm ${darkMode ? 'text-gray-300' : 'text-gray-500'}`}>{rec.branche}</div>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap">
                          <div className="text-sm">
                            <span className={`px-3 py-1 inline-flex text-xs leading-5 font-bold rounded-full ${
                              rec.score_value >= 80 ? 'bg-green-100 text-green-800' : 
                              rec.score_value >= 60 ? 'bg-yellow-100 text-yellow-800' : 
                              'bg-red-100 text-red-800'
                            }`}>
                              {rec.score_pertinence}
                            </span>
                          </div>
                        </td>
                        <td className={`px-6 py-4 whitespace-nowrap text-sm ${darkMode ? 'text-gray-300' : 'text-gray-500'}`}>
                          {new Date(rec.created_at).toLocaleDateString('fr-FR')}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap">
                          <span className={`px-3 py-1 inline-flex text-xs leading-5 font-bold rounded-full ${
                            rec.status === 'Accepté' ? 'bg-green-300 text-green-800' : 
                            rec.status === 'Refusé' ? 'bg-purple-400 text-purple-50' : 
                            
                            rec.status === 'En cours' ? 'bg-gray-200 text-gray-500' :
                            'bg-gray-100 text-gray-800'
                          }`}>
                            {rec.status || 'En attente'}
                          </span>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                          <button
                            onClick={() => openRecommendationModal(rec)}
                            className={`inline-flex items-center px-3 py-1.5 rounded-lg text-xs font-medium transition-colors ${
                              darkMode 
                                ? 'bg-indigo-900/30 text-indigo-300 hover:bg-indigo-800' 
                                : 'bg-indigo-100 text-indigo-700 hover:bg-indigo-200'
                            }`}
                          >
                            Voir détails
                            <svg className="ml-1 w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                            </svg>
                          </button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>
      </main>
      
      {/* Modern Modal */}
      <RecommendationModal 
        recommendation={selectedRecommendation}
        isOpen={isModalOpen}
        onClose={closeRecommendationModal}
        darkMode={darkMode}
      />
    </div>
  );
}

export default Client;