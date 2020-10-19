#!/usr/bin/python
# -*- coding: utf-8 -*-

from java.lang import System as jvm
import sys
sys.modules['AdminConfig'] = AdminConfig
sys.modules['AdminControl'] = AdminControl
sys.modules['AdminApp'] = AdminApp
sys.modules['AdminTask'] = AdminTask
sys.modules['Help'] = Help
import myfunctions as fl

import xml.etree.ElementTree as ET
tree = ET.parse('config/shared_lib.xml')
root = tree.getroot()

scopes = root.findall('.//scope')

def createlib(
    scope_id,
    name,
    isolated,
    class_path,
    ):
    print ('Creating shared library ', name)
    print(scope_id)
    
    AdminConfig.create('Library', scope_id, [['name', name],
                       ['isolatedClassLoader', isolated], ['classPath',
                       class_path]])

for scope in scopes:
    scope_attributes = scope.attrib
    slibs = scope.findall('.//settings')
    for slib in slibs:
        name = slib.find('name').text
        isolated = slib.find('isolatedClassLoader').text
        class_path = slib.find('classPath').text
        scope_type = fl.getScopeType(scope_attributes)
        scope_id = fl.getScopeId(scope_type, scope_attributes)
        members = fl._splitlines(AdminConfig.list('Library'))
        fl.deleteIfLibraryExists(members, name)
        createlib(scope_id, name, isolated, class_path)

AdminConfig.save()
