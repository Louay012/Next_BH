// src/components/AgentSinistre.jsx
import React, { useState, useEffect } from 'react';
import './AgentSinistre.css';

const AgentSinistre = () => {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [claims, setClaims] = useState([]);
  const [selectedClaim, setSelectedClaim] = useState(null);
  const [analysisResult, setAnalysisResult] = useState(null);
  const [emailContent, setEmailContent] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  // Simulation de données de sinistres
  useEffect(() => {
    const mockClaims = [
      {
        id: 1,
        clientName: "Dupont Martin",
        contractId: "CT-2023-789",
        type: "Dégât des eaux",
        date: "2023-10-15",
        status: "Nouveau",
        description: "Fuite d'eau dans la salle de bain, dégâts au plafond du salon",
        severity: "Moyen",
        contractType: "Habitation"
      },
      {
        id: 2,
        clientName: "Leroy Sophie",
        contractId: "CT-2023-456",
        type: "Collision",
        date: "2023-10-12",
        status: "En cours",
        description: "Accident avec un autre véhicule à un feu rouge",
        severity: "Élevé",
        contractType: "Automobile"
      }
    ];
    setClaims(mockClaims);
  }, []);

  const analyzeClaim = (claim) => {
    setIsLoading(true);
    setSelectedClaim(claim);
    
    setTimeout(() => {
      let result;
      
      if (claim.type === "Dégât des eaux") {
        result = {
          procedures: [
            "Couper l'arrivée d'eau si possible",
            "Prendre des photos des dégâts sous différents angles",
            "Contacter un plombier agréé pour réparer la fuite",
            "Faire établir un devis pour les réparations",
            "Remplir le formulaire de déclaration de sinistre en ligne"
          ],
          recommendations: "Dégât d'eau moyen nécessitant une intervention rapide pour éviter les moisissures.",
          deadline: "48 heures pour envoyer les documents",
          assignedAgent: "Jean Martin"
        };
      } else if (claim.type === "Collision") {
        result = {
          procedures: [
            "Remplir un constat amiable avec l'autre conducteur",
            "Prendre des photos des véhicules et de la scène",
            "Obtenir les coordonnées des témoins éventuels",
            "Consulter un médecin en cas de choc même léger",
            "Déclarer le sinistre via l'application mobile"
          ],
          recommendations: "Accident avec tiers, procédure standard à suivre.",
          deadline: "5 jours ouvrés pour la déclaration",
          assignedAgent: "Marie Lambert"
        };
      } else {
        result = {
          procedures: [
            "Prendre des photos du pare-brise endommagé",
            "Contacter un réparateur agréé pour un devis",
            "Transmettre le devis pour approbation",
            "Prendre rendez-vous pour la réparation"
          ],
          recommendations: "Bris de glace simple, réparation rapide possible.",
          deadline: "Sans urgence particulière",
          assignedAgent: "Thomas Dubois"
        };
      }
      
      setAnalysisResult(result);
      generateEmailContent(claim, result);
      setIsLoading(false);
      setActiveTab('analysis');
    }, 1500);
  };

  const generateEmailContent = (claim, analysis) => {
    const content = `
Bonjour ${claim.clientName},

Suite à votre déclaration de sinistre pour ${claim.type.toLowerCase()} survenu le ${claim.date}, nous avons analysé votre situation.

Procédures à suivre :
${analysis.procedures.map((proc, index) => `${index + 1}. ${proc}`).join('\n')}

Recommandation : ${analysis.recommendations}

Délai : ${analysis.deadline}

Votre gestionnaire de sinistre : ${analysis.assignedAgent}

Cordialement,
Votre équipe d'assurance
    `;
    setEmailContent(content);
  };

  const sendEmail = () => {
    setIsLoading(true);
    setTimeout(() => {
      alert(`Email envoyé à ${selectedClaim.clientName}`);
      setIsLoading(false);
    }, 1000);
  };

  return (
    <div className="agent-sinistre">
      <header className="agent-sinistre-header">
        <h1>Agent IA d'Analyse de Sinistres</h1>
        <nav className="tabs">
          <button 
            className={activeTab === 'dashboard' ? 'active' : ''} 
            onClick={() => setActiveTab('dashboard')}
          >
            Tableau de bord
          </button>
          <button 
            className={activeTab === 'analysis' ? 'active' : ''} 
            onClick={() => setActiveTab('analysis')}
            disabled={!selectedClaim}
          >
            Analyse
          </button>
        </nav>
      </header>

      <main className="agent-sinistre-main">
        {activeTab === 'dashboard' && (
          <div className="dashboard">
            <h2>Sinistres récents</h2>
            <div className="claims-list">
              {claims.map(claim => (
                <div 
                  key={claim.id} 
                  className={`claim-card ${claim.status.toLowerCase()}`}
                  onClick={() => analyzeClaim(claim)}
                >
                  <div className="claim-header">
                    <h3>{claim.type}</h3>
                    <span className={`status-badge ${claim.status.toLowerCase()}`}>
                      {claim.status}
                    </span>
                  </div>
                  <p className="client-name">{claim.clientName}</p>
                  <p className="contract-id">Contrat: {claim.contractId}</p>
                  <p className="claim-date">Date: {claim.date}</p>
                  <p className="claim-desc">{claim.description}</p>
                  <div className="claim-footer">
                    <span className={`severity severity-${claim.severity.toLowerCase()}`}>
                      {claim.severity}
                    </span>
                    <span className="contract-type">{claim.contractType}</span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {activeTab === 'analysis' && selectedClaim && (
          <div className="analysis">
            {isLoading ? (
              <div className="loading">Analyse en cours...</div>
            ) : (
              <>
                <div className="analysis-header">
                  <h2>Analyse du sinistre #{selectedClaim.id}</h2>
                  <button className="back-button" onClick={() => setActiveTab('dashboard')}>
                    Retour
                  </button>
                </div>
                
                <div className="claim-details">
                  <h3>Détails du sinistre</h3>
                  <p><strong>Client:</strong> {selectedClaim.clientName}</p>
                  <p><strong>Type:</strong> {selectedClaim.type}</p>
                  <p><strong>Date:</strong> {selectedClaim.date}</p>
                  <p><strong>Description:</strong> {selectedClaim.description}</p>
                </div>
                
                <div className="analysis-result">
                  <h3>Recommandations de l'IA</h3>
                  <div className="procedures">
                    <h4>Procédures à suivre:</h4>
                    <ol>
                      {analysisResult.procedures.map((procedure, index) => (
                        <li key={index}>{procedure}</li>
                      ))}
                    </ol>
                  </div>
                  
                  <div className="recommendation">
                    <h4>Recommandation:</h4>
                    <p>{analysisResult.recommendations}</p>
                  </div>
                  
                  <div className="deadline">
                    <h4>Délai:</h4>
                    <p>{analysisResult.deadline}</p>
                  </div>
                  
                  <div className="assigned-agent">
                    <h4>Gestionnaire assigné:</h4>
                    <p>{analysisResult.assignedAgent}</p>
                  </div>
                </div>
                
                <div className="email-section">
                  <h3>Email à envoyer au client</h3>
                  <textarea 
                    value={emailContent} 
                    onChange={(e) => setEmailContent(e.target.value)}
                    rows="10"
                  />
                  <button onClick={sendEmail} className="send-button">
                    Envoyer l'email
                  </button>
                </div>
              </>
            )}
          </div>
        )}
      </main>
    </div>
  );
};

export default AgentSinistre;