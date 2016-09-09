# XLD Salesforce Plugin
## Preface ##

This document describes the functionality provided by the Salesforce plugin.


## Overview ##

The Salesforce plugin is an XL Deploy plugin that can perform deployments to Salesforce.

The plugin uses the java/ant-based [ Force.com Migration Tool](https://developer.salesforce.com/docs/atlas.en-us.daas.meta/daas/meta_development.htm) for Salesforce integration.

## Features ##

* Deploy and undeploy Salesforce metadata packages

## Requirements ##

* **XLD Server** 5+
* **Force.com Migration tool** 37.0+
* **Ant** 1.7+ 
		

## Installation ##

### Ant ###

If Ant is not alredy present on the XL Deploy server, please download from [here](http://ant.apache.org/bindownload.cgi) and unzip to a location of your choice.

### Salesforce Migration Tool ###

Download the [Salesforce Jar](./dist/ant-salesforce.jar) from this repository to a location of your choice.


### Plugin installation ###

Plugin can be downloaded directly from the plugin's repository on [Github](https://github.com/xebialabs-community/xld-salesforce-plugin/releases).

Place the plugin's XLDP file in the __&lt;xld-home&gt;/plugins__ directory. 

Edit your __&lt;xld-home&gt;/ext/synthetic.xml__ file and copy the following snippet into it.  Remember to change the default values for the location of your Ant executable and ant-salesforce.jar

```xml

<type-modification type="sfdc.Organization">
        <property name="migrationToolJar" default="!!CHANGE ME!!>" description="Absolute file reference to the ant-salesforce.jar" hidden="true" />
        <property name="antExecutable" default="<!!CHANGE ME!!>" description="Absolute file reference to the ant executable (ant, ant.bat, ant.cmd)" hidden="true"  />
</type-modification>

```

## Salesforce Connection Information ##


This plugin adds a new container type __sfdc.Organization__ to the system. This type must be created under the Infrastructure root in the XLD repository.

| Property | Description |
| -------- | ----------- |
| url   | Salesforce login url. Default is https://login.salesforce.com |
| username | The Salesforce username for login |
| password | The Salesforce password for login. If you are using a security token, paste the 25-digit token value to the end of your password |
| proxyHost | If your network requires an HTTP proxy |
| proxyPort | If your network requires an HTTP proxy |


## Deploying a Salesforce Metadata Package ##

The MetadataPackage (__sfdc.MetadataPackage__) configuration item can be defined in a deployment package as a zip file.  


## Sample Dars ##

Sample dars are available to show XLD deployment packaging.
The dar use the codepkg sample from the Force.com Migration Tool.

* [SalesForceMetaPackage-1.0.dar](./src/main/docs/samples/SalesForceMetaPackage-1.0.dar)

