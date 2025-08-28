import React, { useState, useEffect, useRef } from 'react';
import { useParams } from 'react-router-dom';
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
  const { client_ref } = useParams();
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
      client_ref: client_ref || "9086",
      message: input,
      history: []
    };
    try {
      setIsLoading(true);
      await new Promise(resolve => setTimeout(resolve, 800));
      
      const response = await axios.post(
        `http://127.0.0.1:8000/chat`, 
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
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 w-full">
      {/* Modern Header */}
      <div className="font-sans">
        <div className="bg-gradient-to-r from-red-600 to-red-700 text-white text-sm py-3 px-6 flex flex-wrap justify-between items-center shadow-lg">
          <div className="flex flex-wrap gap-6 items-center">
            <span className="flex items-center gap-1"><FaMapMarkerAlt /> Immeuble BH Assurance, Centre Urbain Nord - Tunis</span>
            <span className="flex items-center gap-1"><FaEnvelope /> commercial@bh-assurance.com</span>
            <span className="flex items-center gap-1"><FaPhoneAlt /> +216 71 184 200</span>
          </div>
          <div className="flex gap-4 items-center text-lg">
            <FaFacebookF className="hover:text-blue-200 transition-colors cursor-pointer" />
            <FaLinkedinIn className="hover:text-blue-200 transition-colors cursor-pointer" />
            <FaYoutube className="hover:text-blue-200 transition-colors cursor-pointer" />
            <FaInstagram className="hover:text-blue-200 transition-colors cursor-pointer" />
          </div>
        </div>
        
        {/* Logo + Main Menu */}
        <div className="bg-white shadow-md">
          <div className="container mx-auto flex justify-between items-center px-6 py-3">
            <div className="flex items-center">
              <img src={bh_logo} alt="BH Assurance Logo" className="h-14" />
              <div className="ml-4 h-8 w-px bg-gray-300"></div>
              <nav className="flex gap-8 text-gray-800 font-medium ml-8">
                <button className="hover:text-red-600 transition-colors duration-200">Particuliers</button>
                <button className="hover:text-red-600 transition-colors duration-200">Professionnels & Entreprises</button>
                <button className="hover:text-red-600 transition-colors duration-200">BH Assurance</button>
              </nav>
            </div>
            <button className="bg-gradient-to-r from-red-600 to-red-700 hover:from-red-700 hover:to-red-800 transition-all duration-200 text-white px-6 py-3 rounded-lg font-semibold shadow-md">
              Mon espace Wininti
            </button>
          </div>
        </div>
        
        {/* Submenu */}
        <div className="bg-white border-t border-gray-200 shadow-sm">
          <div className="container mx-auto flex justify-between items-center px-6 py-3">
            <div className="flex gap-6 text-gray-700 text-sm">
              <button className="hover:text-red-600 transition-colors duration-200">À propos de nous</button>
              <button className="hover:text-red-600 transition-colors duration-200">Nos actualités</button>
              <button className="hover:text-red-600 transition-colors duration-200">Nos agences</button>
              <button className="hover:text-red-600 transition-colors duration-200">Assistance et sinistre</button>
              <button className="hover:text-red-600 transition-colors duration-200">FAQ</button>
              <button className="hover:text-red-600 transition-colors duration-200">Contact</button>
              <button className="text-blue-600 font-semibold hover:text-blue-700 transition-colors duration-200">Challenge NEXT</button>
            </div>
            <div className="flex items-center gap-2">
              <div className="relative">
                <input 
                  type="text" 
                  className="border border-gray-300 rounded-lg px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200" 
                  placeholder="Recherche..." 
                />
                <FaSearch className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400" />
              </div>
            </div>
          </div>
        </div>
      </div>
      
      {/* Main Content */}
      <main className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
        {/* Page Header */}
        <div className="text-center mb-12">
          <div className="inline-block bg-gradient-to-r from-blue-800 to-indigo-800 p-1 rounded-full mb-4">
            <div className="bg-white rounded-full px-6 py-1">
              <h1 className="text-3xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-blue-800 to-indigo-900">
                Assistant Virtuel BH Assurance
              </h1>
            </div>
          </div>
          <p className="text-lg text-blue-800 max-w-2xl mx-auto">
            Notre IA est disponible 24h/24 pour répondre à toutes vos questions et vous accompagner dans vos démarches
          </p>
        </div>
        
        {/* Chat Container */}
        <div className="bg-white rounded-2xl shadow-xl overflow-hidden border border-gray-100 transition-all duration-300 hover:shadow-2xl">
          {/* Chat Header */}
          <div className="bg-gradient-to-r from-blue-700 to-indigo-800 p-5 flex items-center">
            <div className="bg-white/20 backdrop-blur-sm rounded-full p-2 mr-4">
              <div className="bg-white rounded-full p-1.5">
                <svg className="h-7 w-7 text-blue-700" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
                </svg>
              </div>
            </div>
            <div>
              <h2 className="text-white text-xl font-semibold">Assistant IA</h2>
              <p className="text-blue-100 text-sm">En ligne et prêt à vous aider</p>
            </div>
            {isLoading && (
              <div className="ml-auto flex space-x-1">
                <div className="h-2.5 w-2.5 bg-white rounded-full animate-bounce" style={{animationDelay: '0ms'}}></div>
                <div className="h-2.5 w-2.5 bg-white rounded-full animate-bounce" style={{animationDelay: '150ms'}}></div>
                <div className="h-2.5 w-2.5 bg-white rounded-full animate-bounce" style={{animationDelay: '300ms'}}></div>
              </div>
            )}
          </div>
          
          {/* Chat Window */}
          <div className="h-96 overflow-y-auto p-6 bg-gradient-to-b from-gray-50 to-gray-100">
            <div className="space-y-6">
              {messages.map((msg, index) => (
                <div 
                  key={`${msg.timestamp}-${index}`}
                  className={`flex ${msg.sender === 'bot' ? 'justify-start' : 'justify-end'}`}
                >
                  <div 
                    className={`max-w-xs md:max-w-md rounded-2xl p-5 ${
                      msg.sender === 'bot' 
                        ? 'bg-white border border-gray-200 text-gray-800 rounded-bl-none shadow-md' 
                        : 'bg-gradient-to-r from-blue-600 to-indigo-700 text-white rounded-br-none shadow-lg'
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
                            strong: ({node, ...props}) => <strong className="font-semibold text-gray-900" {...props} />,
                            a: ({node, ...props}) => <a className="text-blue-600 hover:text-blue-800 hover:underline" {...props} />
                          }}
                        >
                          {msg.text}
                        </ReactMarkdown>
                      </div>
                    ) : (
                      <div className="text-sm">{msg.text}</div>
                    )}
                    <div className={`text-xs mt-3 ${
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
          <div className="border-t border-gray-200 p-5 bg-white">
            <div className="flex space-x-3">
              <input
                type="text"
                value={input}
                onChange={e => setInput(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Posez votre question..."
                className="flex-1 p-4 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 focus:outline-blue-500 transition-all duration-200 shadow-sm"
                disabled={isLoading}
              />
              <button
                onClick={sendMessage}
                disabled={!input.trim() || isLoading}
                className={`flex-shrink-0 p-4 rounded-xl transition-all duration-200 flex items-center justify-center shadow-md ${
                  isLoading || !input.trim() 
                    ? 'bg-gray-300 cursor-not-allowed' 
                    : 'bg-gradient-to-r from-blue-600 to-indigo-700 hover:from-blue-700 hover:to-indigo-800 text-white'
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
            <p className="text-xs text-gray-500 mt-3 text-center">
              BH Assurance protège vos données. Nos conversations sont sécurisées et confidentielles.
            </p>
          </div>
        </div>
        
        {/* Quick Actions */}
        <div className="mt-10 grid grid-cols-2 md:grid-cols-4 gap-5">
          {[
            {icon: '📋', title: 'Demande de devis', desc: 'Obtenez un devis personnalisé'},
            {icon: '🛡️', title: 'Déclarer sinistre', desc: 'Démarrez votre déclaration'},
            {icon: '📞', title: 'Contact urgent', desc: 'Assistance 24/7'},
            {icon: '❓', title: 'FAQ', desc: 'Questions fréquentes'}
          ].map((item, index) => (
            <button 
              key={index}
              className="bg-white p-5 rounded-xl shadow-md border border-gray-100 hover:border-blue-300 hover:shadow-lg transition-all duration-300 text-center group"
            >
              <div className="text-3xl mb-3 group-hover:scale-110 transition-transform duration-300">{item.icon}</div>
              <h3 className="font-semibold text-blue-900 group-hover:text-blue-700 transition-colors duration-200">{item.title}</h3>
              <p className="text-sm text-gray-600 mt-2 group-hover:text-gray-700 transition-colors duration-200">{item.desc}</p>
            </button>
          ))}
        </div>
      </main>
      
      {/* Footer */}
      <footer className="bg-gradient-to-r from-gray-800 to-gray-900 text-white py-10 mt-16">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            <div>
              <h3 className="text-xl font-bold mb-5 text-white">BH Assurance</h3>
              <ul className="space-y-3 text-gray-300">
                <li><a href="#" className="hover:text-white transition-colors duration-200">À propos</a></li>
                <li><a href="#" className="hover:text-white transition-colors duration-200">Actualités</a></li>
                <li><a href="#" className="hover:text-white transition-colors duration-200">Agences</a></li>
              </ul>
            </div>
            <div>
              <h3 className="text-xl font-bold mb-5 text-white">Services</h3>
              <ul className="space-y-3 text-gray-300">
                <li><a href="#" className="hover:text-white transition-colors duration-200">Assistance</a></li>
                <li><a href="#" className="hover:text-white transition-colors duration-200">FAQ</a></li>
                <li><a href="#" className="hover:text-white transition-colors duration-200">Contact</a></li>
              </ul>
            </div>
            <div>
              <h3 className="text-xl font-bold mb-5 text-white">Légal</h3>
              <ul className="space-y-3 text-gray-300">
                <li><a href="#" className="hover:text-white transition-colors duration-200">Mentions légales</a></li>
                <li><a href="#" className="hover:text-white transition-colors duration-200">Confidentialité</a></li>
                <li><a href="#" className="hover:text-white transition-colors duration-200">CGU</a></li>
              </ul>
            </div>
            <div>
              <h3 className="text-xl font-bold mb-5 text-white">Contact</h3>
              <p className="text-gray-300 mb-3 flex items-center"><FaPhoneAlt className="mr-2" /> 0800 123 456</p>
              <p className="text-gray-300 mb-5 flex items-center"><FaEnvelope className="mr-2" /> contact@bhassurance.com</p>
              <div className="flex space-x-4">
                <a href="#" className="bg-gray-700 hover:bg-gray-600 p-2 rounded-full transition-colors duration-200">
                  <span className="sr-only">Facebook</span>
                  <FaFacebookF className="h-5 w-5" />
                </a>
                <a href="#" className="bg-gray-700 hover:bg-gray-600 p-2 rounded-full transition-colors duration-200">
                  <span className="sr-only">Twitter</span>
                  <svg className="h-5 w-5" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M8.29 20.251c7.547 0 11.675-6.253 11.675-11.675 0-.178 0-.355-.012-.53A8.348 8.348 0 0022 5.92a8.19 8.19 0 01-2.357.646 4.118 4.118 0 001.804-2.27 8.224 8.224 0 01-2.605.996 4.107 4.107 0 00-6.993 3.743 11.65 11.65 0 01-8.457-4.287 4.106 4.106 0 001.27 5.477A4.072 4.072 0 002.8 9.713v.052a4.105 4.105 0 003.292 4.022 4.095 4.095 0 01-1.853.07 4.108 4.108 0 003.834 2.85A8.233 8.233 0 002 18.407a11.616 11.616 0 006.29 1.84" />
                  </svg>
                </a>
                <a href="#" className="bg-gray-700 hover:bg-gray-600 p-2 rounded-full transition-colors duration-200">
                  <span className="sr-only">LinkedIn</span>
                  <FaLinkedinIn className="h-5 w-5" />
                </a>
              </div>
            </div>
          </div>
          <div className="border-t border-gray-700 mt-10 pt-8 text-center text-gray-400">
            <p>© {new Date().getFullYear()} BH Assurance. Tous droits réservés.</p>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default Chatbot;