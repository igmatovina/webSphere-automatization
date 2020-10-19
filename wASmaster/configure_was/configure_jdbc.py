#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

import xml.etree.ElementTree as ET
tree = ET.parse('config/jdbc.xml')
root = tree.getroot()
import myfunctions as fl

scopes = root.findall('.//scope')


def createjdbc(
    scope_name,
    name,
    description,
    classpath,
    provider_type,
    database_type,
    implementation_type,
    classname,
    nativepath,
    ):

    print 'creating JDBC ' + name + ' on scope ' + scope_name
    AdminTask.createJDBCProvider([
        '-scope',
        scope_name,
        '-databaseType',
        database_type,
        '-providerType',
        provider_type,
        '-implementationType',
        implementation_type,
        '-implementationClassName',
        classname,
        '-name',
        name,
        '-description',
        description,
        '-classpath',
        classpath,
        '-nativePath',
        nativepath,
        ])

for scope in scopes:
    scope_attributes = scope.attrib
    jdbc = scope.findall('.//jdbc')
    for jdb in jdbc:
        name = jdb.find('name').text
        description = jdb.find('description').text
        classpath = jdb.find('classpath').text
        provider_type = jdb.find('providerType').text
        database_type = jdb.find('databaseType').text
        implementation_type = jdb.find('implementationType').text
        classname = jdb.find('implementationClassName').text
        nativepath = jdb.find('nativePath').text
        scope_type = fl.getScopeType(scope_attributes)
        scope_id = fl.getJDBCScopeId(scope_type, scope_attributes)
        members = fl._splitlines(AdminConfig.list('JDBCProvider'))
        flag = fl.checkIfExists(members,name)
        if flag == 'true':
            print 'jdbc ' + name + ' on scope ' +scope_id+ ' already exists'
        else:
            createjdbc(
                scope_id,
                name,
                description,
                classpath,
                provider_type,
                database_type,
                implementation_type,
                classname,
                nativepath,
                )

AdminConfig.save()

