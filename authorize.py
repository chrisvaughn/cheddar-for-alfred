# Copyright (C) 2012 Chris Vaughn

import webbrowser
import uuid
import urllib
import time
import requests

CLIENT_ID = '672fa96c85fa2036cf12bdb1f21efce1'
AUTH_URL = 'https://api.cheddarapp.com/oauth/authorize'
AUTH_INTERIM_URL = 'https://cheddar-for-alfred.appspot.com/get_access'


def main():
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

    r = requests.get(url)
    while r.status_code != 200:
        time.sleep(2)
        r = requests.get(url)
    data = r.json
    if 'access_token' in data:
        print data['access_token']

if __name__ == '__main__':
    main()
