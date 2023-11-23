import streamlit as st
import easyocr
from PIL import Image
import tempfile
import openai
import os

# Initialize EasyOCR with desired languages
@st.cache_resource
def load_model():
    reader = easyocr.Reader(['pt', 'en'], gpu=False)
    return reader

reader = load_model()

st.header("Tradutor de Laudos de Exames Médicos")
st.caption("Selecione o arquivo que deseja traduzir")

# File uploader for image selection
laudo_original = st.file_uploader("Selecione o arquivo", type=['png', 'jpg', 'jpeg'])

# Define function to process image on button click
@st.cache_data(show_spinner="Extraindo texto do laudo..." )
def process_image():
    # Save the uploaded image to a temporary file
    with tempfile.NamedTemporaryFile(delete=False) as temp_image:
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

#TODO Comment & remove API Key after local testing
#os.environ["OPENAI_API_KEY"] = "sk-..."
openai.api_key = st.secrets["OPENAI_API_KEY"]
client = openai.OpenAI()
if "texto_laudo" in locals():
        with st.spinner("Traduzindo laudo..."):
            llm_call = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                    "role": "system",
                    "content": "Você é um ótimo professor capaz de explicar termos médicos e científicos com linguagem amigável e acessível a leigos. Sua tarefa é receber um laudo de exame médico e fornecer uma explicação sobre os achados descritos para o paciente. O texto deve ser de fácil compreensão e suficientemente simples para ser entendido por um estudante do ensino fundamental. Não use termos técnicos, jargões ou, palavras que podem ser desconhecidas. Use um vocabulário coloquial e sempre que possível faça analogias para melhorar a compreensão.\nSe os achados forem preocupantes, você deve sugerir que a pessoa entre em contato com o médico responsável e marque uma consulta em breve. Use o emoji 🚨 para avisar sobre achados críticos. Se os achados não forem preocupantes, traga alívio, mas ressalte que a opinião do médico responsável deve ser a final.\nResponda no mesmo idioma do texto que você receber. O texto foi escaneado com OCR, então pode conter erros tipográficos. Tente deduzir o significado de palavras sem sentido com base no contexto ao redor. Caso o texto não tenha sentido ou esteja com muitos erros, você pode solicitar uma nova foto. Obrigado!"
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
             