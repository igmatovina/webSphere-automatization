#!/usr/bin/python
# -*- coding: utf-8 -*-

from java.lang import System as jvm
import sys

import xml.etree.ElementTree as ET
tree = ET.parse('config/data_source.xml')
root = tree.getroot()
datasources = root.findall('.//dataSource')
conn = root.findall('.//connection')
import myfunctions as fl

my_dict = {}


def create_datasource(
    provider,
    name,
    jdbc,
    user,
    userxa,
    database,
    server,
    port,
    helper_classname,
    drivertype,
    ):

    jdbc_id = AdminConfig.getid('/JDBCProvider:' + provider + '/')
    try:
        AdminTask.createDatasource(jdbc_id, [
            '-name',
            name,
            '-jndiName',
            jdbc,
            '-dataStoreHelperClassName',
            helper_classname,
            '-componentManagedAuthenticationAlias',
            user,
            '-xaRecoveryAuthAlias',
            userxa,
            '-configureResourceProperties',
            '[[databaseName java.lang.String ' + database
                + '] [driverType ' + drivertype
                + '] [serverName java.lang.String  ' + server
                + '] [portNumber java.lang.Integer ' + port + ']]',
            ])

        print ('Creating datasource ' + name, jdbc)
    except:
        e = sys.exc_info()
        print e

def new_property(
    dsname,
    new_custom_name,
    new_custom_value,
    new_custom_type,
    new_custom_description,
    ):

    datasource_id = AdminConfig.getid('/DataSource:' + dsname + '/')
    property_attribute = AdminConfig.showAttribute(datasource_id,
            'propertySet')
    property_attribute_list = AdminConfig.list('J2EEResourcePropertySet'
            , datasource_id)
    members = fl._splitlines(AdminConfig.list('J2EEResourceProperty',
                             property_attribute_list))
    flag = fl.checkIfExists(members,new_custom_name)
    if flag == 'true':
        config_id = AdminConfig.getid('/DataSource:' + dsname
                + '/J2EEResourcePropertySet:/J2EEResourceProperty:'
                + new_custom_name + '/')
        AdminConfig.modify(config_id, [['name', new_custom_name],
                           ['value', new_custom_value], ['type',
                           new_custom_type], ['description',
                           new_custom_description]])

        print 'Modify property '
        print (new_custom_name, new_custom_value, new_custom_type)
    else:
        name = ['name', new_custom_name]
        value = ['value', new_custom_value]
        typee = ['type', new_custom_type]
        description = ['description', new_custom_description]
        rpAttrs = [name, value, typee, description]
        AdminConfig.create('J2EEResourceProperty', property_attribute,
                           rpAttrs)
        print ('New property' + new_custom_name, new_custom_value,
               new_custom_type)

for con in conn:
    conid = con.find('id').text
    server = con.find('server').text
    port = con.find('port').text
    database = con.find('database').text
    provider = con.find('provider').text
    my_dict[conid] = {
        'server': server,
        'port': port,
        'database': database,
        'provider': provider,
        }

for ds in datasources:
    atributes = ds.findall('.//attributes')
    custom_properties = ds.findall('.//customProperties')
    for atribute in atributes:
        ds_name = atribute.find('name').text
        connection_id = atribute.find('connectionId').text
        jdbc = atribute.find('jdbc').text
        user = atribute.find('user').text
        userxa = atribute.find('userXA').text
        helper_class_name = atribute.find('helperClassName').text
        driver_type = atribute.find('driverType').text
        ds_provider = my_dict[connection_id]['provider']
        ds_database = my_dict[connection_id]['database']
        ds_server = my_dict[connection_id]['server']
        ds_port = my_dict[connection_id]['port']
        create_datasource(
            ds_provider,
            ds_name,
            jdbc,
            user,
            userxa,
            ds_database,
            ds_server,
            ds_port,
            helper_class_name,
            driver_type,
            )
    for customprop in custom_properties:
        try:
            custom_property = customprop.findall('.//customProperty')
        except:
            break;
        for cproperty in custom_property:
            custom_name = cproperty.find('name').text
            custom_value = cproperty.find('value').text
            custom_type = cproperty.find('type').text
            custom_description = cproperty.find('description').text
            new_property(ds_name, custom_name, custom_value,
                        custom_type, custom_description)

AdminConfig.save()
