'''
Created on Nov 25, 2015

@author: stack
'''
import novaclient.client as nvclient
import cinderclient.v2.client as cdclient
from hybrid_cloud.util.Printlog import print_log

def get_nova_credentials_v2(version='2',username=None,api_key=None,project_id=None,auth_url='',**kwargs):
        d = {}
        d["version"] = '2'
        d['username'] = username
        d['api_key'] = api_key
        d['project_id'] = project_id
        d['auth_url'] = auth_url
        return d

class MonitorApi(object):
    def __init__(self, version='2',username=None, api_key=None, project_id=None,auth_url='',**kwargs):
        self.nova_client = nvclient.Client(version, username, api_key, project_id, auth_url,**kwargs)
        self.cinder_client = cdclient.Client(username, api_key, project_id, auth_url,**kwargs)
        
    def getServerList(self):
        return self.nova_client.servers.list()

    def getLimits(self):
        corelimits = self.nova_client.limits.get().absolute

        usage_limits = {}
        for i in corelimits:
            #usage_limits[i.name] = i.value
            if i.name ==  "maxTotalInstances":
                usage_limits["instanceTotal"] = i.value
            elif i.name == "totalInstancesUsed":
                usage_limits["instanceUsed"] = i.value
            elif i.name == "maxTotalCores":
                usage_limits["coresTotal"] = i.value
            elif i.name == "totalCoresUsed":
                usage_limits["coresUsed"] = i.value
            elif i.name == "maxTotalRAMSize":
                usage_limits["ramTotal"] = i.value
            elif i.name == "totalRAMUsed":
                usage_limits["ramUsed"] = i.value

        cinderlimits = self.cinder_client.limits.get().absolute
        for i in cinderlimits:
                #usage_limits[i.name] = i.value

            if i.name ==  "maxTotalVolumeGigabytes":
                usage_limits["volumeStorage"] = i.value
            elif i.name == "totalGigabytesUsed":
                usage_limits["totalGigabytesUsed"] = i.value
            elif i.name == "maxTotalVolumes":
                usage_limits["volumeTotal"] = i.value
            elif i.name == "totalVolumesUsed":
                usage_limits["volumeTotalUsed"] = i.value
        return usage_limits
    
    def getUsages(self):
        servers = self.nova_client.servers.list()
        usages = []
        #to get every server's usage
        for server in servers:
            usage = {}
            usage["name"] = server.name
            usage["id"] = server.id
            usage["createTime"] = server.created
            usage["ram"] = self.nova_client.flavors.get(server.flavor["id"]).ram
            usage["vcpus"] = self.nova_client.flavors.find(id=server.flavor["id"]).vcpus
            usage["disk"] = self.nova_client.flavors.get(server.flavor["id"]).disk
            usages.append(usage)
        return usages
    
    def createDefaultInstance(self,createspec):
        print_log('Start create instance')
        print createspec['type']
        image = self.nova_client.images.find(name="ubuntu16.04LTS")
        print len(createspec['type'])
        flavor = self.nova_client.flavors.find(name=createspec['type'])
        print createspec['type']
        net = self.nova_client.networks.find(label='admin_internal_net')
        print createspec['type']
        nics = [{'net-id':net.id}]

        #create instance
        for instance in createspec['name']:
            instance = self.nova_client.servers.create(name=instance,image=image,flavor=flavor,nics=nics)
    
    def createInstance(self,name,image,flavor,**kwargs):
        pass

    def getInstanceDetail(self,id):
        server = self.nova_client.servers.get(id)
        detail = {}

        #server infomations
        detail["name"] = server.name
        detail["id"] = server.id
        detail["status"] = server.status
        detail["created"] = server.created
        detail["flavor"] = self.nova_client.flavors.get(server.flavor["id"]).name
        detail["ram"] = self.nova_client.flavors.get(server.flavor["id"]).ram
        detail["vcpus"] = self.nova_client.flavors.find(id=server.flavor["id"]).vcpus
        detail["disk"] = self.nova_client.flavors.get(server.flavor["id"]).disk
        ##addr informations
        addresses = []
        address = server.addresses.values()[0]

        detail["image"] = self.nova_client.images.get(server.image['id']).name
        power_states = [
        'NOSTATE',      # 0x00
        'Running',      # 0x01
        '',             # 0x02
        'Paused',       # 0x03
        'Shutdown',     # 0x04
        '',             # 0x05
        'Crashed',      # 0x06
        'Suspended'     # 0x07
        ]
        detail["power_state"] = power_states[getattr(server, "OS-EXT-STS:power_state")]
        detail["availability_zone"] = getattr(server, "OS-EXT-AZ:availability_zone")
        #########end#########33
        return detail
    
    
    
    def stopServer(self,id):
        server = self.nova_client.servers.get(id)
        server.stop()
    
    def startServer(self,id):
        server = self.nova_client.servers.get(id)
        server.start()
    
    def terminateServer(self,id):
        server = self.nova_client.servers.get(id)
        server.delete()
    
    
    def addFloatingIps(self,id):
        floatingip = self.nova_client.floating_ips.create()
        server = self.nova_client.servers.get(id)
        #print floatingip
        server.add_floating_ip(floatingip)

    def getServerNum(self):
        m = {}
        hypervisors = self.nova_client.hypervisors.list(detailed=True)
        for hypervisor in hypervisors:
            m[hypervisor.hypervisor_hostname] = hypervisor.running_vms
        return m


