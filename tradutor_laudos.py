import streamlit as st
import easyocr
from PIL import Image
import tempfile
from openai import OpenAI

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
    with st.spinner("Extraindo texto..."):
        text_results = reader.readtext(temp_image.name, detail=0)
    
    # Combine the list of strings into a paragraph
    # Join the list elements with a space
    texto_laudo = ' '.join(text_results)
    
    # Display the OCR result as a paragraph
    with st.expander("Texto do Laudo Original"):
        st.write(texto_laudo)

# LLM integration
client = OpenAI()
openai.api_key = st.secrets["OPENAI_API_KEY"]
if laudo_original is not None and st.button("Traduzir"):
    with st.spinner("Traduzindo..."):
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
    max_tokens=2048,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
    )
        st.success("Tradução concluída!")
        st.write(response.choices[0].text)