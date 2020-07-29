import requests
import json
import time
import threading
import nexmo


# Authentication Details -> Parsehub
API_KEY = 'tFbQ0kth6vTn'
PROJECT_TOKEN = 'tJhSvz24HZge'
RUN_TOKEN = 'tznJZ08pekP_'


# SMS Client - Get the Keys after signing in at Nexmo / Vonage
client = nexmo.Client(key='7302e26c', secret='xsemUZtjslydSnJ6')
client2 = nexmo.Client(key='7302e26c', secret='xsemUZtjslydSnJ6')

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
		response = requests.get(f'https://www.parsehub.com/api/v2/projects/{self.project_token}/last_ready_run/data', params=self.params)
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
	
	def get_total_recoveries(self):
		data = self.data['total']

		for content in data:
			if content['name'] == 'Recovered:':
				return content['value']
		return "0"

	def get_country_data(self, country):
		data = self.data['country']

		for content in data:
			if content['name'].lower() == country.lower():
				return content
		return "0"

	def update_data(self):
		response = requests.post(f'https://www.parsehub.com/api/v2/projects/{self.project_token}/run', params=self.params)

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
print(f"World Cases : {data.get_total_cases()}")
print(f"World Deaths : {data.get_total_deaths()}")
print(f"World Recoveries : {data.get_total_recoveries()}")
print(f"Cases in Kenya : {data.get_country_data('kenya')['total_cases']}")

data.update_data()

def send_SMS():
	''' For this Demo, I will send Total Cases, Total Deaths, Total Recovered
		+ 
	'''
	world_msg=f"Total Cases : {data.get_total_cases()}\nTotal Deaths : {data.get_total_deaths()}\nTotal Recoveries : {data.get_total_recoveries()}"
	country_msg=f"Total Cases : {data.get_country_data('kenya')['total_cases']}\nTotal Deaths : {data.get_country_data('kenya')['total_deaths']}\nTotal Recoveries : {data.get_country_data('kenya')['total_recoveries']}"

	# First message is for the worldly figures
	client.send_message({
    'from': 'Vonage APIs',
    'to': '254791485681',
    'text': f"WORLD FIGURES\n\n{world_msg}\n\nSent from Lenny\'s Coronavirus-Tracker",
	})
	print('Text Message Sent To Your Phone!! : World Figures ')
	time.sleep(2)

	# Second message is for country figures e.g Kenya ^_*
	client2.send_message({
    'from': 'Vonage APIs',
    'to': '254791485681',
    'text': f"CASES IN KENYA\n\n{country_msg}\n\nSent from Lenny\'s Coronavirus-Tracker",
	})
	print('Text Message Sent To Your Phone!! : Figures in Kenya ')

send_SMS()