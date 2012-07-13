import webapp2
import json
import urllib
import base64

from google.appengine.api import memcache
from google.appengine.api import urlfetch

CLIENT_ID = '672fa96c85fa2036cf12bdb1f21efce1'
CLIENT_SECRET = 'a8760b23fdfacbcbe06feab9adb46a56'
AUTHORIZE_URL = 'https://api.cheddarapp.com/oauth/authorize'
TOKEN_URL = 'https://api.cheddarapp.com/oauth/token'


class OauthRedirectHandler(webapp2.RequestHandler):
    def get(self):
        code = self.request.get('code')
        uuid = self.request.get('state')
        if code:
            params = {
                'grant_type': 'authorization_code',
                'code': code
            }
            auth = {
                "Authorization": "Basic %s" % base64.b64encode(CLIENT_ID + ":" + CLIENT_SECRET)
            }
            result = urlfetch.fetch(url=TOKEN_URL,
                                    payload=urllib.urlencode(params),
                                    method=urlfetch.POST,
                                    headers=auth)
            if result.status_code == 200:
                response = json.loads(result.content)
                memcache.set(uuid, json.dumps({'access_token': response['access_token']}))
                self.response.out.write('Success! You may close this window.')
            else:
                error = self.request.get('error')
                memcache.set(uuid, json.dumps({'error': error}))
                self.response.out.write('There was an error. Please try again.')
        else:
            error = self.request.get('error')
            memcache.set(uuid, json.dumps({'error': error}))
            self.response.out.write('There was an error. Please try again.')
            return


class GetAccessHandler(webapp2.RequestHandler):
    def get(self):
        uuid = self.request.get('uuid')
        data = memcache.get(uuid)
        if data:
            self.response.headers["Content-Type"] = "application/json"
            self.response.out.write(data)
        else:
            self.response.status = 404


app = webapp2.WSGIApplication([
        ('/oauth', OauthRedirectHandler),
        ('/get_access', GetAccessHandler)
    ], debug=True)
