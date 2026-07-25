import streamlit as st
from ui.i18n import t
from ui.components import back_button
from assets.icons import file_text, flask, note

# Mock data — swap with Block 3's document store
MOCK_DOCS = [
    {"type": "prescription", "doctor": "Dr. Saeed Alaoui", "date": "14 Jul 2025",
     "summary": "Metformin 500mg — twice daily"},
    {"type": "lab", "doctor": "Al-Madina Lab", "date": "2 Jun 2025",
     "summary": "Full blood count — normal"},
    {"type": "prescription", "doctor": "Dr. Najwa Benali", "date": "18 May 2025",
     "summary": "Amoxicillin 5mg — once daily"},
    {"type": "note", "doctor": "Personal note", "date": "3 Apr 2025",
     "summary": "Slight knee pain when climbing stairs"},
    {"type": "lab", "doctor": "Dr. Karim Al-Mansouri", "date": "10 Mar 2025",
     "summary": "Blood sugar 5.8 mmol/L"},
]

def render():
    lang = st.session_state.lang
    

    st.markdown(
        f"<h2 style='font-size:28px; margin:16px 0 20px;'>{t('history_title', lang)}</h2>",
        unsafe_allow_html=True,
    )

    # Filter chips
    if "history_filter" not in st.session_state:
        st.session_state.history_filter = "all"

    filters = [
        ("all", t("filter_all", lang)),
        ("prescription", t("filter_prescriptions", lang)),
        ("lab", t("filter_labs", lang)),
        ("note", t("filter_notes", lang)),
    ]

    cols = st.columns(len(filters))
    for i, (key, label) in enumerate(filters):
        with cols[i]:
            active = st.session_state.history_filter == key
            if st.button(
                label,
                key=f"filter_{key}",
                type="primary" if active else "secondary",
            ):
                st.session_state.history_filter = key
                st.rerun()

    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

    # Filter docs
    active_filter = st.session_state.history_filter
    docs = MOCK_DOCS if active_filter == "all" else [d for d in MOCK_DOCS if d["type"] == active_filter]

    # Icon + tag styling per type
    type_meta = {
        "prescription": {"icon": file_text(size=22, color="#D9705B"), "bg": "#FCE0DA",
                          "tag_key": "type_prescription", "tag_class": "tag-prescription"},
        "lab": {"icon": flask(size=22, color="#5C8B6E"), "bg": "#E0EDE4",
                "tag_key": "type_lab", "tag_class": "tag-lab"},
        "note": {"icon": note(size=22, color="#8A6BB0"), "bg": "#ECE4F0",
                 "tag_key": "type_note", "tag_class": "tag-note"},
    }

    for doc in docs:
        meta = type_meta[doc["type"]]
        st.markdown(
            f"""
            <div class="doc-row">
                <div style="width:44px; height:44px; border-radius:12px;
                            background:{meta['bg']}; display:flex;
                            align-items:center; justify-content:center;">
                    {meta['icon']}
                </div>
                <div style="flex:1;">
                    <div style="font-size:16px; font-weight:600; color:#8B5A3C; margin-bottom:2px;">
                        {doc['doctor']}
                    </div>
                    <div style="font-size:13px; color:#A67456; margin-bottom:6px;">
                        {doc['date']} · {doc['summary']}
                    </div>
                    <span class="doc-tag {meta['tag_class']}">{t(meta['tag_key'], lang)}</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    if not docs:
        st.markdown(
            f"""
            <div style="background:rgba(255,255,255,0.5); border-radius:16px;
                        padding:32px; text-align:center; color:#A67456;">
                <div style="margin-bottom:12px;">{file_text(size=32, color="#A67456")}</div>
                <div style="font-size:15px;">{t('no_documents', lang)}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
