"""
Application Streamlit pour exercices de mathématiques - Statistiques niveau 3ème
Compétition Kaggle: Vibe Code with Gemini 3 Pro
Version améliorée avec navigation par onglets (inspirée de l'app React AI Studio)
"""

import streamlit as st
import os
import random
import pandas as pd
from PIL import Image
from dotenv import load_dotenv
from gemini_client import GeminiClient
from exercise_generator import ExerciseGenerator
from student_profile import StudentProfile
from email_notifier import EmailNotifier
import json

# Charger les variables d'environnement
load_dotenv()

# Configuration de la page (sidebar masquée par défaut)
st.set_page_config(
    page_title="Stat'Master 3ème - Statistiques",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Styles globaux (amélioration UI)
st.markdown(
    """
    <style>
    :root {
        --primary: #4f46e5;
        --bg: #f6f7fb;
        --card: #ffffff;
        --border: #e5e7eb;
    }
    body {
        background: var(--bg);
    }
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 1.5rem;
        max-width: 1100px;
        margin: 0 auto;
    }
    .stButton>button, .stDownloadButton>button {
        background: var(--primary);
        color: #fff;
        border: none;
        padding: 0.65rem 1.1rem;
        border-radius: 10px;
        font-weight: 600;
    }
    .stButton>button:hover {
        background: #4338ca;
    }
    .card {
        background: var(--card);
        border: 1px solid var(--border);
        border-radius: 14px;
        padding: 1.25rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    }
    /* Toolbar nav */
    .nav-row {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
        gap: 0.5rem;
        margin: 0.5rem 0 1rem;
    }
    .nav-btn button {
        width: 100%;
        border: 1px solid var(--border);
        background: #fff;
        color: #111827;
    }
    .nav-btn button:hover {
        border-color: var(--primary);
        color: var(--primary);
    }
    .nav-btn.active button {
        background: var(--primary);
        color: #fff;
        border-color: var(--primary);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Initialisation de la session state
if "current_exercise" not in st.session_state:
    st.session_state.current_exercise = None
if "exercise_history" not in st.session_state:
    st.session_state.exercise_history = []
if "gemini_client" not in st.session_state:
    st.session_state.gemini_client = None
if "feedback" not in st.session_state:
    st.session_state.feedback = None
if "student_profile" not in st.session_state:
    st.session_state.student_profile = StudentProfile()
if "use_personalization" not in st.session_state:
    st.session_state.use_personalization = True
if "exercise_examples" not in st.session_state:
    st.session_state.exercise_examples = []
if "examples_analysis" not in st.session_state:
    st.session_state.examples_analysis = None
if "email_notifier" not in st.session_state:
    st.session_state.email_notifier = None
if "parent_email" not in st.session_state:
    st.session_state.parent_email = None
if "student_name" not in st.session_state:
    st.session_state.student_name = None
if "session_exercises" not in st.session_state:
    st.session_state.session_exercises = []
if "current_tab" not in st.session_state:
    st.session_state.current_tab = "Accueil"
if "practice_dataset" not in st.session_state:
    st.session_state.practice_dataset = None
if "practice_feedback" not in st.session_state:
    st.session_state.practice_feedback = {"mean": None, "median": None, "range": None}
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = [
        {
            "role": "model",
            "text": "Bonjour ! Je suis ton tuteur de maths. Je suis là pour t'aider avec les statistiques. Tu ne comprends pas la médiane ? Tu veux un exemple ? Dis-moi tout !",
        }
    ]


def initialize_gemini():
    """Initialise le client Gemini"""
    if st.session_state.gemini_client is None:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            api_key = st.sidebar.text_input(
                "🔑 Clé API Gemini",
                type="password",
                help="Entrez votre clé API Gemini. Obtenez-la sur https://makersuite.google.com/app/apikey",
            )
            if api_key:
                os.environ["GEMINI_API_KEY"] = api_key

        if api_key:
            try:
                st.session_state.gemini_client = GeminiClient(api_key=api_key)
                st.session_state.exercise_generator = ExerciseGenerator(
                    st.session_state.gemini_client
                )
                return True
            except Exception as e:
                st.error(f"Erreur d'initialisation: {str(e)}")
                return False
    return st.session_state.gemini_client is not None


def generate_random_dataset(size=None, min_val=0, max_val=20):
    """Génère un dataset aléatoire pour l'entraînement"""
    if size is None:
        size = random.randint(5, 15)

    values = [random.randint(min_val, max_val) for _ in range(size)]
    sorted_values = sorted(values)
    total_count = len(values)

    # Calculer la moyenne
    mean = round(sum(values) / total_count, 2)

    # Calculer la médiane
    mid = total_count // 2
    if total_count % 2 == 0:
        median = (sorted_values[mid - 1] + sorted_values[mid]) / 2
    else:
        median = sorted_values[mid]

    # Calculer l'étendue
    range_val = sorted_values[-1] - sorted_values[0]

    return {
        "values": values,
        "sorted_values": sorted_values,
        "mean": mean,
        "median": median,
        "range": range_val,
        "total_count": total_count,
    }


def get_frequency_data(values):
    """Calcule les fréquences pour un graphique"""
    freq_map = {}
    for v in values:
        freq_map[v] = freq_map.get(v, 0) + 1

    return pd.DataFrame(
        [{"Valeur": k, "Effectif": v} for k, v in sorted(freq_map.items())]
    )


def render_home():
    """Page d'accueil"""
    st.markdown(
        """
    <div style="text-align: center; padding: 1.5rem 0;">
        <h1 style="font-size: 2.7rem; margin-bottom: 0.5rem; color:#0f172a;">
            Maîtrise les <span style="color: #4f46e5;">Statistiques</span>
        </h1>
        <p style="font-size: 1.05rem; color: #475569; max-width: 680px; margin: 0 auto;">
            Tout ce qu'il te faut pour réussir le brevet : cours clairs, entraînement rapide, correction IA étape par étape, et bilan parent.
        </p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # Barre de navigation sans sidebar
    st.markdown("<div class='nav-row'>", unsafe_allow_html=True)
    tabs = [
        ("Accueil", "🏠 Accueil"),
        ("Cours", "📚 Cours"),
        ("Entraînement", "🎯 Entraînement"),
        ("Exercices IA", "📝 Exercices IA"),
        ("Tuteur IA", "🤖 Tuteur IA"),
    ]
    cols = st.columns(len(tabs))
    for i, (tab_key, label) in enumerate(tabs):
        with cols[i]:
            btn = st.button(label, key=f"nav_{tab_key}", use_container_width=True)
            if btn:
                st.session_state.current_tab = tab_key
                st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    # Actions rapides et configuration parent sur la même page
    st.divider()
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("<h4>Choisis ce que tu veux faire :</h4>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            if st.button("📚 Lire le cours", use_container_width=True):
                st.session_state.current_tab = "Cours"
                st.rerun()
        with c2:
            if st.button("🎯 S'entraîner", use_container_width=True):
                st.session_state.current_tab = "Entraînement"
                st.rerun()
        st.divider()
        c3, c4 = st.columns(2)
        with c3:
            st.markdown(
                "<div class='card'><h4>Mode Évaluation</h4><p>Teste tes compétences, correction photo par IA.</p></div>",
                unsafe_allow_html=True,
            )
            if st.button("Lancer une évaluation", use_container_width=True):
                st.session_state.current_tab = "Exercices IA"
                st.rerun()
        with c4:
            st.markdown(
                "<div class='card'><h4>Tuteur IA</h4><p>Pose tes questions, l'IA te guide pas à pas.</p></div>",
                unsafe_allow_html=True,
            )
            if st.button("Accéder au tuteur", use_container_width=True):
                st.session_state.current_tab = "Tuteur IA"
                st.rerun()

    with col2:
        st.markdown(
            "<div class='card'><h4>Configuration Parent</h4><p>Email pour recevoir le bilan de session.</p></div>",
            unsafe_allow_html=True,
        )
        student_name = st.text_input("Prénom de l'élève", value=st.session_state.student_name or "")
        if student_name:
            st.session_state.student_name = student_name
        parent_email = st.text_input("Email du parent", value=st.session_state.parent_email or "")
        if parent_email:
            st.session_state.parent_email = parent_email
        st.caption("L'email est utilisé pour envoyer le bilan après une session.")


def render_lessons():
    """Section Cours"""
    st.header("📚 Cours de Statistiques")

    lessons = {
        "La Moyenne": {
            "description": "Comment calculer la moyenne d'une série statistique.",
            "content": """
            La **moyenne** d'une série statistique est le quotient de la somme de toutes les valeurs par l'effectif total.
            
            **Formule :**
            ```
            M = (v₁ + v₂ + ... + vₙ) / N
            ```
            Où *v* sont les valeurs et *N* est le nombre total de valeurs.
            
            **Exemple :**
            Notes d'un élève : 12, 15, 8, 14, 11
            
            - Somme = 12 + 15 + 8 + 14 + 11 = 60
            - Effectif total = 5 notes
            - **Moyenne = 60 / 5 = 12**
            """,
        },
        "La Médiane": {
            "description": "La valeur centrale qui partage la série en deux groupes égaux.",
            "content": """
            La **médiane** est la valeur qui partage la série statistique **ordonnée** (classée du plus petit au plus grand) en deux groupes de même effectif.
            
            **Méthode :**
            1. Ordonner les valeurs par ordre croissant.
            2. Si l'effectif total N est **impair** : la médiane est la valeur centrale.
            3. Si l'effectif total N est **pair** : la médiane est la moyenne des deux valeurs centrales.
            
            **Exemples :**
            
            *Cas Impair (5 valeurs) :* 8, 11, **12**, 14, 15
            - La médiane est 12 (la 3ème valeur).
            
            *Cas Pair (6 valeurs) :* 8, 11, **12, 13**, 15, 18
            - Médiane = (12 + 13) / 2 = **12,5**
            """,
        },
        "L'Étendue": {
            "description": "Mesurer la dispersion des valeurs.",
            "content": """
            L'**étendue** d'une série statistique est la différence entre la plus grande valeur et la plus petite valeur.
            
            **Formule :**
            ```
            E = Max - Min
            ```
            
            Plus l'étendue est grande, plus les valeurs sont dispersées.
            """,
        },
    }

    for title, lesson in lessons.items():
        with st.expander(
            f"📖 {title} - {lesson['description']}", expanded=(title == "La Moyenne")
        ):
            st.markdown(lesson["content"])


def render_practice():
    """Section Entraînement rapide"""
    st.header("🎯 Entraînement")

    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("🔄 Nouvelle Série", use_container_width=True):
            st.session_state.practice_dataset = generate_random_dataset()
            st.session_state.practice_feedback = {
                "mean": None,
                "median": None,
                "range": None,
            }
            st.rerun()

    if st.session_state.practice_dataset is None:
        st.session_state.practice_dataset = generate_random_dataset()

    dataset = st.session_state.practice_dataset

    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("📊 La Série Statistique (Notes sur 20)")

        # Afficher les valeurs
        values_display = " ".join([f"`{v}`" for v in dataset["values"]])
        st.markdown(f"**Valeurs :** {values_display}")
        st.caption(f"Effectif total : **{dataset['total_count']}** valeurs")

        st.divider()

        # Graphique
        st.subheader("📈 Répartition des Notes")
        freq_df = get_frequency_data(dataset["values"])
        st.bar_chart(freq_df.set_index("Valeur"))

    with col2:
        st.subheader("✍️ À toi de jouer !")

        user_mean = st.number_input("Moyenne", value=None, step=0.1, format="%.2f")
        user_median = st.number_input("Médiane", value=None, step=0.5, format="%.1f")
        user_range = st.number_input("Étendue", value=None, step=1.0, format="%.0f")

        if st.button(
            "✅ Vérifier mes réponses", use_container_width=True, type="primary"
        ):
            feedback = {
                "mean": (
                    abs(user_mean - dataset["mean"]) < 0.1
                    if user_mean is not None
                    else None
                ),
                "median": (
                    user_median == dataset["median"]
                    if user_median is not None
                    else None
                ),
                "range": (
                    user_range == dataset["range"] if user_range is not None else None
                ),
            }
            st.session_state.practice_feedback = feedback

        # Afficher le feedback
        if st.session_state.practice_feedback["mean"] is not None:
            st.divider()
            if st.session_state.practice_feedback["mean"]:
                st.success("✅ Moyenne correcte !")
            else:
                st.error(f"❌ Moyenne incorrecte. Réponse attendue : {dataset['mean']}")

            if st.session_state.practice_feedback["median"]:
                st.success("✅ Médiane correcte !")
            else:
                st.error(
                    f"❌ Médiane incorrecte. Réponse attendue : {dataset['median']}"
                )

            if st.session_state.practice_feedback["range"]:
                st.success("✅ Étendue correcte !")
            else:
                st.error(
                    f"❌ Étendue incorrecte. Réponse attendue : {dataset['range']}"
                )

        if st.checkbox("👁️ Voir la correction"):
            st.divider()
            st.markdown("**Correction Détaillée :**")
            st.markdown(
                f"**Série ordonnée :** {', '.join(map(str, dataset['sorted_values']))}"
            )
            st.markdown(
                f"**Moyenne :** {dataset['mean']} (Somme des valeurs / {dataset['total_count']})"
            )
            st.markdown(f"**Médiane :** {dataset['median']}")
            st.markdown(
                f"**Étendue :** {dataset['range']} ({dataset['sorted_values'][-1]} - {dataset['sorted_values'][0]})"
            )


def render_ai_tutor():
    """Section Tuteur IA"""
    st.header("🤖 Tuteur IA - Professeur de Mathématiques")
    st.caption("Expert en statistiques niveau 3ème")

    # Afficher les messages
    for msg in st.session_state.chat_messages:
        if msg["role"] == "user":
            with st.chat_message("user"):
                st.write(msg["text"])
        else:
            with st.chat_message("assistant"):
                st.write(msg["text"])

    # Input pour nouveau message
    if prompt := st.chat_input("Pose ta question sur les stats..."):
        # Ajouter le message utilisateur
        st.session_state.chat_messages.append({"role": "user", "text": prompt})

        # Afficher le message
        with st.chat_message("user"):
            st.write(prompt)

        # Générer la réponse avec Gemini en réutilisant le client initialisé
        if st.session_state.gemini_client:
            with st.chat_message("assistant"):
                with st.spinner("Réflexion en cours..."):
                    try:
                        history_text = "\n".join(
                            [
                                f"{'Élève' if m['role'] == 'user' else 'Professeur'}: {m['text']}"
                                for m in st.session_state.chat_messages[-6:]
                            ]
                        )

                        system_instruction = """
                        Tu es un professeur de mathématiques pour des élèves de 3ème.
                        Chapitre : Statistiques (moyenne, médiane, étendue, effectifs, fréquences).
                        Réponds de façon claire, courte, pédagogique. Utilise le gras (**texte**) pour les notions clés.
                        Ne donne pas la réponse directe d'un exercice, guide l'élève par étapes.
                        """

                        prompt_text = f"{system_instruction}\n\nHistorique:\n{history_text}\n\nÉlève: {prompt}\nProfesseur:"

                        # Essayer plusieurs modèles via le client existant
                        models = [
                            "gemini-2.0-flash-exp",
                            "gemini-1.5-flash",
                            "gemini-pro",
                        ]
                        response_text = None
                        for _ in models:
                            try:
                                response = st.session_state.gemini_client.model.generate_content(
                                    prompt_text
                                )
                                response_text = response.text
                                if response_text:
                                    break
                            except Exception:
                                continue

                        if not response_text:
                            raise RuntimeError("Aucune réponse valide reçue.")

                        st.write(response_text)
                        st.session_state.chat_messages.append(
                            {"role": "model", "text": response_text}
                        )
                    except Exception:
                        error_msg = (
                            "Le tuteur ne répond pas. Vérifie la clé API ou réessaie."
                        )
                        st.error(error_msg)
                        st.session_state.chat_messages.append(
                            {"role": "model", "text": error_msg}
                        )
        else:
            st.warning("Configure la clé API Gemini dans la barre latérale.")


def render_exercises_ia():
    """Section Exercices générés avec IA (code existant)"""
    # Code existant de la section exercices
    if st.session_state.current_exercise is None:
        st.info("👈 Utilisez la barre latérale pour générer un exercice")
        return

    exercise = st.session_state.current_exercise

    st.header("📝 Exercice")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"**Type:** {exercise['type_name']}")
    with col2:
        st.markdown(f"**Niveau:** {st.session_state.get('difficulty', 'moyen')}")
    with col3:
        if exercise.get("inspired_by_examples"):
            st.info("✨ Inspiré de tes exemples")

    st.divider()
    st.markdown("### Question")
    st.markdown(exercise["question"])
    st.divider()

    st.header("✍️ Ta réponse")
    uploaded_file = st.file_uploader(
        "📷 Télécharger la photo de ta copie",
        type=["png", "jpg", "jpeg"],
    )

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Ta copie", use_container_width=True)

        if st.button("🔍 Analyser ma copie", type="primary"):
            with st.spinner("Analyse en cours..."):
                try:
                    profile = st.session_state.student_profile.get_profile()
                    student_profile_data = (
                        profile if st.session_state.use_personalization else None
                    )
                    feedback = (
                        st.session_state.gemini_client.analyze_handwritten_solution(
                            image=image,
                            exercise_type=exercise["type"],
                            exercise_data=exercise,
                            question=exercise["question"],
                            student_history=student_profile_data,
                        )
                    )
                    st.session_state.feedback = feedback
                    st.rerun()
                except Exception as e:
                    st.error(f"Erreur: {str(e)}")

    if st.session_state.feedback:
        display_feedback(st.session_state.feedback)


def display_feedback(feedback):
    """Affiche le feedback détaillé"""
    st.divider()
    st.header("📊 Feedback détaillé")

    if feedback.get("feedback"):
        st.subheader("💬 Commentaire général")
        st.info(feedback["feedback"])

    if feedback.get("reasoning_steps"):
        st.subheader("🧠 Analyse de ta démarche")
        with st.expander("Voir l'analyse étape par étape", expanded=True):
            for i, step in enumerate(feedback["reasoning_steps"], 1):
                status_icon = {"correct": "✅", "incorrect": "❌", "partial": "⚠️"}.get(
                    step.get("status", "partial"), "⚠️"
                )
                st.markdown(
                    f"**Étape {i}:** {status_icon} {step.get('description', '')}"
                )
                st.caption(f"*{step.get('reasoning', '')}*")

    if feedback.get("good_points"):
        st.subheader("✅ Points positifs")
        for point in feedback["good_points"]:
            st.success(f"✓ {point}")

    if feedback.get("errors"):
        st.subheader("❌ Erreurs détectées")
        for error in feedback["errors"]:
            st.error(f"✗ {error}")

    if feedback.get("correction"):
        st.subheader("📖 Correction proposée")
        with st.expander("Voir la correction", expanded=True):
            st.markdown(feedback["correction"])

    if feedback.get("score"):
        st.subheader("📈 Évaluation")
        st.metric("Score", feedback["score"])


def render_sidebar():
    """Navigation minimale (non utilisée, navigation en top bar)"""
    # On retourne True pour laisser main() continuer
    return True


def main():
    """Application principale"""

    # Afficher la barre latérale
    if not render_sidebar():
        return

    # Navigation par onglets
    tab = st.session_state.current_tab

    if tab == "Accueil":
        render_home()
    elif tab == "Cours":
        render_lessons()
    elif tab == "Entraînement":
        render_practice()
    elif tab == "Exercices IA":
        render_exercises_ia()
    elif tab == "Tuteur IA":
        render_ai_tutor()


if __name__ == "__main__":
    main()
