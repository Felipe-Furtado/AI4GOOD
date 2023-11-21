import streamlit as st
import easyocr
from PIL import Image
import tempfile

# Initialize EasyOCR with desired languages
reader = easyocr.Reader(['pt', 'en'], gpu=False)

st.header("Tradutor de Laudos de Exames Médicos")
st.caption("Selecione o arquivo que deseja traduzir")

# File uploader for image selection
laudo_original = st.file_uploader("Selecione o arquivo", type=['png', 'jpg', 'jpeg'])

if laudo_original is not None:
    # Save the uploaded image to a temporary file
    temp_image = tempfile.NamedTemporaryFile(delete=False)
    temp_image.write(laudo_original.read())

    # Close the temporary file to release the file handle
    temp_image.close()

    # Read the image using PIL
    image = Image.open(temp_image.name)
    
    # Perform OCR on the image using EasyOCR
    # Extract text from the temporary image file
    text_results = reader.readtext(temp_image.name, detail=0)
    
    # Combine the list of strings into a paragraph
    # Join the list elements with a space
    texto_laudo = ' '.join(text_results)
    
    # Display the OCR result as a paragraph
    st.header("Texto do Laudo Original")
    st.write(texto_laudo)