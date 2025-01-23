from django.shortcuts import render
from adminconsole.constantvariables import APPFOLDERNAME, PAGINATION_PERPAGE
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import random
from django.utils import timezone
from datetime import timedelta
import magic
from django.utils.text import slugify
import random
import string
from adminconsole.models import User


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

def renderfile(request, foldername=None, pagename=None, variableobj=None, innerfolder=None):
    if innerfolder and foldername:
        if innerfolder:
            return render(request, APPFOLDERNAME + '/' + foldername + '/' + pagename + '/' + variableobj + '.html', innerfolder)
    elif foldername:
        if variableobj:
            return render(request, APPFOLDERNAME + '/' + foldername + '/' + pagename + '.html', variableobj)
        else:
            return render(request, APPFOLDERNAME + '/' + foldername + '/' + pagename + '.html', {})
    else:
        if variableobj:
            return render(request, APPFOLDERNAME + '/' + pagename + '.html', variableobj)
        else:
            return render(request, APPFOLDERNAME + '/' + pagename + '.html', {})


def paginationhelper(paginationrecord=None, page=None):
    paginator = Paginator(paginationrecord, PAGINATION_PERPAGE)

    try:
        paginationrecord = paginator.page(page)
    except PageNotAnInteger:
        paginationrecord = paginator.page(1)
    except EmptyPage:
        paginationrecord = paginator.page(paginator.num_pages)
    return paginationrecord



def generate_otp(self):
    # Generate a 6-digit OTP
    otp = str(random.randint(100000, 999999))
    return otp



def is_image_or_video(file):
    # Get MIME type using python-magic
    mime = magic.from_buffer(file.read(), mime=True)
    
    # Check if it's an image or video
    if mime.startswith('image/'):
        return 'image'
    elif mime.startswith('video/'):
        return 'video'
    else:
        return None
    
import re
def clean_text(text):
    # Remove single quotes, square brackets, and special characters (except .)
    cleaned_text = re.sub(r"[\'\[\]\"!@#$%^&*()_+=;:'<>?,/\\-]", "", text)
    cleaned_text = re.sub(r"\s+", " ", cleaned_text)  # Replace multiple spaces with a single space
    return cleaned_text.strip()  # Trim leading and trailing whitespace



def generate_unique_username(name):
    base_username = slugify(name)[:20]  # Slugify the name to create a clean username
    while True:
        username = f"{base_username}{random.randint(100, 999)}"
        if not User.objects.filter(username=username).exists():
            return username
