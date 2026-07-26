# Build-with-Gemma-Hackathon

MediExtract — Build with Gemma Hackathon
Plateforme IA transformant des documents médicaux en historique de santé intelligent, propulsée par Gemma 4.
🎯 Le problème
Se déplacer, attendre son tour, puis réexpliquer un dossier déjà connu : voir un médecin fait perdre du temps à tout le monde. MediExtract structure automatiquement l'information médicale dès l'arrivée du document — le personnel médical n'a plus qu'à valider.
🏗️ Architecture
Le projet est organisé en branches par fonctionnalité :
Branche	Contenu
`Backend`	`patient_module.py` — stockage patient, mode urgence, function calling
`Backend`	`extraction.py`, `rapport.py` — extraction de documents et génération de rapport
`AI`	`assistant.py`, `config.py` — chatbot conversationnel et configuration
`Frontend`	`app.py` — interface Streamlit complète
`Presentation`	Slides et supports de pitch
📦 Structure des fichiers (une fois assemblés)
```
├── app.py            # Interface Streamlit (CSS, pages, routage)
├── config.py          # Configuration (clés API, modèle)
├── extraction.py       # Extraction de documents via Gemma 4 (vision)
├── rapport.py          # Génération de rapport patient (aucun appel IA)
├── assistant.py         # Chatbot / assistant conversationnel
├── email_utils.py       # Envoi de rapport par email (optionnel)
├── patient_module.py     # Stockage patient, mode urgence, QR code
├── requirements.txt      # Dépendances Python
└── .streamlit/config.toml # Thème visuel
```
🚀 Installation
```bash
git clone https://github.com/KawtarElbahaoui/Build-with-Gemma-Hackathon.git
cd Build-with-Gemma-Hackathon
pip install -r requirements.txt
```
⚙️ Configuration
Définissez la clé API OpenRouter en variable d'environnement :
```bash
# Windows (PowerShell)
$env:OPENROUTER_API_KEY="sk-or-v1-..."

# Mac / Linux
export OPENROUTER_API_KEY="sk-or-v1-..."
```
Obtenez une clé gratuite sur openrouter.ai/keys.
▶️ Lancer l'application
```bash
streamlit run app.py
```
🧠 Comment Gemma 4 est utilisé
Fonction	Utilise Gemma ?	Type d'appel	Rôle
`extraire_document_reel`	✅ Oui	Image + texte	Extraire les données structurées d'un document
`decider_action`	✅ Oui	Texte seul	Répondre aux questions du personnel sur un patient
`generer_rapport_patient`	❌ Non	—	Compiler des données déjà validées, zéro hallucination
`sauvegarder_document` / `get_urgence_data`	❌ Non	—	Lecture/écriture de la base patient
🔒 Sécurité et éthique
Aucune décision clinique automatisée : chaque extraction passe par une validation humaine explicite avant d'être considérée comme définitive.
Détection déterministe pour les cas critiques : les questions sur allergies, traitements et contact d'urgence sont routées par correspondance de mots-clés exacte, pas par le jugement variable d'un LLM.
Traçabilité : chaque rapport indique qui l'a validé et quand.

🗺️ Roadmap
Chiffrement du stockage (Fernet/AES au repos, HTTPS en transit).
Authentification réelle par établissement.
Envoi automatique du rapport dès validation.
Support de l'extraction sur documents papier/manuscrits avec validation renforcée.
👥 Équipe
Build with Gemma Hackathon — GDG On Campus ENSA Berrechid × AI Crafters × Gemma Team
