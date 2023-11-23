import streamlit as st
import easyocr
from PIL import Image
import tempfile
import openai
import time
import os

# Initialize EasyOCR with desired languages
reader = easyocr.Reader(['pt', 'en'], gpu=False)

st.header("Tradutor de Laudos de Exames Médicos")
st.caption("Selecione o arquivo que deseja traduzir")

# File uploader for image selection
laudo_original = st.file_uploader("Selecione o arquivo", type=['png', 'jpg', 'jpeg'])

# Define function to process image on button click
@st.cache_data(show_spinner="Extraindo texto do laudo..." )
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
    with st.spinner("Extraindo texto do laudo..."):
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
openai.api_key = st.secrets["OPENAI_API_KEY"]
client = openai.OpenAI()
if "texto_laudo" in locals():
        with st.spinner("Traduzindo laudo..."):
            time.sleep(5)
            llm_call = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                    "role": "system",
                    "content": "Você é um ótimo professor capaz de explicar termos médicos e científicos com linguagem amigável e acessível a leigos, facilitando o entendimento. Sua tarefa é receber um texto extraído de relatórios médicos e fornecer uma explicação sobre os achados descritos de fácil compreensão para o paciente. O texto deve ser suficientemente simples para ser entendido por um estudante do ensino médio, e não deve conter jargões ou palavras que podem ser desconhecidas.\nSe os achados forem preocupantes, você pode sugerir que a pessoa entre em contato com o médico responsável e marque uma consulta em breve. Se os achados não forem preocupantes, traga alívio, mas ressalte que a opinião do médico responsável deve ser a final.\nResponda no mesmo idioma do texto que você receber. O texto foi escaneado com OCR, então pode conter erros tipográficos. Tente deduzir o significado de palavras sem sentido com base no contexto ao redor. Caso o texto não tenha sentido ou esteja com muitos erros, você pode solicitar uma nova foto. Obrigado!"
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
        if llm_call is not None:
            st.success("Tradução concluída!")
            st.cache_data.clear()
            resposta = llm_call.choices[0].message.content
            st.write(resposta)
             