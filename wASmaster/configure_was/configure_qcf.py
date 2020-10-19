#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
sys.modules['AdminConfig'] = AdminConfig
sys.modules['AdminControl'] = AdminControl
sys.modules['AdminApp'] = AdminApp
sys.modules['AdminTask'] = AdminTask
sys.modules['Help'] = Help
import myfunctions as fl

import xml.etree.ElementTree as ET
tree = ET.parse('config/qcf.xml')
root = tree.getroot()

scopes = root.findall('.//scope')
connection = root.findall('.//connection')

my_dict = {}


def createqcf(
    jms_provider_id,
    name,
    jndi,
    qmname,
    transport_type,
    host,
    typee,
    port,
    channel,
    ):

    try:
        AdminTask.createWMQConnectionFactory(jms_provider_id, [
            '-type',
            typee,
            '-name',
            name,
            '-jndiName',
            jndi,
            '-qmgrName',
            qmname,
            '-wmqTransportType',
            transport_type,
            '-qmgrSvrconnChannel',
            channel,
            '-qmgrHostname',
            host,
            '-qmgrPortNumber',
            port,
            ])
        print ''
        print 'Creating QCF ' + name + ' with JNDI ' + jndi
    except:
        e = sys.exc_info()
        print e


for con in connection:
    conid = con.find('id').text
    transport_type = con.find('wmqTransportType').text
    channel = con.find('qmgrSvrconnChannel').text
    host = con.find('qmgrHostname').text
    port = con.find('qmgrPortNumber').text
    my_dict[conid] = {
        'wmqTransportType': transport_type,
        'qmgrSvrconnChannel': channel,
        'qmgrHostname': host,
        'qmgrPortNumber': port,
        }

for scope in scopes:
    scope_attributes = scope.attrib
    atributes = scope.findall('.//attributes')
    for atribute in atributes:
        connectionid = atribute.find('connectionId').text
        name = atribute.find('name').text
        jndi = atribute.find('jndi').text
        qmname = atribute.find('qmgrName').text
        typee = atribute.find('type').text
        channel = my_dict[connectionid]['qmgrSvrconnChannel']
        transport_type = my_dict[connectionid]['wmqTransportType']
        host = my_dict[connectionid]['qmgrHostname']
        port = my_dict[connectionid]['qmgrPortNumber']
        scope_type = fl.getScopeType(scope_attributes)
        jms_provider_id = fl.getJMSProviderId(scope_type,
                scope_attributes)
        createqcf(
            jms_provider_id,
            name,
            jndi,
            qmname,
            transport_type,
            host,
            typee,
            port,
            channel,
            )

AdminConfig.save()
