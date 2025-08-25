import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import bh_logo from './Images/bh_logo-removebg-preview.png';
import {
  FaFacebookF, FaLinkedinIn, FaYoutube, FaInstagram,
  FaMapMarkerAlt, FaEnvelope, FaPhoneAlt, FaSearch,
  FaClipboard, FaHeadset
} from "react-icons/fa";
import { LuSend } from "react-icons/lu";

const Chatbot = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  // Auto-scroll to bottom of chat
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth", block: "center" });
  }, [messages]);

  // Initial greeting
  useEffect(() => {
    setMessages([{
      sender: 'bot',
      text: 'Bonjour ! Je suis l\'assistant virtuel de BH Assurance. Comment puis-je vous aider aujourd\'hui ?',
      timestamp: new Date().toISOString()
    }]);
  }, []);

  // Send message
  const sendMessage = async () => {
    if (!input.trim() || isLoading) return;

    const userMessage = { 
      sender: 'user', 
      text: input,
      timestamp: new Date().toISOString()
    };
    setMessages(prev => [...prev, userMessage]);
    setInput('');

    const payload = {
      client_ref: "9086",  // ⚠️ tu peux le passer dynamiquement si besoin
      message: input,
      history: []
    };

    try {
      setIsLoading(true);
      // Simulate API call (replace with actual API endpoint)
      await new Promise(resolve => setTimeout(resolve, 800));
      
      const response = await axios.post(
        `http://127.0.0.1:5000/chat`, 
        payload,
        {
          headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
          }
        }
      );
      
      const botMessage = { 
        sender: 'bot', 
        text: response?.data?.response || "Je n'ai pas pu traiter votre demande. Veuillez réessayer.",
        timestamp: new Date().toISOString()
      };
      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      console.error('Error:', error);
      setMessages(prev => [...prev, { 
        sender: 'bot', 
        text: 'Désolé, une erreur s\'est produite. Essayez à nouveau.',
        timestamp: new Date().toISOString()
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      sendMessage();
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-blue-50 to-white w-full">
      {/* Modern Header */}
      <div className="font-sans">
        <div className="bg-red-600 text-white text-sm py-3 px-6 flex flex-wrap justify-between items-center">
          <div className="flex flex-wrap gap-6 items-center">
            <span className="flex items-center gap-1"><FaMapMarkerAlt /> Immeuble BH Assurance, Centre Urbain Nord - Tunis</span>
            <span className="flex items-center gap-1"><FaEnvelope /> commercial@bh-assurance.com</span>
            <span className="flex items-center gap-1"><FaPhoneAlt /> +216 71 184 200</span>
          </div>
          <div className="flex gap-4 items-center text-lg">
            <FaFacebookF />
            <FaLinkedinIn />
            <FaYoutube />
            <FaInstagram />
          </div>
        </div>

        {/* Logo + Main Menu */}
        <div className="bg-gray-100 shadow">
          <div className="container mx-auto flex justify-between items-center px-6 py-2">
            <img src={bh_logo} alt="BH Assurance Logo" className="h-12" />
            <nav className="flex gap-8 text-gray-800 font-medium">
              <button className="hover:text-red-600 transition">Particuliers</button>
              <button className="hover:text-red-600 transition">Professionnels & Entreprises</button>
              <button className="hover:text-red-600 transition">BH Assurance</button>
            </nav>
            <button className="bg-red-600 hover:bg-red-700 transition text-white px-5 py-2 rounded-lg font-semibold">Mon espace Wininti</button>
          </div>
        </div>

        {/* Submenu */}
        <div className="bg-white border-t border-gray-200 shadow-sm">
          <div className="container mx-auto flex justify-between items-center px-6 py-3">
            <div className="flex gap-6 text-gray-700 text-sm">
              <button className="hover:text-red-600">À propos de nous</button>
              <button className="hover:text-red-600">Nos actualités</button>
              <button className="hover:text-red-600">Nos agences</button>
              <button className="hover:text-red-600">Assistance et sinistre</button>
              <button className="hover:text-red-600">FAQ</button>
              <button className="hover:text-red-600">Contact</button>
              <button className="text-blue-600 font-semibold">Challenge NEXT</button>
            </div>
            <div className="flex items-center gap-2">
              <input type="text" className="border border-gray-300 rounded px-2 py-1 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500" placeholder="Recherche..." />
              <FaSearch className="text-gray-600" />
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <main className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Page Header */}
        <div className="text-center mb-10">
          <h1 className="text-3xl font-bold text-blue-900 mb-2">Assistant Virtuel BH Assurance</h1>
          <p className="text-blue-700">Notre IA est disponible 24h/24 pour répondre à vos questions</p>
        </div>

        {/* Chat Container */}
        <div className="bg-white rounded-xl shadow-lg overflow-hidden border border-gray-200">
          {/* Chat Header */}
          <div className="bg-gradient-to-r from-blue-800 to-blue-600 p-4 flex items-center">
            <div className="bg-white rounded-full p-1.5 mr-3">
              <svg className="h-6 w-6 text-blue-700" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
              </svg>
            </div>
            <h2 className="text-white text-lg font-semibold">Assistant IA</h2>
            {isLoading && (
              <div className="ml-auto flex space-x-1">
                <div className="h-2 w-2 bg-white rounded-full animate-bounce" style={{animationDelay: '0ms'}}></div>
                <div className="h-2 w-2 bg-white rounded-full animate-bounce" style={{animationDelay: '150ms'}}></div>
                <div className="h-2 w-2 bg-white rounded-full animate-bounce" style={{animationDelay: '300ms'}}></div>
              </div>
            )}
          </div>

          {/* Chat Window */}
          <div className="h-96 overflow-y-auto p-6 bg-gray-50">
            <div className="space-y-4">
              {messages.map((msg, index) => (
                <div 
                  key={`${msg.timestamp}-${index}`}
                  className={`flex ${msg.sender === 'bot' ? 'justify-start' : 'justify-end'}`}
                >
                  <div 
                    className={`max-w-xs md:max-w-md rounded-xl p-4 ${
                      msg.sender === 'bot' 
                        ? 'bg-blue-50 border border-blue-200 text-gray-800 rounded-bl-none shadow-sm' 
                        : 'bg-blue-600 text-white rounded-br-none shadow-md'
                    }`}
                  >
                    {msg.sender === 'bot' ? (
                      <div className="text-sm prose prose-sm max-w-none leading-relaxed">
                        <ReactMarkdown 
                          remarkPlugins={[remarkGfm]}
                          components={{
                            ul: ({node, ...props}) => <ul className="list-disc pl-5 mb-2" {...props} />,
                            ol: ({node, ...props}) => <ol className="list-decimal pl-5 mb-2" {...props} />,
                            li: ({node, ...props}) => <li className="mb-1" {...props} />,
                            p: ({node, ...props}) => <p className="mb-2" {...props} />,
                            strong: ({node, ...props}) => <strong className="font-semibold" {...props} />,
                            a: ({node, ...props}) => <a className="text-blue-600 hover:underline" {...props} />
                          }}
                        >
                          {msg.text}
                        </ReactMarkdown>
                      </div>
                    ) : (
                      <div className="text-sm">{msg.text}</div>
                    )}
                    <div className={`text-xs mt-2 ${
                      msg.sender === 'bot' ? 'text-gray-500' : 'text-blue-100'
                    }`}>
                      {new Date(msg.timestamp).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}
                    </div>
                  </div>
                </div>
              ))}
              <div ref={messagesEndRef} />
            </div>
          </div>

          {/* Input Area */}
          <div className="border-t border-gray-200 p-4 bg-white">
            <div className="flex space-x-3">
              <input
                type="text"
                value={input}
                onChange={e => setInput(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Posez votre question..."
                className="flex-1 p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 focus:outline-blue-500 transition-colors"
                disabled={isLoading}
              />
              <button
                onClick={sendMessage}
                disabled={!input.trim() || isLoading}
                className={`flex-shrink-0 p-3 rounded-lg transition-colors flex items-center justify-center ${
                  isLoading || !input.trim() 
                    ? 'bg-gray-300 cursor-not-allowed' 
                    : 'bg-blue-600 hover:bg-blue-700 text-white'
                }`}
              >
                {isLoading ? (
                  <svg className="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                ) : (
                  <LuSend className="h-5 w-5" />
                )}
              </button>
            </div>
            <p className="text-xs text-gray-500 mt-2 text-center">
              BH Assurance protège vos données. Nos conversations sont sécurisées.
            </p>
          </div>
        </div>

        {/* Quick Actions */}
        <div className="mt-8 grid grid-cols-2 md:grid-cols-4 gap-4">
          {[
            {icon: '📋', title: 'Demande de devis', desc: 'Obtenez un devis personnalisé'},
            {icon: '🛡️', title: 'Déclarer sinistre', desc: 'Démarrez votre déclaration'},
            {icon: '📞', title: 'Contact urgent', desc: 'Assistance 24/7'},
            {icon: '❓', title: 'FAQ', desc: 'Questions fréquentes'}
          ].map((item, index) => (
            <button 
              key={index}
              className="bg-white p-4 rounded-lg shadow-sm border border-gray-200 hover:border-blue-300 transition-colors text-center"
            >
              <div className="text-2xl mb-2">{item.icon}</div>
              <h3 className="font-medium text-blue-900">{item.title}</h3>
              <p className="text-xs text-gray-600 mt-1">{item.desc}</p>
            </button>
          ))}
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-gray-800 text-white py-8 mt-12">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            <div>
              <h3 className="text-lg font-semibold mb-4">BH Assurance</h3>
              <ul className="space-y-2 text-sm text-gray-300">
                <li><a href="#" className="hover:text-white">À propos</a></li>
                <li><a href="#" className="hover:text-white">Actualités</a></li>
                <li><a href="#" className="hover:text-white">Agences</a></li>
              </ul>
            </div>
            <div>
              <h3 className="text-lg font-semibold mb-4">Services</h3>
              <ul className="space-y-2 text-sm text-gray-300">
                <li><a href="#" className="hover:text-white">Assistance</a></li>
                <li><a href="#" className="hover:text-white">FAQ</a></li>
                <li><a href="#" className="hover:text-white">Contact</a></li>
              </ul>
            </div>
            <div>
              <h3 className="text-lg font-semibold mb-4">Légal</h3>
              <ul className="space-y-2 text-sm text-gray-300">
                <li><a href="#" className="hover:text-white">Mentions légales</a></li>
                <li><a href="#" className="hover:text-white">Confidentialité</a></li>
                <li><a href="#" className="hover:text-white">CGU</a></li>
              </ul>
            </div>
            <div>
              <h3 className="text-lg font-semibold mb-4">Contact</h3>
              <p className="text-sm text-gray-300 mb-2">0800 123 456</p>
              <p className="text-sm text-gray-300 mb-4">contact@bhassurance.com</p>
              <div className="flex space-x-4">
                <a href="#" className="text-gray-300 hover:text-white">
                  <span className="sr-only">Facebook</span>
                  <svg className="h-6 w-6" fill="currentColor" viewBox="0 0 24 24">
                    <path fillRule="evenodd" d="M22 12c0-5.523-4.477-10-10-10S2 6.477 2 12c0 4.991 3.657 9.128 8.438 9.878v-6.987h-2.54V12h2.54V9.797c0-2.506 1.492-3.89 3.777-3.89 1.094 0 2.238.195 2.238.195v2.46h-1.26c-1.243 0-1.63.771-1.63 1.562V12h2.773l-.443 2.89h-2.33v6.988C18.343 21.128 22 16.991 22 12z" clipRule="evenodd" />
                  </svg>
                </a>
                <a href="#" className="text-gray-300 hover:text-white">
                  <span className="sr-only">Twitter</span>
                  <svg className="h-6 w-6" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M8.29 20.251c7.547 0 11.675-6.253 11.675-11.675 0-.178 0-.355-.012-.53A8.348 8.348 0 0022 5.92a8.19 8.19 0 01-2.357.646 4.118 4.118 0 001.804-2.27 8.224 8.224 0 01-2.605.996 4.107 4.107 0 00-6.993 3.743 11.65 11.65 0 01-8.457-4.287 4.106 4.106 0 001.27 5.477A4.072 4.072 0 012.8 9.713v.052a4.105 4.105 0 003.292 4.022 4.095 4.095 0 01-1.853.07 4.108 4.108 0 003.834 2.85A8.233 8.233 0 012 18.407a11.616 11.616 0 006.29 1.84" />
                  </svg>
                </a>
              </div>
            </div>
          </div>
          <div className="border-t border-gray-700 mt-8 pt-8 text-center text-sm text-gray-400">
            <p>© {new Date().getFullYear()} BH Assurance. Tous droits réservés.</p>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default Chatbot;