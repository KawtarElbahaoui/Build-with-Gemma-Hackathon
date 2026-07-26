import streamlit as st
from ui.i18n import t
from assets.icons import file_text, camera, siren

def render():
    lang = st.session_state.lang
    step = st.session_state.get("onboard_step", 0)

    steps = [
        {
            "icon": file_text(size=36, color="#C4623E"),
            "badge_class": "badge-peach",
            "title": t("onboard1_title", lang),
            "sub": t("onboard1_sub", lang),
        },
        {
            "icon": camera(size=36, color="#5C8B6E"),
            "badge_class": "badge-mint",
            "title": t("onboard2_title", lang),
            "sub": t("onboard2_sub", lang),
        },
        {
            "icon": siren(size=36, color="#C4623E"),
            "badge_class": "badge-coral",
            "title": t("onboard3_title", lang),
            "sub": t("onboard3_sub", lang),
        },
    ]
    total = len(steps)
    current = steps[step]

    # Skip button (top-left)
    col_skip, _ = st.columns([1, 6])
    with col_skip:
        if st.button(t("skip", lang), key=f"onb_skip_{step}", type="secondary"):
            st.session_state.page = "home"
            st.rerun()

    # Step indicator
    st.markdown(
        f'<div class="onboard-step-indicator">{step + 1} / {total}</div>',
        unsafe_allow_html=True,
    )

    # Illustration with icon badge
    st.markdown(
        f"""
        <div class="onboard-illustration">
            <div class="icon-badge {current['badge_class']}" style="width:96px; height:96px;">
                {current['icon']}
            </div>
        </div>
        <h2 class="onboard-title">{current['title']}</h2>
        <p class="onboard-subtitle">{current['sub']}</p>
        """,
        unsafe_allow_html=True,
    )

    # Progress dots
    dots = '<div class="onboard-progress-dots">'
    for i in range(total):
        active_class = "active" if i == step else ""
        dots += f'<div class="onboard-dot {active_class}"></div>'
    dots += '</div>'
    st.markdown(dots, unsafe_allow_html=True)

    c1, c2, c3 = st.columns([2, 3, 2])
    with c2:
        button_text = t("get_started", lang) if step == total - 1 else t("next", lang) + " →"
        if st.button(button_text, key=f"onb_next_{step}"):
            if step + 1 < total:
                st.session_state.onboard_step = step + 1
            else:
                st.session_state.page = "home"
            st.rerun()

    st.markdown("<div style='height: 60px;'></div>", unsafe_allow_html=True)