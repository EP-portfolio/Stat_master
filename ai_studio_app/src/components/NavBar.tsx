import React from "react";
import { ViewState } from "../types";
import { BookOpen, Calculator, Bot, Home, ClipboardList } from "lucide-react";

interface NavBarProps {
  currentView: ViewState;
  onNavigate: (view: ViewState) => void;
}

export const NavBar: React.FC<NavBarProps> = ({ currentView, onNavigate }) => {
  const navItems = [
    { view: ViewState.HOME, label: "Accueil", icon: Home },
    { view: ViewState.LESSON, label: "Le Cours", icon: BookOpen },
    { view: ViewState.PRACTICE, label: "S'entraîner", icon: Calculator },
    { view: ViewState.ASSESSMENT, label: "Évaluation", icon: ClipboardList },
    { view: ViewState.TUTOR, label: "Tuteur IA", icon: Bot },
  ];

  return (
    <nav className="bg-indigo-600 text-white shadow-lg sticky top-0 z-50">
      <div className="max-w-6xl mx-auto px-4">
        <div className="flex justify-between items-center h-16">
          <div className="flex-shrink-0 font-bold text-xl flex items-center gap-2">
            <span className="bg-white text-indigo-600 p-1 rounded">f(x)</span>
            Stat'Master 3ème
          </div>
          <div className="hidden md:flex space-x-4">
            {navItems.map((item) => {
              const Icon = item.icon;
              const isActive = currentView === item.view;
              return (
                <button
                  key={item.view}
                  onClick={() => onNavigate(item.view)}
                  className={`flex items-center gap-2 px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                    isActive
                      ? "bg-indigo-700 text-white shadow-inner"
                      : "text-indigo-100 hover:bg-indigo-500 hover:text-white"
                  }`}
                >
                  <Icon size={18} />
                  {item.label}
                </button>
              );
            })}
          </div>
        </div>
      </div>
      {/* Mobile */}
      <div className="md:hidden flex justify-around bg-indigo-700 p-2">
        {navItems.map((item) => {
          const Icon = item.icon;
          const isActive = currentView === item.view;
          return (
            <button
              key={item.view}
              onClick={() => onNavigate(item.view)}
              className={`p-2 rounded-md ${isActive ? "bg-indigo-800" : ""}`}
            >
              <Icon size={24} className="text-white" />
            </button>
          );
        })}
      </div>
    </nav>
  );
};

