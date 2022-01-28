# from django.shortcuts import render
from django.http import HttpResponse


def index_users(request):
    return HttpResponse('Hello world from Users!')
