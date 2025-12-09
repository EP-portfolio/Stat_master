import React, { useState } from "react";
import { NavBar } from "./components/NavBar";
import { Lesson } from "./components/Lesson";
import { Practice } from "./components/Practice";
import { Assessment } from "./components/Assessment";
import { AiTutor } from "./components/AiTutor";
import { ViewState } from "./types";
import { GraduationCap, ArrowRight, ClipboardList } from "lucide-react";

const App: React.FC = () => {
  const [currentView, setCurrentView] = useState<ViewState>(ViewState.HOME);

  const renderContent = () => {
    switch (currentView) {
      case ViewState.LESSON:
        return <Lesson />;
      case ViewState.PRACTICE:
        return <Practice />;
      case ViewState.ASSESSMENT:
        return <Assessment />;
      case ViewState.TUTOR:
        return <AiTutor />;
      case ViewState.HOME:
      default:
        return (
          <div className="max-w-4xl mx-auto p-6 text-center space-y-12">
            <div className="mt-12 space-y-6">
              <div className="inline-block p-4 bg-indigo-100 rounded-full mb-4">
                <GraduationCap size={64} className="text-indigo-600" />
              </div>
              <h1 className="text-5xl font-extrabold text-gray-900 tracking-tight">
                Maîtrise les <span className="text-indigo-600">Statistiques</span>
              </h1>
              <p className="text-xl text-gray-600 max-w-2xl mx-auto">
                Tout ce qu'il te faut pour réussir ton brevet : cours interactifs, exercices infinis et un prof IA disponible 24/7.
              </p>
              <div className="flex flex-col sm:flex-row justify-center gap-4 pt-4">
                <button onClick={() => setCurrentView(ViewState.LESSON)} className="px-8 py-4 bg-white text-indigo-600 border-2 border-indigo-600 rounded-xl font-bold text-lg hover:bg-indigo-50 transition-colors shadow-sm">
                  Lire le cours
                </button>
                <button onClick={() => setCurrentView(ViewState.PRACTICE)} className="px-8 py-4 bg-indigo-600 text-white rounded-xl font-bold text-lg hover:bg-indigo-700 transition-colors shadow-lg flex items-center justify-center gap-2">
                  S'entraîner <ArrowRight size={20} />
                </button>
              </div>
            </div>

            <div className="grid md:grid-cols-3 gap-6 text-left mt-16">
              <div className="bg-white p-6 rounded-xl shadow-md border border-gray-100 cursor-pointer hover:shadow-lg transition-shadow" onClick={() => setCurrentView(ViewState.ASSESSMENT)}>
                <div className="flex items-center gap-3 mb-2">
                  <div className="bg-orange-100 p-2 rounded-lg text-orange-600">
                    <ClipboardList size={24} />
                  </div>
                  <h3 className="font-bold text-xl text-gray-800">Mode Évaluation</h3>
                </div>
                <p className="text-gray-600">Teste tes connaissances sur les 4 compétences clés du brevet avec correction photo par IA.</p>
              </div>
              <div className="bg-white p-6 rounded-xl shadow-md border border-gray-100">
                <h3 className="font-bold text-xl text-gray-800 mb-2">📊 Graphiques</h3>
                <p className="text-gray-600">Visualise les données avec des histogrammes interactifs pour mieux comprendre.</p>
              </div>
              <div className="bg-white p-6 rounded-xl shadow-md border border-gray-100">
                <h3 className="font-bold text-xl text-gray-800 mb-2">🤖 Aide IA</h3>
                <p className="text-gray-600">Bloqué sur un concept ? Demande à notre IA spécialisée dans le programme de 3ème.</p>
              </div>
            </div>
          </div>
        );
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col font-sans">
      <NavBar currentView={currentView} onNavigate={setCurrentView} />
      <main className="flex-grow">{renderContent()}</main>
      <footer className="bg-white border-t border-gray-200 py-6 text-center text-gray-500 text-sm">
        <p>2024 Stat'Master 3ème - Conçu pour la réussite au Brevet des Collèges.</p>
      </footer>
    </div>
  );
};

export default App;

