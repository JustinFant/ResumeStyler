from groq import Groq
from dotenv import load_dotenv 


load_dotenv()
client = Groq()


def extract_info(resume, schema):
  response = client.chat.completions.create(
  model="mixtral-8x7b-32768",
  temperature=0,  
  seed= 123455555,
  response_format={"type": "json_object"},
  messages=[
      {"role":"system", "content":"You are an expert in styling resumes. You will take the candidate's resume and style it according to the JSON schema provided. Only use the information found in the candidate's resume, do not invent anything. And make sure to fill as much info as you can using the resume."},
      {"role":"user", "content":f"JSON Schema: {schema}"},
      {"role":"user", "content":f"Candidate Resume: {resume}"},
    ],
  )
  return response.choices[0].message.content