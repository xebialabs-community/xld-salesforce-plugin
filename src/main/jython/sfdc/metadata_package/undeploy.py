from sfdc.metadata_package import SalesForceClient

def deploy_package(org_ci, deployed):
    print "Starting undeployment"
    client = SalesForceClient.new_instance(org_ci)
    client.undeploy_package(deployed.file.path)
    print "Done"

if __name__ == '__main__' or __name__ == '__builtin__':
    container = previousDeployed.container
    deploy_package(container, previousDeployed)

