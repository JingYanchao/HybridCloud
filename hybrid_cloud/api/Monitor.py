'''
Created on Nov 26, 2015

@author: stack
'''
from __future__ import division
import MonitorApi
class Monitor(object):
    def __init__(self, username=None,api_key=None,project_id=None,auth_url='',**kwargs):
        '''
            Constructor
        '''
        self.username = username
        self.api_key = api_key
        self.project_id = project_id
        self.auth_url = auth_url
        self.kwargs = kwargs
        self.authClient = None

    #to get authorize
    def getAuth(self):
        try:
            if not self.authClient:
                client = MonitorApi.MonitorApi(username=self.username,
                                                api_key = self.api_key,
                                                project_id = self.project_id,
                                                auth_url = self.auth_url,
                                                **self.kwargs)
                self.authClient = client  ##initialize self.authClient when first call getAuth
            else:
                client = self.authClient 
            return client
        except Exception,e:
            print Exception,":",e
            return None # if failed,return None
        
    def createInstance(self,createspec):
        try:
            client = self.getAuth()
            # if client not None
            if client:
                client.createDefaultInstance(createspec) #you can use createInstance either
        except Exception,e:
            print Exception,":",e
            return False # if failed,return False
        return True

    def getResource(self):
        resource = {}
        try:
            client = self.getAuth()
            if client:
                limits = client.getLimits()
                resource['vcpu'] = (limits["coresTotal"]-limits["coresUsed"])
                resource['ram']  = ((limits["ramTotal"]-limits["ramUsed"])*1.0)/1000.0
                resource['disk'] = (limits["volumeStorage"]-limits["totalGigabytesUsed"])
            else:
                return None
        except Exception,e:
            print Exception, ":", e
            return None  # if failed,return None
        return resource
    
    def getLimits(self):
        tmp_lists = []
        lists=[]
        try:
            client = self.getAuth()
            if client:
                limits = client.getLimits()
                p=limits["instanceUsed"]/limits["instanceTotal"]
                tmp_lists.append(['Used',p*100])
                tmp_lists.append(['NotUsed',(1-p)*100])
                lists.append(tmp_lists)
                tmp_lists = []
                p=limits["coresUsed"]/limits["coresTotal"]
                tmp_lists.append(['Used',p*100])
                tmp_lists.append(['NotUsed',(1-p)*100])
                lists.append(tmp_lists)
                tmp_lists = []
                p=limits["ramUsed"]/limits["ramTotal"]
                tmp_lists.append(['Used',p*100])
                tmp_lists.append(['NotUsed',(1-p)*100])
                lists.append(tmp_lists)
                tmp_lists = []
                p=limits["totalGigabytesUsed"]/limits["volumeStorage"]
                tmp_lists.append(['Used',p*100])
                tmp_lists.append(['NotUsed',(1-p)*100])
                lists.append(tmp_lists)

        except Exception,e:
            print Exception,":",e
            return None # if failed,return None
        return lists
    
    def getUsages(self):
        try:
            client = self.getAuth()
            if client:
                usages = client.getUsages()
                return usages
        except Exception,e:
            print Exception,":",e
            return None # if failed,return None

    def getInstanceDetail(self,id=''):
        detail = []
        try:
            client = self.getAuth()
            if client:
                detail = client.getInstanceDetail(id)
        except Exception,e:
            print Exception,":",e
            return None # if failed,return None
        return detail

    def getInstanceDetailAll(self):
        details = []
        try:
            client = self.getAuth()
            if client:
                servers = client.getServerList()
                # print servers
                for server in servers:
                    print server.name
                    details.append(client.getInstanceDetail(server.id))
        except Exception,e:
            print Exception,":",e
            return None # if failed,return None
        return details
    
    def stopServer(self,id):
        try:
            client = self.getAuth()
            client.stopServer(id)
        except Exception,e:
            print Exception,":",e
            return None # if failed,return None
        return True
    
    def startServer(self,id):
        try:
            client = self.getAuth()
            client.startServer(id)
        except Exception,e:
            print Exception,":",e
            return False # if failed,return None
        return True
        
    
    def terminateServer(self,id):
        try:
            client = self.getAuth()
            client.terminateServer(id)
        except Exception,e:
            print Exception,":",e
            return False # if failed,return None
        return True
    
    
    def addFloatingIps(self,id):
        try:
            client = self.getAuth()
            client.addFloatingIps(id)
        except Exception,e:
            print Exception,":",e
            return False # if failed,return None
        return True

    def getServerNum(self):
        try:
            client = self.getAuth()
            server = client.getServerNum()
        except Exception,e:
            print Exception,":",e
            return None # if failed,return None
        return server
