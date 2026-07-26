"""
Module Données Patient & Mode Urgence
========================================
Fonctionnalités couvertes :
- Stockage de l'historique (JSON)
- Mode urgence (allergies, traitements, contact d'urgence)
- Lien hôpital le plus proche (géolocalisation + redirection Maps)
- Rappels de médicaments (horaires calculés à partir de la fréquence)
- Connexion aux tools de l'agent (function calling)

⚠️ NOTE PROD : les données patient (allergies, traitements, contact) sont sensibles.
En production, il faudrait chiffrer le fichier JSON au repos (ex: Fernet/AES) et en
transit (HTTPS), et ne jamais logger les données brutes. Non implémenté ici — hors
scope du prototype hackathon.
"""

import json
import os
import re
import uuid
import io
import base64
from datetime import datetime

try:
    import qrcode
    _QRCODE_DISPONIBLE = True
except ImportError:
    _QRCODE_DISPONIBLE = False

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

# Chemin du fichier de stockage. Sur Kaggle : "/kaggle/working/patients_db.json".
# En local / dans le projet Flask final : ajuster vers un dossier data/ du projet.
DATA_FILE = os.environ.get("PATIENT_DB_PATH", "patients_db.json")


# ---------------------------------------------------------------------------
# Initialisation / persistance
# ---------------------------------------------------------------------------

def _patients_fictifs() -> dict:
    """Génère les 3 profils fictifs (utilisé uniquement si aucun fichier n'existe déjà)."""
    patients = [
        {
            "patient_id": "P001",
            "identite": {"nom": "Benali", "prenom": "Rime", "date_naissance": "2003-05-14", "sexe": "F"},
            "allergies": ["Pénicilline", "Arachides"],
            "traitements_en_cours": [
                {"nom": "Ventoline", "dose": "100mcg", "frequence_par_jour": 2}
            ],
            "contact_urgence": {"nom": "Fatima Benali", "lien": "Mère", "telephone": "+212600000001"},
            "historique_documents": []
        },
        {
            "patient_id": "P002",
            "identite": {"nom": "Alaoui", "prenom": "Youssef", "date_naissance": "1985-11-02", "sexe": "M"},
            "allergies": ["Iode"],
            "traitements_en_cours": [
                {"nom": "Metformine", "dose": "500mg", "frequence_par_jour": 3},
                {"nom": "Lisinopril", "dose": "10mg", "frequence_par_jour": 1}
            ],
            "contact_urgence": {"nom": "Sara Alaoui", "lien": "Épouse", "telephone": "+212600000002"},
            "historique_documents": []
        },
        {
            "patient_id": "P003",
            "identite": {"nom": "Fassi", "prenom": "Amina", "date_naissance": "1970-03-22", "sexe": "F"},
            "allergies": ["Latex", "Sulfamides"],
            "traitements_en_cours": [
                {"nom": "Levothyrox", "dose": "75mcg", "frequence_par_jour": 1}
            ],
            "contact_urgence": {"nom": "Karim Fassi", "lien": "Fils", "telephone": "+212600000003"},
            "historique_documents": []
        }
    ]
    return {p["patient_id"]: p for p in patients}


def charger_patients_db() -> dict:
    """Charge la base depuis le fichier JSON si présent, sinon crée les profils fictifs."""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    db = _patients_fictifs()
    sauvegarder_patients_db(db)
    return db


def sauvegarder_patients_db(db: dict) -> None:
    """Écrit la base complète sur disque."""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(db, f, ensure_ascii=False, indent=2)


PATIENTS_DB = charger_patients_db()


# ---------------------------------------------------------------------------
# Fonctions principales
# ---------------------------------------------------------------------------

def enregistrer_nouveau_patient(identite: dict, allergies: list = None, traitements_en_cours: list = None,
                                  contact_urgence: dict = None) -> dict:
    """
    Enregistre un nouveau patient et retourne son patient_id généré.

    identite : {"nom": str, "prenom": str, "date_naissance": str, "sexe": str} — requis
    allergies : liste de strings, ex: ["Pénicilline"] — optionnel, [] par défaut
    traitements_en_cours : liste de dicts {"nom", "dose", "frequence_par_jour"} — optionnel, [] par défaut
    contact_urgence : {"nom": str, "lien": str, "telephone": str} — optionnel, requis pour le mode urgence

    Retourne {"succes": True, "patient_id": "P004"} ou {"succes": False, "erreur": "..."}
    """
    if not identite or not identite.get("nom") or not identite.get("prenom"):
        return {"succes": False, "erreur": "Nom et prénom sont obligatoires"}

    # Génère un nouvel ID séquentiel (P001, P002, ... continue après le dernier existant)
    numeros_existants = [
        int(pid[1:]) for pid in PATIENTS_DB.keys()
        if pid.startswith("P") and pid[1:].isdigit()
    ]
    nouveau_numero = max(numeros_existants, default=0) + 1
    nouveau_id = f"P{nouveau_numero:03d}"

    PATIENTS_DB[nouveau_id] = {
        "patient_id": nouveau_id,
        "identite": identite,
        "allergies": allergies or [],
        "traitements_en_cours": traitements_en_cours or [],
        "contact_urgence": contact_urgence or {"nom": "", "lien": "", "telephone": ""},
        "historique_documents": []
    }
    sauvegarder_patients_db(PATIENTS_DB)

    return {"succes": True, "patient_id": nouveau_id}


def get_urgence_data(patient_id: str) -> dict:
    """Retourne les données critiques d'urgence : allergies, traitements, contact d'urgence."""
    patient = PATIENTS_DB.get(patient_id)
    if patient is None:
        return {"erreur": f"Patient {patient_id} introuvable"}

    return {
        "patient_id": patient_id,
        "nom_complet": f"{patient['identite']['prenom']} {patient['identite']['nom']}",
        "allergies": patient["allergies"],
        "traitements_en_cours": patient["traitements_en_cours"],
        "contact_urgence": patient["contact_urgence"]
    }


def sauvegarder_document(patient_id: str, data_extraite: dict) -> dict:
    """
    Ajoute un document validé (format bloc extraction) à l'historique d'un patient
    et persiste immédiatement sur disque.

    data_extraite : dict au format du bloc extraction (type_document, confidence,
    date_document, medecin, etablissement, patient, resume_court, rubriques_detectees,
    qualite_image, champs_incertains, source, chemin_fichier, medicaments).
    """
    patient = PATIENTS_DB.get(patient_id)
    if patient is None:
        return {"succes": False, "erreur": f"Patient {patient_id} introuvable"}

    document = {
        "document_id": str(uuid.uuid4())[:8],
        "date_ajout": datetime.now().strftime("%Y-%m-%d %H:%M"),  # secours si date_document est null
        "contenu": data_extraite
    }
    patient["historique_documents"].append(document)
    sauvegarder_patients_db(PATIENTS_DB)

    return {"succes": True, "document_id": document["document_id"]}


def _date_pour_tri(doc: dict) -> datetime:
    """Renvoie date_document (JJ/MM/AAAA) si présente et non-null, sinon date_ajout en secours."""
    date_doc = doc["contenu"].get("date_document")
    if date_doc:
        try:
            return datetime.strptime(date_doc, "%d/%m/%Y")
        except (ValueError, TypeError):
            pass
    return datetime.strptime(doc["date_ajout"], "%Y-%m-%d %H:%M")


def retrieve_relevant_docs(query: str, patient_id: str) -> list:
    """
    Recherche par mots-clés dans l'historique de documents d'un patient.
    Filtre : seuls les documents avec au moins un mot-clé en commun sont gardés (score > 0).
    Tri : date_document si disponible, sinon date_ajout en secours ; du plus récent au plus ancien.
    """
    patient = PATIENTS_DB.get(patient_id)
    if patient is None:
        return []

    mots_cles = set(re.findall(r"\w+", query.lower()))
    resultats = []

    for doc in patient["historique_documents"]:
        contenu_str = json.dumps(doc["contenu"], ensure_ascii=False).lower()
        mots_doc = set(re.findall(r"\w+", contenu_str))
        score = len(mots_cles & mots_doc)
        if score > 0:
            resultats.append({**doc, "score_pertinence": score})

    resultats.sort(key=_date_pour_tri, reverse=True)
    return resultats


def construire_lien_hopital_urgence(lat: float, lon: float) -> str:
    """
    Construit une URL Google Maps pointant vers les hôpitaux d'urgence autour des
    coordonnées GPS fournies (typiquement depuis navigator.geolocation côté frontend).
    """
    return f"https://www.google.com/maps/search/hopital+urgence/@{lat},{lon},15z"


def calculer_horaires_prise(frequence_par_jour: int, heure_debut: int = 8, heure_fin: int = 22) -> list:
    """
    (nice-to-have) Calcule des horaires de prise répartis uniformément entre
    heure_debut et heure_fin. Ex: 3x/jour -> ["8h", "15h", "22h"].
    """
    if frequence_par_jour <= 0:
        return []
    if frequence_par_jour == 1:
        return [f"{heure_debut}h"]

    intervalle = (heure_fin - heure_debut) / (frequence_par_jour - 1)
    horaires = [round(heure_debut + i * intervalle) for i in range(frequence_par_jour)]
    return [f"{h}h" for h in horaires]


def generer_qr_code_patient(patient_id: str, base_url: str = "http://localhost:5000/patient") -> dict:
    """
    Génère un QR code encodant l'URL vers la fiche du patient. Le médecin scanne
    le QR code -> arrive sur une page qui affiche get_urgence_data(patient_id).

    base_url : à ajuster une fois l'URL réelle définie avec le bloc frontend
    (ex: "https://mon-app.com/patient" ou une IP locale pour la démo).

    ⚠️ SÉCURITÉ : ce QR code expose l'accès au dossier via un ID en clair dans
    l'URL, sans authentification. Acceptable pour un prototype hackathon ; en
    production il faudrait un token d'accès temporaire plutôt que patient_id.

    Retourne un dict avec l'URL encodée et l'image en base64 (utilisable dans
    <img src="data:image/png;base64,...">côté frontend, ou sauvegardée en fichier).
    """
    if not _QRCODE_DISPONIBLE:
        return {"erreur": "Librairie 'qrcode' non installée. Lancer : pip install qrcode[pil]"}

    patient = PATIENTS_DB.get(patient_id)
    if patient is None:
        return {"erreur": f"Patient {patient_id} introuvable"}

    url = f"{base_url}/{patient_id}"

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    image_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")

    return {
        "patient_id": patient_id,
        "url_encodee": url,
        "image_base64": image_base64
    }


# ---------------------------------------------------------------------------
# Connexion aux tools de l'agent (bloc 1)
# Format function-calling standard (compatible Gemini / Gemma).
# ⚠️ À adapter si le bloc agent utilise un framework différent (LangChain, custom...).
# ---------------------------------------------------------------------------

TOOLS_PATIENT = [
    {
        "name": "enregistrer_nouveau_patient",
        "description": "Enregistre un nouveau patient dans le système et retourne son identifiant (patient_id) généré.",
        "parameters": {
            "type": "object",
            "properties": {
                "identite": {"type": "object", "description": "nom, prenom, date_naissance, sexe"},
                "allergies": {"type": "array", "items": {"type": "string"}},
                "traitements_en_cours": {"type": "array", "items": {"type": "object"}},
                "contact_urgence": {"type": "object", "description": "nom, lien, telephone"}
            },
            "required": ["identite"]
        }
    },
    {
        "name": "get_urgence_data",
        "description": "Récupère les allergies, traitements en cours et contact d'urgence d'un patient. À utiliser en priorité en mode urgence.",
        "parameters": {
            "type": "object",
            "properties": {
                "patient_id": {"type": "string", "description": "Identifiant du patient (ex: P001)"}
            },
            "required": ["patient_id"]
        }
    },
    {
        "name": "retrieve_relevant_docs",
        "description": "Recherche dans l'historique médical d'un patient les documents pertinents par rapport à une requête.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Termes de recherche"},
                "patient_id": {"type": "string", "description": "Identifiant du patient"}
            },
            "required": ["query", "patient_id"]
        }
    },
    {
        "name": "sauvegarder_document",
        "description": "Enregistre un nouveau document médical validé (format bloc extraction) dans l'historique du patient.",
        "parameters": {
            "type": "object",
            "properties": {
                "patient_id": {"type": "string"},
                "data_extraite": {"type": "object", "description": "JSON produit par le bloc extraction"}
            },
            "required": ["patient_id", "data_extraite"]
        }
    },
    {
        "name": "generer_qr_code_patient",
        "description": "Génère un QR code encodant l'URL vers la fiche d'un patient, à faire scanner par un médecin.",
        "parameters": {
            "type": "object",
            "properties": {
                "patient_id": {"type": "string", "description": "Identifiant du patient (ex: P001)"}
            },
            "required": ["patient_id"]
        }
    }
]

TOOL_DISPATCHER = {
    "enregistrer_nouveau_patient": enregistrer_nouveau_patient,
    "get_urgence_data": get_urgence_data,
    "retrieve_relevant_docs": retrieve_relevant_docs,
    "sauvegarder_document": sauvegarder_document,
    "generer_qr_code_patient": generer_qr_code_patient
}


def executer_tool_call(nom_tool: str, arguments: dict):
    """Exécute un appel de tool demandé par l'agent (bloc 1) et retourne le résultat."""
    fonction = TOOL_DISPATCHER.get(nom_tool)
    if fonction is None:
        return {"erreur": f"Tool '{nom_tool}' non reconnu"}
    return fonction(**arguments)


# ---------------------------------------------------------------------------
# Tests (exécutés si le fichier est lancé directement : python patient_module.py)
# ---------------------------------------------------------------------------

def _run_tests():
    r_nouveau = enregistrer_nouveau_patient(
        identite={"nom": "Test", "prenom": "Nouveau", "date_naissance": "1990-01-01", "sexe": "M"},
        allergies=["Test allergie"],
        contact_urgence={"nom": "Contact Test", "lien": "Ami", "telephone": "+212600000099"}
    )
    assert r_nouveau["succes"] is True
    assert r_nouveau["patient_id"] in PATIENTS_DB
    assert enregistrer_nouveau_patient(identite={}).get("succes") is False
    print("✅ enregistrer_nouveau_patient OK")

    result = get_urgence_data("P002")
    assert result["patient_id"] == "P002"
    assert "Iode" in result["allergies"]
    assert len(result["traitements_en_cours"]) == 2
    assert get_urgence_data("P999") .get("erreur")
    print("✅ get_urgence_data OK")

    nb_avant = len(PATIENTS_DB["P002"]["historique_documents"])
    r = sauvegarder_document("P002", {"type_document": "ordonnance", "date_document": "01/07/2026"})
    assert r["succes"] is True
    assert len(PATIENTS_DB["P002"]["historique_documents"]) == nb_avant + 1
    assert sauvegarder_document("P999", {})["succes"] is False
    print("✅ sauvegarder_document OK")

    resultats = retrieve_relevant_docs("ordonnance", "P002")
    assert isinstance(resultats, list)
    assert retrieve_relevant_docs("xyzabc123inexistant", "P002") == []
    print("✅ retrieve_relevant_docs OK")

    lien = construire_lien_hopital_urgence(33.5731, -7.5898)
    assert lien.startswith("https://www.google.com/maps/search/hopital+urgence/@")
    print("✅ construire_lien_hopital_urgence OK")

    assert calculer_horaires_prise(1) == ["8h"]
    assert calculer_horaires_prise(2) == ["8h", "22h"]
    assert calculer_horaires_prise(0) == []
    print("✅ calculer_horaires_prise OK")

    assert "allergies" in executer_tool_call("get_urgence_data", {"patient_id": "P001"})
    assert "erreur" in executer_tool_call("tool_inconnu", {})
    print("✅ executer_tool_call OK")

    if _QRCODE_DISPONIBLE:
        r_qr = generer_qr_code_patient("P001")
        assert "url_encodee" in r_qr
        assert "P001" in r_qr["url_encodee"]
        assert len(r_qr["image_base64"]) > 0
        assert generer_qr_code_patient("P999").get("erreur")
        print("✅ generer_qr_code_patient OK")
    else:
        print("⚠️ generer_qr_code_patient : librairie 'qrcode' non installée, test ignoré")

    print("\n🎉 Tous les tests sont passés")


if __name__ == "__main__":
    _run_tests()
