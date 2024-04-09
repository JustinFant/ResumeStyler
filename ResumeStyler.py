import streamlit as st
import os
import json
import base64
from PyPDF2 import PdfReader
from io import BytesIO
from docx import Document
from functions.extract_info import extract_info
from functions.fetch_data import fetch_data
from functions.format_response import format_response

st.set_page_config(page_title="BEPC-ResumeStyler", page_icon="static/logo.png", layout='wide')


def get_image_base64(image_path):
  with open(image_path, 'rb') as img_file:
    return base64.b64encode(img_file.read()).decode('utf-8')

sr2new = get_image_base64('static/rs2.png')

st.markdown(
  f"""
  <div class="container">
      <h2 class="text-center mt-4">
          <img src="data:image/png;base64,{sr2new}" width="75" height="75" class="d-inline-block align-top" alt="">
          Resume Styler <span style="font-style: italic; font-size: 17px;">for recruiting V2.0</span>
      </h2>
  </div>
  """,
  unsafe_allow_html=True,
)

resume = st.file_uploader('Upload Resume', type=['pdf', 'docx'])
header = st.checkbox('Include Header?', value=False)
if header:
  division = st.selectbox('Select Division', ['US', 'MX'])
else:
  division = None

if st.button('Style Resume', type = 'primary') and resume is not None:
  with st.spinner('Styling resume...'):
    # Read JSON Schema
    with open('helpers/schema.txt', 'r') as file:
      schema = file.read()

    if resume.name.endswith('.pdf'):
      reader = PdfReader(resume)
      content = ''.join([page.extract_text() for page in reader.pages])
    elif resume.name.endswith('.docx'):
      doc = Document(BytesIO(resume.read()))
      content = ' '.join([paragraph.text for paragraph in doc.paragraphs])
  
    # Send info to Groq to extract
    response = extract_info(content, schema)
    
    # Convert to JSON
    response = json.loads(response)
    
    # Convert to docx
    doc = format_response(response, header, division)
    
    st.download_button(
      label="Download Resume",
      data=doc,
      file_name=f"{response['resume']['candidate_name'].title()}.docx")

st.markdown("""
<footer class="footer mt-auto py-3">
  <div class="container text-center">
    <p class="text-muted">
      Copyright © 2023 | BEPC Incorporated | All Rights Reserved |
      <a href="https://52840b2d-10d4-472e-8343-b77dcb77c887.filesusr.com/ugd/17c3bf_3ac57d22aa71435a8e092faeab264e45.pdf">Privacy Policy</a> |
      <a href="https://52840b2d-10d4-472e-8343-b77dcb77c887.filesusr.com/ugd/17c3bf_01578308cc1f4718b62978df425c17c3.pdf">Cybersecurity</a> |
      <a href="https://52840b2d-10d4-472e-8343-b77dcb77c887.filesusr.com/ugd/17c3bf_9ba7da42b5104bc5b8060b236b55276f.pdf">HIPAA</a>
      |  MSMMJFXXIII
    </p>
  </div>
</footer>
""", unsafe_allow_html=True)

    