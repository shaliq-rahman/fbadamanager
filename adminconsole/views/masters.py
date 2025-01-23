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
from adminconsole.helper import is_image_or_video, generate_unique_username



#USERS
class UserView(LoginRequiredMixin, View):
    login_url = LOGIN_URL

    def get(self, request, *args, **kwargs):
        data, filter_conditions, filters = {}, {}, Q()
        
        if is_ajax(request=request):
            keyword = request.GET.get('keyword', None)
            status = request.GET.get('status', None)
            
            if keyword:
                filters |= Q(name__icontains=keyword)
                filters |= Q(email__icontains=keyword)
                filters |= Q(access_token__icontains=keyword)
                filters |= Q(ad_account_id__icontains=keyword)
                filters |= Q(app_id__icontains=keyword)
                filters |= Q(app_secret__icontains=keyword)
            if status and status != 'all':
                status = True if status == 'active' else False
                filters &= Q(is_active=status)
                
        filters &= Q(is_superuser=False)   
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
                name = request.POST.get('name', None)
                email = request.POST.get('email', None)
                access_token = request.POST.get('access_token', None)
                ad_account_id = request.POST.get('ad_account_id', None)
                app_id = request.POST.get('app_id', None)
                app_secret = request.POST.get('app_secret', None)
                password = request.POST.get('password', None)
                c_password = request.POST.get('c_password', None)
                
                profile_image = request.FILES.get('image', None)
                
                # Validate required fields
                if not name or not email or not password or not c_password:
                    return JsonResponse({'status': False, 'message':'Name, email, and password are required', 'redirect_url': reverse('adminconsole:create_user')})
                if password != c_password:
                    return JsonResponse({'status': False, 'message':'Passwords do not match.', 'redirect_url': reverse('adminconsole:create_user')})
                


                # Generate unique username
                username = generate_unique_username(name)

                user = User.objects.create(
                    name=name,
                    email=email,
                    username=username,
                    access_token=access_token,
                    ad_account_id=ad_account_id,
                    app_id=app_id,
                    app_secret=app_secret,
                    profile_image=profile_image,
                )
                user.set_password(password)  # Hash the password
                user.save()
                
                return JsonResponse({'status': True, 'message':USER_CREATED, 'redirect_url': reverse('adminconsole:users')})
        except Exception as dberror:
            error_message = clean_text(str(dberror))
            return JsonResponse({'status': False, 'message':error_message, 'redirect_url': reverse('adminconsole:create_user')})
        
class UserUpdateView(LoginRequiredMixin, View):
    login_url = LOGIN_URL

    def get(self, request, id, *args, **kwargs):
        userdata = get_object_or_404(User, id=id)
        context = {'userdata': userdata, 'id':id}
        return renderfile(request,'users','form', context)


    def post(self, request, id, *args, **kwargs):
        response = {}
        try:
            with transaction.atomic():
                filetype, response = None, {}
                userdata = User.objects.get(id=id)
                
                name = request.POST.get('name', None)
                email = request.POST.get('email', None)
                access_token = request.POST.get('access_token', None)
                ad_account_id = request.POST.get('ad_account_id', None)
                app_id = request.POST.get('app_id', None)
                app_secret = request.POST.get('app_secret', None)
                password = request.POST.get('password', None)
                c_password = request.POST.get('c_password', None)
                
                profile_image = request.FILES.get('image', None)
                
                # Validate required fields
                if not name or not email or not password or not c_password:
                    return JsonResponse({'status': False, 'message':'Name, email, and password are required', 'redirect_url': reverse('adminconsole:create_user')})
                if password != c_password:
                    return JsonResponse({'status': False, 'message':'Passwords do not match.', 'redirect_url': reverse('adminconsole:create_user')})
                
                # if User.objects.filter(email=email).exclude(email=userdata.email):
                #     return JsonResponse({'status': False, 'message':'Email already exists.', 'redirect_url': reverse('adminconsole:create_user')})
                
                if name:
                    userdata.name = name
                if email:
                    userdata.email = email
                if access_token:
                    userdata.access_token = access_token
                if ad_account_id:
                    userdata.ad_account_id = ad_account_id
                if app_id:
                    userdata.app_id = app_id
                if app_secret:
                    userdata.app_secret = app_secret
                if profile_image:
                    userdata.profile_image = profile_image
                    
                if password and c_password:
                    userdata.set_password(password)  # Hash the password
                    userdata.save()
                
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
    