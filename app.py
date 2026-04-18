import streamlit as st


st.set_page_config(page_title="Workers Compensation Project", layout="wide")


pages = {
    "Меню проекта": [
        st.Page("analysis_and_model.py", title=" Анализ и модель"),
        st.Page("presentation.py", title=" Презентация"),
    ]
}


pg = st.navigation(pages)
pg.run()