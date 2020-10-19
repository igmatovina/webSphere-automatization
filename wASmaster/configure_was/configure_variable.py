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
tree = ET.parse('config/variable.xml')
root = tree.getroot()
scopes = root.findall('.//scope')


def createvar(
    variable_map_id,
    name,
    value,
    variable_sub_entry_id,
    ):

    fl.deleteIfVariableExists(variable_sub_entry_id, name)
    nameattr1 = ['symbolicName', name]
    if(value):
        valattr1 = ['value', value]
    else:
        value = ""
        valattr1 = ['value', value]
    attr1 = [nameattr1, valattr1]
    attrs1 = [attr1]
    entries1 = ['entries', attrs1]
    print 'Creating variable ' + name + ' ' + value
    AdminConfig.modify(variable_map_id, [entries1])


for scope in scopes:
    scope_attributes = scope.attrib
    vars = scope.findall('.//attribute')
    for var in vars:
        name = var.find('name').text
        value = var.find('value').text
        scope_type = fl.getScopeType(scope_attributes)
        variable_map_id = fl.getVariableMap(scope_type,
                scope_attributes)
        variable_sub_entry_id = fl.getVariableMapSubentry(scope_type,
                scope_attributes)
        createvar(variable_map_id, name, value, variable_sub_entry_id)

AdminConfig.save()
