import streamlit as st
from PIL import Image
from ui.i18n import t
from ui.components import profile_greeting


def render():
    lang = st.session_state.lang

    st.markdown(f'<h2 class="section-headline">{t("upload_title", lang)}</h2>', unsafe_allow_html=True)
    st.markdown(f'<p>{t("upload_help", lang)}</p>', unsafe_allow_html=True)

    uploaded = st.file_uploader(
        t("upload_button", lang),
        type=["png", "jpg", "jpeg"],
        label_visibility="collapsed",
    )

    if uploaded is not None:
        st.session_state.uploaded_image = uploaded
        with st.spinner(t("extracting", lang)):
            extracted = mock_extraction()
            st.session_state.extracted_data = extracted
        _show_validation(extracted, uploaded, lang)

def _show_validation(data, image_file, lang):
    st.markdown(f'<h3 class="section-headline" style="font-size:32px;">{t("review_title", lang)}</h3>', unsafe_allow_html=True)
    col_img, col_form = st.columns(2)
    with col_img:
        st.image(Image.open(image_file), use_container_width=True)
    with col_form:
        data["medication"] = st.text_input(t("field_medication", lang), data.get("medication", ""))
        data["dosage"] = st.text_input(t("field_dosage", lang), data.get("dosage", ""))
        data["frequency"] = st.text_input(t("field_frequency", lang), data.get("frequency", ""))
        data["doctor"] = st.text_input(t("field_doctor", lang), data.get("doctor", ""))
        data["date"] = st.text_input(t("field_date", lang), data.get("date", ""))
        if st.button(t("confirm_save", lang), key="upload_save"):
            st.success(t("saved_success", lang))

def mock_extraction():
    return {
        "medication": "Amoxicillin 500mg",
        "dosage": "500mg",
        "frequency": "3x per day",
        "doctor": "Dr. Alaoui",
        "date": "2026-07-20",
    }
