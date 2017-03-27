import json
from aliyunsdkcore import client
from aliyunsdkecs.request.v20140526 import DescribeRegionsRequest, DescribeInstancesRequest, CreateInstanceRequest, DeleteInstanceRequest
from Process_aliyun import getinstanceDetal,getinstanceUsage

class AliyunInterface:
    def __init__(self):
        self.access_key = 'ha33EKzYxQlm1OGg'
        self.access_secret = 'cPj7Q06bT04dKqxOiDnvLOIWTCno2t'
        self.region_id = 'cn-hangzhou'
        self.client = client.AcsClient(self.access_key, self.access_secret, self.region_id)

    def getRegions(self):
        req = DescribeRegionsRequest.DescribeRegionsRequest()
        req.set_accept_format('json')
        res = self.client.do_action(req)
        return json.loads(res)

    def getInstanceList(self):
        req = DescribeInstancesRequest.DescribeInstancesRequest()
        req.set_accept_format('json')
        res = self.client.do_action(req)
        return getinstanceDetal(json.loads(res))

    def getUsageList(self):
        req = DescribeInstancesRequest.DescribeInstancesRequest()
        req.set_accept_format('json')
        res = self.client.do_action(req)
        return getinstanceUsage(json.loads(res))

    def createInstance(self, instance_type='ecs.n1.tiny', image_id = 'ubuntu1404_64_40G_cloudinit_20160727.raw'):
        req = CreateInstanceRequest.CreateInstanceRequest()
        req.set_accept_format('json')
        req.set_InstanceType(instance_type)
        req.set_ImageId(image_id)
        req.set_SystemDiskCategory('cloud_efficiency')
        res = self.client.do_action(req)
        return json.loads(res)

    def deleteInstance(self, instance_id):
        req = DeleteInstanceRequest.DeleteInstanceRequest()
        req.set_accept_format('json')
        req.set_InstanceId(instance_id)
        res = self.client.do_action(req)
        return json.loads(res)

if __name__ == '__main__':
    obj = AliyunInterface()
    # print obj.getInstanceList().get(u'Instances').get(u'Instance')
    # print obj.createInstance()
    print obj.getRegions().get(u'Regions').get(u'Region')
    # print obj.deleteInstance('i-wz92o5ndq3w4hksxbuwd')