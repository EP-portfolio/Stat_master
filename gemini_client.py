"""
Client pour interagir avec Gemini 3 Pro API
Gère la vision (analyse d'images) et le raisonnement mathématique
"""

import os
import google.generativeai as genai
from typing import Optional, Dict, Any, List
from PIL import Image
import io
import base64


class GeminiClient:
    """Client pour Gemini 3 Pro avec support de la vision"""

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialise le client Gemini

        Args:
            api_key: Clé API Gemini (ou depuis variable d'environnement)
        """
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError(
                "Clé API Gemini non trouvée. "
                "Définissez GEMINI_API_KEY dans vos variables d'environnement"
            )

        genai.configure(api_key=self.api_key)

        # Utiliser Gemini 3 Pro (ou le modèle disponible)
        # Essayer différents modèles dans l'ordre de préférence
        models_to_try = [
            "gemini-2.0-flash-exp",
            "gemini-1.5-pro",
            "gemini-1.5-flash",
            "gemini-pro",
        ]

        self.model = None
        for model_name in models_to_try:
            try:
                self.model = genai.GenerativeModel(model_name)
                break
            except Exception:
                continue

        if self.model is None:
            # Utiliser le modèle par défaut
            self.model = genai.GenerativeModel("gemini-1.5-flash")

    def analyze_handwritten_solution(
        self,
        image: Image.Image,
        exercise_type: str,
        exercise_data: Dict[str, Any],
        question: str,
        student_history: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Analyse une copie manuscrite d'un élève avec raisonnement multi-étapes

        Args:
            image: Image PIL de la copie de l'élève
            exercise_type: Type d'exercice (effectif, frequence, moyenne, probleme)
            exercise_data: Données de l'exercice (réponse attendue, etc.)
            question: Question posée à l'élève
            student_history: Historique de l'élève pour personnalisation

        Returns:
            Dictionnaire avec feedback, erreurs, bons points, correction, analyse_detailed
        """

        # Étape 1: Analyse de la démarche (raisonnement multi-étapes)
        step1_prompt = self._build_step_analysis_prompt(
            exercise_type, exercise_data, question, student_history
        )

        try:
            # Analyser l'image avec Gemini - Étape 1: Extraction de la démarche
            response_step1 = self.model.generate_content([step1_prompt, image])
            step1_analysis = self._parse_step_analysis(response_step1.text)

            # Étape 2: Analyse détaillée avec la démarche extraite
            step2_prompt = self._build_detailed_analysis_prompt(
                exercise_type,
                exercise_data,
                question,
                step1_analysis,
                student_history,
            )
            response_step2 = self.model.generate_content([step2_prompt, image])

            # Parser la réponse finale
            feedback = self._parse_feedback(response_step2.text)
            feedback["step_analysis"] = step1_analysis
            feedback["reasoning_steps"] = step1_analysis.get("steps", [])

            return feedback

        except Exception as e:
            return {
                "error": f"Erreur lors de l'analyse: {str(e)}",
                "feedback": "",
                "errors": [],
                "good_points": [],
                "correction": "",
                "step_analysis": {},
                "reasoning_steps": [],
            }

    def _build_analysis_prompt(
        self, exercise_type: str, exercise_data: Dict[str, Any], question: str
    ) -> str:
        """Construit le prompt d'analyse selon le type d'exercice"""

        base_prompt = f"""Tu es un professeur de mathématiques de 3ème qui corrige un exercice de statistiques avec bienveillance et pédagogie.

QUESTION POSÉE À L'ÉLÈVE:
{question}

TYPE D'EXERCICE: {exercise_data.get('type_name', exercise_type)}

RÉPONSE ATTENDUE:
{exercise_data.get('expected_answer', 'N/A')}

DONNÉES DE L'EXERCICE:
{exercise_data.get('exercise_info', '')}

INSTRUCTIONS POUR L'ANALYSE:
1. Analyse attentivement la copie manuscrite de l'élève
2. Identifie la démarche utilisée par l'élève (même si elle diffère de la méthode attendue)
3. Détecte les erreurs de manière constructive (calculs, raisonnement, méthode, présentation)
4. Souligne TOUS les bons points (méthode correcte, calculs justes, présentation claire, effort visible)
5. Propose une correction complète et pédagogique étape par étape
6. Sois encourageant et bienveillant dans ton feedback

IMPORTANT: Réponds UNIQUEMENT en JSON valide, sans texte avant ou après.

FORMAT DE RÉPONSE (JSON strict):
{{
    "feedback": "Commentaire général bienveillant sur la copie (2-3 phrases)",
    "errors": ["description précise de l'erreur 1", "description précise de l'erreur 2"],
    "good_points": ["point positif 1 avec détails", "point positif 2 avec détails"],
    "correction": "Correction détaillée étape par étape avec explications pédagogiques",
    "score": "Note sur 20 (ex: 15/20) ou évaluation qualitative (ex: Très bien, Bien, Assez bien, À revoir)"
}}
"""

        # Ajouter des instructions spécifiques selon le type
        if exercise_type == "effectif":
            base_prompt += """
ATTENTION SPÉCIALE:
- Vérifier que tous les effectifs sont corrects
- Vérifier que le total correspond bien
- Vérifier la présentation du tableau
"""
        elif exercise_type == "frequence":
            base_prompt += """
ATTENTION SPÉCIALE:
- Vérifier l'utilisation de la formule ou du produit en croix
- Vérifier le format des fréquences (décimal, fraction, pourcentage)
- Vérifier que la somme des fréquences fait 1 (ou 100%)
"""
        elif exercise_type == "moyenne":
            base_prompt += """
ATTENTION SPÉCIALE:
- Vérifier la formule de la moyenne pondérée
- Vérifier les calculs intermédiaires
- Vérifier le résultat final
"""
        elif exercise_type == "probleme":
            base_prompt += """
ATTENTION SPÉCIALE:
- Vérifier la compréhension du problème
- Vérifier la méthode de résolution
- Vérifier les calculs et l'interprétation du résultat
"""

        return base_prompt

    def _build_step_analysis_prompt(
        self,
        exercise_type: str,
        exercise_data: Dict[str, Any],
        question: str,
        student_history: Optional[Dict[str, Any]] = None,
    ) -> str:
        """Construit le prompt pour l'analyse étape par étape de la démarche"""

        history_context = ""
        if student_history:
            history_context = f"""
CONTEXTE DE L'ÉLÈVE:
- Difficultés précédentes: {student_history.get('common_errors', [])}
- Points forts: {student_history.get('strengths', [])}
- Niveau moyen: {student_history.get('average_score', 'Non défini')}
"""

        return f"""Tu es un expert en analyse pédagogique. Analyse la copie manuscrite étape par étape.

QUESTION: {question}
TYPE: {exercise_data.get('type_name', exercise_type)}
{history_context}

INSTRUCTIONS:
1. Identifie TOUTES les étapes de la démarche de l'élève (même partielles ou erronées)
2. Pour chaque étape, note si elle est correcte, incorrecte, ou partielle
3. Identifie les erreurs de raisonnement (pas seulement de calcul)
4. Note les méthodes alternatives utilisées

Réponds en JSON:
{{
    "steps": [
        {{
            "step_number": 1,
            "description": "Description de l'étape identifiée",
            "status": "correct|incorrect|partial",
            "student_work": "Ce que l'élève a écrit/fait",
            "reasoning": "Analyse du raisonnement de l'élève"
        }}
    ],
    "method_used": "Description de la méthode utilisée par l'élève",
    "alternative_methods": ["Autres méthodes possibles"],
    "reasoning_errors": ["Erreurs de raisonnement identifiées"]
}}"""

    def _build_detailed_analysis_prompt(
        self,
        exercise_type: str,
        exercise_data: Dict[str, Any],
        question: str,
        step_analysis: Dict[str, Any],
        student_history: Optional[Dict[str, Any]] = None,
    ) -> str:
        """Construit le prompt pour l'analyse détaillée avec la démarche extraite"""

        steps_text = "\n".join(
            [
                f"Étape {s.get('step_number', i+1)}: {s.get('description', '')} - {s.get('status', '')}"
                for i, s in enumerate(step_analysis.get("steps", []))
            ]
        )

        return f"""Tu es un professeur de mathématiques de 3ème qui corrige avec bienveillance.

QUESTION: {question}
TYPE: {exercise_data.get('type_name', exercise_type)}
RÉPONSE ATTENDUE: {exercise_data.get('expected_answer', 'N/A')}

DÉMARCHE IDENTIFIÉE DE L'ÉLÈVE:
{steps_text}

MÉTHODE UTILISÉE: {step_analysis.get('method_used', 'Non identifiée')}
ERREURS DE RAISONNEMENT: {', '.join(step_analysis.get('reasoning_errors', []))}

INSTRUCTIONS:
1. Utilise l'analyse de la démarche pour donner un feedback précis
2. Pour chaque étape incorrecte, explique pourquoi et comment corriger
3. Valorise les étapes correctes et les bonnes méthodes
4. Propose une correction qui suit la logique de l'élève quand c'est possible
5. Adapte le niveau d'explication selon les difficultés identifiées

Réponds en JSON:
{{
    "feedback": "Commentaire général bienveillant (2-3 phrases)",
    "errors": ["erreur 1 avec contexte", "erreur 2 avec contexte"],
    "good_points": ["point positif 1 détaillé", "point positif 2 détaillé"],
    "correction": "Correction détaillée étape par étape avec explications",
    "score": "Note sur 20 ou évaluation qualitative",
    "next_steps": ["Recommandations pour progresser"],
    "personalized_tips": ["Conseils personnalisés basés sur les erreurs"]
}}"""

    def _parse_step_analysis(self, response_text: str) -> Dict[str, Any]:
        """Parse l'analyse étape par étape"""

        import json
        import re

        json_match = re.search(
            r"\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}", response_text, re.DOTALL
        )

        if json_match:
            try:
                json_str = json_match.group()
                json_str = re.sub(r"```json\s*", "", json_str)
                json_str = re.sub(r"```\s*", "", json_str)
                return json.loads(json_str)
            except (json.JSONDecodeError, AttributeError):
                pass

        return {"steps": [], "method_used": "", "reasoning_errors": []}

    def _parse_exercise(self, response_text: str, exercise_type: str) -> Dict[str, Any]:
        """Parse la réponse de Gemini pour extraire l'exercice généré"""

        import json
        import re

        json_match = re.search(
            r"\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}", response_text, re.DOTALL
        )

        if json_match:
            try:
                json_str = json_match.group()
                json_str = re.sub(r"```json\s*", "", json_str)
                json_str = re.sub(r"```\s*", "", json_str)
                exercise_data = json.loads(json_str)

                return {
                    "type": exercise_type,
                    "type_name": exercise_data.get("type_name", exercise_type),
                    "question": exercise_data.get("question", ""),
                    "exercise_data": exercise_data,
                    "expected_answer": str(exercise_data.get("expected_answer", "")),
                    "exercise_info": str(exercise_data),
                }
            except (json.JSONDecodeError, AttributeError):
                pass

        # Fallback: retourner un exercice basique
        return {
            "type": exercise_type,
            "type_name": exercise_type,
            "question": response_text[:500],
            "exercise_data": {},
            "expected_answer": "",
            "exercise_info": "",
        }

    def _parse_feedback(self, response_text: str) -> Dict[str, Any]:
        """Parse la réponse de Gemini pour extraire le feedback structuré"""

        import json
        import re

        # Essayer d'extraire le JSON de la réponse (plusieurs tentatives)
        # Pattern 1: JSON entre accolades
        json_match = re.search(
            r"\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}", response_text, re.DOTALL
        )

        if json_match:
            try:
                json_str = json_match.group()
                # Nettoyer le JSON (enlever les markdown code blocks)
                json_str = re.sub(r"```json\s*", "", json_str)
                json_str = re.sub(r"```\s*", "", json_str)
                feedback_data = json.loads(json_str)

                # S'assurer que tous les champs sont présents
                return {
                    "feedback": feedback_data.get("feedback", response_text),
                    "errors": feedback_data.get("errors", []),
                    "good_points": feedback_data.get("good_points", []),
                    "correction": feedback_data.get("correction", ""),
                    "score": feedback_data.get("score", "Non évalué"),
                    "next_steps": feedback_data.get("next_steps", []),
                    "personalized_tips": feedback_data.get("personalized_tips", []),
                }
            except (json.JSONDecodeError, AttributeError):
                pass

        # Si pas de JSON valide, parser manuellement avec regex
        errors = re.findall(
            r"(?:erreur|Erreur|❌)[:\-]?\s*(.+?)(?:\n|$)", response_text, re.IGNORECASE
        )
        good_points = re.findall(
            r"(?:bon|positif|✅|✓)[:\-]?\s*(.+?)(?:\n|$)", response_text, re.IGNORECASE
        )

        return {
            "feedback": (
                response_text[:500] + "..."
                if len(response_text) > 500
                else response_text
            ),
            "errors": errors[:10] if errors else [],
            "good_points": good_points[:10] if good_points else [],
            "correction": response_text,
            "score": "Non évalué",
            "next_steps": [],
            "personalized_tips": [],
        }

    def generate_exercise(
        self, exercise_type: str, difficulty: str = "moyen"
    ) -> Dict[str, Any]:
        """
        Génère un exercice de statistiques avec Gemini

        Args:
            exercise_type: Type d'exercice (effectif, frequence, moyenne, probleme)
            difficulty: Niveau de difficulté (facile, moyen, difficile)

        Returns:
            Dictionnaire avec question, données, réponse attendue
        """

        prompt = self._build_exercise_prompt(exercise_type, difficulty)

        try:
            response = self.model.generate_content(prompt)
            # Parser la réponse pour extraire l'exercice
            exercise = self._parse_exercise(response.text, exercise_type)
            return exercise
        except Exception as e:
            return {
                "error": f"Erreur lors de la génération: {str(e)}",
                "question": "",
                "exercise_data": {},
            }

    def _build_exercise_prompt(self, exercise_type: str, difficulty: str) -> str:
        """Construit le prompt pour générer un exercice avec Gemini"""

        base_instruction = f"""Tu es un professeur de mathématiques créatif qui génère des exercices de statistiques pour des élèves de 3ème.

Niveau de difficulté: {difficulty}
- Facile: 8-12 valeurs, nombres simples (10-15)
- Moyen: 12-18 valeurs, nombres variés (8-16)
- Difficile: 18-25 valeurs, nombres plus variés (5-20)

IMPORTANT: Génère un exercice ORIGINAL et VARIÉ. Ne répète pas toujours les mêmes exemples.
Utilise des contextes différents (notes, tailles, âges, températures, etc.).

Réponds UNIQUEMENT en JSON valide, sans texte avant ou après."""

        prompts = {
            "effectif": f"""{base_instruction}

Type d'exercice: Tableau d'effectifs

Génère un exercice où:
1. Tu fournis une liste de valeurs d'un caractère (choisis un contexte intéressant: notes, tailles, âges, etc.)
2. L'élève doit compléter un tableau d'effectifs
3. L'exercice est adapté au niveau 3ème et à la difficulté {difficulty}

Format JSON:
{{
    "question": "Énoncé complet et clair de l'exercice avec contexte",
    "data": ["valeur1", "valeur2", ...],
    "expected_answer": {{
        "tableau": {{"valeur1": effectif1, "valeur2": effectif2, ...}},
        "total": nombre_total
    }},
    "type_name": "Tableau d'effectifs",
    "context": "Description du contexte (ex: notes d'un contrôle)"
}}""",
            "frequence": f"""{base_instruction}

Type d'exercice: Calcul de fréquences

Génère un exercice où:
1. Tu fournis un tableau d'effectifs (choisis un format: décimal, fraction, ou pourcentage)
2. L'élève doit calculer les fréquences
3. L'exercice permet l'utilisation de la formule ou du produit en croix
4. L'exercice est adapté au niveau 3ème et à la difficulté {difficulty}

Format JSON:
{{
    "question": "Énoncé complet avec tableau d'effectifs et demande de calcul",
    "data": {{"valeur1": effectif1, "valeur2": effectif2, ...}},
    "total": nombre_total,
    "expected_answer": {{
        "frequences": {{"valeur1": freq1, "valeur2": freq2, ...}},
        "format": "decimal|fraction|pourcentage"
    }},
    "type_name": "Calcul de fréquences",
    "context": "Description du contexte"
}}""",
            "moyenne": f"""{base_instruction}

Type d'exercice: Moyenne pondérée

Génère un exercice où:
1. Tu fournis une série statistique avec effectifs (choisis un contexte intéressant)
2. L'élève doit calculer la moyenne pondérée
3. L'exercice est adapté au niveau 3ème et à la difficulté {difficulty}

Format JSON:
{{
    "question": "Énoncé complet avec série statistique et demande de calcul",
    "data": {{"valeur1": effectif1, "valeur2": effectif2, ...}},
    "expected_answer": {{
        "moyenne": valeur_moyenne,
        "calculs": "détail des calculs étape par étape"
    }},
    "type_name": "Moyenne pondérée",
    "context": "Description du contexte"
}}""",
            "probleme": f"""{base_instruction}

Type d'exercice: Problème textuel de statistiques

Génère un problème où:
1. C'est une situation concrète et réaliste (choisis un contexte varié: sport, école, vie quotidienne, etc.)
2. Le problème implique des calculs statistiques (moyenne, effectifs, fréquences)
3. Le problème demande une interprétation du résultat
4. Le problème est adapté au niveau 3ème et à la difficulté {difficulty}

Format JSON:
{{
    "question": "Énoncé complet du problème avec situation concrète",
    "data": "liste des données fournies dans le problème",
    "expected_answer": {{
        "reponse": "réponse attendue",
        "calculs": "détail des calculs étape par étape",
        "interpretation": "interprétation du résultat dans le contexte"
    }},
    "type_name": "Problème textuel",
    "context": "Description du contexte du problème"
}}""",
        }

        return prompts.get(exercise_type, prompts["effectif"])

    def analyze_exercise_examples(
        self, images: List[Image.Image], chapter: str = "statistiques"
    ) -> Dict[str, Any]:
        """
        Analyse plusieurs exemples d'exercices pour vérifier leur complétude
        et leur lien avec le chapitre

        Args:
            images: Liste d'images PIL d'exercices (3-10 images)
            chapter: Nom du chapitre (par défaut "statistiques")

        Returns:
            Dictionnaire avec validation, analyse et exemples extraits
        """

        if len(images) < 3 or len(images) > 10:
            return {
                "valid": False,
                "error": f"Nombre d'images invalide: {len(images)}. Attendu: 3-10",
                "examples": [],
            }

        prompt = self._build_examples_analysis_prompt(chapter, len(images))

        try:
            # Analyser toutes les images ensemble
            response = self.model.generate_content([prompt] + images)
            analysis = self._parse_examples_analysis(response.text)

            return analysis

        except Exception as e:
            return {
                "valid": False,
                "error": f"Erreur lors de l'analyse: {str(e)}",
                "examples": [],
            }

    def _build_examples_analysis_prompt(self, chapter: str, num_images: int) -> str:
        """Construit le prompt pour analyser les exemples d'exercices"""

        return f"""Tu es un expert en pédagogie mathématique. Analyse ces {num_images} exemples d'exercices de statistiques de niveau 3ème.

CHAPITRE: {chapter}

INSTRUCTIONS:
1. Pour chaque image, identifie:
   - Le type d'exercice (effectif, frequence, moyenne, probleme)
   - L'énoncé complet de l'exercice
   - Si l'exercice est complet (énoncé + données + question claire)
   - Le niveau de difficulté (facile, moyen, difficile)
   - Le contexte (notes, tailles, âges, etc.)

2. Vérifie que tous les exercices sont:
   - En lien avec le chapitre des statistiques
   - Adaptés au niveau 3ème
   - Complets (énoncé, données, question)

3. Extrais les caractéristiques communes:
   - Styles d'énoncés
   - Types de contextes utilisés
   - Formats de présentation
   - Niveaux de difficulté

Réponds UNIQUEMENT en JSON valide:

{{
    "valid": true/false,
    "validation_errors": ["erreur 1", "erreur 2"] si valid=false,
    "examples": [
        {{
            "exercise_number": 1,
            "type": "effectif|frequence|moyenne|probleme",
            "question": "Énoncé complet de l'exercice",
            "context": "Description du contexte",
            "difficulty": "facile|moyen|difficile",
            "is_complete": true/false,
            "data": "Données de l'exercice si visible"
        }}
    ],
    "common_characteristics": {{
        "styles": ["style 1", "style 2"],
        "contexts": ["contexte 1", "contexte 2"],
        "formats": ["format 1", "format 2"],
        "difficulty_range": "facile à difficile"
    }},
    "recommendations": "Recommandations pour générer des exercices similaires"
}}"""

    def _parse_examples_analysis(self, response_text: str) -> Dict[str, Any]:
        """Parse l'analyse des exemples d'exercices"""

        import json
        import re

        json_match = re.search(
            r"\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}", response_text, re.DOTALL
        )

        if json_match:
            try:
                json_str = json_match.group()
                json_str = re.sub(r"```json\s*", "", json_str)
                json_str = re.sub(r"```\s*", "", json_str)
                analysis = json.loads(json_str)

                # S'assurer que tous les champs sont présents
                return {
                    "valid": analysis.get("valid", False),
                    "validation_errors": analysis.get("validation_errors", []),
                    "examples": analysis.get("examples", []),
                    "common_characteristics": analysis.get(
                        "common_characteristics", {}
                    ),
                    "recommendations": analysis.get("recommendations", ""),
                }
            except (json.JSONDecodeError, AttributeError) as e:
                return {
                    "valid": False,
                    "error": f"Erreur de parsing JSON: {str(e)}",
                    "examples": [],
                }

        return {
            "valid": False,
            "error": "Format de réponse invalide",
            "examples": [],
        }

    def generate_exercise_from_examples(
        self,
        exercise_type: str,
        difficulty: str,
        examples_analysis: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Génère un exercice en s'inspirant des exemples fournis
        (mais sans les reproduire à l'identique)

        Args:
            exercise_type: Type d'exercice souhaité
            difficulty: Niveau de difficulté
            examples_analysis: Analyse des exemples d'exercices

        Returns:
            Dictionnaire avec l'exercice généré
        """

        prompt = self._build_exercise_from_examples_prompt(
            exercise_type, difficulty, examples_analysis
        )

        try:
            response = self.model.generate_content(prompt)
            exercise = self._parse_exercise(response.text, exercise_type)
            exercise["inspired_by_examples"] = True
            return exercise
        except Exception as e:
            return {
                "error": f"Erreur lors de la génération: {str(e)}",
                "question": "",
                "exercise_data": {},
            }

    def _build_exercise_from_examples_prompt(
        self,
        exercise_type: str,
        difficulty: str,
        examples_analysis: Dict[str, Any],
    ) -> str:
        """Construit le prompt pour générer un exercice inspiré des exemples"""

        examples_text = "\n".join(
            [
                f"Exemple {i+1} ({ex.get('type', 'inconnu')}): {ex.get('question', '')[:200]}"
                for i, ex in enumerate(examples_analysis.get("examples", [])[:5])
            ]
        )

        characteristics = examples_analysis.get("common_characteristics", {})
        styles = ", ".join(characteristics.get("styles", []))
        contexts = ", ".join(characteristics.get("contexts", []))

        return f"""Tu es un professeur de mathématiques créatif. Génère un NOUVEL exercice de statistiques de niveau 3ème.

TYPE D'EXERCICE DEMANDÉ: {exercise_type}
DIFFICULTÉ: {difficulty}

EXEMPLES DE RÉFÉRENCE (à utiliser comme inspiration, PAS à reproduire):
{examples_text}

CARACTÉRISTIQUES COMMUNES DES EXEMPLES:
- Styles: {styles}
- Contextes: {contexts}
- Formats: {', '.join(characteristics.get('formats', []))}

INSTRUCTIONS IMPORTANTES:
1. Inspire-toi du STYLE et du FORMAT des exemples
2. Utilise des CONTEXTES similaires mais différents
3. Crée un exercice NOUVEAU et ORIGINAL (pas une copie)
4. Adapte au niveau 3ème et à la difficulté {difficulty}
5. Assure-toi que l'exercice est complet et clair

Réponds UNIQUEMENT en JSON valide:

{{
    "question": "Énoncé complet et original de l'exercice",
    "data": "données de l'exercice",
    "expected_answer": {{"réponse": "réponse attendue"}},
    "type_name": "{exercise_type}",
    "context": "Description du contexte utilisé"
}}"""
