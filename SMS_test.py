import time
from sinchsms import SinchSMS

number = "mobile-number"
message = 'I Love Python!'

client = SinchSMS(APP_KEY, APP_SECRET)

print(f'Sending {message} to {number}')
response = client.send_message(number, message)