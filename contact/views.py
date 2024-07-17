from django.shortcuts import render, redirect
from django.conf import settings
from contact.forms import Contact
from django.core.mail import send_mail


def contact(request):
    if request.method == "POST":
        form = Contact(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get("name")
            email = form.cleaned_data.get("email")
            subject = form.cleaned_data.get("subject")
            message = form.cleaned_data.get("message")

            full_message = f"""
                Received message below from {name} ({email}),
                Subject: {subject}
                -------------------------------------------------

                {message}
            """
            send_mail(
                subject="Received contact from form submission",
                message=full_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.NOTIFY_EMAIL],
            )
            return redirect("main:index")
    else:
        form = Contact()

    return render(request, "contact/contact.html", {"form": form})
