"""
Module d'envoi d'email aux parents après chaque session
"""

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, Any, Optional, List
from datetime import datetime


class EmailNotifier:
    """Gestionnaire d'envoi d'emails aux parents"""

    def __init__(
        self,
        smtp_server: str = "smtp.gmail.com",
        smtp_port: int = 587,
        sender_email: Optional[str] = None,
        sender_password: Optional[str] = None,
    ):
        """
        Initialise le gestionnaire d'email

        Args:
            smtp_server: Serveur SMTP (par défaut Gmail)
            smtp_port: Port SMTP (587 pour TLS)
            sender_email: Email de l'expéditeur
            sender_password: Mot de passe ou app password
        """
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.sender_email = sender_email or os.getenv("EMAIL_SENDER")
        self.sender_password = sender_password or os.getenv("EMAIL_PASSWORD")

        if not self.sender_email or not self.sender_password:
            print(
                "⚠️ Configuration email manquante. Définissez EMAIL_SENDER et EMAIL_PASSWORD"
            )

    def send_session_report(
        self,
        parent_email: str,
        student_name: str,
        session_data: Dict[str, Any],
    ) -> bool:
        """
        Envoie un rapport de session au parent

        Args:
            parent_email: Email du parent
            student_name: Prénom de l'élève
            session_data: Données de la session

        Returns:
            True si l'email a été envoyé avec succès, False sinon
        """
        if not self.sender_email or not self.sender_password:
            print("❌ Configuration email manquante. Email non envoyé.")
            return False

        try:
            # Créer le message
            message = MIMEMultipart("alternative")
            message["Subject"] = f"📊 Bilan de révision - {student_name}"
            message["From"] = self.sender_email
            message["To"] = parent_email

            # Créer le contenu HTML
            html_content = self._create_email_template(student_name, session_data)

            # Attacher le contenu HTML
            html_part = MIMEText(html_content, "html", "utf-8")
            message.attach(html_part)

            # Envoyer l'email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(message)

            print(f"✅ Email envoyé avec succès à {parent_email}")
            return True

        except Exception as e:
            print(f"❌ Erreur lors de l'envoi de l'email: {str(e)}")
            return False

    def _create_email_template(
        self, student_name: str, session_data: Dict[str, Any]
    ) -> str:
        """Crée le template HTML de l'email"""

        # Extraire les données de la session
        chapter = session_data.get("chapter", "Statistiques")
        level = session_data.get("level", "3ème")
        exercises_count = session_data.get("exercises_count", 0)
        success_rate = session_data.get("success_rate", 0)
        strengths = session_data.get("strengths", [])
        improvement_areas = session_data.get("improvement_areas", [])
        date = session_data.get("date", datetime.now().strftime("%d/%m/%Y %H:%M"))

        # Calculer le niveau de réussite
        if success_rate >= 80:
            success_level = "Excellent"
            success_color = "#28a745"
            success_emoji = "🌟"
        elif success_rate >= 60:
            success_level = "Bien"
            success_color = "#17a2b8"
            success_emoji = "👍"
        elif success_rate >= 40:
            success_level = "Assez bien"
            success_color = "#ffc107"
            success_emoji = "💪"
        else:
            success_level = "À améliorer"
            success_color = "#dc3545"
            success_emoji = "📚"

        # Template HTML
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {{
            font-family: Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
            border-radius: 10px 10px 0 0;
        }}
        .content {{
            background: #f8f9fa;
            padding: 30px;
            border-radius: 0 0 10px 10px;
        }}
        .section {{
            background: white;
            padding: 20px;
            margin: 15px 0;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .success-badge {{
            display: inline-block;
            background: {success_color};
            color: white;
            padding: 10px 20px;
            border-radius: 20px;
            font-weight: bold;
            margin: 10px 0;
        }}
        .strength-item, .improvement-item {{
            padding: 8px;
            margin: 5px 0;
            border-left: 3px solid #667eea;
            background: #f8f9fa;
        }}
        .footer {{
            text-align: center;
            margin-top: 30px;
            color: #666;
            font-size: 12px;
        }}
        h2 {{
            color: #667eea;
            margin-top: 0;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>📊 Bilan de Révision</h1>
        <p style="font-size: 18px; margin: 10px 0;">{student_name}</p>
    </div>
    
    <div class="content">
        <div class="section">
            <h2>📚 Session du {date}</h2>
            <p><strong>Chapitre :</strong> {chapter}</p>
            <p><strong>Niveau :</strong> {level}</p>
            <p><strong>Exercices réalisés :</strong> {exercises_count}</p>
        </div>

        <div class="section">
            <h2>{success_emoji} Niveau de Réussite</h2>
            <div class="success-badge">
                {success_level} - {success_rate}%
            </div>
            <p style="margin-top: 15px;">
                {student_name} a réussi {success_rate}% des exercices lors de cette session.
            </p>
        </div>

        {self._create_strengths_section(strengths) if strengths else ''}
        {self._create_improvements_section(improvement_areas) if improvement_areas else ''}

        <div class="section">
            <h2>💡 Message</h2>
            <p>
                {student_name} progresse régulièrement. Continuez à l'encourager dans ses révisions !
            </p>
        </div>
    </div>

    <div class="footer">
        <p>Cet email a été généré automatiquement par l'application de révision mathématiques.</p>
        <p>Powered by Gemini 3 Pro</p>
    </div>
</body>
</html>
        """

        return html

    def _create_strengths_section(self, strengths: List[str]) -> str:
        """Crée la section des points forts"""
        items = "".join(
            [
                f'<div class="strength-item">✅ {strength}</div>'
                for strength in strengths
            ]
        )
        return f"""
        <div class="section">
            <h2>✅ Points Forts</h2>
            {items}
        </div>
        """

    def _create_improvements_section(self, improvements: List[str]) -> str:
        """Crée la section des axes d'amélioration"""
        items = "".join(
            [
                f'<div class="improvement-item">📈 {improvement}</div>'
                for improvement in improvements
            ]
        )
        return f"""
        <div class="section">
            <h2>📈 Axes de Progression</h2>
            {items}
        </div>
        """

    def prepare_session_data(
        self,
        student_name: str,
        chapter: str,
        level: str,
        exercises: List[Dict[str, Any]],
        student_profile: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Prépare les données de session pour l'email

        Args:
            student_name: Prénom de l'élève
            chapter: Chapitre travaillé
            level: Niveau scolaire
            exercises: Liste des exercices réalisés avec leurs feedbacks
            student_profile: Profil de l'élève (optionnel)

        Returns:
            Dictionnaire avec les données formatées pour l'email
        """
        # Calculer le taux de réussite
        total_exercises = len(exercises)
        successful_exercises = 0
        all_strengths = []
        all_errors = []

        for exercise in exercises:
            feedback = exercise.get("feedback", {})
            score_str = feedback.get("score", "0/20")

            # Extraire le score
            try:
                if "/" in score_str:
                    score = float(score_str.split("/")[0])
                    if score >= 12:  # Considéré comme réussi
                        successful_exercises += 1
                elif score_str.lower() in ["excellent", "très bien", "bien"]:
                    successful_exercises += 1
            except:
                pass

            # Collecter les points forts et erreurs
            all_strengths.extend(feedback.get("good_points", []))
            all_errors.extend(feedback.get("errors", []))

        success_rate = (
            int((successful_exercises / total_exercises) * 100)
            if total_exercises > 0
            else 0
        )

        # Identifier les points forts récurrents
        from collections import Counter

        strengths = [
            strength
            for strength, count in Counter(all_strengths).most_common(3)
            if count >= 1
        ]

        # Identifier les axes d'amélioration
        improvement_areas = [
            error for error, count in Counter(all_errors).most_common(3) if count >= 1
        ]

        return {
            "chapter": chapter,
            "level": level,
            "exercises_count": total_exercises,
            "success_rate": success_rate,
            "strengths": strengths[:3],  # Top 3
            "improvement_areas": improvement_areas[:3],  # Top 3
            "date": datetime.now().strftime("%d/%m/%Y à %H:%M"),
        }
