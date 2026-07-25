import streamlit as st
from ui.i18n import t
from ui.components import back_button

def render():
    lang = st.session_state.lang
    

    st.markdown(
        f"""
        <h2 style="font-size:26px; margin:16px 0 4px;">{t('chat_title', lang)}</h2>
        <p style="font-size:14px; color:#A67456; margin:0 0 20px;">{t('chat_sub', lang)}</p>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"<div style='font-size:13px; color:#A67456; font-weight:600; margin-bottom:10px; text-transform:uppercase; letter-spacing:0.5px;'>{t('suggested', lang)}</div>",
        unsafe_allow_html=True,
    )
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button(t("q1", lang), key="q1", type="secondary"):
            _handle(t("q1", lang))
    with c2:
        if st.button(t("q2", lang), key="q2", type="secondary"):
            _handle(t("q2", lang))
    with c3:
        if st.button(t("q3", lang), key="q3", type="secondary"):
            _handle(t("q3", lang))

    st.markdown("<div style='height:16px;'></div>", unsafe_allow_html=True)

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if not st.session_state.messages:
        st.markdown(
            f"""
            <div style="background:rgba(255,255,255,0.5); border-radius:20px;
                        padding:32px; text-align:center; color:#A67456;
                        font-style:italic; margin-bottom:16px;">
                {t('chat_empty', lang)}
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        for msg in st.session_state.messages:
            _render_bubble(msg, lang)

    st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)
    with st.form(key="chat_form", clear_on_submit=True):
        col_input, col_send = st.columns([6, 1])
        with col_input:
            prompt = st.text_input(
                "msg",
                placeholder=t("chat_placeholder", lang),
                label_visibility="collapsed",
                key="chat_input_field",
            )
        with col_send:
            submitted = st.form_submit_button("↑", use_container_width=True)

        if submitted and prompt:
            _handle(prompt)

def _render_bubble(msg, lang):
    is_user = msg["role"] == "user"
    if is_user:
        # Filled coral bubble, right-aligned in LTR / left-aligned in RTL
        align = "flex-start" if lang == "ar" else "flex-end"
        st.markdown(
            f"""
            <div style="display:flex; justify-content:{align}; margin-bottom:10px;">
                <div style="max-width:75%; background:linear-gradient(135deg, #E8967D 0%, #D9705B 100%);
                            color:white; border-radius:20px; padding:12px 18px;
                            font-size:15px; line-height:1.5;
                            box-shadow: 0 4px 12px rgba(217,112,91,0.2);">
                    {msg['content']}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        # White bubble with small avatar dot
        align = "flex-end" if lang == "ar" else "flex-start"
        st.markdown(
            f"""
            <div style="display:flex; justify-content:{align}; margin-bottom:10px; gap:8px;
                        {'flex-direction: row-reverse;' if lang == 'ar' else ''}">
                <div style="width:28px; height:28px; border-radius:50%;
                            background:#E0EDE4; display:flex; align-items:center;
                            justify-content:center; font-size:12px; font-weight:700;
                            color:#5C8B6E; flex-shrink:0; margin-top:6px;">S</div>
                <div style="max-width:75%; background:white; border:1px solid #F5D5C4;
                            border-radius:20px; padding:12px 18px; color:#8B5A3C;
                            font-size:15px; line-height:1.5;
                            box-shadow: 0 2px 8px rgba(139,90,60,0.05);">
                    {msg['content']}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

def _handle(prompt):
    st.session_state.messages.append({"role": "user", "content": prompt})
    response = f"(Mock) You asked: '{prompt}'. Once Block 1 is wired, real reply here."
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.rerun()
