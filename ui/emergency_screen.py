import streamlit as st
from ui.i18n import t
from assets.icons import siren, alert_triangle, pill, droplet, phone, map_pin

def render():
    lang = st.session_state.lang    


    # Big emergency banner
    st.markdown(
        f"""
        <div style="background:linear-gradient(135deg, #E85A4F 0%, #C43D3D 100%);
                    border-radius:24px; padding:28px; margin-bottom:24px;
                    text-align:center; color:white;
                    box-shadow:0 12px 32px rgba(196,61,61,0.3);">
            <div style="margin-bottom:12px;">{siren(size=52, color="#FFFFFF")}</div>
            <div style="font-size:26px; font-weight:700; margin-bottom:6px;">{t('emergency', lang)}</div>
            <div style="font-size:15px; color:rgba(255,255,255,0.9);">{t('critical_info', lang)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    data = mock_urgence()

    fields = [
        (t("allergies", lang), ", ".join(data["allergies"]), alert_triangle(size=20, color="#D9705B")),
        (t("current_meds", lang), ", ".join(data["treatments"]), pill(size=20, color="#7BA88F")),
        (t("blood_type", lang), f'<span class="ltr-inline">{data["blood_type"]}</span>', droplet(size=20, color="#D9705B")),
        (t("emergency_contact", lang), f'<span class="ltr-inline">{data["contact"]}</span>', phone(size=20, color="#8B5A3C")),
    ]

    for label, value, icon in fields:
        border_side = "right" if lang == "ar" else "left"
        st.markdown(
            f"""
            <div style="background:white; border-{border_side}:6px solid #E85A4F;
                        border-radius:16px; padding:20px 24px; margin-bottom:12px;
                        box-shadow:0 4px 12px rgba(139,90,60,0.06);">
                <div style="font-size:14px; color:#A67456; margin-bottom:6px;
                            display:flex; align-items:center; gap:6px;">
                    {icon} {label}
                </div>
                <div style="font-size:22px; font-weight:700; color:#8B5A3C;">
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
            <div style="background:linear-gradient(135deg, #7BA88F 0%, #5C8B6E 100%);
                        color:white; padding:22px; border-radius:20px;
                        text-align:center; font-size:20px; font-weight:700;
                        margin-top:20px; box-shadow:0 8px 24px rgba(92,139,110,0.3);
                        display:flex; align-items:center; justify-content:center; gap:10px;">
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