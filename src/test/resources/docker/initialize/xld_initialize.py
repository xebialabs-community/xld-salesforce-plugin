#
# Copyright 2018 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

import os

from java.io import File, FileInputStream, FileOutputStream
from java.util.zip import ZipEntry, ZipOutputStream
from jarray import zeros

def zipdir(basedir, archivename):
    assert os.path.isdir(basedir)
    fos = FileOutputStream(archivename)
    zos = ZipOutputStream(fos)
    add_folder(zos, basedir, basedir)
    zos.close()
    return archivename

def add_folder(zos, folder_name, base_folder_name):
    f = File(folder_name)
    if not f.exists():
        return
    if f.isDirectory():
        for f2 in f.listFiles():
            add_folder(zos, f2.absolutePath, base_folder_name)
        return
    entry_name = folder_name[len(base_folder_name) + 1:len(folder_name)]
    ze = ZipEntry(entry_name)
    zos.putNextEntry(ze)
    input_stream = FileInputStream(folder_name)
    buffer = zeros(1024, 'b')
    rlen = input_stream.read(buffer)
    while (rlen > 0):
        zos.write(buffer, 0, rlen)
        rlen = input_stream.read(buffer)
    input_stream.close()
    zos.closeEntry()

result = zipdir("/data/build/resources/test/docker/initialize/cis", "/tmp/cis.zip")
repository.importCisAndWait("/tmp/cis.zip")


try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser

cp = ConfigParser()
cp.read("/keys/sfdc-credentials.conf")

USERNAME=cp.get('sfdc', 'username')
PASSWORD=cp.get('sfdc', 'password')

sfdcOrg = repository.read('Infrastructure/sfdc')
sfdcOrg.username = USERNAME
sfdcOrg.password = PASSWORD
repository.update(sfdcOrg)

print "Updated SFDC credentials"


