import streamlit as st
from ui.i18n import t
from ui.components import back_button
from assets.icons import clock, check

MOCK_MEDS = [
    {"name": "Metformin", "dosage": "500 mg", "schedule": "morning_evening",
     "next_dose": "next_dose_in", "taken": False},
    {"name": "Amlodipine", "dosage": "5 mg", "schedule": "once_daily_morning",
     "next_dose": "taken_today", "taken": True},
]

def render():
    lang = st.session_state.lang
   

    st.markdown(
        f"<h2 style='font-size:28px; margin:16px 0 24px;'>{t('meds_title', lang)}</h2>",
        unsafe_allow_html=True,
    )

    for i, med in enumerate(MOCK_MEDS):
        _med_card(med, lang, key=f"med_{i}")

def _med_card(med, lang, key):
    taken = med["taken"]
    schedule_label = t(med["schedule"], lang)

    if taken:
        card_class = "med-card taken"
        status_html = f'<div class="med-status-circle done">{check(size=18, color="#FFFFFF")}</div>'
        footer = f"""
        <div style="display:flex; align-items:center; gap:6px; color:#5C8B6E;
                    font-size:14px; font-weight:600; margin-top:12px;">
            {clock(size=16, color="#5C8B6E")} {t('taken_today', lang)}
        </div>
        """
    else:
        card_class = "med-card"
        status_html = '<div class="med-status-circle"></div>'
        footer = f"""
        <div style="display:flex; align-items:center; gap:6px; color:#D9705B;
                    font-size:14px; font-weight:600; margin-top:8px; margin-bottom:12px;">
            {clock(size=16, color="#D9705B")} {t('next_dose_in', lang)} {t('hours', lang)}
        </div>
        """

    st.markdown(
        f"""
        <div class="{card_class}">
            <div style="display:flex; align-items:flex-start; gap:14px;">
                {status_html}
                <div style="flex:1;">
                    <div style="display:flex; justify-content:space-between; align-items:baseline;">
                        <div style="font-size:20px; font-weight:700; color:#8B5A3C;">{med['name']}</div>
                        <div style="font-size:14px; color:#D9705B; font-weight:600;">{med['dosage']}</div>
                    </div>
                    <div style="font-size:14px; color:#A67456; margin-top:4px;">{schedule_label}</div>
                    {footer}
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if not taken:
        st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)
        if st.button(t("log_taken", lang), key=key, type="secondary"):
            # In real version, call Block 3 to record the intake
            st.success("✓")
