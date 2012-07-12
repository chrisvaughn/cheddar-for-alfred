
import requests
import json
from array import *
import gntp.notifier



def main():
	payload = {'access_token': 'c58e04371525420c79fd6df8ef4677ec'}
	r = requests.get('https://api.cheddarapp.com/v1/lists', params=payload)
	data = r.json
	a = []
	for list in data:
		a.append(list['id'])

	print a


	#payload2 = {'access_token': 'c58e04371525420c79fd6df8ef4677ec', 'task[text]': 'Buy Milk'}
	#s = requests.post('https://api.cheddarapp.com/v1/lists/3960/tasks', params=payload2)


	q = requests.get('https://api.cheddarapp.com/v1/lists/2024/tasks', params=payload)
	d = q.json
	b = []
	for list in d:
		b.append(list['display_text'])
	for x in xrange(0,len(b)):
		gntp.notifier.mini(b[x])

	
	

if __name__ == '__main__':
	main()
	