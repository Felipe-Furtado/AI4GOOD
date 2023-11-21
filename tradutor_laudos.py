import streamlit as st
import easyocr

reader = easyocr.Reader('pt', gpu = False)

st.header("Tradutor de Laudos de Exames Médicos")
st.caption("Selecione o arquivo que deseja traduzir")

laudo_original = st.file_uploader("Selecione o arquivo", type=['png', 'jpg', 'jpeg'])

if laudo_original is not None:
    texto_laudo = reader.readtext(laudo_original, detail = 0)
    # Imprimir texto para debug
    st.header("Texto do Laudo Original")
    st.write(texto_laudo)