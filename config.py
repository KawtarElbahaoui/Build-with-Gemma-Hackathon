"""
CONFIGURATION
=============
Clés API et paramètres du modèle. Remplacez les valeurs avant de lancer l'app.

⚠️ Pour un vrai dépôt public, ne mettez JAMAIS de vraies clés ici — utilisez
des variables d'environnement à la place (voir commentaire en bas du fichier).
"""

import os

# ============================================================
# OPENROUTER (Gemma 4 via API cloud)
# ============================================================
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY", "VOTRE_CLE_ICI")
MODEL = "google/gemma-4-26b-a4b-it:free"  # version qui fonctionne sans rate-limit

# ============================================================
# EMAIL (envoi de rapport, fonctionnalité optionnelle)
# ============================================================
EMAIL_EXPEDITEUR = os.environ.get("EMAIL_EXPEDITEUR", "votre_email@gmail.com")
EMAIL_MOT_DE_PASSE_APP = os.environ.get("EMAIL_MOT_DE_PASSE_APP", "VOTRE_MOT_DE_PASSE_APPLICATION")

# ============================================================
# Pour la production, remplacez les lignes ci-dessus par :
#
#   OPENROUTER_API_KEY = os.environ["OPENROUTER_API_KEY"]
#
# et définissez la variable d'environnement avant de lancer l'app :
#   Windows (PowerShell) : $env:OPENROUTER_API_KEY="sk-or-v1-..."
#   Mac/Linux            : export OPENROUTER_API_KEY="sk-or-v1-..."
# ============================================================
