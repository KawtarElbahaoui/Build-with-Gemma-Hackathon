"""
Landing / splash screen — organic-system-aligned rebuild.

Layout matches the Claude Design mockups:
    1. Landing header (compact: brand + text nav + language pill + Get Started CTA)
    2. Hero — left-aligned, Caprasimo headline, sage quarter-circle decoration
    3. Mission card — warm tan background
    4. How it works — 3 step cards with colored icon badges
    5. Trust pills — outlined rust
    6. Split section — "See your history, instantly" + photo placeholder
    7. Final CTA — mint card with text left + button right (single visual unit)
    8. Landing footer — brand / tagline / hackathon credit
"""

import streamlit as st
from ui.i18n import t
from assets.icons import (
    file_text, camera, siren, lock, wifi_off, heart, image_icon,
)


# ============================================================================
# Copy that isn't in ui/i18n.py yet.
# When you're ready, migrate these keys into i18n.py and swap `s()` for `t()`.
# ============================================================================
_STRINGS = {
    "en": {
        "hero_headline_1":   "Your health,",
        "hero_headline_2":   "remembered.",
        "hero_body":         ("Sehati uses AI to reconstruct your medical history from "
                              "photos of your documents — so critical information is "
                              "never lost when it matters most."),
        "nav_how":           "How it works",
        "nav_chat":          "Chat",
        "paper_eyebrow":     "FROM PAPER TO PIXELS",
        "paper_headline_1":  "See your history,",
        "paper_headline_2":  "instantly",
        "paper_body":        ("Every document you photograph is read, structured and "
                              "stored on your device — readable at a glance by you, "
                              "a doctor, or an emergency responder, even without a "
                              "connection."),
        "final_cta_body":    "Join now — your digital medical record takes just a few minutes to set up.",
        "photo_caption":     "Photo: a hand photographing a prescription with a phone",
        "browse_files":      "or browse files",
    },
    "ar": {
        "hero_headline_1":   "صحتك،",
        "hero_headline_2":   "محفوظة.",
        "hero_body":         ("تستخدم صحتي الذكاء الاصطناعي لإعادة بناء تاريخك الطبي "
                              "من صور مستنداتك — حتى لا تُفقد المعلومات الحيوية عندما "
                              "تحتاج إليها."),
        "nav_how":           "كيف يعمل",
        "nav_chat":          "الدردشة",
        "paper_eyebrow":     "من الورق إلى البكسل",
        "paper_headline_1":  "شاهد تاريخك،",
        "paper_headline_2":  "فوراً",
        "paper_body":        ("كل مستند تصوّره يُقرأ ويُنظَّم ويُحفَظ على جهازك — يمكن "
                              "قراءته بلمحة من قِبَلك أو من قِبَل الطبيب أو المسعف، "
                              "حتى بدون اتصال بالإنترنت."),
        "final_cta_body":    "انضم الآن — يستغرق سجلك الطبي الرقمي بضع دقائق فقط للإعداد.",
        "photo_caption":     "صورة: يد تصوّر وصفة طبية بالهاتف",
        "browse_files":      "أو تصفّح الملفات",
    },
}


def s(key: str, lang: str) -> str:
    """Local copy fallback — mirrors t() shape."""
    return _STRINGS.get(lang, _STRINGS["en"]).get(key) or _STRINGS["en"].get(key, key)


# ============================================================================
# Public render
# ============================================================================
def render():
    lang = st.session_state.lang
    _render_landing_header(lang)
    _render_hero(lang)
    _render_mission(lang)
    _render_how_it_works(lang)
    _render_trust(lang)
    _render_split(lang)
    _render_final_cta(lang)
    _render_landing_footer(lang)


# ============================================================================
# Landing header — brand + text-link nav + lang pill + filled Get Started CTA
# ============================================================================
def _render_landing_header(lang):
    other_lang = "en" if lang == "ar" else "ar"
    other_label = "English" if lang == "ar" else "العربية"

    col_brand, col_home, col_how, col_chat, col_lang, col_cta = st.columns(
        [4, 1, 1.6, 1, 1.1, 1.7]
    )

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
    with col_home:
        if st.button(t("nav_home", lang), key="lp_home", type="secondary"):
            st.session_state.page = "splash"
            st.rerun()
    with col_how:
        st.markdown(
            f'<a href="#how-it-works" class="nav-anchor">{s("nav_how", lang)}</a>',
            unsafe_allow_html=True,
        )
    with col_chat:
        if st.button(s("nav_chat", lang), key="lp_chat", type="secondary"):
            st.session_state.page = "chat"
            st.rerun()
    with col_lang:
        if st.button(other_label, key="lp_lang", type="secondary"):
            st.session_state.lang = other_lang
            st.rerun()
    with col_cta:
        if st.button(t("get_started", lang), key="lp_cta", type="primary"):   # primary (filled rust)
            st.session_state.page = "onboard"
            st.rerun()

    st.markdown('<hr class="app-header-divider">', unsafe_allow_html=True)


# ============================================================================
# Hero — left-aligned editorial layout with sage quarter-circle
# ============================================================================
def _render_hero(lang):
    # Activity/pulse icon (Lucide) — matches the small stroked icon in the mockup
    pulse_svg = (
        '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" '
        'viewBox="0 0 24 24" fill="none" stroke="#C4623E" stroke-width="2.5" '
        'stroke-linecap="round" stroke-linejoin="round">'
        '<polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/>'
        '</svg>'
    )
    st.markdown(
        f"""
        <div class="hero-wrap">
            <div class="hero-eyebrow-row">
                <div class="hero-eyebrow-icon">{pulse_svg}</div>
                <div class="section-eyebrow" style="margin:0;">
                    {t('hero_eyebrow', lang)}
                </div>
            </div>
            <h1 class="hero-title">
                {s('hero_headline_1', lang)}<br>{s('hero_headline_2', lang)}
            </h1>
            <p class="hero-tagline">{s('hero_body', lang)}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # CTAs — narrow columns on the left keep them left-aligned + naturally sized
    c1, c2, _spacer = st.columns([1.4, 1.8, 4])
    with c1:
        if st.button(t("get_started", lang), key="hero_start", type="primary"):     # primary
            st.session_state.page = "onboard"
            st.rerun()
    with c2:
        if st.button(t("skip_emergency", lang) + " →",
                     key="hero_emerg", type="secondary"):
            st.session_state.page = "emergency"
            st.rerun()


# ============================================================================
# Mission — warm tan card
# ============================================================================
def _render_mission(lang):
    st.markdown(
        f"""
        <div class="mission-card">
            <div class="section-eyebrow">{t('mission_eyebrow', lang)}</div>
            <h2>{t('mission_headline', lang)}</h2>
            <p>{t('mission_body', lang)}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================================
# How it works — 3 step cards
# ============================================================================
def _render_how_it_works(lang):
    st.markdown(
        f"""
        <div class="how-header" id="how-it-works">
            <div class="section-eyebrow">{t('how_eyebrow', lang)}</div>
            <h2 class="section-headline">{t('how_headline', lang)}</h2>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns(3, gap="medium")
    with col1:
        st.markdown(
            f"""
            <div class="step-card">
                <div class="icon-badge badge-coral">{file_text(size=22, color="#C4623E")}</div>
                <h3>{t('step1_title', lang)}</h3>
                <p>{t('step1_desc', lang)}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            f"""
            <div class="step-card">
                <div class="icon-badge badge-mint">{camera(size=22, color="#4B7A5F")}</div>
                <h3>{t('step2_title', lang)}</h3>
                <p>{t('step2_desc', lang)}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col3:
        st.markdown(
            f"""
            <div class="step-card">
                <div class="icon-badge badge-peach">{siren(size=22, color="#C4623E")}</div>
                <h3>{t('step3_title', lang)}</h3>
                <p>{t('step3_desc', lang)}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )


# ============================================================================
# Trust pills — outlined rust
# ============================================================================
def _render_trust(lang):
    st.markdown(
        f"""
        <div class="trust-strip">
            <span class="trust-pill">{lock(size=16, color="#C4623E")} {t('trust_privacy', lang)}</span>
            <span class="trust-pill">{wifi_off(size=16, color="#C4623E")} {t('trust_offline', lang)}</span>
            <span class="trust-pill">{heart(size=16, color="#C4623E")} {t('trust_morocco', lang)}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================================
# Split section — text left, photo placeholder right (single HTML block, grid)
# ============================================================================
def _render_split(lang):
    st.markdown(
        f"""
        <div class="split-section">
            <div class="split-grid">
                <div class="split-left">
                    <div class="section-eyebrow">{s('paper_eyebrow', lang)}</div>
                    <h2 class="section-headline">
                        {s('paper_headline_1', lang)}<br>{s('paper_headline_2', lang)}
                    </h2>
                    <p>{s('paper_body', lang)}</p>
                </div>
                <div class="split-right">
                    <div class="split-placeholder">
                        {image_icon(size=32, color="#7A5F49")}
                        <div>{s('photo_caption', lang)}</div>
                        <a class="browse-link" href="#">{s('browse_files', lang)}</a>
                    </div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================================
# Final CTA — mint card, text left, filled button right (single visual unit)
#
# Trick: emit a hidden marker markdown, immediately followed by st.columns.
# CSS hides the marker's element_container and styles the *next sibling*
# (the columns' horizontal block) as the mint card. Text + button therefore
# render visually inside the same card even though they're separate widgets.
# ============================================================================
def _render_final_cta(lang):
    st.markdown('<div class="__mint-cta-marker"></div>', unsafe_allow_html=True)

    c_text, c_btn = st.columns([3.2, 1.3])
    with c_text:
        st.markdown(
            f"""
            <div class="mint-cta-text">
                <h2>{t('final_cta_headline', lang)}</h2>
                <p>{s('final_cta_body', lang)}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c_btn:
        if st.button(t("final_cta_button", lang), key="final_cta", type="primary"):
            st.session_state.page = "onboard"
            st.rerun()


# ============================================================================
# Landing footer — brand / tagline / hackathon credit
# ============================================================================
def _render_landing_footer(lang):
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