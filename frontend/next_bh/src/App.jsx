import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Chatbot from './Chatbot.jsx'; // Adjust path if necessary
import './App.css'; // Keep for any global styles

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-100">
        {/* Define Routes */}
        <Routes>
          <Route path="/chatbot" element={<Chatbot />} />
          {/* Add more routes as needed, e.g., */}
          {/* <Route path="/dashboard" element={<Dashboard />} /> */}
          {/* <Route path="/clients" element={<ClientList />} /> */}
        </Routes>
      </div>
    </Router>
  );
}

export default App;