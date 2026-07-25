import streamlit as st
from ui.i18n import t
from ui.components import profile_greeting, go_to
from assets.icons import file_text, message_circle, pill, heart, siren


def render():
    lang = st.session_state.lang

    profile_greeting()

    # Emergency banner — clickable
    st.markdown(
        f"""
        <style>
            .stButton > button[data-testid="baseButton-primary"][key="home_emerg_btn"] {{
                background: linear-gradient(135deg, #E85A4F 0%, #C43D3D 100%) !important;
                color: white !important;
                border: none !important;
                border-radius: 20px !important;
                padding: 24px !important;
                font-size: 20px !important;
                font-weight: 700 !important;
                min-height: auto !important;
                box-shadow: 0 8px 24px rgba(196, 61, 61, 0.3) !important;
                display: flex !important;
                align-items: center !important;
                justify-content: flex-start !important;
                gap: 20px !important;
                text-align: left !important;
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )
    
    if st.button(f"{siren(size=30, color='#FFFFFF')} {t('emergency', lang)}", key="home_emerg_btn", use_container_width=True):
        go_to("emergency")

    st.markdown(
        f"<div style='font-size:13px; color:#A67456; font-weight:600; margin:28px 0 12px; text-transform:uppercase; letter-spacing:0.5px;'>{t('quick_actions', lang)}</div>",
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)
    with col1:
        _card(
            icon=message_circle(size=24, color="#8A6BB0"),
            badge_class="badge-lavender",
            title=t("ask_health", lang),
            subtitle=t("ask_health_sub", lang),
            target="chat",
            key="c_chat",
        )
        _card(
            icon=pill(size=24, color="#5C8B6E"),
            badge_class="badge-mint",
            title=t("my_meds", lang),
            subtitle=t("my_meds_sub", lang),
            target="meds",
            key="c_meds",
        )
    with col2:
        _card(
            icon=file_text(size=24, color="#D9705B"),
            badge_class="badge-coral",
            title=t("add_doc", lang),
            subtitle=t("add_doc_sub", lang),
            target="upload",
            key="c_up",
        )
        _card(
            icon=heart(size=24, color="#C88569"),
            badge_class="badge-peach",
            title=t("my_history", lang),
            subtitle=t("my_history_sub", lang),
            target="history",
            key="c_hist",
        )

    st.markdown(
        f"""
        <div style="background: rgba(255,255,255,0.5); border-radius:16px;
                    padding: 16px 20px; margin-top: 24px;">
            <div style="font-size:12px; color:#A67456; font-weight:600;
                        margin-bottom:6px; text-transform:uppercase; letter-spacing:0.5px;">
                {t('recent', lang)}
            </div>
            <div style="font-size:15px; color:#8B5A3C; display:flex; align-items:center; gap:8px;">
                {file_text(size=18, color="#8B5A3C")} {t('last_doc', lang)}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _card(icon, badge_class, title, subtitle, target, key):
    st.markdown(
        f"""
        <div style="background:white; border:1px solid #F5D5C4; border-radius:18px;
                    padding:20px; margin-bottom:8px; min-height:140px;">
            <div class="icon-badge {badge_class}">{icon}</div>
            <div style="font-size:17px; font-weight:600; color:#8B5A3C; margin-bottom:4px;">{title}</div>
            <div style="font-size:13px; color:#A67456;">{subtitle}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button(title, key=key, type="secondary"):
        go_to(target)
        