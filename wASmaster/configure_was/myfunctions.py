#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
AdminConfig = sys._getframe(1).f_locals['AdminConfig']
AdminApp = sys._getframe(1).f_locals['AdminApp']
AdminControl = sys._getframe(1).f_locals['AdminControl']
AdminTask = sys._getframe(1).f_locals['AdminTask']
Help = sys._getframe(1).f_locals['Help']


def getScopeType(scope_attributes):
    scope_type = ""
    for x in scope_attributes:
        scope_type += x
    return scope_type

def getScopeId(scope_type,x):
    if scope_type == 'ServerNode':
        server_id = AdminConfig.getid('/Node:' + x["Node"] + '/Server:'
                + x["Server"] + '/')
    elif scope_type == 'Node':
        server_id = AdminConfig.getid('/Node:' +  x["Node"] + '/')
    elif scope_type == 'Cluster':
        server_id = AdminConfig.getid('/ServerCluster:' +  x["Cluster"] + '/')
    elif scope_type == 'Cell':
        server_id = AdminConfig.getid('/Cell:' +  x["Cell"] + '/')
    return server_id


def getServerId(node, server):
    get_id = AdminConfig.getid('/Node:' + node + '/Server:' + server
                               + '/')
    return get_id

def getNodeId(node):
    node_id = AdminConfig.getid('/Node:' +  node + '/')
    return node_id

def getCellId():
    cell = AdminControl.getCell()
    cell_id = AdminConfig.getid('/Cell:' + cell + '/')
    return cell_id

def getVariableMapSubentry(
    scope_type,
    x,
    ):
    if scope_type == 'ServerNode':
        varmap = AdminConfig.getid('/Node:' + x["Node"] + '/Server:'
                                   + x["Server"]
                                   + '/VariableMap:/VariableSubstitutionEntry:/'
                                   )
    elif scope_type == 'Node':
        varmap = AdminConfig.getid('/Node:' + x["Node"]
                                   + '/VariableMap:/VariableSubstitutionEntry:/'
                                   )
    elif scope_type == 'Cluster':
        varmap = AdminConfig.getid('/ServerCluster:' + x["Cluster"]
                                   + '/VariableMap:/VariableSubstitutionEntry:/'
                                   )
    elif scope_type == 'Cell':
        varmap = AdminConfig.getid('/Cell:' + x["Cell"]
                                   + '/VariableMap:/VariableSubstitutionEntry:/'
                                   )
    variable_map_split = _splitlines(varmap)
    return variable_map_split


def getVariableMap(
    scope_type,
    x,
    ):
    if scope_type == 'ServerNode':
        varmap = AdminConfig.getid('/Node:' + x["Node"] + '/Server:'
                                   + x["Server"] + '/VariableMap:/')
    elif scope_type == 'Node':
        varmap = AdminConfig.getid('/Node:' + x["Node"] + '/VariableMap:/')
    elif scope_type == 'Cluster':
        varmap = AdminConfig.getid('/ServerCluster:' + x["Cluster"]
                                   + '/VariableMap:/')
    elif scope_type == 'Cell':
        varmap = AdminConfig.getid('/Cell:' + x["Cell"]
                                   + '/VariableMap:/')
    return varmap

def getJMSProviderId(
    scope_type,
    x,
    ):
    if scope_type == 'ServerNode':
        jms_provider_id = AdminConfig.getid('/Node:' + x["Node"] + '/Server:' + x["Server"]
                                + '/JMSProvider:WebSphere MQ JMS Provider/'
                                )
    elif scope_type == 'Node':
        jms_provider_id = AdminConfig.getid('/Node:' + x["Node"]
                                + '/JMSProvider:WebSphere MQ JMS Provider/'
                                )
    elif scope_type == 'Cluster':
        jms_provider_id = AdminConfig.getid('/ServerCluster:' + x["Cluster"]
                                + '/JMSProvider:WebSphere MQ JMS Provider/'
                                )
    return jms_provider_id


def _splitlist(s):
    if s[0] != '[' or s[-1] != ']':
        raise 'Invalid string: %s' % s
    return s[1:-1].split(' ')

def checkIfExists(members,name):
    global flag
    flag = ''
    for item in members:
        propname = AdminConfig.showAttribute(item, 'name')
        if propname == name:
            flag = 'true'
            break
        else:
            flag = 'false'
    return(flag)

def checkIfProviderExists(members):
    global flag
    flag = ''
    for first_item in members:
        for item in members:
            if first_item == item:
                flag = 'true'
                break
            else:
                flag = 'false'                
    return flag
 

def deleteIfLibraryExists(members,name):
    for item in members:
        propname = AdminConfig.showAttribute(item, 'name')
        if propname == name:
            AdminConfig.remove(item)
            AdminConfig.save()
            break

def deleteIfVariableExists(members,name):
    for variable in members:
        propname = AdminConfig.showAttribute(variable, "symbolicName")
        if propname == name:
            AdminConfig.remove(variable)
            AdminConfig.save()
            break

def _splitlines(s):
    rv = [s]
    if '\r' in s:
        rv = s.split('\r\n')
    elif '\n' in s:
        rv = s.split('\n')
    if rv[-1] == '':
        rv = rv[:-1]
    return rv

def getCertificatesStoreScope(
    scope_type,
    x,
    ):
    if scope_type == 'Cell':
        scope = '(cell):' + x["Cell"]
    elif scope_type == 'NodeCell':
        scope = '(cell):' + x["Cell"] + ':(node):' + x["Node"]
    elif scope_type == 'ServerNodeCell':
        scope = '(cell):' + x["Cell"] + ':(node):' + x["Node"] + ':(server):' \
            + x["Server"]
    elif scope_type == 'ClusterCell':
        scope = '(cell):' + x["Cell"] + ':(cluster):' + x["Cluster"]
    return scope

def getJDBCScopeId(
    scope_type,
    x,
    ):
    if scope_type == 'Cluster':
        scope = 'Cluster=' + x["Cluster"]
    elif scope_type == 'Node':
        scope = 'Node=' + x["Node"]
    elif scope_type == 'ServerNode':
        scope = 'Node=' + x["Node"] + ', Server=' + x["Server"]
    return scope
