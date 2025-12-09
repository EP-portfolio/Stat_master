"""
Gestion du profil de l'élève et personnalisation adaptative
"""

from typing import Dict, Any, List, Optional
from collections import Counter, defaultdict


class StudentProfile:
    """Gère le profil et l'historique de l'élève pour personnalisation"""

    def __init__(self):
        self.history: List[Dict[str, Any]] = []
        self.scores: List[float] = []
        self.errors_by_type: Dict[str, List[str]] = defaultdict(list)
        self.strengths: List[str] = []
        self.exercise_types_attempted: Dict[str, int] = defaultdict(int)
        self.difficulty_progression: Dict[str, List[str]] = defaultdict(list)

    def add_result(
        self,
        exercise_type: str,
        difficulty: str,
        feedback: Dict[str, Any],
        exercise_data: Dict[str, Any],
    ):
        """Ajoute un résultat d'exercice au profil"""

        # Extraire le score
        score_str = feedback.get("score", "0/20")
        try:
            if "/" in score_str:
                score = float(score_str.split("/")[0])
            else:
                score = 0.0
        except:
            score = 0.0

        # Enregistrer le résultat
        result = {
            "exercise_type": exercise_type,
            "difficulty": difficulty,
            "score": score,
            "errors": feedback.get("errors", []),
            "good_points": feedback.get("good_points", []),
            "timestamp": self._get_timestamp(),
        }

        self.history.append(result)
        self.scores.append(score)
        self.exercise_types_attempted[exercise_type] += 1
        self.difficulty_progression[exercise_type].append(difficulty)

        # Analyser les erreurs
        for error in feedback.get("errors", []):
            self.errors_by_type[exercise_type].append(error)

        # Analyser les points forts
        for point in feedback.get("good_points", []):
            if point not in self.strengths:
                self.strengths.append(point)

    def get_profile(self) -> Dict[str, Any]:
        """Retourne le profil complet de l'élève"""

        # Calculer les erreurs les plus communes
        all_errors = []
        for errors in self.errors_by_type.values():
            all_errors.extend(errors)

        common_errors = [
            error for error, count in Counter(all_errors).most_common(5) if count >= 2
        ]

        # Calculer la moyenne des scores
        average_score = sum(self.scores) / len(self.scores) if self.scores else 0.0

        # Déterminer le niveau recommandé
        recommended_difficulty = self._recommend_difficulty()

        # Identifier les types d'exercices à travailler
        weak_areas = self._identify_weak_areas()

        return {
            "common_errors": common_errors,
            "strengths": self.strengths[:5],  # Top 5
            "average_score": round(average_score, 1),
            "total_exercises": len(self.history),
            "recommended_difficulty": recommended_difficulty,
            "weak_areas": weak_areas,
            "exercise_types_attempted": dict(self.exercise_types_attempted),
            "recent_scores": self.scores[-5:] if len(self.scores) >= 5 else self.scores,
        }

    def _recommend_difficulty(self) -> str:
        """Recommandation de difficulté basée sur les performances récentes"""

        if not self.scores:
            return "moyen"

        recent_scores = self.scores[-5:] if len(self.scores) >= 5 else self.scores
        avg_recent = sum(recent_scores) / len(recent_scores)

        if avg_recent >= 16:
            return "difficile"
        elif avg_recent >= 12:
            return "moyen"
        else:
            return "facile"

    def _identify_weak_areas(self) -> List[str]:
        """Identifie les domaines où l'élève a des difficultés"""

        weak_areas = []
        type_scores = defaultdict(list)

        # Calculer les scores moyens par type d'exercice
        for result in self.history:
            type_scores[result["exercise_type"]].append(result["score"])

        for ex_type, scores in type_scores.items():
            avg_score = sum(scores) / len(scores)
            if avg_score < 12 and len(scores) >= 2:
                weak_areas.append(ex_type)

        return weak_areas

    def get_recommended_exercise_type(self) -> Optional[str]:
        """Recommandation du type d'exercice à travailler"""

        weak_areas = self._identify_weak_areas()
        if weak_areas:
            # Recommander le type le plus faible
            return weak_areas[0]

        # Sinon, recommander le type le moins pratiqué
        if self.exercise_types_attempted:
            least_practiced = min(
                self.exercise_types_attempted.items(), key=lambda x: x[1]
            )
            return least_practiced[0]

        return None

    def get_personalized_difficulty(self, exercise_type: str) -> str:
        """Retourne la difficulté personnalisée pour un type d'exercice"""

        # Filtrer les résultats pour ce type
        type_results = [r for r in self.history if r["exercise_type"] == exercise_type]

        if not type_results:
            return "moyen"

        # Calculer la moyenne pour ce type
        type_scores = [r["score"] for r in type_results]
        avg_score = sum(type_scores) / len(type_scores)

        # Recommander selon la performance
        if avg_score >= 16:
            return "difficile"
        elif avg_score >= 12:
            return "moyen"
        else:
            return "facile"

    def _get_timestamp(self) -> str:
        """Retourne un timestamp simple"""
        from datetime import datetime

        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def get_progress_summary(self) -> Dict[str, Any]:
        """Résumé de la progression de l'élève"""

        if not self.history:
            return {
                "message": "Aucun exercice complété pour le moment",
                "trend": "stable",
            }

        # Calculer la tendance
        if len(self.scores) >= 3:
            recent_avg = sum(self.scores[-3:]) / 3
            older_avg = (
                sum(self.scores[:-3]) / (len(self.scores) - 3)
                if len(self.scores) > 3
                else recent_avg
            )

            if recent_avg > older_avg + 1:
                trend = "amélioration"
            elif recent_avg < older_avg - 1:
                trend = "baisse"
            else:
                trend = "stable"
        else:
            trend = "stable"

        return {
            "total_exercises": len(self.history),
            "average_score": round(sum(self.scores) / len(self.scores), 1),
            "trend": trend,
            "best_score": max(self.scores) if self.scores else 0,
            "recent_improvement": trend == "amélioration",
        }
