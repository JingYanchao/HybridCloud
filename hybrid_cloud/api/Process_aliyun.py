def getinstanceDetal(request):
    print request['TotalCount']
    num = int(request['TotalCount'])
    instances = request['Instances']['Instance']
    ret=[]
    for i in range(0,num):
        aliyun_instance={}
        aliyun_instance['id'] = instances[i]['InstanceId']
        aliyun_instance['cloud'] ='Aliyun'
        aliyun_instance['name'] = instances[i]['InstanceName']
        aliyun_instance['type'] = instances[i]['InstanceType']
        aliyun_instance['ip'] = instances[i]['InnerIpAddress']['IpAddress'][0]
        aliyun_instance['Region_id'] = instances[i]['RegionId']
        aliyun_instance['status'] = instances[i]['Status']
        aliyun_instance['image'] = instances[i]['ImageId']
        aliyun_instance['time']= instances[i]['CreationTime']
        ret.append(aliyun_instance)
    return ret

def getinstanceUsage(request):
    print request
    print request['TotalCount']
    num = int(request['TotalCount'])
    instances = request['Instances']['Instance']
    ret = []
    for i in range(0, num):
        aliyun_usage = {}
        aliyun_usage['name'] = instances[i]['InstanceName']
        aliyun_usage['type'] = instances[i]['InstanceType']
        aliyun_usage['Region_id'] = instances[i]['RegionId']
        aliyun_usage['status'] = instances[i]['Status']
        aliyun_usage['time'] = instances[i]['CreationTime']
        ret.append(aliyun_usage)
    return ret

