from django.shortcuts import render
from client.models import Client


def index(request):
    context = {"title": "Welcome"}
    return render(request, "main/index.html", context=context)
