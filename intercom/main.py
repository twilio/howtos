#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import os
import organization
import settings
from django.utils import simplejson as json
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp import util
from twilio.util import TwilioCapability


class IntercomHandler(webapp.RequestHandler):

    def get(self, user_filter="all"):

        user = users.get_current_user()
        client_name = user.email().split("@")[0]

        capability = TwilioCapability(settings.ACCOUNT_SID,
            settings.AUTH_TOKEN)
        capability.allow_client_outgoing(settings.APP_SID)
        capability.allow_client_incoming(client_name)

        tp = {
            'token': capability.generate(),
            "user_filter": user_filter,
            }

        path = os.path.join(os.path.dirname(__file__),
            'templates', 'intercom.html')
        self.response.out.write(template.render(path, tp))


class UsersHandler(webapp.RequestHandler):

    def get(self):
        self.response.headers["Content-Type"] = "application/json"
        self.response.out.write(json.dumps(organization.users()))


class TwimlHandler(webapp.RequestHandler):

    def get(self):
        tp = {"client": self.request.get("Person")}

        self.response.headers["Content-Type"] = "application/xml"
        path = os.path.join(os.path.dirname(__file__),
            'templates', 'twiml.html')
        self.response.out.write(template.render(path, tp))

    def post(self):
        self.get()


def main():
    application = webapp.WSGIApplication([
            ('/(available|unavailable)?', IntercomHandler),
            ('/users', UsersHandler),
            ('/call', TwimlHandler),
            ], debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
