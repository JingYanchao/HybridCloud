def get_nova_credentials(request,cloudname):
    cloud = {}
    cloudinfo = request.session.get("cloud")
    if cloudinfo and cloudinfo.has_key(cloudname):
        cloud['username'] = cloudinfo[cloudname]["user"]    
        cloud['api_key'] = cloudinfo[cloudname]["pwd"]
        cloud['auth_url'] = cloudinfo[cloudname]["endpoint"]
        cloud['project_id'] = cloudinfo[cloudname]["project"]
    return cloud
