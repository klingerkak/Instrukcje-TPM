import streamlit as st
import pandas as pd
from datetime import datetime
from io import BytesIO

st.set_page_config(page_title="Instrukcje TPM", layout="wide")
st.title("🛠️ Kreator instrukcji TPM")

if "data" not in st.session_state:
    st.session_state.data = []

with st.form("add_task"):
    st.subheader("➕ Dodaj nowe zadanie")
    col1, col2 = st.columns(2)

    with col1:
        no = st.text_input("Numer (No)")
        czynnosc = st.text_input("Czynność")
        kategoria = st.selectbox("Kategoria", ["BHP", "Jakość", "Inna"])
        odpowiedzialny = st.text_input("Odpowiedzialny dział", value="PRD")

    with col2:
        metoda = st.multiselect("Metoda wykonania", ["Wizualnie", "Manualnie", "Pomiar", "Inna"])
        uwagi = st.text_area("Uwagi")
        data = st.date_input("Data aktualizacji", value=datetime.today())

    if st.form_submit_button("Dodaj zadanie"):
        st.session_state.data.append({
            "No": no,
            "Czynność": czynnosc,
            "Kategoria": kategoria,
            "Metoda": ", ".join(metoda),
            "Uwagi": uwagi,
            "Odpowiedzialny": odpowiedzialny,
            "Data": data.strftime("%Y-%m-%d")
        })
        st.success("✅ Zadanie dodane!")

if st.session_state.data:
    st.subheader("📋 Lista zadań")
    df = pd.DataFrame(st.session_state.data)
    st.dataframe(df, use_container_width=True)

    def to_excel(df):
        output = BytesIO()
        with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
            df.to_excel(writer, index=False, sheet_name="Instrukcja")
        return output.getvalue()

    excel_data = to_excel(df)
    st.download_button("📥 Pobierz jako Excel", data=excel_data,
                       file_name="instrukcja_TPM.xlsx")
