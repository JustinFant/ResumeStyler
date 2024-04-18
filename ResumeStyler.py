import streamlit as st
import os
import json
import base64
import time
from PyPDF2 import PdfReader
from io import BytesIO
from docx import Document
from functions.groq_call import groq_call
from functions.gpt_call import gpt_call
from functions.format_response import format_response

st.set_page_config(page_title="BEPC-ResumeStyler", page_icon="static/logo.png", layout='wide')

# Timer to track seconds spent in each function, set to True to enable
DEBUG_TIMER = False

def get_image_base64(image_path):
  with open(image_path, 'rb') as img_file:
    return base64.b64encode(img_file.read()).decode('utf-8')

sr2new = get_image_base64('static/RS_2.png')

st.markdown(
  f"""
  <div class="container">
      <h2 class="text-center mt-4">
          <img src="data:image/png;base64,{sr2new}" width="125" height="125" class="d-inline-block align-top" alt="">
          Resume Styler <span style="font-style: italic; font-size: 17px;">for recruiting V2.0</span>
      </h2>
  </div>
  """,
  unsafe_allow_html=True,
)

model = st.selectbox('Select Model', ['Groq', 'Chat GPT'])
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
      resume = ''.join([page.extract_text() for page in reader.pages])
    elif resume.name.endswith('.docx'):
      doc = Document(BytesIO(resume.read()))
      resume = ' '.join([paragraph.text for paragraph in doc.paragraphs])

    if resume != "":
      
      if model == 'Groq':
        if DEBUG_TIMER:
          # Start timer before groq call
          start_time = time.time()
        
        response = groq_call(resume, schema)
        
        if DEBUG_TIMER:
          # Print time spent in groq call
          print(f"Time in groq call: {time.time() - start_time} seconds")
      else:
        
        if DEBUG_TIMER:
          # Start timer before gpt call
          start_time = time.time()
        
        response = gpt_call(resume, schema)
        
        if DEBUG_TIMER:
          # Print time spent in gpt call
          print(f"Time in gpt call: {time.time() - start_time} seconds")
      
      # Convert to JSON
      response = json.loads(response)
      
      if DEBUG_TIMER:
        # Start timer before format response
        start_time = time.time()
      
      # Convert to docx
      doc = format_response(response, header, division)

      if DEBUG_TIMER:
        # Print time spent in format response
        print(f"Time in format response: {time.time() - start_time} seconds")
      
      st.download_button(
        label="Download Resume",
        data=doc,
        file_name=f"{response['resume']['candidate_name'].title()}.docx")
    else:
      st.error("No text found in the resume. Please upload a .pdf or .docx file.")

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

    