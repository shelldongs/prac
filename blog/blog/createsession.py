# coding:utf-8

from django.utils.deprecation import MiddlewareMixin
from django.db import connection

class CreateSessionMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.session['createsession'] = True
