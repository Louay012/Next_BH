// --- NavbarSection.jsx ---
import { Link } from "react-router-dom";

function NavbarSection({ darkMode, toggleDarkMode }) {
  return (
    <nav
      className={`mb-10  fixed top-0 left-0 w-full
        flex justify-between items-center px-6 py-3 rounded-2xl z-50
        backdrop-blur-xl shadow-2xl border border-white/20
        transition-all duration-500 
        
        ${darkMode ? "bg-slate-900/70" : "bg-white/30"}`}
    >
      {/* --- Logo / Titre --- */}
      <div className="flex items-center justify-center gap-4 mb-8">
        <img
          src="src/images/gemini_logo.png"
          alt="Logo Assurance"
          className="h-10 w-10 rounded-full object-cover shadow-md"
        />
      <h1
        className={`text-2xl font-extrabold tracking-wide transition-all duration-300 
          ${darkMode ? "text-amber-300" : "text-indigo-700"}`}
      >
        Recommendation System 
      </h1>
      </div>

      {/* --- Menu --- */}
      <div className="flex items-center gap-6">
        <Link
          to="/dashboard"
          className={`px-5 py-2 rounded-xl text-sm font-semibold transition-all duration-300 
            hover:scale-110 hover:shadow-[0_0_15px_rgba(99,102,241,0.7)] 
            ${
              darkMode
                ? "bg-gradient-to-r from-indigo-500 to-purple-500 text-white"
                : "bg-gradient-to-r from-pink-500 to-orange-400 text-white"
            }`}
        >
          Dashboard
        </Link>
        <Link
          to="/client"
          className={`px-5 py-2 rounded-xl text-sm font-semibold transition-all duration-300 
            hover:scale-110 hover:shadow-[0_0_15px_rgba(99,102,241,0.7)] 
            ${
              darkMode
                ? "bg-gradient-to-r from-indigo-500 to-purple-500 text-white"
                : "bg-gradient-to-r from-pink-500 to-orange-400 text-white"
            }`}
        >
          Page Clients
        </Link>
        <Link
          to="/assistant"
          className={`px-5 py-2 rounded-xl text-sm font-semibold transition-all duration-300 
            hover:scale-110 hover:shadow-[0_0_15px_rgba(99,102,241,0.7)] 
            ${
              darkMode
                ? "bg-gradient-to-r from-indigo-500 to-purple-500 text-white"
                : "bg-gradient-to-r from-pink-500 to-orange-400 text-white"
            }`}
        >
          Assistant 
        </Link>

        {/* --- Bouton Dark Mode --- */}
        <button
          onClick={toggleDarkMode}
          className={`w-10 h-10 flex items-center justify-center rounded-full transition-all duration-500
            hover:rotate-180 hover:scale-110
            ${
              darkMode
                ? "bg-gradient-to-br from-yellow-300 to-orange-400 text-slate-900"
                : "bg-gradient-to-br from-slate-800 to-slate-900 text-amber-200"
            } shadow-lg`}
          aria-label="Basculer le thème"
        >
          {darkMode ? (
            <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 24 24">
              <path d="M12 18a6 6 0 100-12 6 6 0 000 12z" />
            </svg>
          ) : (
            <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 24 24">
              <path d="M21 12.79A9 9 0 1111.21 3 7 7 0 0021 12.79z" />
            </svg>
          )}
        </button>
      </div>
    </nav>
  );
}

export default NavbarSection;
