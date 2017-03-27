from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from hybrid_cloud.action.jsonAction import get_private_usage_Action,get_private_instance_Action
from hybrid_cloud.api.AliyunApi import AliyunInterface
from django.template import  Context
# Create your views here.
def isLogin(request):
    username = request.COOKIES.get('username')
    if username:
        return True
    else:
        return False

@csrf_exempt
def login(request):
    return render(request, 'login.html',{})

@csrf_exempt
def index(request):
    if(isLogin(request)):
        return render(request, 'index.html',{})
    else:
        return render(request, 'login.html', {})

@csrf_exempt
def overview(request):
    if (isLogin(request)):
        private_usages = get_private_usage_Action(request)
        Aliyunclient = AliyunInterface()
        public_usages = Aliyunclient.getUsageList()
        return render(request, 'overview.html',{'private_usages': private_usages ,'public_usages':public_usages})
    else:
        return render(request, 'login.html',{})

@csrf_exempt
def instance(request):
    if (isLogin(request)):
        private_instances = get_private_instance_Action(request)
        Aliyunclient = AliyunInterface()
        public_instances = Aliyunclient.getInstanceList()
        return render(request, 'instance.html',{'private_instances':private_instances ,'public_instances':public_instances})
    else:
        return render(request, 'login.html', {})

@csrf_exempt
def create(request):
    if (isLogin(request)):
        return render(request, 'create.html',{})
    else:
        return render(request, 'login.html', {})
