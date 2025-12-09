"""
Générateur d'exercices de statistiques pour niveau 3ème
Utilise Gemini 3 Pro pour générer des exercices variés et adaptés
"""

import random
from typing import Dict, Any, List, Optional
from gemini_client import GeminiClient


class ExerciseGenerator:
    """Générateur d'exercices de statistiques utilisant Gemini"""

    def __init__(self, gemini_client: GeminiClient):
        self.gemini = gemini_client
        # Fallback: exercices prédéfinis si Gemini échoue
        self.fallback_exercises = self._init_fallback_exercises()

    def generate(
        self,
        exercise_type: str,
        difficulty: str = "moyen",
        student_profile: Optional[Dict[str, Any]] = None,
        examples_analysis: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Génère un exercice selon le type demandé avec Gemini
        Utilise le profil de l'élève et/ou des exemples pour personnaliser

        Args:
            exercise_type: effectif, frequence, moyenne, probleme
            difficulty: facile, moyen, difficile
            student_profile: Profil de l'élève pour personnalisation
            examples_analysis: Analyse d'exemples d'exercices pour inspiration
        """

        # Priorité 1: Générer avec exemples si disponibles
        if examples_analysis and examples_analysis.get("valid"):
            try:
                exercise = self.gemini.generate_exercise_from_examples(
                    exercise_type, difficulty, examples_analysis
                )
                if exercise and not exercise.get("error"):
                    # Personnaliser l'exercice selon le profil
                    if student_profile:
                        exercise = self._personalize_exercise(exercise, student_profile)
                    return exercise
            except Exception as e:
                print(f"Erreur génération avec exemples: {e}")

        # Priorité 2: Générer avec Gemini standard
        try:
            exercise = self.gemini.generate_exercise(exercise_type, difficulty)
            if exercise and not exercise.get("error"):
                # Personnaliser l'exercice selon le profil
                if student_profile:
                    exercise = self._personalize_exercise(exercise, student_profile)
                return exercise
        except Exception as e:
            print(f"Erreur génération Gemini: {e}")

        # Fallback vers exercices prédéfinis
        return self._generate_fallback(exercise_type, difficulty)

    def _personalize_exercise(
        self, exercise: Dict[str, Any], student_profile: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Personnalise un exercice selon le profil de l'élève"""

        # Adapter la difficulté selon les performances
        common_errors = student_profile.get("common_errors", [])
        strengths = student_profile.get("strengths", [])

        # Ajouter des indices si l'élève a des difficultés
        if common_errors:
            hints = self._generate_hints(exercise["type"], common_errors)
            exercise["hints"] = hints

        # Adapter le contexte selon les intérêts (si disponibles)
        interests = student_profile.get("interests", [])
        if interests:
            # Modifier le contexte de l'exercice pour l'adapter
            exercise["personalized_context"] = True

        return exercise

    def _generate_hints(
        self, exercise_type: str, common_errors: List[str]
    ) -> List[str]:
        """Génère des indices basés sur les erreurs communes"""

        hints_map = {
            "effectif": [
                "Pense à compter chaque valeur une par une",
                "Vérifie que la somme des effectifs correspond au total",
            ],
            "frequence": [
                "Rappelle-toi: fréquence = effectif / total",
                "Pour les pourcentages, multiplie la fréquence décimale par 100",
            ],
            "moyenne": [
                "Calcule d'abord: valeur × effectif pour chaque ligne",
                "Puis additionne tous ces produits avant de diviser",
            ],
            "probleme": [
                "Lis bien l'énoncé et identifie les données importantes",
                "Vérifie que ta réponse a du sens dans le contexte",
            ],
        }

        return hints_map.get(exercise_type, [])

    def _generate_fallback(self, exercise_type: str, difficulty: str) -> Dict[str, Any]:
        """Génère un exercice de secours si Gemini échoue"""

        generators = {
            "effectif": self._generate_effectif_fallback,
            "frequence": self._generate_frequence_fallback,
            "moyenne": self._generate_moyenne_fallback,
            "probleme": self._generate_probleme_fallback,
        }

        generator = generators.get(exercise_type)
        if not generator:
            raise ValueError(f"Type d'exercice inconnu: {exercise_type}")

        return generator(difficulty)

    def _generate_effectif_fallback(self, difficulty: str) -> Dict[str, Any]:
        """Génère un exercice d'effectif (fallback)"""

        if difficulty == "facile":
            values = [random.choice([10, 11, 12]) for _ in range(10)]
        elif difficulty == "moyen":
            values = [random.choice([10, 11, 12, 13, 14]) for _ in range(15)]
        else:
            values = [
                random.choice([8, 9, 10, 11, 12, 13, 14, 15, 16]) for _ in range(20)
            ]

        effectifs = {}
        for val in values:
            effectifs[val] = effectifs.get(val, 0) + 1

        total = len(values)

        question = f"""Voici une liste de {total} valeurs d'un caractère :

{', '.join(map(str, values))}

Complète le tableau d'effectifs suivant :

| Valeur | Effectif |
|--------|----------|
|        |          |
|        |          |
|        |          |
|        |          |
| Total  |          |"""

        return {
            "type": "effectif",
            "type_name": "Tableau d'effectifs",
            "question": question,
            "exercise_data": {
                "values": values,
                "expected_effectifs": effectifs,
                "expected_total": total,
            },
            "expected_answer": f"Tableau d'effectifs: {effectifs}, Total: {total}",
            "exercise_info": f"Liste de {total} valeurs à classer en effectifs",
        }

    def _generate_frequence_fallback(self, difficulty: str) -> Dict[str, Any]:
        """Génère un exercice de fréquence (fallback)"""

        if difficulty == "facile":
            effectifs = {10: 2, 11: 3, 12: 5}
        elif difficulty == "moyen":
            effectifs = {10: 3, 11: 4, 12: 5, 13: 3}
        else:
            effectifs = {8: 2, 9: 3, 10: 4, 11: 5, 12: 6}

        total = sum(effectifs.values())
        format_type = random.choice(["decimal", "fraction", "pourcentage"])

        frequences = {}
        for val, eff in effectifs.items():
            if format_type == "decimal":
                frequences[val] = round(eff / total, 3)
            elif format_type == "fraction":
                from fractions import Fraction

                freq_frac = Fraction(eff, total)
                frequences[val] = f"{freq_frac.numerator}/{freq_frac.denominator}"
            else:
                frequences[val] = round((eff / total) * 100, 1)

        format_text = {
            "decimal": "sous forme décimale",
            "fraction": "sous forme de fraction",
            "pourcentage": "en pourcentage",
        }[format_type]

        question = f"""Voici un tableau d'effectifs :

| Valeur | Effectif |
|--------|----------|
{chr(10).join([f"| {val}      | {eff}      |" for val, eff in effectifs.items()])}
| Total  | {total}     |

Calcule les fréquences {format_text} de chaque valeur.
Tu peux utiliser la formule : fréquence = effectif / total
ou le produit en croix."""

        return {
            "type": "frequence",
            "type_name": "Calcul de fréquences",
            "question": question,
            "exercise_data": {
                "effectifs": effectifs,
                "total": total,
                "format": format_type,
            },
            "expected_answer": f"Fréquences ({format_type}): {frequences}",
            "exercise_info": f"Total: {total}, Format demandé: {format_type}",
        }

    def _generate_moyenne_fallback(self, difficulty: str) -> Dict[str, Any]:
        """Génère un exercice de moyenne (fallback)"""

        if difficulty == "facile":
            data = {10: 2, 11: 3, 12: 5}
        elif difficulty == "moyen":
            data = {10: 3, 11: 4, 12: 5, 13: 3}
        else:
            data = {8: 2, 9: 3, 10: 4, 11: 5, 12: 6, 13: 4}

        somme_produits = sum(valeur * effectif for valeur, effectif in data.items())
        total_effectifs = sum(data.values())
        moyenne = round(somme_produits / total_effectifs, 2)

        question = f"""Calcule la moyenne pondérée de la série statistique suivante :

| Valeur | Effectif |
|--------|----------|
{chr(10).join([f"| {val}      | {eff}      |" for val, eff in data.items()])}
| Total  | {sum(data.values())}     |

Utilise la formule : Moyenne = (Σ valeur × effectif) / total des effectifs"""

        return {
            "type": "moyenne",
            "type_name": "Moyenne pondérée",
            "question": question,
            "exercise_data": {"data": data, "total": total_effectifs},
            "expected_answer": f"Moyenne = {moyenne}",
            "exercise_info": f"Calcul: ({' + '.join([f'{v}×{e}' for v, e in data.items()])}) / {total_effectifs} = {moyenne}",
        }

    def _generate_probleme_fallback(self, difficulty: str) -> Dict[str, Any]:
        """Génère un problème textuel (fallback)"""

        problemes = {
            "facile": {
                "question": """Dans une classe de 3ème, on a relevé les notes suivantes à un contrôle :
10, 12, 10, 14, 12, 10, 12, 14, 10, 12

1. Complète le tableau d'effectifs
2. Calcule la moyenne de la classe
3. Quelle est la note la plus fréquente ?""",
                "data": [10, 12, 10, 14, 12, 10, 12, 14, 10, 12],
                "expected": {
                    "effectifs": {10: 4, 12: 4, 14: 2},
                    "moyenne": 11.6,
                    "note_frequente": 10,
                },
            },
            "moyen": {
                "question": """Un professeur a relevé les tailles (en cm) de ses 20 élèves de 3ème :
150, 152, 150, 155, 152, 150, 152, 155, 150, 152,
158, 160, 158, 155, 160, 158, 160, 155, 158, 160

1. Construis le tableau d'effectifs
2. Calcule les fréquences en pourcentage
3. Calcule la taille moyenne de la classe
4. Interprète tes résultats""",
                "data": [
                    150,
                    152,
                    150,
                    155,
                    152,
                    150,
                    152,
                    155,
                    150,
                    152,
                    158,
                    160,
                    158,
                    155,
                    160,
                    158,
                    160,
                    155,
                    158,
                    160,
                ],
                "expected": {
                    "effectifs": {150: 4, 152: 4, 155: 4, 158: 4, 160: 4},
                    "frequences_pct": {150: 20, 152: 20, 155: 20, 158: 20, 160: 20},
                    "moyenne": 155.5,
                },
            },
            "difficile": {
                "question": """Un club de sport organise un tournoi. Voici les âges des participants :
12, 13, 12, 14, 13, 12, 13, 14, 12, 13, 15, 14, 13, 15, 14, 13, 15, 14, 13, 15

1. Construis le tableau d'effectifs et de fréquences (en pourcentage)
2. Calcule l'âge moyen des participants
3. Le club veut organiser deux groupes : un pour les moins de 14 ans et un pour les 14 ans et plus.
   Combien de participants dans chaque groupe ?
4. Quelle proportion (en pourcentage) représente chaque groupe ?""",
                "data": [
                    12,
                    13,
                    12,
                    14,
                    13,
                    12,
                    13,
                    14,
                    12,
                    13,
                    15,
                    14,
                    13,
                    15,
                    14,
                    13,
                    15,
                    14,
                    13,
                    15,
                ],
                "expected": {
                    "effectifs": {12: 4, 13: 7, 14: 5, 15: 4},
                    "moyenne": 13.5,
                    "moins_14": 11,
                    "plus_14": 9,
                },
            },
        }

        probleme = problemes.get(difficulty, problemes["moyen"])

        return {
            "type": "probleme",
            "type_name": "Problème textuel",
            "question": probleme["question"],
            "exercise_data": {"data": probleme["data"], "difficulty": difficulty},
            "expected_answer": f"Réponses attendues: {probleme['expected']}",
            "exercise_info": f"Problème de niveau {difficulty} avec {len(probleme['data'])} données",
        }

    def _init_fallback_exercises(self) -> Dict[str, Any]:
        """Initialise les exercices de secours"""
        return {}
