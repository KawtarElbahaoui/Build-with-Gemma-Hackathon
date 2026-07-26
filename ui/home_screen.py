import streamlit as st
from ui.i18n import t
from ui.components import profile_greeting, go_to
from assets.icons import file_text, message_circle, pill, heart, siren


def render():
    lang = st.session_state.lang

    profile_greeting()

    # Emergency banner — clickable whole card
    emerg_html = f"""
    <div class="emergency-banner">
        <div class="emergency-icon">{siren(size=36, color="#FFFFFF")}</div>
        <div class="emergency-content">
            <div class="emergency-title">{t('emergency', lang)}</div>
            <div class="emergency-subtitle">{t('critical_info', lang)}</div>
        </div>
        <div class="emergency-chevron">→</div>
    </div>
    """
    st.markdown(f'<div class="clickable-emerg-anchor">{emerg_html}</div>', unsafe_allow_html=True)
    if st.button(" ", key="home_emerg_btn"):
        go_to("emergency")

    st.markdown(f'<div class="section-eyebrow">{t("quick_actions", lang)}</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        _card(
            icon=message_circle(size=22, color="#8A6BB0"),
            badge_class="badge-lavender",
            title=t("ask_health", lang),
            subtitle=t("ask_health_sub", lang),
            target="chat",
            key="c_chat",
        )
        _card(
            icon=pill(size=22, color="#5C8B6E"),
            badge_class="badge-mint",
            title=t("my_meds", lang),
            subtitle=t("my_meds_sub", lang),
            target="meds",
            key="c_meds",
        )
    with col2:
        _card(
            icon=file_text(size=22, color="#C4623E"),
            badge_class="badge-coral",
            title=t("add_doc", lang),
            subtitle=t("add_doc_sub", lang),
            target="upload",
            key="c_up",
        )
        _card(
            icon=heart(size=22, color="#C4623E"),
            badge_class="badge-peach",
            title=t("my_history", lang),
            subtitle=t("my_history_sub", lang),
            target="history",
            key="c_hist",
        )

    # Recent activity strip
    st.markdown(
        f"""
        <div class="recent-activity">
            <div class="section-eyebrow" style="margin-bottom: 8px;">{t('recent', lang)}</div>
            <div class="recent-item">
                {file_text(size=18, color="#C4623E")} {t('last_doc', lang)}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _card(icon, badge_class, title, subtitle, target, key):
    st.markdown(
        f"""
        <div class="action-card card-clickable-anchor" data-card-key="{key}">
            <div class="icon-badge {badge_class}">{icon}</div>
            <h3>{title}</h3>
            <p>{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button(" ", key=key):
        go_to(target)
        