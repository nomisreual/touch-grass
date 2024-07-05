from django.shortcuts import render


def index(request):
    context = {"title": "Welcome"}
    return render(request, "main/index.html", context=context)
