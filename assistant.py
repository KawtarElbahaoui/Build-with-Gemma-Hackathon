"""
ASSISTANT / CHATBOT (Bloc 1)
=============================
Répond aux questions du personnel médical sur un patient précis, en
s'appuyant sur patient_module.py (get_urgence_data, retrieve_relevant_docs).

Détection fiable par colonne exacte du JSON pour les questions critiques
(allergies, traitements, contact urgence) — pas de dépendance au jugement
variable du LLM pour ces cas sensibles.
"""

import json
import unicodedata

import requests

from config import OPENROUTER_URL, OPENROUTER_API_KEY, MODEL
from patient_module import get_urgence_data, retrieve_relevant_docs


def enlever_accents(texte):
    """Normalise les accents pour une comparaison fiable, peu importe l'encodage d'origine."""
    return ''.join(c for c in unicodedata.normalize('NFD', texte) if unicodedata.category(c) != 'Mn')


# Mapping : mot-clé détecté dans la question → colonne exacte du JSON patient à extraire
MAPPING_CHAMPS = {
    "allergie": "allergies",
    "allergique": "allergies",
    "traitement": "traitements_en_cours",
    "medicament": "traitements_en_cours",
    "contact urgence": "contact_urgence",
    "urgence": "contact_urgence",
}

PROMPT_SYSTEME_AGENT = """Tu es un assistant qui aide le personnel médical (laboratoire, hôpital,
médecin) à consulter et gérer les dossiers patients. Tu n'es JAMAIS toi-même un médecin, tu ne
donnes JAMAIS de diagnostic ni de conseil médical.

Règles :
- Réponds toujours en te basant sur les données réelles, jamais en inventant.
- Ne mentionne QUE l'information demandée — si on te demande les allergies, ne parle pas des
  traitements ou du contact d'urgence, et inversement.
- Ne donne jamais d'avis clinique sur un traitement, un dosage ou un diagnostic.
"""


def appeler_gemma_texte(prompt, timeout=60):
    """Appel texte simple à Gemma via OpenRouter (pas d'image)."""
    headers = {"Authorization": f"Bearer {OPENROUTER_API_KEY}", "Content-Type": "application/json"}
    try:
        response = requests.post(OPENROUTER_URL, headers=headers, json={
            "model": MODEL,
            "messages": [{"role": "user", "content": prompt}]
        }, timeout=timeout)
        if response.status_code != 200:
            return f"Erreur API : {response.status_code} — {response.text[:200]}"
        return response.json()["choices"][0]["message"]["content"].strip()
    except requests.exceptions.RequestException as e:
        return f"Erreur de connexion : {e}"


def decider_action(question, patient_id):
    """
    Décide quelle donnée exacte consulter, en se basant sur la colonne JSON précise
    demandée par la question (pas de fuite entre allergies/traitements/contact),
    puis génère une réponse naturelle basée uniquement sur cette donnée.
    """
    question_normalisee = enlever_accents(question.lower())
    donnees = get_urgence_data(patient_id)

    champ_cible = None
    for mot_cle, nom_champ in MAPPING_CHAMPS.items():
        if mot_cle in question_normalisee:
            champ_cible = nom_champ
            break

    if champ_cible and champ_cible in donnees:
        # On n'envoie QUE cette colonne précise à Gemma, rien d'autre
        contexte = {champ_cible: donnees[champ_cible]}
        source = f"get_urgence_data[{champ_cible}]"
    else:
        docs = retrieve_relevant_docs(question, patient_id)
        contexte = docs if docs else {}
        source = "retrieve_relevant_docs" if docs else "Aucun"

    prompt_final = f"""{PROMPT_SYSTEME_AGENT}

Question posée : "{question}"
Patient concerné : {patient_id}
Information disponible ({source}) : {json.dumps(contexte, ensure_ascii=False)}

Réponds UNIQUEMENT avec cette information précise. Ne mentionne AUCUNE autre donnée
si la question ne porte pas dessus. Si l'information est absente, dis-le simplement
sans inventer.
"""
    reponse = appeler_gemma_texte(prompt_final)
    return {"reponse": reponse, "tool_utilise": source, "patient_id": patient_id}
