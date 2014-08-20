from django.core.handlers.wsgi import WSGIHandler
import django.core.handlers.wsgi
import os
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "BaseApp.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

class WSGIEnvironment(WSGIHandler):

    def __call__(self, environ, start_response):

        # for local server, export var in ~/.bashrc
        # for apache server, SetEnv var in /etc/apache2/httpd.conf
        os.environ['EMAIL_PASSWORD'] = environ['EMAIL_PASSWORD']
        return super(WSGIEnvironment, self).__call__(environ, start_response)

application = WSGIEnvironment()

