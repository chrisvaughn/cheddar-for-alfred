
import sys
import webbrowser
import uuid
import urllib
import time
import requests
import pickle
#import gntp.notifier

import dl

CLIENT_ID = '672fa96c85fa2036cf12bdb1f21efce1'
AUTH_URL = 'https://api.cheddarapp.com/oauth/authorize'
AUTH_INTERIM_URL = 'https://cheddar-for-alfred.appspot.com/get_access'


def main(args):
    if len(args) == 0:
        print 'expected 1 argument'
        return

    user_list = args[0]
    task = args[1]

    #get access token from file or got through auth process
    access_token = authorize()

    if not access_token:
        print 'Something is not right. Aborting'
        return

    #fetch lists and filter out archived lists
    lists = fetch_lists(access_token)

    list = guess_the_list(lists, user_list)

    print create_task(access_token, list, task)

    #payload = {'access_token': access_token}
    #q = requests.get('https://api.cheddarapp.com/v1/lists/2024/tasks', params=payload)
    #d = q.json
    #b = []
    #for list in d:
    #    b.append(list['display_text'])
    #for x in xrange(0, len(b)):
    #    gntp.notifier.mini(b[x])


def fetch_lists(access_token):
    payload = {'access_token': access_token}
    r = requests.get('https://api.cheddarapp.com/v1/lists', params=payload)
    lists = r.json
    unloaded_lists = [{'id': x['id'], 'title': x['title']} for x in lists if not x['archived_at']]
    return unloaded_lists


def guess_the_list(lists, user_list):
    best_choice = {'dm': 1000}
    for list in lists:
        distances = []
        print list
        for l in list['title'].lower().split(' '):
            distance = dl.dameraulevenshtein(l, user_list.lower())
            distances.append(distance)
            #print l
            #print distance
        average = float(sum(distances)) / len(distances)
        distance = average
        print 'distance: ' + str(distance)
        print 'best match: ' + str(best_choice)
        if distance < best_choice['dm']:
            print 'new best match'
            best_choice = list
            best_choice['dm'] = distance
        print ''
    return best_choice


def create_task(access_token, list, task):
    payload = {
        'access_token': access_token,
        'task[text]': task
    }
    url = 'https://api.cheddarapp.com/v1/lists/%s/tasks' % list['id']
    r = requests.post(url, params=payload)
    print r.status_code
    if r.status_code == 201:
        return r.json
    else:
        return False


def get_access_token():
    data = read_store()
    if 'access_token' not in data:
        data['access_token'] = authorize()
        write_store(data)
    return data['access_token']


def authorize():
    #try and get token from file
    #if it's not there then go though OAuth dance
    data = read_store()
    if 'access_token' not in data:
        uuid_for_state = uuid.uuid1().hex
        params = {
            'client_id': CLIENT_ID,
            'state': uuid_for_state
        }
        authorize_url = '%s?%s' % (AUTH_URL, urllib.urlencode(params))
        webbrowser.open(authorize_url, new=1, autoraise=True)

        time.sleep(5)

        params = {'uuid': uuid_for_state}
        url = '%s?%s' % (AUTH_INTERIM_URL, urllib.urlencode(params))

        count = 0
        r = requests.get(url)
        while count < 15 and r.status_code != 200:
            count += 1
            time.sleep(2)
            r = requests.get(url)

        if r.status_code == 200:
            resp = r.json
            if 'access_token' in resp:
                data['access_token'] = resp['access_token']
                #now that we fetched it let's store it
                write_store(data)
        else:
            print 'error getting token. giving up'
            return False

    return data['access_token']


def read_store():
    try:
        with open('data.pkl') as f:
            data = pickle.load(f)
    except:
        data = {}
    return data


def write_store(data):
    try:
        with open('data.pkl', 'w') as f:
            pickle.dump(data, f)
    except:
        pass

if __name__ == '__main__':
    main(sys.argv[1:])
