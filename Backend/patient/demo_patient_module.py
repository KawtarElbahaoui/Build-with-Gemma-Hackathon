"""
Démo — Module Données Patient & Mode Urgence
==============================================
Ce script simule un scénario complet : consultation des données d'urgence,
ajout d'un document médical extrait, recherche dans l'historique, et
génération du lien vers l'hôpital le plus proche.

Lancer avec : python demo_patient_module.py
"""

from patient_module import (
    enregistrer_nouveau_patient,
    get_urgence_data,
    sauvegarder_document,
    valider_rapport,
    retrieve_relevant_docs,
    construire_lien_hopital_urgence,
    calculer_horaires_prise,
    generer_qr_code_patient,
    executer_tool_call,
    TOOLS_PATIENT,
)

print("=" * 60)
print("SCÉNARIO 0 — Enregistrement d'un nouveau patient")
print("=" * 60)
nouveau = enregistrer_nouveau_patient(
    identite={"nom": "Chraibi", "prenom": "Salma", "date_naissance": "1998-09-10", "sexe": "F"},
    allergies=["Aspirine"],
    contact_urgence={"nom": "Hicham Chraibi", "lien": "Frère", "telephone": "+212600000004"}
)
print(f"Nouveau patient enregistré : {nouveau}")

print("\n" + "=" * 60)
print("SCÉNARIO 1 — Mode urgence : consultation rapide")
print("=" * 60)
urgence = get_urgence_data("P002")
print(f"Patient : {urgence['nom_complet']}")
print(f"Allergies : {', '.join(urgence['allergies'])}")
print("Traitements en cours :")
for t in urgence["traitements_en_cours"]:
    print(f"  - {t['nom']} ({t['dose']}, {t['frequence_par_jour']}x/jour)")
print(f"Contact d'urgence : {urgence['contact_urgence']['nom']} "
      f"({urgence['contact_urgence']['lien']}) — {urgence['contact_urgence']['telephone']}")

print("\n" + "=" * 60)
print("SCÉNARIO 2 — Ajout d'un document extrait (simulation bloc extraction)")
print("=" * 60)
document_extrait = {
    "type_document": "ordonnance",
    "confidence": 0.88,
    "date_document": "20/07/2026",
    "medecin": "Dr. Zineb Bouabidi",
    "etablissement": "Clinique Al Amal, Casablanca",
    "patient": "Youssef Alaoui",
    "resume_court": "Renouvellement traitement diabète.",
    "source": "document_papier",
    "medicaments": []
}
resultat = sauvegarder_document("P002", document_extrait)
print(f"Document enregistré : {resultat}")

print("\n" + "=" * 60)
print("SCÉNARIO 2bis — Validation par un médecin/clinique")
print("=" * 60)
validation = valider_rapport("P002", "Dr. Zineb Bouabidi")
print(f"Rapport validé : {validation}")

print("\n" + "=" * 60)
print("SCÉNARIO 3 — Recherche dans l'historique")
print("=" * 60)
resultats = retrieve_relevant_docs("diabète traitement", "P002")
for r in resultats:
    print(f"  - {r['contenu'].get('date_document')} : {r['contenu']['resume_court']}")

print("\n" + "=" * 60)
print("SCÉNARIO 4 — Lien hôpital le plus proche (coordonnées simulées : Casablanca)")
print("=" * 60)
lien = construire_lien_hopital_urgence(33.5731, -7.5898)
print(f"Lien Maps : {lien}")

print("\n" + "=" * 60)
print("SCÉNARIO 5 — Rappels de médicaments (nice-to-have)")
print("=" * 60)
horaires = calculer_horaires_prise(frequence_par_jour=3)
print(f"Horaires suggérés pour un traitement 3x/jour : {horaires}")

print("\n" + "=" * 60)
print("SCÉNARIO 6 — Appel simulé depuis l'agent (function calling)")
print("=" * 60)
print(f"Tools exposés à l'agent : {[t['name'] for t in TOOLS_PATIENT]}")
appel_agent = executer_tool_call("get_urgence_data", {"patient_id": "P003"})
print(f"Résultat de l'appel de l'agent : {appel_agent}")

print("\n" + "=" * 60)
print("SCÉNARIO 7 — QR code pour accès rapide au dossier (médecin)")
print("=" * 60)
qr_result = generer_qr_code_patient("P003")
print(f"URL encodée dans le QR code : {qr_result['url_encodee']}")
print(f"Image générée (base64, {len(qr_result['image_base64'])} caractères)")

print("\n✅ Démo terminée — tous les scénarios se sont exécutés sans erreur.")
