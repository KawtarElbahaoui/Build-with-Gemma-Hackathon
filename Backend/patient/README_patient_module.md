# Module 3 — Données Patient & Mode Urgence

## Fonctionnalités
- Enregistrement d'un nouveau patient (génère un patient_id)
- Stockage de l'historique médical (JSON persistant sur disque)
- Mode urgence : allergies, traitements en cours, contact d'urgence
- Lien vers l'hôpital le plus proche (à partir de coordonnées GPS)
- Rappels de médicaments (horaires calculés selon la fréquence de prise)
- Recherche par mots-clés dans l'historique, triée par date
- QR code pour accès rapide au dossier patient (à scanner par un médecin)
- Connexion aux tools de l'agent (function calling, format Gemini/Gemma)

## Dépendances
```bash
pip install qrcode[pil]
```
(Le reste du module n'utilise que la librairie standard Python.)

## Fichiers
- `patient_module.py` — le module complet, importable directement
- `demo_patient_module.py` — scénario de démonstration de bout en bout

## Utilisation

```python
from patient_module import enregistrer_nouveau_patient, get_urgence_data, sauvegarder_document, retrieve_relevant_docs

# Enregistrer un nouveau patient
nouveau = enregistrer_nouveau_patient(
    identite={"nom": "Chraibi", "prenom": "Salma", "date_naissance": "1998-09-10", "sexe": "F"},
    allergies=["Aspirine"],
    contact_urgence={"nom": "Hicham Chraibi", "lien": "Frère", "telephone": "+212600000004"}
)
patient_id = nouveau["patient_id"]  # ex: "P004"

# Consulter les données d'urgence d'un patient
urgence = get_urgence_data("P001")

# Enregistrer un document extrait (format du bloc extraction)
sauvegarder_document("P001", data_extraite)

# Rechercher dans l'historique
resultats = retrieve_relevant_docs("allergie pénicilline", "P001")

# Générer un QR code vers la fiche patient (pour un médecin)
qr = generer_qr_code_patient("P001", base_url="https://mon-app.com/patient")
# qr["image_base64"] -> utilisable dans <img src="data:image/png;base64,...">
```

## ⚠️ Note sécurité QR code
Le QR code encode `{base_url}/{patient_id}` — l'accès n'est protégé par aucune
authentification dans ce prototype. En production, remplacer `patient_id` en
clair par un token d'accès temporaire à usage unique.

## Lancer les tests
```bash
python patient_module.py
```

## Lancer la démo complète
```bash
python demo_patient_module.py
```

## Format attendu pour `data_extraite`
Voir le module extraction pour le schéma complet (`type_document`, `confidence`,
`date_document`, `medecin`, `resume_court`, etc.). Le champ `medicaments` est
toujours vide `[]` à l'extraction — rempli uniquement par le patient (formulaire).

## Intégration avec l'agent (bloc 1)
`TOOLS_PATIENT` expose le schéma des 3 fonctions au format function-calling.
`executer_tool_call(nom_tool, arguments)` route l'appel vers la bonne fonction.

## ⚠️ Note sécurité (hors scope prototype)
Les données patient ne sont pas chiffrées dans ce prototype. En production,
il faudrait chiffrer `patients_db.json` au repos (ex: Fernet/AES) et servir
l'application en HTTPS uniquement.
