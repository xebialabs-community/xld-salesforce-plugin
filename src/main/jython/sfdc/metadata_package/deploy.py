from sfdc.metadata_package import SalesForceClient

def deploy_package(org_ci, deployed):
    print "Starting deployment"
    client = SalesForceClient.new_instance(org_ci)
    client.deploy_package(deployed.file.path)
    print "Done"

if __name__ == '__main__' or __name__ == '__builtin__':
    container = deployed.container
    deploy_package(container, deployed)

