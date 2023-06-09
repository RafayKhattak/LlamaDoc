# Import necessary libraries and modules
import streamlit as st
import urllib
import base64
import openai
import os
import fitz
from model import search
from PIL import Image

# Get API key 
OPENAI_API_KEY = st.secrets['OPENAI_API_KEY']
# Set OpenAI API key
openai.api_key = OPENAI_API_KEY

# Set page configuration and title for Streamlit
st.set_page_config(page_title="LlamaDoc", page_icon="📁", layout="wide")

# Add header with title and description
st.markdown('<p style="display:inline-block;font-size:40px;font-weight:bold;">🦙LlamaDoc </p> <p style="display:inline-block;font-size:16px;">With LlamaIndex&#39;s in-context learning approach, LlamaDoc leverages the reasoning capabilities of LLMs to provide accurate and insightful responses from a PDF file. <br><br></p>', unsafe_allow_html=True)

# Function to save an uploaded file
def save_uploadedfile(uploaded_file):
    with open(os.path.join("data", uploaded_file.name), "wb") as file:
        file.write(uploaded_file.getbuffer())
    return st.success("Saved File: {} to directory".format(uploaded_file.name))

@st.cache_data
# Function to display the PDF of a given file
def display_PDF(file):
    # Opening file from the file path
    with open(file, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')

    # Converting Base64-encoded PDF data to bytes
    pdf_data = base64.b64decode(base64_pdf)

    # Opening PDF with PyMuPDF
    doc = fitz.open(stream=pdf_data, filetype="pdf")

    # Displaying each page of the PDF
    for page in doc:
        pix = page.get_pixmap()
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        st.image(img)

    # Closing the PDF document
    doc.close()
    
# File upload section
uploaded_pdf = st.file_uploader("Upload your PDF", type=['pdf'])

if uploaded_pdf is not None:
    col1, col2 = st.columns([3, 2])
    with col1:
        input_file = save_uploadedfile(uploaded_pdf)
        pdf_file = "data/" + uploaded_pdf.name
        pdf_view = display_PDF(pdf_file)
    with col2:
        query_search = st.text_area("Search your query:")
        if st.checkbox("Search"):
            st.info("Your query: " + query_search)
            st.text("Please wait...")
            result = search(query_search)
            st.write("🤖: ")
            st.write(result)

# Hide Streamlit header, footer, and menu
hide_st_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
"""

# Apply CSS code to hide header, footer, and menu
st.markdown(hide_st_style, unsafe_allow_html=True)
