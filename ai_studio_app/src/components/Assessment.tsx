import React, { useState, useRef, useEffect } from "react";
import { GoogleGenAI } from "@google/genai";
import { Camera, Send, CheckCircle, AlertCircle, FileText, ChevronRight, Mail } from "lucide-react";

interface ExerciseStep {
  id: number;
  title: string;
  description: string;
  problem: string;
  promptText: string;
  type: "table" | "frequency" | "indicators" | "problem";
}

const EXERCISES: ExerciseStep[] = [
  {
    id: 1,
    title: "Construction de Tableau",
    description: "Capacité à construire un tableau statistique à partir d'une liste brute.",
    type: "table",
    problem: `Voici les pointures de chaussures relevées dans une classe de 3ème :
38, 40, 39, 42, 38, 39, 41, 40, 38, 42, 43, 39, 40, 38, 41.

Construis le tableau des effectifs.
Colonnes suggérées : "Pointure" et "Effectif".`,
    promptText: "Liste : 38, 40, 39, 42, 38, 39, 41, 40, 38, 42, 43, 39, 40, 38, 41. Faire un tableau des effectifs.",
  },
  {
    id: 2,
    title: "Calcul de Fréquences",
    description: "Calculer des fréquences (décimales, fractions, pourcentages).",
    type: "frequency",
    problem: "Dans un club de sport de 50 adhérents, 12 pratiquent le tennis.\n\nCalcule la fréquence des joueurs de tennis sous trois formes :\n1. Fraction irréductible\n2. Valeur décimale\n3. Pourcentage",
    promptText: "Club : 50 adhérents, 12 tennis. Calculer la fréquence (fraction, décimal, %).",
  },
  {
    id: 3,
    title: "Indicateurs Statistiques",
    description: "Calculer la moyenne, la médiane et les quartiles.",
    type: "indicators",
    problem: "Voici les notes obtenues par un élève : 8, 12, 14, 9, 15, 12, 11.\n\n1. Calcule la moyenne.\n2. Détermine la médiane.\n3. (Optionnel) Détermine Q1 et Q3.",
    promptText: "Notes : 8, 12, 14, 9, 15, 12, 11. Calculer Moyenne et Médiane.",
  },
  {
    id: 4,
    title: "Résolution de Problème",
    description: "Interpréter des données pour résoudre un problème.",
    type: "problem",
    problem: "Entreprise A : Salaire moyen 2500€, Médian 1800€.\nEntreprise B : Salaire moyen 2500€, Médian 2400€.\n\nSi tu veux gagner plus de 2000€, quelle entreprise choisir ?",
    promptText: "A : Moyenne 2500, Médiane 1800. B : Moyenne 2500, Médiane 2400. Choix pour > 2000 ?",
  },
];

export const Assessment: React.FC = () => {
  const [currentStepIndex, setCurrentStepIndex] = useState(0);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [feedbackHistory, setFeedbackHistory] = useState<string[]>([]);
  const [reportReady, setReportReady] = useState(false);
  const [parentEmail, setParentEmail] = useState("");
  const [emailSent, setEmailSent] = useState(false);
  const [generatedProblemImages, setGeneratedProblemImages] = useState<Record<number, string>>({});
  const [isGeneratingImage, setIsGeneratingImage] = useState(false);
  const [showTextFallback, setShowTextFallback] = useState(false);

  const fileInputRef = useRef<HTMLInputElement>(null);
  const currentExercise = EXERCISES[currentStepIndex];

  // Generate a "handwritten" problem image
  useEffect(() => {
    const generateProblemImage = async () => {
      if (generatedProblemImages[currentStepIndex]) return;
      setIsGeneratingImage(true);
      setShowTextFallback(false);
      try {
        const apiKey = process.env.API_KEY;
        if (!apiKey) throw new Error("API Key missing");
        const ai = new GoogleGenAI({ apiKey });
        const response = await ai.models.generateContent({
          model: "gemini-2.5-flash-image",
          contents: {
            parts: [
              {
                text: `Une feuille de papier à grands carreaux (type cahier d'école).
              Au centre, écrit à l'encre bleue manuscrite, le texte court suivant :
              "${currentExercise.promptText}"
              Photo zénithale, éclairage naturel, écriture lisible.`,
              },
            ],
          },
          config: {
            imageConfig: {
              aspectRatio: "16:9",
            },
          },
        });
        let imageUrl = "";
        if (response.candidates?.[0]?.content?.parts) {
          for (const part of response.candidates[0].content.parts) {
            if (part.inlineData) {
              imageUrl = `data:image/png;base64,${part.inlineData.data}`;
              break;
            }
          }
        }
        if (imageUrl) {
          setGeneratedProblemImages((prev) => ({ ...prev, [currentStepIndex]: imageUrl }));
        } else {
          setShowTextFallback(true);
        }
      } catch {
        setShowTextFallback(true);
      } finally {
        setIsGeneratingImage(false);
      }
    };
    generateProblemImage();
  }, [currentStepIndex, currentExercise.promptText, generatedProblemImages]);

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;
    setIsAnalyzing(true);
    try {
      const apiKey = process.env.API_KEY;
      if (!apiKey) throw new Error("Clé API manquante");
      const reader = new FileReader();
      reader.readAsDataURL(file);
      reader.onloadend = async () => {
        const base64Data = reader.result as string;
        const base64Content = base64Data.split(",")[1];
        const mimeType = file.type;
        const ai = new GoogleGenAI({ apiKey });
        const prompt = `
          Tu es un professeur de mathématiques (niveau 3ème).
          Sujet : ${currentExercise.problem}
          Objectif : ${currentExercise.description}
          Consignes : corrige l'image fournie, liste erreurs et bons points, donne une correction courte et claire.`;
        const response = await ai.models.generateContent({
          model: "gemini-2.5-flash",
          contents: {
            parts: [
              { text: prompt },
              {
                inlineData: {
                  mimeType,
                  data: base64Content,
                },
              },
            ],
          },
        });
        const feedback = response.text || "Analyse impossible.";
        setFeedbackHistory([...feedbackHistory, feedback]);
      };
    } catch (error) {
      console.error(error);
      alert("Erreur lors de l'analyse de l'image.");
    } finally {
      setIsAnalyzing(false);
    }
  };

  const handleNext = () => {
    if (currentStepIndex < EXERCISES.length - 1) {
      setCurrentStepIndex((prev) => prev + 1);
      if (fileInputRef.current) fileInputRef.current.value = "";
      setShowTextFallback(false);
    } else {
      setReportReady(true);
    }
  };

  const handleSendReport = () => {
    if (!parentEmail.includes("@")) {
      alert("Veuillez entrer une adresse email valide.");
      return;
    }
    setTimeout(() => setEmailSent(true), 800); // simulation
  };

  if (reportReady) {
    return (
      <div className="max-w-4xl mx-auto p-4 md:p-8">
        <div className="bg-white rounded-2xl shadow-xl overflow-hidden border border-gray-200">
          <div className="bg-green-600 p-6 text-white text-center">
            <h2 className="text-3xl font-bold">Bilan de Compétences</h2>
            <p className="text-green-100 mt-2">Évaluation terminée</p>
          </div>
          <div className="p-8 space-y-8">
            <div className="space-y-6">
              <h3 className="text-xl font-bold text-gray-800 border-b pb-2">Détail par compétence</h3>
              {EXERCISES.map((ex, idx) => (
                <div key={ex.id} className="bg-gray-50 rounded-lg p-4">
                  <h4 className="font-bold text-indigo-700 mb-1">
                    Exercice {idx + 1} : {ex.title}
                  </h4>
                  <div className="text-sm text-gray-600 mb-3 italic">{ex.description}</div>
                  <div className="text-sm text-gray-800 bg-white p-3 rounded border border-gray-200 whitespace-pre-wrap">
                    {feedbackHistory[idx]}
                  </div>
                </div>
              ))}
            </div>
            <div className="bg-indigo-50 p-6 rounded-xl border border-indigo-100">
              <h3 className="text-lg font-bold text-indigo-900 mb-4 flex items-center gap-2">
                <Mail size={20} />
                Informer les parents
              </h3>
              {!emailSent ? (
                <div className="flex flex-col sm:flex-row gap-3">
                  <input
                    type="email"
                    placeholder="email.parent@exemple.com"
                    value={parentEmail}
                    onChange={(e) => setParentEmail(e.target.value)}
                    className="flex-1 p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 outline-none"
                  />
                  <button onClick={handleSendReport} className="bg-indigo-600 text-white font-bold py-3 px-6 rounded-lg hover:bg-indigo-700 transition-colors">
                    Envoyer le bilan
                  </button>
                </div>
              ) : (
                <div className="flex items-center gap-2 text-green-700 bg-green-100 p-4 rounded-lg">
                  <CheckCircle size={20} />
                  Le compte-rendu a été envoyé.
                </div>
              )}
              <p className="text-xs text-gray-500 mt-3">Un récapitulatif des points forts et axes d'amélioration sera transmis.</p>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-3xl mx-auto p-4 md:p-8">
      <div className="mb-8">
        <div className="flex justify-between text-sm font-medium text-gray-500 mb-2">
          <span>Progression</span>
          <span>
            {currentStepIndex + 1} / {EXERCISES.length}
          </span>
        </div>
        <div className="w-full bg-gray-200 rounded-full h-2.5">
          <div
            className="bg-indigo-600 h-2.5 rounded-full transition-all duration-500"
            style={{ width: `${((currentStepIndex + 1) / EXERCISES.length) * 100}%` }}
          ></div>
        </div>
      </div>

      <div className="bg-white rounded-2xl shadow-lg overflow-hidden border border-gray-100">
        <div className="p-6 md:p-8">
          <div className="flex justify-between items-start mb-6">
            <div className="inline-block px-3 py-1 bg-indigo-100 text-indigo-700 text-xs font-bold rounded-full uppercase tracking-wide">
              Compétence : {currentExercise.title}
            </div>
            <button onClick={() => setShowTextFallback(!showTextFallback)} className="text-gray-400 hover:text-indigo-600 flex items-center gap-1 text-sm">
              <FileText size={16} />
              {showTextFallback ? "Voir le cahier" : "Voir texte brut"}
            </button>
          </div>

          <h2 className="text-2xl font-bold text-gray-900 mb-6">À toi de jouer !</h2>

          <div className="mb-8 relative min-h-[200px] rounded-xl overflow-hidden border border-indigo-100 shadow-sm bg-gray-50">
            {!showTextFallback && generatedProblemImages[currentStepIndex] ? (
              <div className="relative">
                <img src={generatedProblemImages[currentStepIndex]} alt="Énoncé de l'exercice sur cahier" className="w-full h-auto object-cover" />
                <div className="absolute bottom-2 right-2 bg-black/50 text-white text-xs px-2 py-1 rounded">Généré par IA</div>
              </div>
            ) : !showTextFallback && isGeneratingImage ? (
              <div className="flex flex-col items-center justify-center h-64 bg-indigo-50/50">
                <div className="w-10 h-10 border-4 border-indigo-200 border-t-indigo-600 rounded-full animate-spin mb-3"></div>
                <p className="text-indigo-600 text-xl">L'IA écrit l'énoncé...</p>
              </div>
            ) : (
              <div className="p-8 bg-white" style={{ backgroundImage: "radial-gradient(#e5e7eb 1px, transparent 1px)", backgroundSize: "20px 20px" }}>
                <p className="whitespace-pre-wrap text-xl text-indigo-900 leading-loose">{currentExercise.problem}</p>
              </div>
            )}
          </div>

          {feedbackHistory[currentStepIndex] ? (
            <div className="mb-8">
              <div className="bg-green-50 p-5 rounded-xl border border-green-200">
                <h3 className="font-bold text-green-900 mb-3 flex items-center gap-2">
                  <CheckCircle size={20} />
                  Correction de l'IA
                </h3>
                <div className="prose prose-sm max-w-none text-gray-800 whitespace-pre-wrap">{feedbackHistory[currentStepIndex]}</div>
              </div>
              <div className="mt-6 flex justify-end">
                <button onClick={handleNext} className="flex items-center gap-2 bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-3 px-6 rounded-lg transition-colors shadow-md">
                  {currentStepIndex < EXERCISES.length - 1 ? "Page Suivante" : "Voir le Bilan"}
                  <ChevronRight size={20} />
                </button>
              </div>
            </div>
          ) : (
            <div className="space-y-4">
              <div className="bg-blue-50 p-4 rounded-lg text-blue-800 text-sm mb-4 flex items-start gap-2">
                <AlertCircle size={18} className="mt-0.5 flex-shrink-0" />
                <p>Résous l'exercice sur papier libre, puis prends une photo de ta réponse pour que je puisse la corriger.</p>
              </div>
              <div className="flex flex-col items-center justify-center border-2 border-dashed border-gray-300 rounded-xl p-8 hover:bg-gray-50 transition-colors group cursor-pointer relative">
                {isAnalyzing ? (
                  <div className="text-center py-4">
                    <div className="w-12 h-12 border-4 border-indigo-200 border-t-indigo-600 rounded-full animate-spin mx-auto mb-4"></div>
                    <p className="text-indigo-600 font-medium">Je lis ta copie...</p>
                  </div>
                ) : (
                  <>
                    <input
                      ref={fileInputRef}
                      type="file"
                      accept="image/*"
                      capture="environment"
                      onChange={handleFileUpload}
                      className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
                      id="camera-input"
                    />
                    <div className="bg-indigo-100 p-4 rounded-full group-hover:scale-110 transition-transform duration-200">
                      <Camera size={40} className="text-indigo-600" />
                    </div>
                    <span className="font-bold text-lg text-gray-700 mt-3 group-hover:text-indigo-700">Scanner ma réponse</span>
                  </>
                )}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

