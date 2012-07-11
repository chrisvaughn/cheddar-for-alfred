# Copyright (C) 2012 Chris Vaughn
#
#
#
#

"""Command-line tools for authenticating via OAuth 2.0
   flow and idea taken from Google's oauth2client
   rewritten to get rid of Google imports
"""

import BaseHTTPServer
import socket
import sys
import webbrowser
from urlparse import parse_qsl
import urllib
import requests
from anyjson import simplejson
import config


class ClientRedirectServer(BaseHTTPServer.HTTPServer):
    """A server to handle OAuth 2.0 redirects back to localhost.

    Waits for a single request and parses the query parameters
    into query_params and then stops serving.
    """
    query_params = {}


class ClientRedirectHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    """A handler for OAuth 2.0 redirects back to localhost.

    Waits for a single request and parses the query parameters
    into the servers query_params and then stops serving.
    """

    def do_GET(s):
        """Handle a GET request.

        Parses the query parameters and prints a message
        if the flow has completed. Note that we can't detect
        if an error occurred.
        """
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()
        query = s.path.split('?', 1)[-1]
        query = dict(parse_qsl(query))
        s.server.query_params = query
        s.wfile.write("<html><head>")
        s.wfile.write("<title>Authentication Status</title>")
        s.wfile.write("</head>")
        s.wfile.write("<body><p>The authentication flow has completed.</p>")
        s.wfile.write("</body></html>")

    def log_message(self, format, *args):
        """Don't log messages to stdout while running as command line."""
        pass


def main():
    auth_local_webserver = True
    auth_host_name = 'localhost'
    auth_host_port = 9294
    if auth_local_webserver:
        success = False
        try:
            httpd = ClientRedirectServer((auth_host_name, auth_host_port),
                                     ClientRedirectHandler)
        except socket.error:
            pass
        else:
            success = True
    auth_local_webserver = success
    if not success:
        print 'Failed to start a local webserver.'
        print 'Please check your firewall settings and locally'
        print 'running programs that may be blocking or using those ports.'
        print
        print 'Falling back to alternate method of authentication.',
        print

    if auth_local_webserver:
        oauth_callback = 'http://%s:%s/' % (auth_host_name, auth_host_port)
    else:
        pass
        #oauth_callback = OOB_CALLBACK_URN
    authorize_url = build_authorize_url(oauth_callback)

    if auth_local_webserver:
        webbrowser.open(authorize_url, new=1, autoraise=True)
        print 'Your browser has been opened to visit:'
        print
        print '    ' + authorize_url
        print
        print
    else:
        print 'Go to the following link in your browser:'
        print
        print '    ' + authorize_url
        print

    code = None
    if auth_local_webserver:
        httpd.handle_request()
        if 'error' in httpd.query_params:
            sys.exit('Authentication request was rejected.')
        if 'code' in httpd.query_params:
            code = httpd.query_params['code']
        else:
            print 'Failed to find "code" in the query parameters'
            sys.exit('Try running with --noauth_local_webserver.')
    else:
        code = raw_input('Enter verification code: ').strip()

    access_token = exchange_for_access_token(oauth_callback, code)
    if access_token:
        print 'Authentication successful.'
        print access_token
    else:
        print 'Authentication has failed'


def build_authorize_url(oauth_callback):
    oauth_callback = urllib.quote_plus(oauth_callback)
    scope = urllib.quote_plus(config.SCOPE)
    client_id = urllib.quote_plus(config.CLIENT_ID)
    return (config.AUTH_URL +
            '?scope=' + scope +
            '&redirect_uri=' + oauth_callback + '&response_type=code' +
            '&client_id=' + client_id +
            '&access_type=offline')


def exchange_for_access_token(redirect_uri, code):

    body = urllib.urlencode({
        'grant_type': 'authorization_code',
        'client_id': config.CLIENT_ID,
        'client_secret': config.CLIENT_SECRET,
        'code': code,
        'redirect_uri': redirect_uri,
        'scope': config.SCOPE,
        })
    headers = {
        'content-type': 'application/x-www-form-urlencoded',
    }
    r = requests.post(config.TOKEN_URL, data=body, headers=headers)
    access_token = False
    if r.status_code == 200:
        d = simplejson.loads(r.content)
        access_token = d['access_token']

    return access_token
if __name__ == '__main__':
    main()
