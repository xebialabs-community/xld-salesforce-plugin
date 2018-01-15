from subprocess import Popen, PIPE, CalledProcessError, STDOUT
from string import Template
import zipfile
import xml.etree.ElementTree as ET
from java.nio.file import Files, Paths
from org.apache.commons.io import FileUtils


class SalesForceClient(object):

    def __init__(self, url, username, password, proxy_host=None, proxy_port=None, ant_executable="ant.sh",
                 migration_tool_jar="salesforce/ant-salesforce.jar"):

        path = Paths.get(migration_tool_jar)
        if not Files.exists(path):
            raise Exception("Migration jar not found [%s]." % migration_tool_jar)
        self.migration_tool_jar = str(path.toAbsolutePath())
        self.ant_executable = ant_executable
        self.proxy_port = proxy_port
        self.proxy_host = proxy_host
        self.url = url
        self.username = username
        self.password = password

    @staticmethod
    def new_instance(ci):
        return SalesForceClient(ci.url, ci.username, ci.password, proxy_host=ci.proxyHost, proxy_port=ci.proxyPort,
                                ant_executable=ci.antExecutable, migration_tool_jar=ci.migrationToolJar)

    def _get_env_properties(self):
        env_properties = {}
        if self.proxy_host is not None and self.proxy_port is not None:
            env_properties['ANT_OPTS'] = "-Dhttp.proxyHost=%s -Dhttp.proxyPort=%s" % (self.proxy_host, self.proxy_port)
        return env_properties

    def _setup_working_dir(self):
        working_dir = Files.createTempDirectory("sfdc_tempdir")
        working_dir_path = str(working_dir.toAbsolutePath())
        package_path = Files.createDirectory(working_dir.resolve("deploy_root"))
        return working_dir, working_dir_path, package_path

    def _extract_package(self, zipped_package, target_dir):
        zip_file = zipfile.ZipFile(zipped_package, 'r')
        zip_file.extractall(target_dir)
        zip_file.close()

    def _execute(self, working_dir):
        working_dir_path = str(working_dir.toAbsolutePath())
        build_xml = self._project_xml_template(working_dir_path)

        Files.write(working_dir.resolve("build.xml"), bytearray(str(build_xml)))

        process = Popen([self.ant_executable], stdout=PIPE, stderr=STDOUT, cwd=working_dir_path, env=self._get_env_properties(), universal_newlines=True)
        stdout_lines = iter(process.stdout.readline, "")
        for stdout_line in stdout_lines:
            yield stdout_line
        process.stdout.close()
        rc = process.wait()
        if rc != 0:
            raise CalledProcessError(rc, self.ant_executable)

    def undeploy_package(self, zipped_package):
        working_dir, working_dir_path, undeploy_package_path = self._setup_working_dir()

        try:
            unzipped_package_path = Files.createDirectory(working_dir.resolve("undeploy_root"))
            self._extract_package(zipped_package, str(unzipped_package_path.toAbsolutePath()))
            package_xml_file = unzipped_package_path.resolve("package.xml")
            root = ET.parse(str(package_xml_file.toAbsolutePath())).getroot()
            ns = {'sf': 'http://soap.sforce.com/2006/04/metadata'}
            version = root.find('sf:version', ns).text

            Files.copy(package_xml_file, undeploy_package_path.resolve('destructiveChanges.xml'))
            Files.write(undeploy_package_path.resolve("package.xml"), bytearray(self.empty_package_template(version)))

            for output in self._execute(working_dir):
                print output
        finally:
            FileUtils.deleteDirectory(working_dir.toFile())

    def deploy_package(self, zipped_package):
        working_dir, working_dir_path, unzipped_package_path = self._setup_working_dir()

        try:
            self._extract_package(zipped_package, str(unzipped_package_path.toAbsolutePath()))
            for output in self._execute(working_dir):
                print output
        finally:
            FileUtils.deleteDirectory(working_dir.toFile())

    @staticmethod
    def empty_package_template(version):
        template = Template("""<?xml version="1.0" encoding="UTF-8"?>
                               <Package xmlns="http://soap.sforce.com/2006/04/metadata">
                                  <version>$version</version>
                               </Package>
            """)
        return template.substitute(version=version)

    def _deploy_task_template(self):
        template = Template("""
        <sf:deploy username="$username" password="$password" serverurl="$serverurl" deployRoot="deploy_root" ignoreWarnings="true" rollbackOnError="true"/>
        """)
        return template.substitute(username=self.username, password=self.password, serverurl=self.url)

    def _project_xml_template(self, working_dir_path):
        template = Template("""
        <project name="XL Deploy Salesforce Ant task" default="run" basedir="$working_dir" xmlns:sf="antlib:com.salesforce">
            <taskdef resource="com/salesforce/antlib.xml" uri="antlib:com.salesforce">
                <classpath><pathelement location="$salesforce_jar" /></classpath>
            </taskdef>
            <target name="run">
                $sf_task
            </target>
        </project>
        """)
        return template.substitute(working_dir=working_dir_path,
                                   salesforce_jar=self.migration_tool_jar, sf_task=self._deploy_task_template())
