from django.views import View
from adminconsole.helper import renderfile, is_ajax
from adminconsole.constantvariables import LOGIN_URL
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from adminconsole.constantvariables import PAGINATION_PERPAGE, LOGIN_URL
from django.core.paginator import *
from django.http import JsonResponse
from django.urls import reverse
from django.template.loader import render_to_string
from django.db import transaction
from adminconsole.models import *
from django.db.models import Q
from adminconsole.helper import clean_text
from ..constantlabels import *
from django.db.models import Prefetch
from django.db.models import F
from datetime import date
import pdb
from django.db.models import Q
from django.http import Http404
today = date.today()
import pdb
from adminconsole.helper import is_image_or_video


#USERS
class UserView(LoginRequiredMixin, View):
    login_url = LOGIN_URL

    def get(self, request, *args, **kwargs):
        data, filter_conditions, filters = {}, {}, Q()
        
        if is_ajax(request=request):
            keyword = request.GET.get('keyword', None)
            status = request.GET.get('status', None)
            
            if keyword:
                filters |= Q(title__icontains=keyword)
                
            if status and status != 'all':
                status = True if status == 'active' else False
                filters &= Q(is_active=status)
                
        users = User.objects.filter(filters).order_by('-id')
        try:
            page = int(request.GET.get("page", 1))
        except ValueError:
            page = 1

        paginator = Paginator(users, PAGINATION_PERPAGE)
        try:
            users = paginator.page(page)
        except PageNotAnInteger:
            users = paginator.page(1)  
        except EmptyPage:
            users = paginator.page(paginator.num_pages)

        if is_ajax(request=request):
            context = {}
            context['users']= users
            response = {'status': True,
                        "template": render_to_string("adminconsole/users/list_view.html", context, request=request),
                        "pagination": render_to_string("adminconsole/users/pagination_view.html", context=context, request=request),
                        }
            return JsonResponse(response)
        
        data['users'], data['current_page'] = users, page
        return renderfile(request,'users','index', data)
    
class UserCreateView(LoginRequiredMixin, View):
    login_url = LOGIN_URL
    
    def get(self, request, *args, **kwargs):
        data = {}
        max_sequence = User.objects.all().count()
        data['sequence'] = (max_sequence or 0) + 1  
        return renderfile(request,'users','form',data)
    

    def post(self, request, *args, **kwargs):   
        try:
            with transaction.atomic():
                title = request.POST.get('title', None)
                max_sequence = User.objects.all().count()
                sequence = (max_sequence or 0) + 1  
            
                User.objects.create(title=title, sequence=sequence)
                return JsonResponse({'status': True, 'message':USER_CREATED, 'redirect_url': reverse('adminconsole:users')})
        except Exception as dberror:
            error_message = clean_text(str(dberror))
            return JsonResponse({'status': False, 'message':error_message, 'redirect_url': reverse('adminconsole:create_user')})
        
class UserUpdateView(LoginRequiredMixin, View):
    login_url = LOGIN_URL

    def get(self, request, id, *args, **kwargs):
        user = get_object_or_404(User, id=id)
        context = {'user': user, 'id':id}
        return renderfile(request,'users','form', context)


    def post(self, request, id, *args, **kwargs):
        response = {}
        try:
            with transaction.atomic():
                filetype, response = None, {}
                user = get_object_or_404(User, id=id)
                
                sequence = request.POST.get('sequence', None)
                title = request.POST.get('title', None)
                
                
                if sequence:
                    user.sequence = sequence
                if title:
                    user.title = title
                    
                user.save()
                response['status'] = True
                response['message'] = USER_CREATED
                response['redirect_url'] = reverse('adminconsole:users')
        except Exception as error:
            response['status'] = False
            response['message'] = clean_text(str(error))
        return JsonResponse(response)

class UserToggleView(LoginRequiredMixin, View):
    login_url = LOGIN_URL

    def post(self, request, id, *args, **kwargs):
        response = {}
        id  = request.POST.get('id', None)
        status  = request.POST.get('status', None)
        
        try:
            with transaction.atomic():
                response = {}
                user = get_object_or_404(User, id=id)
                if status == 'unchecked':
                    user.is_active = False
                    message = USER_DEACTIVATED
                else:
                    user.is_active = True
                    message = USER_ACTIVATED
                user.save()
                response['status'] = True
                response['message'] = message
                response['redirect_url'] = reverse('adminconsole:users')
        except Exception as error:
            response['status'] = False
            response['message'] = clean_text(str(error))
        return JsonResponse(response)
    
class UserDeleteView(LoginRequiredMixin, View):
    login_url = LOGIN_URL

    def post(self, request, id, *args, **kwargs):
        response = {}
        id  = request.POST.get('id', None)
        try:
            with transaction.atomic():
                response = {}
                user = get_object_or_404(User, id=id)
                user.delete()
                
                response['status'] = True
                response['message'] = USER_DELETED
                response['redirect_url'] = reverse('adminconsole:users')
        except Exception as error:
            response["status"] = False
            response['message'] = clean_text(str(error))
        return JsonResponse(response)
    