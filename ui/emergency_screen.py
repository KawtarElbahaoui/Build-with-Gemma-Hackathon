import streamlit as st
from ui.i18n import t
from assets.icons import siren, alert_triangle, pill, droplet, phone, map_pin

def render():
    lang = st.session_state.lang

    # Big emergency banner — bright red for life-safety
    st.markdown(
        f"""
        <div class="emergency-banner-large">
            <div class="emergency-icon-large">{siren(size=52, color="#FFFFFF")}</div>
            <div class="emergency-content-large">
                <div class="emergency-title-large">{t('emergency', lang)}</div>
                <div class="emergency-subtitle-large">{t('critical_info', lang)}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    data = mock_urgence()

    fields = [
        (t("allergies", lang), ", ".join(data["allergies"]), alert_triangle(size=20, color="#C4623E")),
        (t("current_meds", lang), ", ".join(data["treatments"]), pill(size=20, color="#5C8B6E")),
        (t("blood_type", lang), f'<span class="ltr-inline">{data["blood_type"]}</span>', droplet(size=20, color="#C4623E")),
        (t("emergency_contact", lang), f'<span class="ltr-inline">{data["contact"]}</span>', phone(size=20, color="#C4623E")),
    ]

    for label, value, icon in fields:
        border_side = "right" if lang == "ar" else "left"
        st.markdown(
            f"""
            <div class="emergency-info-card" style="border-{border_side}-color: #E85A4F;">
                <div class="emergency-info-label">
                    {icon} {label}
                </div>
                <div class="emergency-info-value">
                    {value}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    lat, lon = 33.2651, -7.5877
    maps_url = f"https://www.google.com/maps/search/hopital+urgence/@{lat},{lon},15z"
    st.markdown(
        f"""
        <a href="{maps_url}" target="_blank" style="text-decoration:none;">
            <div class="hospital-button">
                {map_pin(size=24, color="#FFFFFF")} {t('nearest_hospital', lang)}
            </div>
        </a>
        """,
        unsafe_allow_html=True,
    )

def mock_urgence():
    return {
        "allergies": ["Penicillin", "Peanuts"],
        "treatments": ["Metformin 500mg", "Lisinopril 10mg"],
        "blood_type": "O+",
        "contact": "+212 6 12 34 56 78",
    }