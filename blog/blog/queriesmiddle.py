# coding:utf-8

from django.utils.deprecation import MiddlewareMixin
from django.db import connection

class QueriesMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        print '-'*80
        print 'path: ',request.get_full_path()
        print connection.queries
        print '-'*80
        return response
