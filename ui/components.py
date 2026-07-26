"""
Shared UI components — header, footer, greeting card, nav helpers.

Design notes:
- Landing header (marketing nav: Home / How it works / Chat) lives in
  splash_screen.py because it has different items than the internal nav.
- This module's app_header() is for internal screens: Home / History /
  Meds / Chat. Same visual language (small brand + text-link nav + lang
  pill) — the landing header just swaps its middle items.
"""

import streamlit as st
from ui.i18n import t


# ============================================================================
# CSS loader
# ============================================================================
def load_css():
    """Inject the global CSS + RTL adjustments for Arabic."""
    with open("ui/styles.css", "r", encoding="utf-8") as f:
        css = f.read()
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

    if st.session_state.get("lang") == "ar":
        st.markdown(
            """
            <style>
                .stApp { direction: rtl; }
                .block-container { text-align: right; }
                h1, h2, h3, h4 { font-family: 'Cairo', sans-serif !important; }
                p, div, span, li { font-family: 'Cairo', sans-serif; }
            </style>
            """,
            unsafe_allow_html=True,
        )


# ============================================================================
# Internal-screen header — brand + Home/History/Meds/Chat + language pill
# ============================================================================
def app_header(show_nav: bool = True):
    lang = st.session_state.get("lang", "ar")
    other_lang = "en" if lang == "ar" else "ar"
    other_label = "English" if lang == "ar" else "العربية"

    if show_nav:
        col_brand, col_h, col_hi, col_me, col_ch, col_lang = st.columns(
            [4, 1, 1.3, 1.3, 1, 1.1]
        )
    else:
        col_brand, _, col_lang = st.columns([4, 5, 1.1])

    with col_brand:
        st.markdown(
            f"""
            <div class="app-header-brand">
                <div class="dot">S</div>
                <div class="name">{t('app_name', lang)}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    if show_nav:
        nav_pairs = [
            (col_h,  "home",    t("nav_home", lang)),
            (col_hi, "history", t("nav_history_short", lang)),
            (col_me, "meds",    t("nav_meds_short", lang)),
            (col_ch, "chat",    t("nav_chat_short", lang)),
        ]
        for col, page_key, label in nav_pairs:
            with col:
                if st.button(label, key=f"nav_{page_key}", type="secondary"):
                    st.session_state.page = page_key
                    st.rerun()

    with col_lang:
        if st.button(other_label, key="header_lang_flip", type="secondary"):
            st.session_state.lang = other_lang
            st.rerun()

    st.markdown('<hr class="app-header-divider">', unsafe_allow_html=True)


# ============================================================================
# Global footer
# ============================================================================
def app_footer():
    lang = st.session_state.get("lang", "ar")
    st.markdown(
        f"""
        <div class="app-footer-row">
            <div class="brand">
                <div class="brand-dot"></div>
                <span><strong>{t('app_name', lang)}</strong> · v1.0</span>
            </div>
            <div class="center-tagline">{t('footer_tagline', lang)}</div>
            <div class="credit">GDG × Gemma · 2026</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================================
# Profile greeting — small "Hello, {name}" card for Home + internal screens
# ============================================================================
def profile_greeting():
    p = st.session_state.profile
    lang = st.session_state.lang
    name = p["nameAr"] if lang == "ar" else p["name"]
    initials = name[0] if name else "?"

    st.markdown(
        f"""
        <div class="profile-greeting">
            <div class="avatar">{initials}</div>
            <div>
                <div class="hi">{t('hello', lang)}</div>
                <div class="who">{name}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================================
# Legacy helpers (kept so existing screens don't break)
# ============================================================================
def back_button():
    """Nav header replaces most uses — kept for screens that still call it."""
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


def language_toggle():
    lang = st.session_state.get("lang", "ar")
    other_lang = "en" if lang == "ar" else "ar"
    other_label = "English" if lang == "ar" else "العربية"
    if st.button(other_label, key="fallback_lang_flip", type="secondary"):
        st.session_state.lang = other_lang
        st.rerun()


def profile_header():
    """Old screens that call profile_header() get header + greeting together."""
    app_header(show_nav=True)
    profile_greeting()
    