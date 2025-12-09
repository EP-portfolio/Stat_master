import React, { useState, useEffect } from "react";
import { generateRandomDataSet, getFrequencyData } from "../utils/math";
import { DataSet } from "../types";
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell } from "recharts";
import { RefreshCw, CheckCircle, XCircle, Eye } from "lucide-react";

export const Practice: React.FC = () => {
  const [dataSet, setDataSet] = useState<DataSet | null>(null);
  const [userInputs, setUserInputs] = useState({ mean: "", median: "", range: "" });
  const [feedback, setFeedback] = useState<{ mean: boolean | null; median: boolean | null; range: boolean | null }>({
    mean: null,
    median: null,
    range: null,
  });
  const [showSolution, setShowSolution] = useState(false);

  const generateNewExercise = () => {
    const count = Math.floor(Math.random() * 10) + 5; // 5 à 15 valeurs
    const newSet = generateRandomDataSet(count, 0, 20);
    setDataSet(newSet);
    setUserInputs({ mean: "", median: "", range: "" });
    setFeedback({ mean: null, median: null, range: null });
    setShowSolution(false);
  };

  useEffect(() => {
    generateNewExercise();
  }, []);

  const handleCheck = () => {
    if (!dataSet) return;
    const userMean = parseFloat(userInputs.mean.replace(",", "."));
    const userMedian = parseFloat(userInputs.median.replace(",", "."));
    const userRange = parseFloat(userInputs.range.replace(",", "."));
    setFeedback({
      mean: Math.abs(userMean - dataSet.mean) < 0.1,
      median: userMedian === dataSet.median,
      range: userRange === dataSet.range,
    });
  };

  if (!dataSet) return <div>Chargement...</div>;
  const frequencyData = getFrequencyData(dataSet.values);

  return (
    <div className="max-w-5xl mx-auto p-4 md:p-8">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-3xl font-bold text-gray-800">Entraînement</h2>
        <button
          onClick={generateNewExercise}
          className="flex items-center gap-2 bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-lg transition-colors shadow-sm"
        >
          <RefreshCw size={18} />
          Nouvelle Série
        </button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="lg:col-span-2 space-y-6">
          <div className="bg-white p-6 rounded-xl shadow-md border border-gray-100">
            <h3 className="text-lg font-semibold text-gray-700 mb-4">La Série Statistique (Notes sur 20)</h3>
            <div className="flex flex-wrap gap-2">
              {dataSet.values.map((v, i) => (
                <span key={i} className="inline-block bg-gray-100 text-gray-800 font-mono px-3 py-1 rounded-full text-lg">
                  {v}
                </span>
              ))}
            </div>
            <div className="mt-4 text-sm text-gray-500">
              Effectif total : <span className="font-bold text-gray-800">{dataSet.totalCount}</span> valeurs
            </div>
          </div>

          <div className="bg-white p-6 rounded-xl shadow-md border border-gray-100 h-80">
            <h3 className="text-lg font-semibold text-gray-700 mb-4">Répartition des Notes</h3>
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={frequencyData}>
                <XAxis dataKey="value" stroke="#6b7280" />
                <YAxis stroke="#6b7280" allowDecimals={false} />
                <Tooltip contentStyle={{ backgroundColor: "#fff", borderRadius: "8px", border: "1px solid #e5e7eb" }} cursor={{ fill: "#f3f4f6" }} />
                <Bar dataKey="count" fill="#4f46e5" radius={[4, 4, 0, 0]}>
                  {frequencyData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill="#4f46e5" />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="lg:col-span-1 space-y-6">
          <div className="bg-white p-6 rounded-xl shadow-lg border border-indigo-100">
            <h3 className="text-xl font-bold text-indigo-900 mb-6">À toi de jouer !</h3>

            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Moyenne</label>
                <div className="relative">
                  <input
                    type="number"
                    step="0.1"
                    value={userInputs.mean}
                    onChange={(e) => setUserInputs({ ...userInputs, mean: e.target.value })}
                    className={`block w-full rounded-md border-gray-300 shadow-sm p-3 border focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none ${
                      feedback.mean === true ? "border-green-500 bg-green-50" : ""
                    } ${feedback.mean === false ? "border-red-500 bg-red-50" : ""}`}
                    placeholder="Ex: 12.5"
                  />
                  <div className="absolute inset-y-0 right-0 flex items-center pr-3 pointer-events-none">
                    {feedback.mean === true && <CheckCircle className="text-green-600" size={20} />}
                    {feedback.mean === false && <XCircle className="text-red-600" size={20} />}
                  </div>
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Médiane</label>
                <div className="relative">
                  <input
                    type="number"
                    step="0.5"
                    value={userInputs.median}
                    onChange={(e) => setUserInputs({ ...userInputs, median: e.target.value })}
                    className={`block w-full rounded-md border-gray-300 shadow-sm p-3 border focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none ${
                      feedback.median === true ? "border-green-500 bg-green-50" : ""
                    } ${feedback.median === false ? "border-red-500 bg-red-50" : ""}`}
                    placeholder="Ex: 12"
                  />
                  <div className="absolute inset-y-0 right-0 flex items-center pr-3 pointer-events-none">
                    {feedback.median === true && <CheckCircle className="text-green-600" size={20} />}
                    {feedback.median === false && <XCircle className="text-red-600" size={20} />}
                  </div>
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Étendue</label>
                <div className="relative">
                  <input
                    type="number"
                    value={userInputs.range}
                    onChange={(e) => setUserInputs({ ...userInputs, range: e.target.value })}
                    className={`block w-full rounded-md border-gray-300 shadow-sm p-3 border focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none ${
                      feedback.range === true ? "border-green-500 bg-green-50" : ""
                    } ${feedback.range === false ? "border-red-500 bg-red-50" : ""}`}
                    placeholder="Ex: 8"
                  />
                  <div className="absolute inset-y-0 right-0 flex items-center pr-3 pointer-events-none">
                    {feedback.range === true && <CheckCircle className="text-green-600" size={20} />}
                    {feedback.range === false && <XCircle className="text-red-600" size={20} />}
                  </div>
                </div>
              </div>

              <div className="pt-4 flex flex-col gap-3">
                <button onClick={handleCheck} className="w-full bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-3 px-4 rounded-lg shadow-md transition-colors">
                  Vérifier mes réponses
                </button>
                <button
                  onClick={() => setShowSolution(!showSolution)}
                  className="w-full bg-white hover:bg-gray-50 text-indigo-600 border border-indigo-200 font-medium py-2 px-4 rounded-lg transition-colors flex items-center justify-center gap-2"
                >
                  <Eye size={16} />
                  {showSolution ? "Masquer la correction" : "Voir la correction"}
                </button>
              </div>
            </div>
          </div>

          {showSolution && (
            <div className="bg-yellow-50 p-6 rounded-xl border border-yellow-200 animate-fade-in">
              <h4 className="font-bold text-yellow-900 mb-4">Correction Détaillée</h4>
              <ul className="space-y-3 text-sm text-yellow-800">
                <li>
                  <strong>Série ordonnée :</strong>
                  <br />
                  <span className="font-mono bg-white px-2 py-1 rounded border border-yellow-100 block mt-1">
                    {dataSet.sortedValues.join(", ")}
                  </span>
                </li>
                <li>
                  <strong>Moyenne :</strong> {dataSet.mean}
                  <br />
                  <span className="text-xs text-yellow-600">(Somme des valeurs / {dataSet.totalCount})</span>
                </li>
                <li>
                  <strong>Médiane :</strong> {dataSet.median}
                  <br />
                  <span className="text-xs text-yellow-600">
                    {dataSet.totalCount % 2 === 0 ? "Effectif pair : moyenne des 2 valeurs centrales." : "Effectif impair : valeur centrale."}
                  </span>
                </li>
                <li>
                  <strong>Étendue :</strong> {dataSet.range}
                  <br />
                  <span className="text-xs text-yellow-600">
                    ({dataSet.sortedValues[dataSet.totalCount - 1]} - {dataSet.sortedValues[0]})
                  </span>
                </li>
              </ul>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

