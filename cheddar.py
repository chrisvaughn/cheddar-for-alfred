
import requests
import json
from array import *



def main():
	payload = {'access_token': 'c58e04371525420c79fd6df8ef4677ec'}
	r = requests.get('https://api.cheddarapp.com/v1/lists', params=payload)
	data = r.json
	a = array('i',[])
	for list in data:
		a.append(list['id'])


	"""payload2 = {'access_token': 'c58e04371525420c79fd6df8ef4677ec', 'task[text]': 'Buy Milk'}
	s = requests.post('https://api.cheddarapp.com/v1/lists/3960/tasks', params=payload2)"""


	q = requests.get('https://api.cheddarapp.com/v1/lists/3960/tasks', params=payload)
	print q.json
	

if __name__ == '__main__':
	main()
	