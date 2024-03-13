import logging
from django.db import connection


class SqlLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        sql_logger = logging.getLogger('sql_logger')
        sql_logger.setLevel(logging.DEBUG)
        # Логика отслеживания SQL-запросов
        for query in connection.queries:
            sql = query['sql']
            sql_logger.debug(sql)

        return response