// src/App.js
import React, { useState, useEffect } from 'react';
import { BarChart, Bar, PieChart, Pie, Cell, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import './App.css';

// Palette de couleurs mise à jour pour correspondre au style du tableau de bord
const COLORS = [
  "#1C398E",  // Bleu Profond (Couleur principale de la marque)
  "#9F0712",  // Rouge Profond (Couleur secondaire de la marque)
  "#62748E",  // Bleu Acier
  "#2C3E50",  // Bleu Gris Foncé
  "#34495E",  // Bleu Gris
  "#516A8B",  // Bleu Adouci
  "#BDC3C7",  // Gris Argenté Clair
  "#ECF0F1",  // Gris Très Clair
  "#8E44AD",  // Violet Royal (pour les points forts/accents)
  "#16A085",  // Turquoise (équilibre frais avec les rouges/bleus)
  "#27AE60",  // Vert Émeraude (métriques de croissance/positives)
  "#F39C12",  // Ambre Chaud (avertissement/accent)
  "#E67E22",  // Orange Doux (point fort secondaire)
  "#D35400",  // Orange Profond (contraste fort)
  "#C0392B"   // Rouge Bourgogne (variante plus foncée)
];

// Données statiques basées sur votre document
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
      pitch: "Bonjour [Nom du client], En tant que chauffeur, vous êtes quotidiennement exposé à des risques liés à votre activité et à vos déplacements. À 63 ans, il est essentiel de protéger votre santé et celle de votre famille. Nous vous recommandons notre assurance santé adaptée aux déplacements fréquents, qui vous offre une couverture complète en cas d'accident ou de problème de santé, où que vous soyez. Cette assurance inclut des prestations médicales étendues, une prise en charge rapide, et des garanties adaptées à votre rythme de vie. Protégez-vous et votre famille dès aujourd'hui en souscrivant à cette solution sur mesure. N'hésitez pas à nous contacter pour plus d'informations ou pour finaliser votre souscription. Cordialement, Votre conseiller en assurance."
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
      pitch: "Bonjour Monsieur Personne_00002, En tant que chauffeur professionnel, votre métier vous expose quotidiennement à des risques liés à vos déplacements. À 63 ans, il est également essentiel de vous protéger contre les imprévus de santé. Notre assurance santé est spécialement conçue pour les personnes actives comme vous, offrant une couverture complète même en déplacement, des consultations médicales à l'hospitalisation. Avec des garanties adaptées à votre rythme de vie, vous pourrez conduire l'esprit tranquille, sachant que vous et votre famille êtes protégés. N'attendez pas pour sécuriser votre avenir et celui de vos proches. Contactez-nous dès aujourd'hui pour en savoir plus !"
    },
    {
      id: '68a1a7b36e02d805ed273494',
      client_ref: '1381',
      produit_recommande: 'assurance groupe maladie',
      branche: 'santé',
      score_pertinence: '70/100',
      score_value: 70,
      created_at: '2025-08-17T11:58:11.498Z',
      status: "Acheté",
      raisonnement: "Le client est un chauffeur de 63 ans, marié, travaillant dans le secteur des services personnels. Il possède actuellement un contrat automobile et a eu dans le passé des contrats d'assurance décès temporaire. Les opportunités détectées indiquent un manque de couverture santé et vie. Étant donné son âge et sa profession, il est crucial de lui proposer une assurance santé pour couvrir les risques médicaux et une assurance vie pour protéger sa famille en cas de décès ou invalidité. Le produit 'assurance groupe maladie' est pertinent pour la couverture santé, bien que l'âge maximal ciblé soit de 60 ans, ce qui pourrait nécessiter une adaptation. L'assurance vie pourrait être complétée par un produit adapté aux personnes de plus de 60 ans.",
      pitch: "Bonjour Monsieur Personne_00002, En tant que chauffeur professionnel, votre métier expose à des risques spécifiques, et il est essentiel de vous protéger ainsi que votre famille. Nous vous recommandons notre assurance groupe maladie, qui couvre les frais de santé, le décès et l'invalidité. Bien que l'âge cible maximal soit de 60 ans, nous pouvons adapter cette offre pour répondre à vos besoins. Cette assurance vous apportera une tranquillité d'esprit, notamment pour vos déplacements fréquents. N'hésitez pas à nous contacter pour personnaliser cette solution avec vous. Cordialement, Votre conseiller en assurance."
    },
    {
      id: '68a1ae8ca0882520a1464818',
      client_ref: '1381',
      produit_recommande: 'assurance individuelle contre les accidents corporels',
      branche: '4/IARD',
      score_pertinence: '80/100',
      score_value: 80,
      created_at: '2025-08-17T12:27:24.597Z',
      status: "Acheté",
      raisonnement: "Le client, un chauffeur de 63 ans, marié, travaillant dans les services personnels, a un historique de contrats automobiles et temporaire décès. Il ne dispose actuellement que d'un contrat automobile résilié et non payé. Les opportunités détectées comprennent l'absence d'assurance santé et d'assurance vie. Compte tenu de son âge et de sa profession, une assurance santé serait pertinente pour couvrir les risques liés à son activité professionnelle, tandis qu'une assurance vie pourrait garantir sa famille en cas de décès ou d'invalidité. Parmi les produits proposés, l'assurance individuelle contre les accidents corporels (IARD) est adaptée à son profil, ainsi que le contrat 'Rahma' (assurance vie) qui propose des garanties en cas de décès ou invalidité.",
      pitch: "Objet : Offre d'assurance adaptée à votre profil professionnel et personnel\n\nCher Monsieur Personne_00002,\n\nEn tant que chauffeur professionnel, vous êtes exposé quotidiennement à des risques d'accidents corporels, que ce soit sur la route ou dans le cadre de votre activité. Nous avons le plaisir de vous proposer notre assurance individuelle contre les accidents corporels, spécialement conçue pour vous protéger, vous et votre famille, des conséquences financières d'un accident.\n\nCette assurance couvre les frais médicaux, les indemnités en cas d'incapacité temporaire ou permanente, ainsi qu'un capital en cas de décès. Elle vous offre une tranquillité d'esprit, sachant que vous et vos proches êtes protégés en toutes circonstances.\n\nNous vous invitons à nous contacter pour en savoir plus sur les garanties et les modalités de souscription. Nous sommes à votre disposition pour répondre à toutes vos questions et vous accompagner dans le choix des options les plus adaptées à votre situation.\n\nCordialement,\nVotre conseiller en assurance"
    }
  ],
  stats: {
    total_recommendations: 7,
    accepted_count: 2,
    refused_count: 3,
    purchased_count: 2,
    avg_score: 84.3,
    branch_distribution: {
      'Assurance Santé': 1,
      'Assurance Vie': 1,
      'Santé': 3,
      'santé': 1,
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

// Info-bulle personnalisée pour les graphiques
const CustomTooltip = ({ active, payload, label }) => {
  if (active && payload && payload.length) {
    return (
      <div className="bg-white p-3 shadow-md rounded-md border border-gray-200">
        <p className="font-semibold text-gray-800">{label}</p>
        <p className="text-sm text-gray-600">
          {payload[0].name}: <span className="font-medium">{payload[0].value}</span>
        </p>
      </div>
    );
  }
  return null;
};

// Étiquette personnalisée pour le graphique circulaire
const renderCustomizedLabel = ({ cx, cy, midAngle, innerRadius, outerRadius, percent, index }) => {
  const RADIAN = Math.PI / 180;
  const radius = innerRadius + (outerRadius - innerRadius) * 0.5;
  const x = cx + radius * Math.cos(-midAngle * RADIAN);
  const y = cy + radius * Math.sin(-midAngle * RADIAN);
  return (
    <text x={x} y={y} fill="white" textAnchor={x > cx ? 'start' : 'end'} dominantBaseline="central" className="text-xs font-semibold">
      {`${(percent * 100).toFixed(0)}%`}
    </text>
  );
};

// Composant Modal pour les détails de recommandation
const RecommendationModal = ({ recommendation, isOpen, onClose }) => {
  if (!isOpen) return null;
  return (
    <div className="fixed inset-0 backdrop-blur-sm bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-xl shadow-2xl max-w-4xl w-full max-h-[90vh] overflow-y-auto">
        <div className="p-6">
          <div className="flex justify-between items-start mb-6">
            <h2 className="text-2xl font-bold text-gray-800">{recommendation.produit_recommande}</h2>
            <button 
              onClick={onClose}
              className="text-gray-400 hover:text-gray-600 focus:outline-none transition-colors"
            >
              <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
          
          <div className="flex flex-wrap items-center mb-6 gap-2">
            <span className={`px-3 py-1 text-sm font-semibold rounded-full ${
              recommendation.score_value >= 80 ? 'bg-green-100 text-green-800' : 
              recommendation.score_value >= 60 ? 'bg-yellow-100 text-yellow-800' : 
              'bg-red-100 text-red-800'
            }`}>
              Score: {recommendation.score_pertinence}
            </span>
            <span className="px-3 py-1 bg-blue-100 text-blue-800 text-sm font-semibold rounded-full">
              {recommendation.branche}
            </span>
            <span className="text-sm text-gray-500">
              {new Date(recommendation.created_at).toLocaleDateString('fr-FR')}
            </span>
          </div>
          
          <div className="mb-6">
            <h3 className="text-lg font-semibold text-gray-800 mb-3 flex items-center">
              <svg className="w-5 h-5 mr-2 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z"></path>
              </svg>
              Raisonnement
            </h3>
            <div className="bg-gray-50 p-4 rounded-lg border border-gray-200">
              <p className="text-gray-700">{recommendation.raisonnement}</p>
            </div>
          </div>
          
          <div className="mb-6">
            <h3 className="text-lg font-semibold text-gray-800 mb-3 flex items-center">
              <svg className="w-5 h-5 mr-2 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z"></path>
              </svg>
              Argumentaire de vente
            </h3>
            <div className="bg-blue-50 p-4 rounded-lg border border-blue-100">
              <p className="text-gray-700 whitespace-pre-line">{recommendation.pitch}</p>
            </div>
          </div>
          
          <div className="flex justify-end mt-6">
            <button
              onClick={onClose}
              className="px-4 py-2 bg-gray-200 text-gray-800 rounded-lg hover:bg-gray-300 focus:outline-none focus:ring-2 focus:ring-gray-400 transition-colors"
            >
              Fermer
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

  useEffect(() => {
    // Simuler un appel API avec des données statiques
    setLoading(true);
    setTimeout(() => {
      setDashboard(staticData);
      setLoading(false);
    }, 800);
  }, [clientId]);

  const handleSubmit = (e) => {
    e.preventDefault();
    // Dans une vraie application, cela récupérerait les données pour le nouvel ID client
    // Pour la démo, nous utiliserons simplement les mêmes données
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
    <div className="flex justify-center items-center h-screen bg-gray-50">
      <div className="flex flex-col items-center">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-600"></div>
        <p className="mt-4 text-gray-600">Chargement des données client...</p>
      </div>
    </div>
  );
  
  if (error) return (
    <div className="flex justify-center items-center h-screen bg-gray-50">
      <div className="bg-white p-6 rounded-xl shadow-md max-w-md w-full">
        <div className="flex items-center justify-center h-12 w-12 rounded-md bg-red-100 text-red-600 mx-auto">
          <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
          </svg>
        </div>
        <h3 className="mt-4 text-lg font-medium text-gray-900 text-center">Erreur de chargement des données</h3>
        <p className="mt-2 text-sm text-gray-500 text-center">{error}</p>
        <button 
          onClick={() => setError(null)}
          className="mt-4 w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
        >
          Réessayer
        </button>
      </div>
    </div>
  );
  
  if (!dashboard) return (
    <div className="flex justify-center items-center h-screen bg-gray-50">
      <div className="text-center">
        <svg className="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        <h3 className="mt-2 text-lg font-medium text-gray-900">Aucune donnée client</h3>
        <p className="mt-1 text-sm text-gray-500">Veuillez rechercher un ID client pour commencer.</p>
      </div>
    </div>
  );

  const { recommendations, stats, client_name, client_details } = dashboard;

  // Préparer les données pour les graphiques
  const branchData = Object.entries(stats.branch_distribution).map(([name, value]) => ({ name, value }));
  const scoreData = Object.entries(stats.score_distribution).map(([name, value]) => ({ name, value }));

  return (
    <div className="min-h-screen bg-gray-50">
      {/* En-tête */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 py-4 sm:px-6 lg:px-8 flex flex-col sm:flex-row justify-between items-start sm:items-center space-y-4 sm:space-y-0">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">Tableau de Bord des Recommandations Client</h1>
            <p className="text-sm text-gray-500 mt-1">Recommandations d'assurance alimentées par l'IA</p>
          </div>
          <div className="flex items-center space-x-4 w-full sm:w-auto">
            <form onSubmit={handleSubmit} className="flex w-full sm:w-auto">
              <div className="relative flex-grow">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <svg className="h-5 w-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                  </svg>
                </div>
                <input
                  type="text"
                  value={clientId}
                  onChange={(e) => setClientId(e.target.value)}
                  placeholder="Entrez l'ID client"
                  className="pl-10 pr-4 py-2 border border-gray-300 rounded-l-lg focus:outline-none focus:ring-2 focus:ring-blue-800 focus:border-transparent w-full"
                />
              </div>
              <button
                type="submit"
                className="bg-blue-800 text-white px-4 py-2 rounded-r-lg hover:bg-blue-900 focus:outline-none focus:ring-2 focus:ring-blue-800 focus:ring-offset-2 transition-colors whitespace-nowrap"
              >
                Rechercher
              </button>
            </form>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 py-6 sm:px-6 lg:px-8">
        {/* Carte d'informations client */}
        <div className="bg-white rounded-xl shadow-sm p-6 mb-8 border border-gray-200">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <div className="w-16 h-16 rounded-full bg-blue-900 flex items-center justify-center text-white font-bold text-2xl">
                {client_name ? client_name.charAt(0) : clientId.charAt(0)}
              </div>
              <div>
                <h2 className="text-xl font-semibold text-gray-900">{client_name || `Client ${clientId}`}</h2>
                <p className="text-sm text-gray-500">ID Client: {clientId}</p>
              </div>
            </div>
            <div className="hidden md:flex space-x-16 text-md">
              {client_details && (
                <>
                  <div>
                    <p className="text-gray-500">Âge</p>
                    <p className="font-medium text-gray-900">{client_details.age}</p>
                  </div>
                  <div>
                    <p className="text-gray-500">Profession</p>
                    <p className="font-medium text-gray-900">{client_details.profession}</p>
                  </div>
                  <div>
                    <p className="text-gray-500">Statut</p>
                    <p className="font-medium text-gray-900">{client_details.marital_status}</p>
                  </div>
                </>
              )}
            </div>
          </div>
        </div>

        {/* Cartes de statistiques */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <div className="bg-white rounded-xl shadow-sm px-4 py-6 border border-gray-200 hover:shadow-md transition-shadow">
            <div className="flex items-center">
              <div className="p-2 rounded-lg bg-blue-100">
                <svg className="h-6 w-6 text-slate-800" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                </svg>
              </div>
              <div className="ml-4">
                <h3 className="text-sm font-medium text-gray-700">Total des Recommandations</h3>
                <p className="text-2xl font-bold text-slate-800">{stats.total_recommendations}</p>
              </div>
            </div>
            <p className="text-xs text-gray-500 mt-3">+12% cette semaine</p>
          </div>
          
          <div className="bg-white rounded-xl shadow-sm p-6 border border-gray-200 hover:shadow-md transition-shadow">
            <div className="flex items-center">
              <div className="p-2 rounded-lg bg-blue-100">
                <svg className="h-6 w-6 text-blue-800" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                </svg>
              </div>
              <div className="ml-4">
                <h3 className="text-sm font-medium text-blue-800">Acceptées</h3>
                <p className="text-2xl font-bold text-blue-800">{stats.accepted_count}</p>
              </div>
            </div>
            <p className="text-xs text-gray-500 mt-3">Taux de conversion</p>
          </div>
          
          <div className="bg-white rounded-xl shadow-sm p-6 border border-gray-200 hover:shadow-md transition-shadow">
            <div className="flex items-center">
              <div className="p-2 rounded-lg bg-red-100">
                <svg className="h-6 w-6 text-red-800" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                </svg>
              </div>
              <div className="ml-4">
                <h3 className="text-sm font-medium text-red-800">Refusées</h3>
                <p className="text-2xl font-bold text-red-800">{stats.refused_count}</p>
              </div>
            </div>
            <p className="text-xs text-gray-500 mt-3">À revoir</p>
          </div>
          
          <div className="bg-white rounded-xl shadow-sm p-6 border border-gray-200 hover:shadow-md transition-shadow">
            <div className="flex items-center">
              <div className="p-2 rounded-lg bg-slate-100">
                <svg className="h-6 w-6 text-slate-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <div className="ml-4">
                <h3 className="text-sm font-medium text-slate-500">Achetées</h3>
                <p className="text-2xl font-bold text-slate-500">{stats.purchased_count}</p>
              </div>
            </div>
            <p className="text-xs text-gray-500 mt-3">Revenus générés</p>
          </div>
        </div>

        {/* Section des graphiques */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
          {/* Graphique circulaire de répartition par branche */}
          <div className="bg-white rounded-xl shadow-sm p-6 border border-gray-200">
            <h3 className="text-lg font-medium text-gray-800 mb-4 flex items-center">
              <svg className="w-5 h-5 mr-2 text-blue-900" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 3.055A9.001 9.001 0 1020.945 13H11V3.055z"></path>
              </svg>
              Répartition des Recommandations par Branche
            </h3>
            <div className="h-80">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={branchData}
                    cx="50%"
                    cy="50%"
                    labelLine={false}
                    outerRadius={80}
                    fill="#8884d8"
                    dataKey="value"
                    label={renderCustomizedLabel}
                  >
                    {branchData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip content={<CustomTooltip />} />
                  <Legend 
                    layout="vertical" 
                    verticalAlign="middle" 
                    align="right"
                    wrapperStyle={{ paddingLeft: '20px' }}
                    formatter={(value, entry, index) => (
                      <span className="text-sm text-gray-600">{value}</span>
                    )}
                  />
                </PieChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* Graphique à barres de distribution des scores */}
          <div className="bg-white rounded-xl shadow-sm p-6 border border-gray-200">
            <h3 className="text-lg font-medium text-gray-800 mb-4 flex items-center">
              <svg className="w-5 h-5 mr-2 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path>
              </svg>
              Distribution des Scores de Pertinence
            </h3>
            <div className="h-80">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={scoreData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#eee" />
                  <XAxis dataKey="name" tick={{ fontSize: 12 }} />
                  <YAxis tick={{ fontSize: 12 }} />
                  <Tooltip content={<CustomTooltip />} />
                  <Bar dataKey="value" name="Recommandations" fill="#1C398E" radius={[4, 4, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>
        </div>

        {/* Graphique chronologique */}
        <div className="bg-white rounded-xl shadow-sm p-6 mb-8 border border-gray-200">
          <h3 className="text-lg font-medium text-gray-800 mb-4 flex items-center">
            <svg className="w-5 h-5 mr-2 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
            </svg>
              Chronologie des Recommandations
          </h3>
          <div className="h-80">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={stats.timeline_data}>
                <CartesianGrid strokeDasharray="3 3" stroke="#eee" />
                <XAxis dataKey="date" tick={{ fontSize: 12 }} />
                <YAxis tick={{ fontSize: 12 }} />
                <Tooltip content={<CustomTooltip />} />
                <Line 
                  type="monotone" 
                  dataKey="count" 
                  name="Recommandations" 
                  stroke="#1C398E" 
                  strokeWidth={2} 
                  activeDot={{ r: 6, fill: '#3B82F6' }} 
                  dot={{ r: 3, fill: '#3B82F6' }}
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Tableau des recommandations */}
        <div className="bg-white rounded-xl shadow-sm overflow-hidden border border-gray-200">
          <div className="px-6 py-4 border-b border-gray-200 bg-gray-50">
            <h3 className="text-lg font-medium text-gray-800 flex items-center">
              <svg className="w-5 h-5 mr-2 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 10h16M4 14h16M4 18h16"></path>
              </svg>
              Détails des Recommandations
            </h3>
          </div>
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Produit</th>
                  <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Branche</th>
                  <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Score</th>
                  <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Date</th>
                  <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Statut</th>
                  <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {recommendations.map((rec) => (
                  <tr 
                    key={rec.id} 
                    className="hover:bg-gray-50 transition-colors duration-150"
                  >
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm font-medium text-gray-900">{rec.produit_recommande}</div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm text-gray-500">{rec.branche}</div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm text-gray-900">
                        <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${
                          rec.score_value >= 80 ? 'bg-green-100 text-green-800' : 
                          rec.score_value >= 60 ? 'bg-yellow-100 text-yellow-800' : 
                          'bg-red-100 text-red-800'
                        }`}>
                          {rec.score_pertinence}
                        </span>
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {new Date(rec.created_at).toLocaleDateString('fr-FR')}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${
                        rec.status === 'Accepté' ? 'bg-green-100 text-green-800' : 
                        rec.status === 'Refusé' ? 'bg-red-100 text-red-800' : 
                        rec.status === 'Acheté' ? 'bg-blue-100 text-blue-800' :
                        'bg-gray-100 text-gray-800'
                      }`}>
                        {rec.status || 'En attente'}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                      <button
                        onClick={() => openRecommendationModal(rec)}
                        className="text-slate-700 hover:text-blue-600 cursor-pointer focus:outline-none"
                      >
                        Voir les détails
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </main>

      {/* Modal des détails de recommandation */}
      <RecommendationModal 
        recommendation={selectedRecommendation}
        isOpen={isModalOpen}
        onClose={closeRecommendationModal}
      />
    </div>
  );
}

export default Client;