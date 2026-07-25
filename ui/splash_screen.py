import streamlit as st
from ui.i18n import t
from assets.icons import stethoscope, file_text, camera, siren, lock, wifi_off, heart

def render():
    lang = st.session_state.lang
    _render_hero(lang)
    _render_mission(lang)
    _render_how_it_works(lang)
    _render_trust(lang)
    _render_final_cta(lang)

def _render_hero(lang):
    st.markdown(
        f"""
        <div style="text-align:center; width:100%; max-width:700px; margin:0 auto; padding:40px 0;">
            <div class="section-eyebrow">{t('hero_eyebrow', lang)}</div>
            <div style="display:inline-flex; width:160px; height:160px; border-radius:50%;
                        background: linear-gradient(135deg, #FDE4D0 0%, #F5B79A 100%);
                        align-items:center; justify-content:center; margin:24px auto 32px;">
                {stethoscope(size=80, color="#8B5A3C")}
            </div>
            <h1 style="font-size:56px; margin:0 0 16px; color:#8B5A3C; text-align:center;">
                {t('app_name', lang)}
            </h1>
            <p style="font-size:20px; color:#A67456; margin:0 0 48px; text-align:center;">
                {t('tagline', lang)}
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Centered CTAs
    c1, c2, c3 = st.columns([2, 3, 2])
    with c2:
        if st.button(t("get_started", lang), key="splash_start", use_container_width=True):
            st.session_state.page = "onboard"
            st.rerun()

        st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

        if st.button(t("skip_emergency", lang) + " →", key="splash_emerg", type="secondary"):
            st.session_state.page = "emergency"
            st.rerun()

    st.markdown("<div style='height: 60px;'></div>", unsafe_allow_html=True)

def _render_mission(lang):
    st.markdown(
        f"""
        <div style="text-align:center;">
            <div class="mission-card" style="max-width:640px; margin:48px auto;">
                <div class="section-eyebrow">{t('mission_eyebrow', lang)}</div>
                <h2 class="section-headline">{t('mission_headline', lang)}</h2>
                <p style="font-size:16px; color:#A67456; line-height:1.7; margin:0; text-align:center;">
                    {t('mission_body', lang)}
                </p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

def _render_how_it_works(lang):
    st.markdown(
        f"""
        <div style="text-align:center; margin:48px 0 24px;">
            <div class="section-eyebrow">{t('how_eyebrow', lang)}</div>
            <h2 class="section-headline">{t('how_headline', lang)}</h2>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(
            f"""
            <div class="step-card">
                <div class="numbered-badge-1">1</div>
                <div style="margin-bottom:12px;">{file_text(size=32, color="#D9705B")}</div>
                <div style="font-size:16px; font-weight:600; color:#8B5A3C; margin-bottom:8px;">
                    {t('step1_title', lang)}
                </div>
                <div style="font-size:14px; color:#A67456; line-height:1.5;">
                    {t('step1_desc', lang)}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            f"""
            <div class="step-card">
                <div class="numbered-badge-2">2</div>
                <div style="margin-bottom:12px;">{camera(size=32, color="#5C8B6E")}</div>
                <div style="font-size:16px; font-weight:600; color:#8B5A3C; margin-bottom:8px;">
                    {t('step2_title', lang)}
                </div>
                <div style="font-size:14px; color:#A67456; line-height:1.5;">
                    {t('step2_desc', lang)}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col3:
        st.markdown(
            f"""
            <div class="step-card">
                <div class="numbered-badge-3">3</div>
                <div style="margin-bottom:12px;">{siren(size=32, color="#C43D3D")}</div>
                <div style="font-size:16px; font-weight:600; color:#8B5A3C; margin-bottom:8px;">
                    {t('step3_title', lang)}
                </div>
                <div style="font-size:14px; color:#A67456; line-height:1.5;">
                    {t('step3_desc', lang)}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

def _render_trust(lang):
    st.markdown(
        f"""
        <div style="text-align:center; margin:48px 0 24px; padding:24px;">
            <span class="trust-pill">
                {lock(size=16, color="#A67456")} {t('trust_privacy', lang)}
            </span>
            <span class="trust-pill">
                {wifi_off(size=16, color="#A67456")} {t('trust_offline', lang)}
            </span>
            <span class="trust-pill">
                {heart(size=16, color="#A67456")} {t('trust_morocco', lang)}
            </span>
        </div>
        """,
        unsafe_allow_html=True,
    )

def _render_final_cta(lang):
    st.markdown(
        f"""
        <div style="text-align:center;">
            <div class="final-cta-card" style="max-width:640px; margin:48px auto; padding:48px 32px;">
                <h2 class="section-headline" style="margin-bottom:24px; text-align:center;">{t('final_cta_headline', lang)}</h2>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    c1, c2, c3 = st.columns([2, 3, 2])
    with c2:
        if st.button(t("final_cta_button", lang), key="final_cta", use_container_width=True):
            st.session_state.page = "onboard"
            st.rerun()
