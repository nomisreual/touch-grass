from django.shortcuts import render, redirect
from contact.forms import Contact


def contact(request):
    if request.method == "POST":
        form = Contact(request.POST)
        if form.is_valid():
            # TODO: Send email
            return redirect("main:index")
    else:
        form = Contact()

    return render(request, "contact/contact.html", {"form": form})
