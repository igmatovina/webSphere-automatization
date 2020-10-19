#!/usr/bin/python
# -*- coding: utf-8 -*-

from java.lang import System as jvm
import sys
import myfunctions as fl

import xml.etree.ElementTree as ET
tree = ET.parse('config/signer_certificate.xml')
root = tree.getroot()

scopes = root.findall('.//scope')


def retriveSigneFromPort(
    host,
    port,
    key_store_name,
    certificate_alias,
    key_store_scope,
    ):

    try:
        AdminTask.retrieveSignerFromPort([
            '-host',
            host,
            '-port',
            port,
            '-keyStoreName',
            key_store_name,
            '-certificateAlias',
            certificate_alias,
            '-keyStoreScope',
            key_store_scope,
            ])
        print ''
        print ('Retrive Singer ' + key_store_name, certificate_alias
               + ' From host ' + host + ':' + port)
    except:
        e = sys.exc_info()
        print e


for scope in scopes:
    scope_attributes = scope.attrib
    connections = scope.findall('.//connection')
    for conn in connections:
        host = conn.find('host').text
        port = conn.find('port').text
        key_store_name = conn.find('keyStoreName').text
        certificate_alias = conn.find('certificateAlias').text
        scope_type = fl.getScopeType(scope_attributes)
        scope_id = fl.getCertificatesStoreScope(scope_type,
                scope_attributes)
        retriveSigneFromPort(host, port, key_store_name,
                             certificate_alias, scope_id)

AdminConfig.save()
