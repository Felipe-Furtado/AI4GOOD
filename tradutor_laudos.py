import streamlit as st
import easyocr
from PIL import Image
import io

reader = easyocr.Reader(['pt', 'en'], gpu=False)

st.header("Tradutor de Laudos de Exames Médicos")
st.caption("Selecione o arquivo que deseja traduzir")

laudo_original = st.file_uploader("Selecione o arquivo", type=['png', 'jpg', 'jpeg'])

if laudo_original is not None:
    # Read the uploaded image
    image = Image.open(io.BytesIO(laudo_original.read()))
    
    # Perform OCR on the image
    texto_laudo = reader.readtext(image, detail=0)
    
    # Display the OCR result
    st.header("Texto do Laudo Original")
    st.write(texto_laudo)