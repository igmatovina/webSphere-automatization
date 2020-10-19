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
tree = ET.parse('config/jvm_settings.xml')
root = tree.getroot()


def setJVMProperties(server_name, node_name, properties):
    for prop in properties:
        initial_heap_size = prop.find('initialHeapSize').text
        max_heap_size = prop.find('maxHeapSize').text
        debug_mode = prop.find('debugMode').text
        debug_args = prop.find('debugArgs').text
        try:
            AdminServerManagement.setJVMProperties(
                node_name,
                server_name,
                "",
                "",
                initial_heap_size,
                max_heap_size,
                debug_mode,
                debug_args,
                )
        except:
            e = sys.exc_info()
            print e

def addCustomProperties(server_name, node_name, custom_properties):
    for custom_properties in custom_properties:
        custom_property = custom_properties.findall('.//customProperty')
        for prop in custom_property:
            property_name = prop.find('propertyName').text
            property_value = prop.find('propertyValue').text
            try:
                AdminTask.setJVMSystemProperties([
                    '-serverName',
                    server_name,
                    '-nodeName',
                    node_name,
                    '-propertyName',
                    property_name,
                    '-propertyValue',
                    property_value,
                    ])
            except:
                e = sys.exc_info()
                print e



def setlogoutlogerr(log_parameters, get_id):
    for log in log_parameters:
        errror_rollovertype = log.find('errorRolloverType').text
        error_roleoversize = log.find('errorRolloverSize').text
        rollover_type = log.find('rolloverType').text
        rollover_size = log.find('rolloverSize').text
        try:
            log_out = AdminConfig.showAttribute(get_id,
                    'outputStreamRedirect')
        except:
            e = sys.exc_info()
            print e
        try:
            AdminConfig.modify(log_out, [['rolloverType', rollover_type],
                            ['rolloverSize', rollover_size]])
        except:
            e = sys.exc_info()
            print e
        try:
            log_err = AdminConfig.showAttribute(get_id,
                    'errorStreamRedirect')
        except:
            e = sys.exc_info()
            print e
        try:
            AdminConfig.modify(log_err, [['rolloverType',
                            errror_rollovertype], ['rolloverSize',
                            error_roleoversize]])
        except:
            e = sys.exc_info()
            print e


def processexe(process_execution_parameters, get_id):
    for exe in process_execution_parameters:
        umask = exe.find('umask').text
        process_def = AdminConfig.list('JavaProcessDef', get_id)
        AdminConfig.modify(process_def, [['execution', [['umask',
                           umask]]]])


def getServerList(scope_type, scope_attributes):
    if scope_type == 'NodeAgent':
        server_list = AdminTask.listServers('[-serverType NODE_AGENT]'
                ).splitlines()
    elif scope_type == 'DeploymentManager':

        server_list = \
            AdminTask.listServers('[-serverType DEPLOYMENT_MANAGER]'
                                  ).splitlines()
    elif scope_type == 'Cluster':
        cluster = fl.getScopeId(scope_type, scope_attributes)
        server_list = fl._splitlist(AdminConfig.showAttribute(cluster,
                                    'members'))
    else:
        return 0
    return server_list


def customizeJVM(
    server_name,
    node_name,
    member_id,
    properties,
    processe_execution_parameters,
    log_parameters,
    custom_properties,
    ):

    setJVMProperties(server_name, node_name, properties)
    processexe(processe_execution_parameters, member_id)
    setlogoutlogerr(log_parameters, member_id)
    addCustomProperties(server_name, node_name, custom_properties)


def callForCustomize(
    server_list,
    properties,
    processe_execution_parameters,
    log_parameters,
    scope_attributes,
    scope_type,
    custom_propertiesm
    ):

    if scope_type == 'NodeAgent' or scope_type == 'DeploymentManager':
        for member in server_list:
            node_name = member.split('/')[3]
            server_name = scope_attributes[scope_type]
            customizeJVM(
                server_name,
                node_name,
                member,
                properties,
                processe_execution_parameters,
                log_parameters,
                custom_properties,
                )
    elif scope_type == 'Cluster':

        for member in server_list:
            server_name = AdminConfig.showAttribute(member, 'memberName'
                    )
            node_name = AdminConfig.showAttribute(member, 'nodeName')
            server_id = fl.getServerId(node_name, server_name)
            customizeJVM(
                server_name,
                node_name,
                server_id,
                properties,
                processe_execution_parameters,
                log_parameters,
                custom_properties,
                )
    elif scope_type == 'ServerNode':

        node_name = scope_attributes['Node']
        server_name = scope_attributes['Server']
        server_id = fl.getScopeId(scope_type, scope_attributes)
        customizeJVM(
            server_name,
            node_name,
            server_id,
            properties,
            processe_execution_parameters,
            log_parameters,
            custom_properties,
            )


scopes = root.findall('.//scope')
for scope in scopes:
    scope_attributes = scope.attrib
    scope_type = fl.getScopeType(scope_attributes)
    configuration = scope.findall('.//configuration')
    log_parameters = scope.findall('.//logParameters')
    custom_properties = scope.findall('.//customProperties')
    processe_execution_parameters = \
        scope.findall('.//processExecutionParameters')
    server_list = getServerList(scope_type, scope_attributes)
    callForCustomize(
        server_list,
        configuration,
        processe_execution_parameters,
        log_parameters,
        scope_attributes,
        scope_type,
        custom_properties,
        )

AdminConfig.save()
