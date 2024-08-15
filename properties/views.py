from django.http import HttpResponse


def index(request):
    return HttpResponse("Welcome to my Django Assignment. This page is currently under construction. Please visit the admin page to interact with the database.")
