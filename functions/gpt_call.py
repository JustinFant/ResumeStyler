from openai import OpenAI
from dotenv import load_dotenv 


load_dotenv()
client = OpenAI()


def gpt_call(resume, schema):
  response = client.chat.completions.create(
  model="gpt-4-turbo",
  temperature=0,  
  seed= 123455555,
  response_format={"type": "json_object"},
  messages=[
      {"role":"system", "content":"Your job is to extract information from a resume and match it to a JSON schema. \
        Do not add, change or remove any information from the resume. It is important to extract the information as \
        accurately as possible. If a field is missing from the resume, leave it blank."},
      {"role":"user", "content":f"Candidate's Resume: {resume}"},
      {"role":"user", "content":f"JSON Schema: {schema}"},
    ],
  )
  return response.choices[0].message.content