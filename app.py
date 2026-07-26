"""
APPLICATION PRINCIPALE — MediExtract
=====================================
Interface Streamlit : CSS, pages, routage. La logique métier (extraction,
rapport, assistant, email) vit dans des modules séparés, importés ci-dessous.

Lancer avec : streamlit run app.py
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
import json
import os
import tempfile

import streamlit as st

from config import OPENROUTER_API_KEY
from extraction import extraire_document_reel
from rapport import generer_rapport_patient
from assistant import decider_action
from email_utils import envoyer_rapport_par_email
from patient_module import (
    PATIENTS_DB,
    enregistrer_nouveau_patient,
    sauvegarder_document,
    sauvegarder_patients_db,
    valider_rapport,
)


# ============================================================
# CONFIGURATION GÉNÉRALE
# ============================================================

st.set_page_config(
    page_title="MediExtract",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ============================================================
# INITIALISATION DE LA SESSION
# ============================================================

if "page" not in st.session_state:
    st.session_state.page = "accueil"

if "nom_utilisateur" not in st.session_state:
    st.session_state.nom_utilisateur = ""

if "etablissement_utilisateur" not in st.session_state:
    st.session_state.etablissement_utilisateur = ""

if "patient_id_actuel" not in st.session_state:
    st.session_state.patient_id_actuel = list(PATIENTS_DB.keys())[0] if PATIENTS_DB else None


# ============================================================
# STYLE CSS — thème bleu ciel (inchangé)
# ============================================================

st.markdown(
    """
    <style>
        .stApp,
        [data-testid="stAppViewContainer"],
        [data-testid="stMain"],
        html, body {
            background-color: #EEF4FE !important;
            background-image:
                linear-gradient(160deg, #C7DBFC 0%, #DCE9FD 25%, #EEF4FE 55%, #FFFFFF 100%),
                repeating-linear-gradient(0deg, rgba(30,58,138,0.18) 0px, rgba(30,58,138,0.18) 2px, transparent 2px, transparent 40px),
                repeating-linear-gradient(90deg, rgba(30,58,138,0.18) 0px, rgba(30,58,138,0.18) 2px, transparent 2px, transparent 40px) !important;
            background-attachment: fixed !important;
        }
        [data-testid="stHeader"] { background: transparent !important; }
        #MainMenu { visibility: hidden; }
        footer { visibility: hidden; }
        header { visibility: hidden; }

        @keyframes fadeInUp {
            from { opacity: 0; transform: translateY(12px); }
            to { opacity: 1; transform: translateY(0); }
        }

        @keyframes floatGlow {
            0%, 100% { transform: translate(0, 0) scale(1); }
            50% { transform: translate(20px, -15px) scale(1.08); }
        }

        @keyframes shine {
            0% { left: -75%; }
            100% { left: 125%; }
        }

        .block-container {
            padding-top: 1.5rem;
            padding-bottom: 3rem;
            max-width: 1250px;
        }

        .navbar {
            background: white;
            padding: 16px 26px;
            border-radius: 18px;
            box-shadow: 0 8px 24px rgba(15, 23, 42, 0.10);
            margin-bottom: 30px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            border-bottom: 3px solid #1E3A8A;
            animation: fadeInUp 0.4s ease;
        }

        .logo { font-size: 25px; font-weight: 800; color: #0f172a; }
        .logo span {
            background: linear-gradient(135deg, #1E3A8A, #2563EB);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }

        .hero {
            background: linear-gradient(135deg, #0F172A 0%, #1E3A8A 55%, #2563EB 100%);
            padding: 65px 55px;
            border-radius: 28px;
            box-shadow: 0 20px 50px rgba(15, 23, 42, 0.35);
            margin-bottom: 35px;
            animation: fadeInUp 0.5s ease;
            position: relative;
            overflow: hidden;
        }

        .hero::before, .hero::after {
            content: "";
            position: absolute;
            border-radius: 50%;
            filter: blur(50px);
            pointer-events: none;
            z-index: 0;
        }
        .hero::before {
            width: 260px; height: 260px;
            background: radial-gradient(circle, rgba(96,165,250,0.55), transparent 70%);
            top: -60px; right: 10%;
            animation: floatGlow 8s ease-in-out infinite;
        }
        .hero::after {
            width: 200px; height: 200px;
            background: radial-gradient(circle, rgba(147,197,253,0.4), transparent 70%);
            bottom: -50px; left: 15%;
            animation: floatGlow 10s ease-in-out infinite reverse;
        }
        .hero > * { position: relative; z-index: 1; }

        .hero-badge {
            display: inline-block;
            background-color: rgba(255,255,255,0.14);
            color: #DBEAFE;
            padding: 8px 14px;
            border-radius: 999px;
            font-weight: 700;
            font-size: 14px;
            margin-bottom: 18px;
            border: 1px solid rgba(255,255,255,0.25);
        }

        .hero-title {
            color: #FFFFFF;
            font-size: 52px;
            line-height: 1.1;
            font-weight: 850;
            margin-bottom: 20px;
        }
        .hero-title span {
            background: linear-gradient(135deg, #60A5FA, #93C5FD);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }

        .hero-text { color: #CBD5E1; font-size: 19px; line-height: 1.7; max-width: 780px; }

        .custom-card {
            background-color: white;
            padding: 28px;
            border-radius: 20px;
            border: 1px solid #E2E8F0;
            box-shadow: 0 4px 15px rgba(15, 23, 42, 0.05);
            height: 100%;
            transition: transform 0.25s ease, box-shadow 0.25s ease, border-color 0.25s ease;
            animation: fadeInUp 0.5s ease both;
        }
        .custom-card:hover {
            transform: translateY(-8px) scale(1.015);
            box-shadow: 0 20px 40px rgba(30, 58, 138, 0.20);
            border-color: #93C5FD;
        }

        .card-icon {
            font-size: 26px;
            margin-bottom: 14px;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 56px;
            height: 56px;
            border-radius: 16px;
            background: linear-gradient(135deg, #EFF6FF, #DBEAFE);
            box-shadow: inset 0 0 0 1px rgba(30,58,138,0.08);
        }
        .card-title { color: #0f172a; font-size: 20px; font-weight: 750; margin-bottom: 8px; }
        .card-text { color: #64748b; line-height: 1.6; font-size: 15px; }

        .section-title { color: #0f172a; font-size: 32px; font-weight: 800; margin-top: 25px; margin-bottom: 10px; }
        .section-subtitle { color: #64748b; font-size: 16px; margin-bottom: 25px; }

        .welcome-box {
            background: linear-gradient(135deg, #0F172A, #1E3A8A, #2563EB);
            color: white;
            padding: 34px;
            border-radius: 24px;
            margin-bottom: 28px;
            box-shadow: 0 16px 36px rgba(15, 23, 42, 0.30);
            animation: fadeInUp 0.5s ease;
            position: relative;
            overflow: hidden;
        }
        .welcome-box::before {
            content: "";
            position: absolute;
            width: 180px; height: 180px;
            border-radius: 50%;
            background: radial-gradient(circle, rgba(147,197,253,0.35), transparent 70%);
            top: -40px; right: 5%;
            filter: blur(30px);
            animation: floatGlow 9s ease-in-out infinite;
        }
        .welcome-box h1, .welcome-box p { position: relative; z-index: 1; }
        .welcome-box h1 { margin: 0; font-size: 36px; }
        .welcome-box p { margin-top: 12px; margin-bottom: 0; color: #BFDBFE; font-size: 17px; }

        .security-box {
            background-color: #EFF6FF;
            border: 1px solid #93C5FD;
            border-left: 4px solid #1E3A8A;
            padding: 24px;
            border-radius: 18px;
            color: #1E3A8A;
            margin-top: 30px;
        }

        .result-card {
            background-color: white;
            border: 1px solid #93C5FD;
            padding: 25px;
            border-radius: 18px;
            margin-top: 20px;
            box-shadow: 0 8px 20px rgba(30, 58, 138, 0.08);
            animation: fadeInUp 0.4s ease;
        }

        .stButton > button {
            border-radius: 12px;
            padding: 0.7rem 1.3rem;
            font-weight: 700;
            border: none;
            transition: all 0.25s ease;
            position: relative;
            overflow: hidden;
        }
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 24px rgba(30, 58, 138, 0.30);
        }
        .stButton > button[kind="primary"] {
            background: linear-gradient(135deg, #1E3A8A, #2563EB);
        }
        .stButton > button[kind="primary"]::before {
            content: "";
            position: absolute;
            top: 0; left: -75%;
            width: 50%; height: 100%;
            background: linear-gradient(120deg, transparent, rgba(255,255,255,0.35), transparent);
            transform: skewX(-20deg);
        }
        .stButton > button[kind="primary"]:hover::before {
            animation: shine 0.9s ease forwards;
        }
        .stTextInput input {
            border-radius: 12px;
            border-color: #CBD5E1 !important;
        }
        .stTextInput input:focus {
            border-color: #1E3A8A !important;
            box-shadow: 0 0 0 1px #1E3A8A !important;
        }
        .stTextArea textarea {
            border-radius: 12px;
            border-color: #CBD5E1 !important;
        }
        .stTextArea textarea:focus {
            border-color: #1E3A8A !important;
            box-shadow: 0 0 0 1px #1E3A8A !important;
        }
        div[data-baseweb="select"] > div {
            border-color: #CBD5E1 !important;
        }
        div[data-baseweb="select"] > div:focus-within {
            border-color: #1E3A8A !important;
            box-shadow: 0 0 0 1px #1E3A8A !important;
        }

        [data-testid="stFileUploader"] {
            background-color: white;
            border: 2px dashed #60A5FA;
            padding: 25px;
            border-radius: 18px;
            transition: border-color 0.25s ease, background-color 0.25s ease, box-shadow 0.25s ease;
        }
        [data-testid="stFileUploader"]:hover {
            border-color: #1E3A8A;
            background-color: #F8FAFF;
            box-shadow: 0 8px 20px rgba(30, 58, 138, 0.12);
        }

        [data-testid="stMetric"] {
            background: white;
            border-radius: 16px;
            padding: 12px 16px;
            border: 1px solid #E2E8F0;
            transition: transform 0.25s ease, box-shadow 0.25s ease;
        }
        [data-testid="stMetric"]:hover {
            transform: translateY(-4px);
            box-shadow: 0 12px 24px rgba(30, 58, 138, 0.15);
        }

        .tag {
            display: inline-block;
            background-color: #EFF6FF;
            color: #1E3A8A;
            border-radius: 999px;
            padding: 6px 11px;
            margin: 4px 3px;
            font-size: 13px;
            font-weight: 650;
            border: 1px solid #BFDBFE;
            transition: transform 0.2s ease;
        }
        .tag:hover { transform: translateY(-2px); }

        @media (max-width: 768px) {
            .hero { padding: 40px 25px; }
            .hero-title { font-size: 36px; }
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# FONCTIONS DE NAVIGATION
# ============================================================

def changer_page(page: str) -> None:
    st.session_state.page = page
    st.rerun()


def navbar() -> None:
    info_utilisateur = ""
    if st.session_state.nom_utilisateur:
        info_utilisateur = (
            f"{st.session_state.nom_utilisateur}"
            f"{' — ' + st.session_state.etablissement_utilisateur if st.session_state.etablissement_utilisateur else ''}"
        )

    st.markdown(
        f"""
        <div class="navbar">
            <div class="logo">🩺 Medi<span>Extract</span></div>
            <div style="color:#64748b; font-weight:600;">
                {info_utilisateur or "Classement sécurisé de documents médicaux"}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if OPENROUTER_API_KEY == "VOTRE_CLE_ICI":
        st.warning("⚠️ Remplacez OPENROUTER_API_KEY dans le code par votre vraie clé OpenRouter.")


# ============================================================
# PAGE D'ACCUEIL
# ============================================================

def page_accueil() -> None:
    navbar()

    st.markdown(
        """
        <div class="hero">
            <div class="hero-badge">🔒 Extraction administrative sécurisée</div>
            <div class="hero-title">Classez vos documents médicaux <span>simplement</span></div>
            <div class="hero-text">
                Importez une ordonnance, un compte rendu, une analyse
                ou une image. MediExtract identifie le type du document
                et extrait uniquement les informations administratives
                autorisées, sans interprétation médicale.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    left, right = st.columns([1.4, 1], gap="large")

    with left:
        st.markdown(
            """
            <div class="section-title">Commencer</div>
            <div class="section-subtitle">Indiquez votre nom et votre établissement pour accéder à votre espace.</div>
            """,
            unsafe_allow_html=True,
        )

        nom = st.text_input("Votre nom", placeholder="Exemple : Dr. Hind Alaoui")
        etablissement = st.text_input("Votre établissement (hôpital / clinique / laboratoire)",
                                       placeholder="Exemple : Clinique Al Amal, Casablanca")

        if st.button("Accéder à mon espace →", type="primary", use_container_width=True):
            if nom.strip() and etablissement.strip():
                st.session_state.nom_utilisateur = nom.strip()
                st.session_state.etablissement_utilisateur = etablissement.strip()
                changer_page("espace")
            else:
                st.warning("Veuillez saisir votre nom et votre établissement.")

    with right:
        st.markdown(
            """
            <div class="custom-card">
                <div class="card-icon">📄</div>
                <div class="card-title">Documents acceptés</div>
                <div class="card-text">
                    <span class="tag">PDF</span>
                    <span class="tag">PNG</span>
                    <span class="tag">JPG</span>
                    <span class="tag">JPEG</span>
                    <br><br>
                    Ordonnances, certificats, comptes rendus,
                    analyses, lettres d'orientation et documents administratifs.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        """
        <div class="section-title" style="text-align:center; margin-top:55px;">Comment ça fonctionne ?</div>
        <div class="section-subtitle" style="text-align:center;">Un processus simple en trois étapes.</div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns(3, gap="large")

    with col1:
        st.markdown(
            """
            <div class="custom-card">
                <div class="card-icon">📤</div>
                <div class="card-title">1. Importation</div>
                <div class="card-text">Ajoutez une image ou un fichier PDF depuis votre ordinateur.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            """
            <div class="custom-card">
                <div class="card-icon">🤖</div>
                <div class="card-title">2. Analyse</div>
                <div class="card-text">Gemma (via OpenRouter) reconnaît le type du document et extrait les métadonnées autorisées.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            """
            <div class="custom-card">
                <div class="card-icon">🗂️</div>
                <div class="card-title">3. Classement</div>
                <div class="card-text">Le document est ajouté à votre espace personnel pour être consulté plus tard.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        """
        <div class="security-box">
            <strong>🛡️ Sécurité :</strong><br><br>
            Aucun diagnostic n'est interprété, aucun dosage n'est utilisé
            et aucun médicament n'est extrait. Les champs illisibles ou
            incertains sont signalés au lieu d'être devinés.
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# MENU DE L'ESPACE PERSONNEL
# ============================================================

def menu_espace() -> None:
    col1, col2, col3, col4, col5, col6 = st.columns([1, 1, 1, 1, 1, 1.2])

    with col1:
        if st.button("🏠 Tableau de bord", key="nav_dashboard", use_container_width=True):
            changer_page("espace")

    with col2:
        if st.button("📤 Importer", key="nav_importer", use_container_width=True):
            changer_page("importer")

    with col3:
        if st.button("📁 Mes documents", key="nav_documents", use_container_width=True):
            changer_page("documents")

    with col4:
        if st.button("🤖 Assistant", key="nav_assistant", use_container_width=True):
            changer_page("assistant")

    with col5:
        if st.button("ℹ️ À propos", key="nav_apropos", use_container_width=True):
            changer_page("apropos")

    with col6:
        if st.button("🚪 Quitter l'espace", key="nav_quitter", use_container_width=True):
            st.session_state.nom_utilisateur = ""
            st.session_state.etablissement_utilisateur = ""
            changer_page("accueil")

    st.divider()


# ============================================================
# PAGE ESPACE PERSONNEL
# ============================================================

def selecteur_patient() -> str | None:
    """
    Affiche un sélecteur de patient (liste déroulante + option 'Nouveau patient').
    Met à jour st.session_state.patient_id_actuel et retourne le patient_id choisi.
    """
    patients_existants = list(PATIENTS_DB.keys())
    labels = {
        pid: f"{pid} — {PATIENTS_DB[pid]['identite']['prenom']} {PATIENTS_DB[pid]['identite']['nom']}"
        for pid in patients_existants
    }
    options = patients_existants + ["+ Nouveau patient"]

    index_defaut = 0
    if st.session_state.patient_id_actuel in patients_existants:
        index_defaut = patients_existants.index(st.session_state.patient_id_actuel)

    choix = st.selectbox(
        "Patient",
        options=options,
        index=index_defaut,
        format_func=lambda x: labels.get(x, x),
    )

    if choix == "+ Nouveau patient":
        with st.form("form_nouveau_patient"):
            st.markdown("**Créer un nouveau patient**")
            nom = st.text_input("Nom")
            prenom = st.text_input("Prénom")
            date_naissance = st.text_input("Date de naissance (AAAA-MM-JJ)")
            sexe = st.selectbox("Sexe", ["F", "M"])
            tel_urgence = st.text_input("Téléphone contact d'urgence")
            nom_urgence = st.text_input("Nom du contact d'urgence")
            if st.form_submit_button("Créer le patient"):
                resultat = enregistrer_nouveau_patient(
                    identite={"nom": nom, "prenom": prenom, "date_naissance": date_naissance, "sexe": sexe},
                    allergies=[],
                    contact_urgence={"nom": nom_urgence, "lien": "-", "telephone": tel_urgence},
                )
                if resultat["succes"]:
                    st.session_state.patient_id_actuel = resultat["patient_id"]
                    st.success(f"Patient créé : {resultat['patient_id']}")
                    st.rerun()
                else:
                    st.error(resultat.get("erreur", "Erreur inconnue"))
        return None

    st.session_state.patient_id_actuel = choix
    return choix


def page_espace() -> None:
    navbar()
    menu_espace()

    nom = st.session_state.nom_utilisateur or "Utilisateur"

    st.markdown(
        f"""
        <div class="welcome-box">
            <h1>Bonjour {nom} 👋</h1>
            <p>Bienvenue dans votre espace personnel MediExtract. Vous pouvez importer, analyser et classer vos documents.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    total_patients = len(PATIENTS_DB)
    total_documents = sum(len(p["historique_documents"]) for p in PATIENTS_DB.values())
    total_valides = sum(1 for p in PATIENTS_DB.values() if p.get("rapport_valide"))

    col1, col2, col3 = st.columns(3, gap="large")

    with col1:
        st.metric(label="Patients enregistrés", value=total_patients)
    with col2:
        st.metric(label="Documents au total", value=total_documents)
    with col3:
        st.metric(label="Rapports validés", value=total_valides)

    st.markdown(
        """
        <div class="section-title">Actions rapides</div>
        <div class="section-subtitle">Sélectionnez l'action que vous souhaitez effectuer.</div>
        """,
        unsafe_allow_html=True,
    )

    action1, action2 = st.columns(2, gap="large")

    with action1:
        st.markdown(
            """
            <div class="custom-card">
                <div class="card-icon">📤</div>
                <div class="card-title">Analyser un nouveau document</div>
                <div class="card-text">Importez une ordonnance, un compte rendu, une analyse ou un certificat.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Importer un document", type="primary", use_container_width=True):
            changer_page("importer")

    with action2:
        st.markdown(
            """
            <div class="custom-card">
                <div class="card-icon">📂</div>
                <div class="card-title">Consulter mes documents</div>
                <div class="card-text">Retrouvez les documents déjà importés dans votre espace personnel.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Voir mes documents", use_container_width=True):
            changer_page("documents")


# ============================================================
# PAGE D'IMPORTATION — CONNECTÉE AU VRAI BACKEND
# ============================================================

def page_importer() -> None:
    navbar()
    menu_espace()

    st.markdown(
        """
        <div class="section-title">Importer un document</div>
        <div class="section-subtitle">Sélectionnez le patient concerné, puis ajoutez un PDF ou une image.</div>
        """,
        unsafe_allow_html=True,
    )

    patient_id = selecteur_patient()
    if not patient_id:
        return

    patient = PATIENTS_DB[patient_id]

    fichiers = st.file_uploader(
        "Glissez vos documents ici",
        type=["pdf", "png", "jpg", "jpeg"],
        help="Formats acceptés : PDF, PNG, JPG et JPEG. Vous pouvez en sélectionner plusieurs.",
        accept_multiple_files=True,
    )

    if fichiers:
        fichiers_non_analyses = list(fichiers)

        if fichiers_non_analyses:
            if st.button(f"⚡ Tout analyser ({len(fichiers_non_analyses)} document(s))",
                         type="primary", use_container_width=True, key="tout_analyser"):
                barre_progression = st.progress(0, text="Démarrage de l'analyse...")
                for idx, f in enumerate(fichiers_non_analyses):
                    ext = Path(f.name).suffix.lower().replace(".", "")
                    barre_progression.progress(
                        idx / len(fichiers_non_analyses),
                        text=f"Analyse de {f.name} ({idx + 1}/{len(fichiers_non_analyses)})..."
                    )

                    chemin_temp = os.path.join(tempfile.gettempdir(), f.name)
                    with open(chemin_temp, "wb") as out:
                        out.write(f.getbuffer())

                    resultat_reel = extraire_document_reel(chemin_temp, ext)
                    sauvegarder_document(patient_id, resultat_reel)

                barre_progression.progress(1.0, text="Terminé !")
                st.success(f"{len(fichiers_non_analyses)} document(s) analysé(s) et ajouté(s) au dossier de {patient_id}.")
                st.rerun()

            st.markdown("---")

        for i, fichier in enumerate(fichiers):
            extension = Path(fichier.name).suffix.lower().replace(".", "")

            st.markdown(f"#### 📄 {fichier.name}")
            col1, col2 = st.columns([1, 1.2], gap="large")

            with col1:
                if extension in {"png", "jpg", "jpeg"}:
                    st.image(fichier, caption=fichier.name, use_container_width=True)
                else:
                    st.info("📄 Aperçu PDF sélectionné")
                    st.write(f"**Nom :** {fichier.name}")
                    st.write(f"**Taille :** {fichier.size / 1024:.2f} Ko")

            with col2:
                st.markdown(
                    """
                    <div class="custom-card">
                        <div class="card-title">Informations du fichier</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                st.write(f"**Nom du fichier :** {fichier.name}")
                st.write(f"**Format :** {extension.upper()}")
                st.write(f"**Taille :** {fichier.size / 1024:.2f} Ko")
                st.write(f"**Patient concerné :** {patient_id}")

                if st.button(
                    "🔍 Analyser et enregistrer",
                    key=f"analyser_{i}_{fichier.name}",
                    type="primary",
                    use_container_width=True,
                ):
                    chemin_temp = os.path.join(tempfile.gettempdir(), fichier.name)
                    with open(chemin_temp, "wb") as f:
                        f.write(fichier.getbuffer())

                    with st.spinner(f"Analyse de {fichier.name} en cours (Gemma via OpenRouter)..."):
                        resultat_reel = extraire_document_reel(chemin_temp, extension)

                    sauvegarder_document(patient_id, resultat_reel)

                    st.success(f"{fichier.name} analysé et ajouté au dossier de {patient_id}.")

                    st.markdown(
                        """
                        <div class="result-card"><strong>Résultat de l'analyse</strong></div>
                        """,
                        unsafe_allow_html=True,
                    )

                    st.json(resultat_reel)

            st.divider()


# ============================================================
# PAGE MES DOCUMENTS — + BOUTON RAPPORT
# ============================================================

def page_documents() -> None:
    navbar()
    menu_espace()

    st.markdown(
        """
        <div class="section-title">Mes documents</div>
        <div class="section-subtitle">Sélectionnez un patient pour consulter son dossier.</div>
        """,
        unsafe_allow_html=True,
    )

    patient_id = selecteur_patient()
    if not patient_id:
        return

    patient = PATIENTS_DB[patient_id]

    if not patient["historique_documents"]:
        st.info("Aucun document n'a encore été importé pour ce patient.")
        if st.button("Importer un premier document", type="primary"):
            changer_page("importer")
        return

    if st.button("📄 Générer le rapport complet", type="primary"):
        st.session_state.dernier_rapport = generer_rapport_patient(patient_id)

    rapport = st.session_state.get("dernier_rapport")
    if rapport and rapport.get("patient_id") == patient_id:
        rapport_texte = rapport["texte"]
        st.markdown(f'<div class="result-card">{rapport_texte}</div>', unsafe_allow_html=True)

        col_dl, col_email = st.columns(2)

        with col_dl:
            st.download_button("Télécharger le rapport", data=rapport_texte,
                                file_name=f"rapport_{patient_id}.txt", mime="text/plain",
                                use_container_width=True)

        with col_email:
            with st.popover("📧 Envoyer par email", use_container_width=True):
                st.markdown("**Envoyer ce rapport par email**")
                email_destinataire = st.text_input("Adresse email du destinataire",
                                                    placeholder="exemple@hopital.ma",
                                                    key="email_dest_rapport")
                if st.button("Envoyer", key="btn_envoyer_email", type="primary", use_container_width=True):
                    if email_destinataire.strip():
                        resultat_envoi = envoyer_rapport_par_email(email_destinataire.strip(), rapport_texte)
                        if resultat_envoi["succes"]:
                            st.success(f"Rapport envoyé à {email_destinataire} ✅")
                        else:
                            st.error(f"Échec de l'envoi : {resultat_envoi['erreur']}")
                    else:
                        st.warning("Veuillez saisir une adresse email.")

        if not patient.get("rapport_valide"):
            nom_medecin_validateur = st.text_input("Votre nom (pour valider le rapport complet)",
                                                     key="nom_valid_rapport")
            if st.button("✅ Valider ce rapport", type="primary", disabled=not nom_medecin_validateur):
                resultat_validation = valider_rapport(patient_id, nom_medecin_validateur)
                if resultat_validation["succes"]:
                    st.success("Rapport validé.")
                    st.session_state.dernier_rapport = generer_rapport_patient(patient_id)
                    st.rerun()
                else:
                    st.error(resultat_validation.get("erreur", "Erreur inconnue"))
        else:
            st.success(f"✅ Rapport déjà validé par {patient.get('valide_par')} le {patient.get('date_validation')}")

    st.divider()

    documents_tries = sorted(patient["historique_documents"],
                              key=lambda d: d.get("date_ajout", ""), reverse=True)

    for vrai_index, document in enumerate(documents_tries):
        resultat = document["contenu"]

        titre_expander = f"📄 {resultat.get('type_document', 'document')} — {document['date_ajout']}"

        with st.expander(titre_expander):
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Source :** {resultat.get('source', '?')}")
            with col2:
                st.write(f"**Confiance :** {resultat.get('confidence', 0)}")

            st.markdown("---")

            tab_general, tab_medical = st.tabs(["📋 Informations générales", "💊 Médicaments & Résultats"])

            with tab_general:
                type_doc_modifie = st.text_input("Type de document", value=resultat.get("type_document") or "",
                                                  key=f"type_doc_{patient_id}_{vrai_index}")
                date_modifiee = st.text_input("Date du document", value=resultat.get("date_document") or "",
                                               key=f"date_{patient_id}_{vrai_index}")
                patient_modifie = st.text_input("Patient", value=resultat.get("patient") or "",
                                                 key=f"patient_{patient_id}_{vrai_index}")
                medecin_modifie = st.text_input("Médecin", value=resultat.get("medecin") or "",
                                                 key=f"medecin_{patient_id}_{vrai_index}")
                etablissement_modifie = st.text_input("Établissement", value=resultat.get("etablissement") or "",
                                                       key=f"etab_{patient_id}_{vrai_index}")
                resume_modifie = st.text_area("Résumé", value=resultat.get("resume_court") or "",
                                               key=f"resume_{patient_id}_{vrai_index}")

            with tab_medical:
                st.caption("Un médicament ou résultat par ligne, sous la forme : nom - dosage - fréquence")

                medicaments_texte_defaut = "\n".join(
                    f"{m.get('nom', '')} - {m.get('dosage', '')} - {m.get('frequence', '')}"
                    for m in resultat.get("medicaments", [])
                )
                medicaments_modifies = st.text_area("Médicaments", value=medicaments_texte_defaut,
                                                     key=f"medocs_{patient_id}_{vrai_index}", height=100)

                resultats_texte_defaut = "\n".join(
                    f"{r.get('parametre', '')} - {r.get('valeur', '')} - {r.get('unite', '')} - "
                    f"{r.get('valeurs_normales', '')}"
                    for r in resultat.get("resultats_examens", [])
                )
                resultats_modifies = st.text_area(
                    "Résultats d'examens (paramètre - valeur - unité - valeurs normales)",
                    value=resultats_texte_defaut, key=f"resexam_{patient_id}_{vrai_index}", height=100)

                diagnostic_modifie = st.text_area("Diagnostic", value=resultat.get("diagnostic") or "",
                                                   key=f"diag_{patient_id}_{vrai_index}")
                recommandations_modifiees = st.text_area("Recommandations",
                                                          value=resultat.get("recommandations") or "",
                                                          key=f"reco_{patient_id}_{vrai_index}")

            if st.button("✏️ Enregistrer les modifications", key=f"btn_mod_{patient_id}_{vrai_index}",
                          use_container_width=True):
                resultat["type_document"] = type_doc_modifie
                resultat["date_document"] = date_modifiee
                resultat["patient"] = patient_modifie
                resultat["medecin"] = medecin_modifie
                resultat["etablissement"] = etablissement_modifie
                resultat["resume_court"] = resume_modifie
                resultat["diagnostic"] = diagnostic_modifie
                resultat["recommandations"] = recommandations_modifiees

                nouveaux_medicaments = []
                for ligne in medicaments_modifies.strip().split("\n"):
                    if ligne.strip():
                        parts = [p.strip() for p in ligne.split(" - ")]
                        nouveaux_medicaments.append({
                            "nom": parts[0] if len(parts) > 0 else "",
                            "dosage": parts[1] if len(parts) > 1 else "",
                            "frequence": parts[2] if len(parts) > 2 else "",
                        })
                resultat["medicaments"] = nouveaux_medicaments

                nouveaux_resultats = []
                for ligne in resultats_modifies.strip().split("\n"):
                    if ligne.strip():
                        parts = [p.strip() for p in ligne.split(" - ")]
                        nouveaux_resultats.append({
                            "parametre": parts[0] if len(parts) > 0 else "",
                            "valeur": parts[1] if len(parts) > 1 else "",
                            "unite": parts[2] if len(parts) > 2 else "",
                            "valeurs_normales": parts[3] if len(parts) > 3 else "",
                        })
                resultat["resultats_examens"] = nouveaux_resultats

                document["contenu"] = resultat
                sauvegarder_patients_db(PATIENTS_DB)
                st.success("Modifications enregistrées.")
                st.rerun()


# ============================================================
# PAGE ASSISTANT — CHATBOT SUR LES DOCUMENTS ANALYSÉS
# ============================================================

def page_assistant() -> None:
    navbar()
    menu_espace()

    st.markdown(
        """
        <div class="section-title">Assistant</div>
        <div class="section-subtitle">Sélectionnez un patient, puis posez une question sur son dossier.</div>
        """,
        unsafe_allow_html=True,
    )

    patient_id = selecteur_patient()
    if not patient_id:
        return

    if "messages_chat" not in st.session_state:
        st.session_state.messages_chat = {}
    if patient_id not in st.session_state.messages_chat:
        st.session_state.messages_chat[patient_id] = []

    for msg in st.session_state.messages_chat[patient_id]:
        with st.chat_message(msg["role"]):
            st.write(msg["texte"])

    question = st.chat_input(f"Exemple : Ce patient a-t-il des allergies connues ?")
    if question:
        st.session_state.messages_chat[patient_id].append({"role": "user", "texte": question})
        with st.chat_message("user"):
            st.write(question)

        with st.chat_message("assistant"):
            with st.spinner("Recherche dans le dossier..."):
                resultat = decider_action(question, patient_id)
            st.write(resultat["reponse"])

        st.session_state.messages_chat[patient_id].append({"role": "assistant", "texte": resultat["reponse"]})


# ============================================================
# PAGE À PROPOS
# ============================================================

def page_apropos() -> None:
    navbar()
    menu_espace()

    st.markdown(
        """
        <div class="section-title">À propos de MediExtract</div>
        <div class="section-subtitle">Une application de classement intelligent de documents médicaux.</div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="custom-card">
            <div class="card-icon">🩺</div>
            <div class="card-title">Objectif de l'application</div>
            <div class="card-text">
                MediExtract permet d'importer des documents médicaux
                sous forme de PDF ou d'image, de reconnaître leur type
                et d'extraire uniquement des métadonnées administratives à faible risque.
                <br><br>
                L'application ne doit pas interpréter un diagnostic,
                utiliser un dosage ou générer un conseil médical.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# PROTECTION DES PAGES PERSONNELLES
# ============================================================

def utilisateur_connecte() -> bool:
    return bool(st.session_state.nom_utilisateur.strip())


# ============================================================
# ROUTEUR PRINCIPAL
# ============================================================

page = st.session_state.page

if page != "accueil" and not utilisateur_connecte():
    st.session_state.page = "accueil"
    st.rerun()

if page == "accueil":
    page_accueil()
elif page == "espace":
    page_espace()
elif page == "importer":
    page_importer()
elif page == "documents":
    page_documents()
elif page == "assistant":
    page_assistant()
elif page == "apropos":
    page_apropos()
else:
    st.session_state.page = "accueil"
    st.rerun()
