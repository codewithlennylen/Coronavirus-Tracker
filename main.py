import requests
import json


API_KEY = ''
PROJECT_TOKEN = ''
RUN_TOKEN = ''

response = requests.get(f'https://www.parsehub.com/api/v2/projects/{PROJECT_TOKEN}/last_ready_run/data', params={'api_key' : API_KEY})
data = json.loads(response.text)