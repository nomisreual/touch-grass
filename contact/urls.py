from django.urls import path
from contact.views import contact


app_name = "contact"
urlpatterns = [
    path("", contact, name="contact"),
]
