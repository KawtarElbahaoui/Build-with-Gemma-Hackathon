import streamlit as st
from ui.i18n import t
from ui.components import back_button

def render():
    lang = st.session_state.lang

    st.markdown(f'<h2 class="section-headline">{t("chat_title", lang)}</h2>', unsafe_allow_html=True)
    st.markdown(f'<p>{t("chat_sub", lang)}</p>', unsafe_allow_html=True)

    st.markdown(f'<div class="section-eyebrow">{t("suggested", lang)}</div>', unsafe_allow_html=True)
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
            <div class="chat-empty-state">
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
        align = "flex-start" if lang == "ar" else "flex-end"
        st.markdown(
            f"""
            <div class="chat-bubble-row" style="justify-content:{align};">
                <div class="chat-bubble chat-bubble-user">
                    {msg['content']}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        align = "flex-end" if lang == "ar" else "flex-start"
        st.markdown(
            f"""
            <div class="chat-bubble-row" style="justify-content:{align}; gap:8px; {'flex-direction: row-reverse;' if lang == 'ar' else ''}">
                <div class="chat-avatar">S</div>
                <div class="chat-bubble chat-bubble-assistant">
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
