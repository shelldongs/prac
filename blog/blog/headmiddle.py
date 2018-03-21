# coding:utf-8

from django.utils.deprecation import MiddlewareMixin
from django.db import connection

class HeadMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        print response
        return response
