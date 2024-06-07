from django.http import HttpRequest
from django.shortcuts import HttpResponse


def index(_: HttpRequest):
    return HttpResponse("index")
