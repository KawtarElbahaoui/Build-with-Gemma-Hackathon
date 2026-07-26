"""
EXTRACTION DE DOCUMENTS (Bloc 2)
================================
Convertit un PDF/image en données structurées via Gemma 4 (vision), en
utilisant OpenRouter comme API cloud.
"""

import base64
import json
import os

import requests
import streamlit as st

from config import OPENROUTER_URL, OPENROUTER_API_KEY, MODEL


PROMPT_NUMERIQUE = """Tu es un assistant qui extrait fidèlement toutes les informations visibles
dans un document médical numérique (PDF ou image déjà numérique, texte net).

RÈGLES :
1. Extrais toutes les informations clairement visibles et lisibles dans le document :
   médicaments, dosages, fréquences, résultats d'analyses avec leurs valeurs, diagnostic
   mentionné, recommandations.
2. N'invente RIEN — si une information est illisible ou absente, utilise null et ajoute
   le nom du champ dans "champs_incertains".
3. "patient" doit TOUJOURS être une simple chaîne de texte (nom complet), jamais un objet.
4. Retourne uniquement un objet JSON valide, sans explication avant ou après.

Retourne exactement cette structure :
{
  "type_document": null, "confidence": 0.0, "date_document": null, "medecin": null,
  "etablissement": null, "patient": null, "resume_court": null,
  "diagnostic": null,
  "medicaments": [
    {"nom": "...", "dosage": "...", "frequence": "..."}
  ],
  "resultats_examens": [
    {"parametre": "...", "valeur": "...", "unite": "...", "valeurs_normales": "..."}
  ],
  "recommandations": null,
  "champs_incertains": []
}
- "resume_court" : une phrase générale résumant l'objet du document.
- "confidence" : ta confiance globale (0 à 1) dans l'exactitude de l'extraction.
- Laisse "medicaments" ou "resultats_examens" en liste vide [] s'ils ne sont pas présents
  dans le document.
"""


def image_vers_base64(chemin_image):
    """Encode une image en base64, nécessaire pour l'envoyer dans une requête JSON."""
    with open(chemin_image, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def convertir_pdf_en_image(chemin_pdf, dossier_sortie=None):
    """
    Convertit la première page d'un PDF en image PNG via PyMuPDF (fitz).
    Ne dépend d'aucun programme externe (contrairement à pdf2image + Poppler).
    """
    import fitz  # PyMuPDF
    import tempfile
    if dossier_sortie is None:
        dossier_sortie = tempfile.gettempdir()
    doc = fitz.open(chemin_pdf)
    page = doc[0]
    pix = page.get_pixmap(dpi=200)
    nom_fichier = os.path.splitext(os.path.basename(chemin_pdf))[0]
    chemin_image = os.path.join(dossier_sortie, f"{nom_fichier}.png")
    pix.save(chemin_image)
    doc.close()
    return chemin_image


def parser_json(texte_brut):
    """Extrait un JSON valide même si Gemma ajoute du texte avant/après."""
    try:
        debut = texte_brut.find("{")
        fin = texte_brut.rfind("}") + 1
        if debut == -1 or fin == 0:
            return None
        return json.loads(texte_brut[debut:fin])
    except json.JSONDecodeError:
        return None


def finaliser_json(data):
    """Uniformise le JSON, garantissant que tous les champs attendus existent."""
    if data is None:
        data = {}
    if isinstance(data.get("patient"), dict):
        nom = data["patient"].get("nom", "") or ""
        prenom = data["patient"].get("prenom", "") or ""
        data["patient"] = f"{prenom} {nom}".strip() or None
    data.setdefault("type_document", "autre")
    data.setdefault("confidence", 0.0)
    data.setdefault("date_document", None)
    data.setdefault("medecin", None)
    data.setdefault("etablissement", None)
    data.setdefault("patient", None)
    data.setdefault("resume_court", None)
    data.setdefault("diagnostic", None)
    data.setdefault("medicaments", [])
    data.setdefault("resultats_examens", [])
    data.setdefault("recommandations", None)
    data.setdefault("champs_incertains", [])
    return data


def extraire_document_reel(chemin_fichier, extension):
    """Appelle réellement Gemma 4 via OpenRouter pour analyser le document."""
    if extension == "pdf":
        chemin_image = convertir_pdf_en_image(chemin_fichier)
    else:
        chemin_image = chemin_fichier

    image_b64 = image_vers_base64(chemin_image)
    headers = {"Authorization": f"Bearer {OPENROUTER_API_KEY}", "Content-Type": "application/json"}

    try:
        response = requests.post(OPENROUTER_URL, headers=headers, json={
            "model": MODEL,
            "messages": [{
                "role": "user",
                "content": [
                    {"type": "text", "text": PROMPT_NUMERIQUE},
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{image_b64}"}}
                ]
            }]
        }, timeout=120)

        if response.status_code != 200:
            st.error(f"Erreur OpenRouter : {response.status_code} — {response.text[:200]}")
            return finaliser_json(None)

        texte_brut = response.json()["choices"][0]["message"]["content"].strip()
        return finaliser_json(parser_json(texte_brut))

    except requests.exceptions.RequestException as e:
        st.error(f"Erreur de connexion : {e}")
        return finaliser_json(None)
