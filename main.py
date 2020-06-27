import requests
import json
import time
import threading
import nexmo


# Authentication Details -> Parsehub
API_KEY = 'tFbQ0kth6vTn'
PROJECT_TOKEN = 'tJhSvz24HZge'
RUN_TOKEN = 't1oT4C0wafTM'

# initial tests to ensure we can successfully get data from the API
response = requests.get(f'https://www.parsehub.com/api/v2/projects/{PROJECT_TOKEN}/last_ready_run/data', params={'api_key' : API_KEY})
print(f'Test Data: {response}')
# data = json.loads(response.text)

# SMS Client
client = nexmo.Client(key='7302e26c', secret='xsemUZtjslydSnJ6')

class Data:
	''' This class helps us parse the data from the api-response
	'''
	def __init__(self, api_key, project_token):
		self.api_key = api_key
		self.project_token = project_token
		self.params = {
			"api_key" : self.api_key
		}
		self.data = self.get_data()

	def get_data(self):
		response = requests.get(f'https://www.parsehub.com/api/v2/projects/{self.project_token}/last_ready_run/data', params=self.api_key)
		print(response.text)
		data = json.loads(response.text)
		return data

	def get_total_cases(self):
		data = self.data['total']

		for content in data:
			if content['name'] == 'Coronavirus Cases:':
				return content['value']
		return "0"

	def get_total_deaths(self):
		data = self.data['total']

		for content in data:
			if content['name'] == 'Deaths:':
				return content['value']
		return "0"
	
	def get_country_data(self, country):
		data = self.data['country']

		for content in data:
			if content['name'].lower() == country.lower():
				return content
		return "0"

	def update_data():
		response = requests.post(f'https://www.parsehub.com/api/v2/projects/{self.project_token}/run', params=self.api_key)

		def poll():
			time.sleep(0.1)
			old_data = self.data
			while True:
				new_data = self.get_data()
				if new_data != old_data:
					self.data = new_data
					print('Data Updated')
					break
				time.sleep(5)

		t = threading.Thread(target=poll)
		t.start()

# Playing around with the script to get coronavirus cases
# With this information, you can setup any interface for the user : speech(Text-to-Speech), Web-App, CLI, etc
data = Data(API_KEY, PROJECT_TOKEN)
# print(data.data)
print(data.get_total_cases())
print(data.get_total_deaths())
print(data.get_country_data('canada')['total_cases'])

data.update_data()

def send_SMS():
	''' For this Demo, I will send Total Cases, Total Deaths, Total Recovered
		+ 
	'''

	# First message is for the worldly figures
	client.send_message({
    'from': 'Vonage APIs',
    'to': '254791485681',
    'text': f"WORLD FIGURES\n\n{world_msg}\n\n\nSent from Lenny\'s Coronavirus-Tracker",
	})
	print('Text Message Sent!! :> World Figures')

	# Second message is for country figures e.g Kenya ^_*
	client.send_message({
    'from': 'Vonage APIs',
    'to': '254791485681',
    'text': f"CASES IN KENYA\n\n{country_msg}\n\n\nSent from Lenny\'s Coronavirus-Tracker",
	})
	print('Text Message Sent!! :> World Figures')