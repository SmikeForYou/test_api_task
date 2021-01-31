from django.db import connection
from django.http.request import HttpRequest
from django.http.response import JsonResponse


def keepalive(request: HttpRequest) -> JsonResponse:
    data = {}
    with connection.cursor() as cursor:
        cursor.execute("SELECT 1")
        data["DB"] = bool(cursor.fetchone())

    return JsonResponse(data=data, )
