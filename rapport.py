"""
GÉNÉRATION DE RAPPORT
=====================
Compile les données d'un patient (identité, infos vitales, historique de
documents) en un rapport lisible. Aucun appel IA ici — zéro risque
d'hallucination à cette étape, tout vient de données déjà stockées.
"""

from datetime import datetime

from patient_module import PATIENTS_DB, _date_pour_tri


def generer_rapport_patient(patient_id: str) -> dict:
    """
    Construit un rapport structuré pour un patient donné, à partir de
    PATIENTS_DB (patient_module.py). Retourne un dict avec le texte du
    rapport et quelques métadonnées.
    """
    patient = PATIENTS_DB.get(patient_id)
    if patient is None:
        return {"erreur": f"Patient {patient_id} introuvable", "texte": "", "nombre_documents": 0}

    identite = patient["identite"]
    nom_complet = f"{identite['prenom']} {identite['nom']}"

    documents_tries = sorted(patient["historique_documents"], key=_date_pour_tri, reverse=True)

    lignes = [f"# Rapport médical — {nom_complet}",
              f"*Généré le {datetime.now().strftime('%d/%m/%Y à %H:%M')}*\n"]

    lignes.append("## Informations personnelles")
    lignes.append(f"- **Nom complet :** {nom_complet}")
    lignes.append(f"- **Date de naissance :** {identite.get('date_naissance', 'non renseignée')}")
    lignes.append(f"- **Sexe :** {identite.get('sexe', 'non renseigné')}\n")

    lignes.append("## Informations vitales")
    if patient["allergies"]:
        lignes.append(f"- **Allergies connues :** {', '.join(patient['allergies'])}")
    else:
        lignes.append("- **Allergies connues :** aucune renseignée")

    if patient["traitements_en_cours"]:
        lignes.append("- **Traitements en cours :**")
        for t in patient["traitements_en_cours"]:
            lignes.append(f"  - {t['nom']} — {t['dose']}, {t['frequence_par_jour']}x/jour")
    else:
        lignes.append("- **Traitements en cours :** aucun renseigné")

    contact = patient["contact_urgence"]
    lignes.append(f"- **Contact d'urgence :** {contact.get('nom', '-')} "
                   f"({contact.get('lien', '-')}) — {contact.get('telephone', '-')}\n")

    lignes.append("## Historique des documents")
    if not documents_tries:
        lignes.append("*Aucun document enregistré pour le moment.*")
    else:
        for doc in documents_tries:
            contenu = doc["contenu"]
            date_affichee = contenu.get("date_document") or doc["date_ajout"]
            lignes.append(f"### {date_affichee} — {contenu.get('type_document', 'autre')}")
            if contenu.get("medecin"):
                lignes.append(f"- **Médecin :** {contenu['medecin']}")
            if contenu.get("etablissement"):
                lignes.append(f"- **Établissement :** {contenu['etablissement']}")
            lignes.append(f"- **Confiance de l'analyse :** {contenu.get('confidence', 0)}")
            if contenu.get("diagnostic"):
                lignes.append(f"- **Diagnostic :** {contenu['diagnostic']}")
            if contenu.get("medicaments"):
                lignes.append("- **Médicaments :**")
                for m in contenu["medicaments"]:
                    lignes.append(f"  - {m.get('nom', '?')} — {m.get('dosage', '?')}, {m.get('frequence', '?')}")
            if contenu.get("resultats_examens"):
                lignes.append("- **Résultats d'examens :**")
                for res in contenu["resultats_examens"]:
                    lignes.append(f"  - {res.get('parametre', '?')} : {res.get('valeur', '?')} "
                                   f"{res.get('unite', '')} (normale : {res.get('valeurs_normales', '?')})")
            if contenu.get("recommandations"):
                lignes.append(f"- **Recommandations :** {contenu['recommandations']}")
            lignes.append(f"- **Résumé :** {contenu.get('resume_court') or 'Aucun résumé disponible.'}")
            if contenu.get("champs_incertains"):
                lignes.append(f"- ⚠️ *À vérifier : {', '.join(contenu['champs_incertains'])}*")
            lignes.append("")

    if patient.get("rapport_valide"):
        lignes.append(f"✅ **Rapport validé par {patient.get('valide_par', '?')} "
                       f"le {patient.get('date_validation', '?')}**\n")
    else:
        lignes.append("⏳ **Rapport en attente de validation**\n")

    lignes.append("---")
    lignes.append("*Rapport généré automatiquement à partir d'une extraction IA — "
                   "à vérifier par un professionnel de santé avant toute décision clinique.*")

    return {
        "patient_id": patient_id,
        "nom_complet": nom_complet,
        "texte": "\n".join(lignes),
        "nombre_documents": len(documents_tries),
    }
