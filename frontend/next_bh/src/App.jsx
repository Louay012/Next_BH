import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Chatbot from './Chatbot.jsx'; // Adjust path if necessary
import './App.css'; // Keep for any global styles
import Dashboard from './Dashboard.jsx'; 
import Client from './Client.jsx';
import ClientSinistres from './ClientsSinistres.jsx';
import AgentSinistre from './AgentSinistre.jsx';
import AssistantRecommandation from './AssistantRecommandation.jsx';
import NavbarSection from './NavbarSection.jsx';
import AcceptedRecommendations from './AcceptedRecommendations.jsx';
import PendingRecommendations from './PendingRecommendations.jsx';
import RefusedRecommendations from './RefusedRecommendations.jsx';

function App() {
  return (

    <Router>
      <div className="min-h-screen bg-gray-100 pt-8">
        {/* Navbar globale */}
      <NavbarSection  className="mb-5"/>
        {/* Routes */}
        <Routes>
          <Route path="/chatbot/:client_ref" element={<Chatbot />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/client" element={<Client />} />
          <Route path="/sinistres" element={<ClientSinistres/>} />
          <Route path="/agentsinistre" element={<AgentSinistre />} /> 
          <Route path="/assistant" element={<AssistantRecommandation />} />
          <Route path="/list_accepted" element={<AcceptedRecommendations />} />
          <Route path="/list_pending" element={<PendingRecommendations />} />
          <Route path="/list_refused" element={<RefusedRecommendations />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;