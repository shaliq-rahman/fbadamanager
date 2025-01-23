from django.shortcuts import render
from django.views import View
from .. helper import renderfile
from django.contrib.auth import login, authenticate, logout
from urllib.parse import urlparse, parse_qs
from django.urls import resolve
from django.http import JsonResponse
from django.urls import reverse
from django.urls.exceptions import Resolver404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.core.paginator import *
from django.contrib.auth.hashers import check_password
from django.db import transaction
from adminconsole.constantvariables import LOGIN_URL
from adminconsole.constantlabels import *
import pdb

#LOGIN LOGOUT
class Login(View):
    def get(self, request, *args, **kwargs):
        data = {}
        return renderfile(request,'account','login',data)
    
    
    def post(self, request, *args, **kwargs):
        context = {}
        username = request.POST.get('email')
        password = request.POST.get('password')
        current_url = request.POST.get('current_url')   
        user = authenticate(username=username, password=password)
        
        if current_url:
            try:
                parsed_url = urlparse(current_url)
                query_params = parse_qs(parsed_url.query)
                next_url = query_params.get('next', [None])[0]
                if next_url:
                    resolve_result = resolve(next_url)
                    redirect_url = next_url
                else:
                    redirect_url = reverse('adminconsole:dashboard')
            except Resolver404:
                redirect_url = reverse('adminconsole:dashboard')  
                
        if user is not None and user.is_active:
            login(request, user)
            return JsonResponse({'status': True, 'redirect_url': redirect_url})
        else:
            if user:
                if not user.is_active:
                    return JsonResponse({'status': False, 'message': ACCOUNT_NOT_ACTIVE})
                
            return JsonResponse({'status': False, 'message': INCORRECT_PASSWORD})
        
class Logout(LoginRequiredMixin, View):
    login_url = LOGIN_URL
    
    def get(self, request, *args, **kwargs):
        context = {}
        logout(request)
        request.session.flush()
        return redirect(reverse('adminconsole:login'))
    
class Profile(LoginRequiredMixin, View):
    login_url = LOGIN_URL
    
    def get(self, request, *args, **kwargs):
        data = {}
        return renderfile(request,'account','profile',data)
    
    
    def post(self, request, *args, **kwargs):
        context, create_conditions = {}, {}
        current_password = request.POST.get('current_password', None)
        new_password = request.POST.get('new_password', None)
        confirm_new_password = request.POST.get('confirm_new_password', None)

        try:
            with transaction.atomic():
                user = request.user
                # Check if the provided current_password matches the user's old password
                if not check_password(current_password, user.password):
                    return JsonResponse({'status': False, 'message': CURRENT_PASS_INCORRECT, 'redirect_url': reverse('adminconsole:profile')})

                # Continue with your password change logic
                if new_password != confirm_new_password:
                    return JsonResponse({'status': False, 'message': PASSWORDS_DONOT_MATCH, 'redirect_url': reverse('adminconsole:profile')})

                # Change the user's password
                user.set_password(new_password)
                user.save()
                logout(request)
                return JsonResponse({'status': True, 'message': PASSWORD_CHANGED, 'redirect_url': reverse('adminconsole:login')})
        except Exception as dberror:
            error_message = str(dberror)
            print(dberror)
            return JsonResponse({'status': False, 'message': error_message, 'redirect_url': reverse('adminconsole:profile')})
