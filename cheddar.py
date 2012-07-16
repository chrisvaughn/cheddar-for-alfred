#!/usr/bin/env python
import os
import sys
import uuid
import urllib
import time
import requests
import pickle
import re

import dl

CLIENT_ID = 'YOUR_CLIENT_ID'
AUTH_URL = 'https://api.cheddarapp.com/oauth/authorize'
AUTH_INTERIM_URL = 'https://cheddar-for-alfred.appspot.com/get_access'


def main(args):

    if len(args) == 0:
        show_help()
        return

    (cmd, user_list, task) = process_input(args[0])

    if cmd == 'help':
        show_help()
    elif cmd == 'create_task':
        #get access token from file or got through auth process
        access_token = authorize()

        if not access_token:
            print 'Something is not right. Aborting.'
            return

        #fetch lists and filter out archived lists
        lists = fetch_lists(access_token)
        if lists:
            list = guess_the_list(lists, user_list)

            task_response = create_task(access_token, list, task)
            if task_response:
                print "Task Created in %s" % list['title']
            else:
                print "Error. Could not create task."
        else:
            "Error. Please delete data.pkl file and try again."
    else:
        print 'Command unrecognized. Aborting.'


def process_input(input_str):
    cmd = user_list = task = ''
    pattern = re.compile(r'''((?:[^\s"']|"[^"]*"|'[^']*')+)''')
    inputs = pattern.split(input_str)[1::2]

    if inputs[0] == 'help' and len(inputs) == 1:
        cmd = 'help'
    else:
        cmd = 'create_task'
        user_list = inputs[0].strip('"')
        task = inputs[1].strip('"')
    return (cmd, user_list, task)


def fetch_lists(access_token):
    payload = {'access_token': access_token}
    r = requests.get('https://api.cheddarapp.com/v1/lists', params=payload)
    if r.status_code == 200:
        lists = r.json
        unloaded_lists = [{'id': x['id'], 'title': x['title']} for x in lists if not x['archived_at']]
        return unloaded_lists
    else:
        return False


def guess_the_list(lists, user_list):
    best_choice = {'dm': 1000}
    for list in lists:
        distances = []
        for l in list['title'].lower().split(' '):
            distance = dl.dameraulevenshtein(l, user_list.lower())
            distances.append(distance)
        average = float(sum(distances)) / len(distances)
        distance = average

        if distance < best_choice['dm']:
            best_choice = list
            best_choice['dm'] = distance
    return best_choice


def create_task(access_token, list, task):
    payload = {
        'access_token': access_token,
        'task[text]': task
    }
    url = 'https://api.cheddarapp.com/v1/lists/%s/tasks' % list['id']
    r = requests.post(url, params=payload)

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
        os.system('open "%s"' % authorize_url)

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
            print 'Error getting token. Aborting'
            return False

    return data['access_token']


def show_help():
    print "Cheddar For Alfred Help"
    print "help - display this help menu"
    print ""
    print "to create a task:"
    print "list \"task you want to create in quotes\""
    print "  list matching works well at matching if you"
    print "  give it at least half of the name"


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
