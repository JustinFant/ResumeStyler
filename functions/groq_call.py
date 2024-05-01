from groq import Groq
from dotenv import load_dotenv 


load_dotenv()
client = Groq()


def groq_call(resume, schema):
  response = client.chat.completions.create(
  model="mixtral-8x7b-32768",
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
  # print(response.choices[0].message.content)
  return response.choices[0].message.content