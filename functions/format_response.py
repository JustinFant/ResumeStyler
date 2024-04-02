from docx import Document
from io import BytesIO
from docx.shared import Pt
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.shared import RGBColor


def format_response(response):
  doc = Document()

  # Title section
  title = doc.add_paragraph()
  run = title.add_run(response['resume']['candidate_name'])
  run.font.size = Pt(14)
  run.font.name = 'Times New Roman'
  title.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER

  # Summary section
  summary = doc.add_paragraph()
  run = summary.add_run("Summary")
  run.font.name = 'Times New Roman'
  run.font.all_caps = True
  run.font.bold = True
  run.font.underline = True

  summary = doc.add_paragraph(response['resume']['summary'])


  # Skills section
  skills = doc.add_paragraph()
  run = skills.add_run("Skills")
  run.font.name = 'Times New Roman'
  run.font.all_caps = True
  run.font.bold = True
  run.font.underline = True

  for skill in response['resume']['skills']:
    paragraph = doc.add_paragraph(style='List Bullet')
    run = paragraph.add_run(skill)
    run.font.name = 'Times New Roman'

  
  # Education section
  education = doc.add_paragraph()
  run = education.add_run("Education")
  run.font.name = 'Times New Roman'
  run.font.all_caps = True
  run.font.bold = True
  run.font.underline = True

  for edu in response['resume']['education']:
    school = doc.add_paragraph()
    run = school.add_run(edu['school'])
    run.font.name = 'Times New Roman'
    run.font.bold = True
    run.font.italic = True
    run.font.color.rgb = RGBColor(118, 113, 113) 

    degree = doc.add_paragraph()
    run = degree.add_run(f"{edu['degree']}, ({edu['date']})")
    run.font.name = 'Times New Roman'
    run.font.bold = True

  
  # Experience section
  experience = doc.add_paragraph()
  run = experience.add_run("Professional Experience")
  run.font.name = 'Times New Roman'
  run.font.all_caps = True
  run.font.bold = True
  run.font.underline = True

  for exp in response['resume']['experience']:
    employer = doc.add_paragraph()
    run = employer.add_run(f"{exp['employer']}\t\t{exp['work_dates']}")
    run.font.name = 'Times New Roman'
    run.font.bold = True
    run.font.italic = True
    run.font.color.rgb = RGBColor(118, 113, 113) 

    title = doc.add_paragraph()
    run = title.add_run(exp['job_title'])
    run.font.name = 'Times New Roman'
    run.font.bold = True

    for res in exp['responsibilities']:
      paragraph = doc.add_paragraph(style='List Bullet')
      run = paragraph.add_run(res)
      run.font.name = 'Times New Roman'

    doc.add_paragraph() # Empty paragraph for spacing

  
  # Save the document to a BytesIO object
  doc_bin = BytesIO()
  doc.save(doc_bin)
  doc_bin.seek(0)
  
  return doc_bin