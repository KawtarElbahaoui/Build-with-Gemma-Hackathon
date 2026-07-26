import streamlit as st
from ui.components import load_css, app_header, app_footer
from ui import (
    splash_screen,
    onboard_screen,
    home_screen,
    upload_screen,
    chat_screen,
    emergency_screen,
    history_screen,
    meds_screen,
)

st.set_page_config(
    page_title="Sehati",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# --- Session state defaults ---
if "lang" not in st.session_state:
    st.session_state.lang = "ar"
if "page" not in st.session_state:
    st.session_state.page = "splash"
if "onboard_step" not in st.session_state:
    st.session_state.onboard_step = 0
if "profile" not in st.session_state:
    st.session_state.profile = {
        "name": "Fatima Zahra",
        "nameAr": "فاطمة الزهراء",
        "age": 68,
        "color": "#F5B79A",
        "blood_type": "O+",
    }

load_css()

page = st.session_state.page

# Splash renders its OWN landing header + footer — do not wrap it.
if page == "splash":
    splash_screen.render()
elif page == "onboard":
    app_header(show_nav=True)
    onboard_screen.render()
    app_footer()
else:
    app_header(show_nav=True)
    if page == "home":
        home_screen.render()
    elif page == "upload":
        upload_screen.render()
    elif page == "chat":
        chat_screen.render()
    elif page == "emergency":
        emergency_screen.render()
    elif page == "history":
        history_screen.render()
    elif page == "meds":
        meds_screen.render()
    else:
        st.session_state.page = "splash"
        st.rerun()
    app_footer()