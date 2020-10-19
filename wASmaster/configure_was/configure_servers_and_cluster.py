#!/usr/bin/python
# -*- coding: utf-8 -*-
# exit()

from java.lang import System as jvm
import sys
sys.modules['AdminConfig'] = AdminConfig
sys.modules['AdminControl'] = AdminControl
sys.modules['AdminApp'] = AdminApp
sys.modules['AdminTask'] = AdminTask
sys.modules['Help'] = Help
import myfunctions as fl

import xml.etree.ElementTree as ET
try:
    tree = ET.parse('config/new_cluster.xml')
    root = tree.getroot()
    scopes = root.findall('.//scope')
except:
    e = sys.exc_info()
    sys.exit(e)



def createserver(node, server_name):
    AdminTask.createApplicationServer(node, ['-name', server_name])


def converttocluster(server_scope, cluster_name):
    AdminConfig.convertToCluster(server_scope, cluster_name)


def createclustermember(cluster, node, server_name):
    AdminConfig.createClusterMember(cluster, node, [['memberName',
                                    server_name]])


for scope in scopes:
    scope_attributes = scope.attrib
    cluster_scope_type = fl.getScopeType(scope_attributes)
    cluster_name = scope.attrib['Cluster']
    print cluster_name
    members = scope.findall('.//member')
    for member in members:
        member_attributes = member.attrib
        node_name = member.attrib['Node']
        server_name = member.attrib['Server']
        scope_type = fl.getScopeType(member_attributes)
        if AdminClusterManagement.checkIfClusterExists(cluster_name) \
            == 'false':
            createserver(node_name, server_name)
            server_id = fl.getScopeId(scope_type, member_attributes)
            converttocluster(server_id, cluster_name)
        elif AdminClusterManagement.checkIfClusterMemberExists(cluster_name,
                server_name) == 'false':

            clusterid = fl.getScopeId(cluster_scope_type,
                    scope_attributes)
            node_id = fl.getNodeId(node_name)
            createclustermember(clusterid, node_id, server_name)
        else:
            print ''
            print 'Cluster ' + cluster_name + ' and cluster member ' \
                + server_name + ' already exist'
            print ''

AdminConfig.save()
