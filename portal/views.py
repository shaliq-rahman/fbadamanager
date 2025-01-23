from django.shortcuts import render
from portal.helper import renderhelper

# Create your views here.
def myfunction(request):
    print("Hello")


def login(request):
    context = {
        "title": "Example Page",
        "message": "This is an example of using render_helper."
    }
    return renderhelper(request, "portal", "auth", template_name="login.html", context=context)


def dashboard(request):
    context = {
        "title": "Example Page",
        "message": "This is an example of using render_helper."
    }
    return renderhelper(request, "portal", "dashboard", template_name="index.html", context=context)



def data(request):
    context = {
        "title": "Example Page",
        "message": "This is an example of using render_helper."
    }
    return renderhelper(request, "portal", "data_list", template_name="index.html", context=context)


def data_edit(request):
    context = {
        "title": "Example Page",
        "message": "This is an example of using render_helper."
    }
    return renderhelper(request, "portal", "data_list", template_name="edit.html", context=context)


def profile_update(request):
    context = {
        "title": "Example Page",
        "message": "This is an example of using render_helper."
    }
    return renderhelper(request, "portal", "profile", template_name="edit.html", context=context)