from django.shortcuts import render
from client.models import Client


def index(request):
	# NOTE: to be removed, just for testing it out!
	client = Client.objects.get(user=request.user)
	context = {
		"api_key": client.key,
	}
	print(client.key)
	return render(request, "main/index.html", context=context)
