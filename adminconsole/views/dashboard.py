from django.views import View
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from adminconsole.helper import renderfile
from adminconsole.models import *
from django.db.models import Sum
from adminconsole.constantvariables import LOGIN_URL
import datetime

class HomeView(View):
    def get(self, request, *args, **kwargs):
        data = {}
        if request.user.is_authenticated:
            return redirect('adminconsole:dashboard')
        else:
            return redirect('adminconsole:login')

class Dashboard(LoginRequiredMixin, View):
    login_url = LOGIN_URL
    
    def get(self, request, *args, **kwargs):
        data = {}
        return renderfile(request,'dashboard','index',data)