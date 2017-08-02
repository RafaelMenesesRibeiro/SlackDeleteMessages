import sys
import requests
import time
import json

#TO BE FILLED BY THE USER
token = ''
count = 1000 #Number of messages to get (min = 1, max = 1000)

#-------------------------------------------------------------------------------
userID = json.loads(requests.get('https://slack.com/api/auth.test', {'token': token}).text)['user_id']

def channelGetID():
	params = {
		'token': token,
		'exclude_archived': True,
		'exclude_members': True
	}
	response = requests.get('https://slack.com/api/channels.list', params=params)
	respT = json.loads(response.text)
	channels  = respT['channels']
	channelsMember = []
	for i in range(len(channels)):
		if channels[i]['is_member']:
			channelsMember.append(channels[i])
	for i in range(len(channelsMember)):
		print(i, ' : ', channelsMember[i]['name'])
	channelIndex = int(input('\nWhere are the messages you want to delete. (Input the index of the channel)\t'))
	if channelIndex < 0 or channelIndex > len(channelsMember):
		sys.exit('ABORTED - Invalid input - the channel index needs to be on the list presented above')
	return channelsMember[channelIndex]['id']

def messagesList(channelCode):
	params = {
		'token': token,
		'channel': channelCode,
		'count': count
	}
	response = requests.get('https://slack.com/api/channels.history', params=params)
	return json.loads(response.text)['messages']

def messagesDelete(channelCode, messages):
	c = d = 0
	for msg in messages:
		c += 1
		if msg['user'] == userID:
			params = {
				'token': token,
				'channel': channelCode,
				'ts': msg['ts'],
				'as_user': 1
			}	
			response = requests.get('https://slack.com/api/chat.delete', params=params)
			respT = json.loads(response.text)
			d = d+1 if (respT['ok'] == True) else d
			print('message #', c, ' of ', count, '. Deleted ', d, ' -> ', msg['text'])
			time.sleep(1) #Used so slack doens't return 'ratelimited' ('https://api.slack.com/docs/rate-limits')
		else:
			print('message #', c, ' of ', count, '. Deleted ', d)

count = 1 if (count > 1000 or count < 1) else count
channelID = channelGetID()
messages = messagesList(channelID)
messagesDelete(channelID, messages)
print('\nDone.')
