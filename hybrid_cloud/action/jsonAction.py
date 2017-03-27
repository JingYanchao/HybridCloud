# -*- coding:utf-8 -*-
from hybrid_cloud.util.Printlog import print_log
import hybrid_cloud.util.Passwd as passwd
from hybrid_cloud.api import Monitor
import hybrid_cloud.util.Cloud as Cloud
from django.http import HttpResponse, HttpResponseRedirect
import json
from django.views.decorators.csrf import csrf_exempt
from hybrid_cloud.api.ODA import ODA
from hybrid_cloud.api.AliyunApi import AliyunInterface
import time as time_module

@csrf_exempt
def loginAction(request):
    print_log('Start loginAction')
    if request.method == "POST":
        # get username pwd from post method
        username = request.POST["username"]
        password = request.POST["password"]
        # print username, password
        if username == passwd.Identity["username"] and password == passwd.Identity["passwd"]:
            # return HttpResponseRedirect("/main/")
            response = HttpResponse(json.dumps({}), content_type="application/json")
            cloudinfo={}
            cloudinfo["openstack"] = {"user": passwd.Identity['clouduser'], "pwd": passwd.Identity['cloudpasswd'],
                                     "project":passwd.Identity['project'], "endpoint":passwd.Identity['endpoint']}
            # create session
            request.session["cloud"] = cloudinfo
            # create cookies
            response.set_cookie('username', username, 3600)  # create cookies
            return response

@csrf_exempt
def logoutAction(request):
    print_log('Start logoutAction')
    username = request.COOKIES.get('username')  # TO GET THE COOKIES
    if request.session.get('cloud'):
        del request.session['cloud']
    if username:
        response = HttpResponseRedirect("/login/")
        response.delete_cookie('username')
        return response

@csrf_exempt
def overviewAction(request):
    print_log('Start overviewAction')
    if request.method == 'POST':
        cloudname = request.POST["cloud"]
        # print authurl
        # print cloudname
        cloud = Monitor.Monitor(**Cloud.get_nova_credentials(request, cloudname))
        limits = cloud.getLimits()
        if limits !=None:
            return HttpResponse(json.dumps({"limits": limits}), content_type="application/json")

def get_private_usage_Action(request):
    print_log('Start get private usage')
    cloud = Monitor.Monitor(**Cloud.get_nova_credentials(request, 'openstack'))
    Usages = cloud.getUsages()
    private_usage = []
    for item in Usages:
        single_usage={}
        single_usage['name'] = item['name']
        single_usage['vcpus'] = item['vcpus']
        single_usage['disk'] = str(item['disk'])+" GB"
        single_usage['ram'] = str(item['ram'])+" MB"
        single_usage['createTime'] = item['createTime']
        private_usage.append(single_usage)
    if Usages != None:
        return private_usage


def get_private_instance_Action(request):
    print_log('Start get private instance')
    cloud = Monitor.Monitor(**Cloud.get_nova_credentials(request, 'openstack'))
    instances = cloud.getInstanceDetailAll()
    print instances
    private_instance = []
    for item in instances:
        single_instance = {}
        single_instance['cloud'] = 'openstack'
        single_instance['id'] = item['id']
        single_instance['status'] = item['status']
        single_instance['name'] = item['name']
        single_instance['image'] = item['image']
        single_instance['createTime'] = item['created']
        single_instance['flavor'] = item['flavor']
        single_instance['availability_zone'] = item['availability_zone']
        single_instance['power_state'] = item['power_state']
        private_instance.append(single_instance)
    if private_instance != None:
        return private_instance

@csrf_exempt
def instanceActionsAction(request):
    print_log('Start_instacneActionsAction')
    if request.method == 'POST':
        actions = request.POST["actions"]
        cloudname = request.POST["cloud"]
        serverid = request.POST["serverid"]
        # print actions,cloudname,serverid
        print actions,cloudname,serverid
        cloudname = cloudname.strip()
        cloud = Monitor.Monitor(**Cloud.get_nova_credentials(request,cloudname))
        print cloud.auth_url
        if actions:
            if "start" == actions:
                cloud.startServer(serverid)
            elif "stop" == actions:
                cloud.stopServer(serverid)
            elif "terminate" == actions:
                cloud.terminateServer(serverid)
            elif "addfloatingip" == actions:
                cloud.addFloatingIps(serverid)
        return HttpResponse(json.dumps({}), content_type="application/json")

@csrf_exempt
def AliyunActionsAction(request):
    print_log('Start_AliyunActionsAction')
    if request.method == 'POST':
        instance_id = request.POST["instance_id"]
        instance_id = instance_id.encode('utf-8').strip()
        AliyunClient = AliyunInterface()
        AliyunClient.deleteInstance(instance_id)
        return HttpResponse(json.dumps({}), content_type="application/json")


@csrf_exempt
def createAdvanceAction(request):
    print_log('Start_createAdvancedAction')
    if request.method == 'POST':
        small_num = request.POST["small_num"]
        medium_num = request.POST["medium_num"]
        large_num = request.POST["large_num"]
        time = request.POST["time"]
        is_private = request.POST["is_private"]
        cloud = Monitor.Monitor(**Cloud.get_nova_credentials(request, "openstack"))
        resource = cloud.getResource()
        print small_num,medium_num,large_num,time,type(is_private),type(resource["vcpu"]),resource["ram"],resource["disk"]
        R_private=[]
        R_public=[]
        A = []
        num_small = int(small_num.encode('utf-8'))
        num_medium = int(medium_num.encode('utf-8'))
        num_large = int(medium_num.encode('utf-8'))
        A.append(0)
        A.append(int(small_num.encode('utf-8')))
        A.append(int(medium_num.encode('utf-8')))
        A.append(int(large_num.encode('utf-8')))
        A.append(int(time.encode('utf-8')))
        if(int(is_private.encode('utf-8')) == 1):
            R_private.append(A)
        else:
            R_public.append(A)
        T=[]
        T.append(resource["vcpu"])
        T.append(resource["ram"])
        T.append(resource["disk"])
        h = 0
        print R_private,R_public,T
        x_private,x_public,h,E = ODA(R_private,R_public,T,h)
        print x_private,x_public,h,E

        if(len(x_private)>0):
            if(x_private[0] == 1):#可以创建在私有云上
                if(num_small>0):
                    instances = {}
                    name = []
                    instances['type'] = 'm1.small'
                    for i in range(0, num_small):
                        name.append('instance' +'_small_' +  str(int(time_module.time()))+"_"+str(i + 1))
                    instances['name'] = name
                    cloud.createInstance(instances)
                if (num_medium > 0):
                    instances = {}
                    name = []
                    instances['type'] = 'm1.medium'
                    for i in range(0, num_medium):
                        name.append('instance' + '_medium_' + str(int(time_module.time()))+"_"+str(i + 1))
                    instances['name'] = name
                    cloud.createInstance(instances)
                if ( num_large > 0):
                    instances = {}
                    name = []
                    instances['type'] = 'm1.large'
                    for i in range(0, num_large):
                        name.append('instance' + '_large_' + str(int(time_module.time()))+"_"+str(i + 1))
                    instances['name'] = name
                    cloud.createInstance(instances)
                return HttpResponse(json.dumps({"limits": "虚拟机全部成功被创建在私有云上"}), content_type="application/json")
            else:#不能创建在私有云上
                return HttpResponse(json.dumps({"limits": "私有云资源不够，请求被拒绝"}), content_type="application/json")

        if(len(x_public)>0):
            if(x_public[0] == 1):#可以创建在私有云上
                if (num_small > 0):
                    instances = {}
                    name = []
                    instances['type'] = 'm1.small'
                    for i in range(0, num_small):
                        name.append('instance' + '_small_' + str(i + 1))
                    instances['name'] = name
                    cloud.createInstance(instances)
                if (num_medium > 0):
                    instances = {}
                    name = []
                    instances['type'] = 'm1.medium'
                    for i in range(0, num_medium):
                        name.append('instance' + '_medium_' + str(i + 1))
                    instances['name'] = name
                    cloud.createInstance(instances)
                if (num_large > 0):
                    instances = {}
                    name = []
                    instances['type'] = 'm1.large'
                    for i in range(0, num_large):
                        name.append('instance' + '_large_' + str(i + 1))
                    instances['name'] = name
                    cloud.createInstance(instances)
                return HttpResponse(json.dumps({"limits": "虚拟机全部成功被创建在私有云上"}), content_type="application/json")

            else:#可以创建在公有云上
                Aliclient = AliyunInterface()
                if (num_small > 0):
                    instance_type = "ecs.n1.small"
                    for i in range(0, num_small):
                        res = Aliclient.createInstance(instance_type)
                        print res
                if (num_medium > 0):
                    instance_type = "ecs.n1.medium"
                    for i in range(0, num_medium):
                        res = Aliclient.createInstance(instance_type)
                        print res
                if (num_large > 0):
                    instance_type = "ecs.n1.large"
                    for i in range(0, num_large):
                        res = Aliclient.createInstance(instance_type)
                        print res
                return HttpResponse(json.dumps({"limits": "虚拟机全部成功被创建在公有云上"}), content_type="application/json")

        return HttpResponse(json.dumps({"limits": "虚拟机创建成功"}), content_type="application/json")





