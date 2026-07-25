import streamlit as st
from ui.i18n import t


def load_css():
    """Inject the global CSS + RTL toggle."""
    with open("ui/styles.css", "r", encoding="utf-8") as f:
        css = f.read()
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

    if st.session_state.get("lang") == "ar":
        st.markdown(
            """
            <style>
                .stApp { direction: rtl; }
                .block-container { text-align: right; }
                h1, h2, h3, h4, p, div, span { font-family: 'Cairo', sans-serif !important; }
            </style>
            """,
            unsafe_allow_html=True,
        )


def app_header(show_nav: bool = True):
    """Persistent global header. Logo + nav + language flip, in a flat column layout."""
    lang = st.session_state.get("lang", "ar")
    current_page = st.session_state.get("page", "home")
    other_lang = "en" if lang == "ar" else "ar"
    other_label = "English" if lang == "ar" else "العربية"

    if show_nav:
        # Flat columns: logo, 4 nav buttons, language = 6 columns total
        col_logo, col_h, col_hi, col_me, col_ch, col_lang = st.columns([3, 2, 2, 2, 2, 2])
    else:
        col_logo, _, col_lang = st.columns([2, 6, 2])

    with col_logo:
        st.markdown(
            f"""
            <div style="display:flex; align-items:center; gap:10px; padding-top:8px;">
                <div style="width:36px; height:36px; border-radius:50%;
                            background: linear-gradient(135deg, #E8967D 0%, #D9705B 100%);
                            display:flex; align-items:center; justify-content:center;
                            font-size:16px; font-weight:700; color:white;
                            box-shadow: 0 4px 12px rgba(217,112,91,0.25);">S</div>
                <div style="font-size:20px; font-weight:700; color:#8B5A3C;
                            font-family: 'Inter', sans-serif;">
                    {t('app_name', lang)}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("", key="logo_home_link"):
            st.session_state.page = "home"
            st.rerun()

    if show_nav:
        nav_pairs = [
            (col_h, "home", t("nav_home", lang)),
            (col_hi, "history", t("nav_history_short", lang)),
            (col_me, "meds", t("nav_meds_short", lang)),
            (col_ch, "chat", t("nav_chat_short", lang)),
        ]
        for col, page_key, label in nav_pairs:
            with col:
                active = current_page == page_key
                if st.button(
                    label,
                    key=f"nav_{page_key}",
                    type="primary" if active else "secondary",
                    use_container_width=True,
                ):
                    st.session_state.page = page_key
                    st.rerun()

    with col_lang:
        if st.button(other_label, key="header_lang_flip", type="secondary", use_container_width=True):
            st.session_state.lang = other_lang
            st.rerun()

    st.markdown(
        """
        <hr style="margin: 20px 0 32px; border: none;
                   border-top: 1px solid rgba(245, 213, 196, 0.6);">
        """,
        unsafe_allow_html=True,
    )


def app_footer():
    """Persistent global footer."""
    lang = st.session_state.get("lang", "ar")
    st.markdown(
        f"""
        <div style="margin-top: 60px; padding-top: 24px;
                    border-top: 1px solid rgba(245, 213, 196, 0.5);
                    display: flex; justify-content: space-between;
                    align-items: center; flex-wrap: wrap; gap: 12px;
                    color: #A67456; font-size: 13px;">
            <div style="display:flex; align-items:center; gap:8px;">
                <div style="width:20px; height:20px; border-radius:50%;
                            background: linear-gradient(135deg, #E8967D 0%, #D9705B 100%);"></div>
                <span><strong style="color:#8B5A3C;">{t('app_name', lang)}</strong> · v1.0</span>
            </div>
            <div style="text-align:center; opacity:0.85;">
                {t('footer_tagline', lang)}
            </div>
            <div style="opacity:0.7;">
                GDG × Gemma · 2026
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def profile_greeting():
    """Small in-page greeting card. Used on Home and internal screens.
       This is NOT the header — it's a warm hello above the content."""
    p = st.session_state.profile
    lang = st.session_state.lang
    name = p["nameAr"] if lang == "ar" else p["name"]
    initials = name[0] if name else "?"

    st.markdown(
        f"""
        <div style="max-width: 320px; display:flex; align-items:center; gap:14px; margin-bottom: 24px;
                    background: rgba(255,255,255,0.6); padding: 14px 18px;
                    border-radius: 16px; border: 1px solid rgba(245,213,196,0.5);">
            <div style="width:44px; height:44px; border-radius:50%;
                        background: linear-gradient(135deg, #F5B79A 0%, #E8967D 100%);
                        display:flex; align-items:center; justify-content:center;
                        font-size:18px; font-weight:700; color:white; flex-shrink:0;">
                {initials}
            </div>
            <div>
                <div style="font-size:12px; color:#A67456; line-height:1.2;">
                    {t('hello', lang)}
                </div>
                <div style="font-size:16px; font-weight:700; color:#8B5A3C; line-height:1.3;">
                    {name}
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def back_button():
    """Kept for backward compat but the nav header replaces the need for it."""
    lang = st.session_state.lang
    arrow = "→" if lang == "ar" else "←"
    c1, _ = st.columns([2, 8])
    with c1:
        if st.button(
            f"{arrow} {t('back', lang)}",
            key=f"back_{st.session_state.page}",
            type="secondary",
        ):
            st.session_state.page = "home"
            st.rerun()


def go_to(page: str):
    st.session_state.page = page
    st.rerun()


# Kept for splash/onboarding backward compat if any old code still calls them
def language_toggle():
    lang = st.session_state.get("lang", "ar")
    other_lang = "en" if lang == "ar" else "ar"
    other_label = "English" if lang == "ar" else "العربية"
    if st.button(other_label, key="fallback_lang_flip", type="secondary"):
        st.session_state.lang = other_lang
        st.rerun()


def profile_header():
    """Backward compat wrapper — old screens still call this."""
    app_header(show_nav=True)
    profile_greeting()