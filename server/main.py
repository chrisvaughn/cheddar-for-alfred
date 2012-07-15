import webapp2
import json
import urllib
import base64

from google.appengine.api import memcache, urlfetch


CLIENT_ID = 'YOUR_CLIENT_ID'
CLIENT_SECRET = 'YOUR_CLIENT_SECRET'
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
            #don't keep the token around forever just to be safe
            memcache.delete(uuid)

            self.response.headers["Content-Type"] = "application/json"
            self.response.out.write(data)
        else:
            self.response.status = 404


app = webapp2.WSGIApplication([
        ('/oauth', OauthRedirectHandler),
        ('/get_access', GetAccessHandler)
    ], debug=True)
