import streamlit as st
import easyocr
from PIL import Image
import tempfile
import openai
import time

# Initialize EasyOCR with desired languages
reader = easyocr.Reader(['pt', 'en'], gpu=False)

st.header("Tradutor de Laudos de Exames Médicos")
st.caption("Selecione o arquivo que deseja traduzir")

# File uploader for image selection
laudo_original = st.file_uploader("Selecione o arquivo", type=['png', 'jpg', 'jpeg'])

# Define function to process image on button click
@st.cache_data(show_spinner="Extaindo texto do laudo..." )
def process_image():
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
    return texto_laudo

if laudo_original is not None:
    if st.button("Enviar"):
    # Display the OCR result as a paragraph
        texto_laudo = process_image()
        expander = st.expander("Texto Extraído do Laudo Original")
        expander.write(texto_laudo)

# LLM integration
client = openai.OpenAI()
openai.api_key = st.secrets["OPENAI_API_KEY"]

if "texto_laudo" in locals():
        with st.spinner("Traduzindo laudo..."):
            time.sleep(5)
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                    "role": "system",
                    "content": "You are a specialist in translating medical and scientific jargon to laypeople for easy understanding. You are to receive as input a text extracted from medical reports, and to give as output an easy-to-understand explanation of the described findings. If the findings are concerning, you may suggest the person to contact the referring provider and book an appointment soon. If the findings are not concerning, provide relief but state that the referring doctor's opinion should be the final one. Respond in the same language as the text you receive. The text is scanned with OCR so it could contain typos. Guess the meaning of nonsense words by the surrounding context."
                    },
                    {
                    "role": "user",
                    "content": texto_laudo
                    }
                ],
                temperature=1,
                max_tokens=1024,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
                )
        st.success("Tradução concluída!")
        resposta = response['choices'][0]['message']['content']
        st.write(resposta)