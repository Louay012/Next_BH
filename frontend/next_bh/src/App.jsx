import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Chatbot from './Chatbot.jsx'; // Adjust path if necessary
import './App.css'; // Keep for any global styles
import Dashboard from './Dashboard.jsx'; 
function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-100">
        {/* Routes */}
        <Routes>
          <Route path="/chatbot" element={<Chatbot />} />
          <Route path="/dashboard" element={<Dashboard />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;