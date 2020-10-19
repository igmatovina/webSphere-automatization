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
tree = ET.parse('config/queue.xml')
root = tree.getroot()

scopes = root.findall('.//scope')


def createqueue(
    scope_id,
    name,
    jndi,
    mqname,
    ):

    try:
        AdminTask.createWMQQueue(scope_id, [
            '-name',
            name,
            '-jndiName',
            jndi,
            '-queueName',
            mqname,
            ])
        print ''
        print ('creating Queue ' + name, jndi)
    except:
        e = sys.exc_info()
        print e


for scope in scopes:
    scope_attributes = scope.attrib
    queues = scope.findall('.//queue')
    for q in queues:
        ime = q.find('name').text
        jndi = q.find('jndi').text
        mqname = q.find('queueName').text
        scope_type = fl.getScopeType(scope_attributes)
        scope_id = fl.getScopeId(scope_type, scope_attributes)
        createqueue(scope_id, ime, jndi, mqname)

AdminConfig.save()
