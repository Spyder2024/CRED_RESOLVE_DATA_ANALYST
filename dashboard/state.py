import streamlit as st


def get_theme() -> str:
    if "theme" not in st.session_state:
        qp = st.query_params.get("theme", "light")
        st.session_state["theme"] = "dark" if qp == "dark" else "light"
    return st.session_state["theme"]


def set_theme(mode: str) -> None:
    st.session_state["theme"] = mode
    st.query_params["theme"] = mode
    st.rerun()


def init_state() -> None:
    st.session_state.setdefault("complete_only", True)
    st.session_state.setdefault("segment", "All")
