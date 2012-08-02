import httplib
import urllib
import json


class Response():
    def __init__(self, status, body):
        self.status_code = status
        self.json = json.loads(body)


class CheddarApi():
    def __init__(self, access_token):
        self.access_token = access_token
        self.connection = httplib.HTTPSConnection("api.cheddarapp.com")
        self.headers = {"Authorization": "Bearer " + self.access_token}

    def lists(self):
        self.connection.request("GET", "/v1/lists", headers=self.headers)
        r = self.connection.getresponse()
        return Response(r.status, r.read())

    def create_task(self, list_id, task):
        params = urllib.urlencode({'task[text]': task})
        self.connection.request("POST", "/v1/lists/%s/tasks" % list_id,
                                body=params,
                                headers=self.headers)
        r = self.connection.getresponse()
        return Response(r.status, r.read())
