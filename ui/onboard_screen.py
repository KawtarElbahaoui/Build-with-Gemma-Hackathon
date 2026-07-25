import streamlit as st
from ui.i18n import t
from assets.icons import file_text, camera, siren

def render():
    lang = st.session_state.lang
    step = st.session_state.get("onboard_step", 0)

    steps = [
        {
            "icon": file_text(size=64, color="#D9705B"),
            "bg": "#FDE4D0",
            "outer_ring": "rgba(217, 112, 91, 0.15)",
            "dot_color": "#E8967D",
            "title": t("onboard1_title", lang),
            "sub": t("onboard1_sub", lang),
        },
        {
            "icon": camera(size=64, color="#5C8B6E"),
            "bg": "#E0EDE4",
            "outer_ring": "rgba(92, 139, 110, 0.15)",
            "dot_color": "#7BA88F",
            "title": t("onboard2_title", lang),
            "sub": t("onboard2_sub", lang),
        },
        {
            "icon": siren(size=64, color="#C43D3D"),
            "bg": "#FCE0DA",
            "outer_ring": "rgba(196, 61, 61, 0.15)",
            "dot_color": "#D9705B",
            "title": t("onboard3_title", lang),
            "sub": t("onboard3_sub", lang),
        },
    ]
    total = len(steps)
    current = steps[step]

    # Skip button (top-left), language flip is now handled by the global header
    col_skip, _ = st.columns([1, 6])
    with col_skip:
        if st.button(t("skip", lang), key=f"onb_skip_{step}", type="secondary"):
            st.session_state.page = "home"
            st.rerun()

    # Step indicator
    st.markdown(
        f"""
        <div style="text-align:center; font-size:13px; color:#A67456;
                    font-weight:600; margin: 8px 0 20px; text-transform:uppercase;
                    letter-spacing:0.5px;">
            {step + 1} / {total}
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Illustration with double-ring effect
    st.markdown(
        f"""
        <div style="text-align:center; margin-bottom: 24px;">
            <div style="display:inline-flex; width:180px; height:180px; border-radius:50%;
                        background: {current['outer_ring']}; align-items:center;
                        justify-content:center; position:relative;">
                <div style="width:120px; height:120px; border-radius:50%;
                            background: {current['bg']}; display:flex;
                            align-items:center; justify-content:center;">
                    {current['icon']}
                </div>
                <div style="position:absolute; bottom:20px; right:20px; width:12px; height:12px;
                            border-radius:50%; background:{current['dot_color']};"></div>
            </div>
        </div>
        <h2 style="text-align:center; font-size:32px; margin:0 0 16px; color:#8B5A3C;">
            {current['title']}
        </h2>
        <p style="text-align:center; font-size:18px; color:#A67456; max-width:500px;
                  margin:0 auto 40px; line-height:1.6;">
            {current['sub']}
        </p>
        """,
        unsafe_allow_html=True,
    )

    # Progress dots
    dots = '<div style="display:flex; justify-content:center; gap:8px; margin-bottom:32px;">'
    for i in range(total):
        w = "32px" if i == step else "8px"
        c = current['dot_color'] if i == step else "#F5D5C4"
        dots += f'<div style="width:{w}; height:8px; border-radius:4px; background:{c}; transition:all 0.3s;"></div>'
    dots += '</div>'
    st.markdown(dots, unsafe_allow_html=True)

    c1, c2, c3 = st.columns([2, 3, 2])
    with c2:
        if st.button(t("next", lang) + " →", key=f"onb_next_{step}"):
            if step + 1 < total:
                st.session_state.onboard_step = step + 1
            else:
                st.session_state.page = "home"
            st.rerun()

    st.markdown("<div style='height: 60px;'></div>", unsafe_allow_html=True)