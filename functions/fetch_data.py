import requests

def fetch_data(candidate_id):
  url_resume = 'https://bepc.backnetwork.net/JobSiftBeta/assets/php/job.php'
  data_resume = {"candidate": candidate_id}
  response_resume = requests.post(url_resume, data=data_resume)
  candidate_resume = response_resume.text

  return candidate_resume