import nexmo

client = nexmo.Client(key='7302e26c', secret='xsemUZtjslydSnJ6')

client.send_message({
    'from': 'Vonage APIs',
    'to': '254791485681',
    'text': 'This message was sent from my Python Script',
})