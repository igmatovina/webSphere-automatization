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
tree = ET.parse('config/active_specification.xml')
root = tree.getroot()

scopes = root.findall('.//scope')
connections = root.findall('.//connection')
my_dict = {}


def createacspec(
    scope,
    name,
    jndi,
    destination_jndi,
    qmname,
    transport_type,
    channel,
    host_name,
    port,
    destination_type,
    ):

    try:
        AdminTask.createWMQActivationSpec(scope, [
            '-name',
            name,
            '-jndiName',
            jndi,
            '-destinationJndiName',
            destination_jndi,
            '-destinationType',
            destination_type,
            '-qmgrName',
            qmname,
            '-wmqTransportType',
            transport_type,
            '-qmgrSvrconnChannel',
            channel,
            '-qmgrHostname',
            host_name,
            '-qmgrPortNumber',
            port,
            ])
        print ''
        print ('Creating activation specification ' + name, jndi)
    except:
        e = sys.exc_info()
        print e

for con in connections:
    connection_id = con.find('id').text
    qmgr_name = con.find('qmgrName').text
    transport_type = con.find('wmqTransportType').text
    channel = con.find('qmgrSvrconnChannel').text
    host_name = con.find('qmgrHostname').text
    port = con.find('qmgrPortNumber').text
    my_dict[connection_id] = {
        'qmgr_name': qmgr_name,
        'transport_type': transport_type,
        'channel': channel,
        'host_name': host_name,
        'port': port,
        }

for scope in scopes:
    scope_attributes = scope.attrib
    scope_type = fl.getScopeType(scope_attributes)
    scope_id = fl.getScopeId(scope_type, scope_attributes)
    atributes = scope.findall('.//activationAttributes')
    for atribute in atributes:
        connection_id = atribute.find('connectionId').text
        name = atribute.find('name').text
        jndi = atribute.find('jndi').text
        destination_jndi = atribute.find('destinationJndi').text
        destination_type = atribute.find('destinationType').text
        qmgr_name = my_dict[connection_id]['qmgr_name']
        transport_type = my_dict[connection_id]['transport_type']
        channel = my_dict[connection_id]['channel']
        host_name = my_dict[connection_id]['host_name']
        port = my_dict[connection_id]['port']
        createacspec(
            scope_id,
            name,
            jndi,
            destination_jndi,
            qmgr_name,
            transport_type,
            channel,
            host_name,
            port,
            destination_type,
            )

AdminConfig.save()
