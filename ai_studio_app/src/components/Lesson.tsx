import React, { useState } from "react";
import { LessonTopic } from "../types";
import { ChevronRight, ChevronDown, BookOpen } from "lucide-react";

const lessons: LessonTopic[] = [
  {
    id: "moyenne",
    title: "La Moyenne",
    description: "Comment calculer la moyenne d'une série statistique.",
    content: (
      <div className="space-y-4">
        <p className="text-gray-700">
          La <strong>moyenne</strong> d'une série statistique est le quotient de
          la somme de toutes les valeurs par l'effectif total.
        </p>
        <div className="bg-blue-50 p-4 rounded-lg border-l-4 border-blue-500">
          <h4 className="font-bold text-blue-900 mb-2">Formule :</h4>
          <p className="font-mono text-sm text-blue-800">
            M = (v₁ + v₂ + ... + vₙ) / N
          </p>
          <p className="text-sm mt-2 text-blue-800">
            Où <em>v</em> sont les valeurs et <em>N</em> est le nombre total de
            valeurs.
          </p>
        </div>
        <div className="bg-white p-4 rounded shadow-sm border">
          <h4 className="font-semibold mb-2">Exemple :</h4>
          <p>Notes : 12, 15, 8, 14, 11</p>
          <p className="mt-2">
            Somme = 60 — Effectif = 5 — <strong>Moyenne = 12</strong>
          </p>
        </div>
      </div>
    ),
  },
  {
    id: "mediane",
    title: "La Médiane",
    description: "La valeur centrale qui partage la série en deux groupes égaux.",
    content: (
      <div className="space-y-4">
        <p className="text-gray-700">
          La <strong>médiane</strong> est la valeur qui partage la série
          statistique ordonnée en deux groupes de même effectif.
        </p>
        <div className="bg-yellow-50 p-4 rounded-lg border-l-4 border-yellow-500">
          <h4 className="font-bold text-yellow-900 mb-2">Méthode :</h4>
          <ol className="list-decimal list-inside space-y-1 text-yellow-800">
            <li>Ordonner les valeurs.</li>
            <li>Si N est impair : la valeur centrale.</li>
            <li>Si N est pair : moyenne des deux valeurs centrales.</li>
          </ol>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="bg-white p-4 rounded shadow-sm border">
            <h4 className="font-semibold mb-2 text-sm text-gray-500 uppercase">
              Cas Impair (5 valeurs)
            </h4>
            <p className="font-mono bg-gray-100 p-2 rounded text-center">
              8, 11, <strong className="text-indigo-600">12</strong>, 14, 15
            </p>
            <p className="text-sm mt-2">Médiane = 12</p>
          </div>
          <div className="bg-white p-4 rounded shadow-sm border">
            <h4 className="font-semibold mb-2 text-sm text-gray-500 uppercase">
              Cas Pair (6 valeurs)
            </h4>
            <p className="font-mono bg-gray-100 p-2 rounded text-center">
              8, 11, <span className="text-indigo-600">12, 13</span>, 15, 18
            </p>
            <p className="text-sm mt-2">Médiane = (12 + 13) / 2 = 12,5</p>
          </div>
        </div>
      </div>
    ),
  },
  {
    id: "etendue",
    title: "L'Étendue",
    description: "Mesurer la dispersion des valeurs.",
    content: (
      <div className="space-y-4">
        <p className="text-gray-700">
          L'<strong>étendue</strong> est la différence entre la plus grande et la
          plus petite valeur.
        </p>
        <div className="bg-green-50 p-4 rounded-lg border-l-4 border-green-500">
          <h4 className="font-bold text-green-900 mb-2">Formule :</h4>
          <p className="font-mono text-sm text-green-800">E = Max - Min</p>
        </div>
        <p className="text-sm text-gray-600 italic">
          Plus l'étendue est grande, plus la dispersion est forte.
        </p>
      </div>
    ),
  },
];

export const Lesson: React.FC = () => {
  const [openLesson, setOpenLesson] = useState<string | null>("moyenne");
  const toggleLesson = (id: string) => setOpenLesson((prev) => (prev === id ? null : id));

  return (
    <div className="max-w-4xl mx-auto p-4 md:p-8">
      <h2 className="text-3xl font-bold text-gray-800 mb-6 flex items-center gap-3">
        <BookOpen className="text-indigo-600" />
        Cours de Statistiques
      </h2>
      <div className="space-y-4">
        {lessons.map((lesson) => (
          <div key={lesson.id} className="bg-white rounded-xl shadow-md overflow-hidden border border-gray-100 transition-all">
            <button
              onClick={() => toggleLesson(lesson.id)}
              className="w-full flex items-center justify-between p-6 text-left hover:bg-gray-50 focus:outline-none"
            >
              <div>
                <h3 className="text-xl font-bold text-gray-900">{lesson.title}</h3>
                <p className="text-gray-500 text-sm mt-1">{lesson.description}</p>
              </div>
              {openLesson === lesson.id ? <ChevronDown className="text-indigo-600" /> : <ChevronRight className="text-gray-400" />}
            </button>
            {openLesson === lesson.id && (
              <div className="p-6 pt-0 border-t border-gray-100 bg-gray-50/50">
                <div className="prose max-w-none mt-4">{lesson.content}</div>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};

