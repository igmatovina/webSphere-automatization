#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import xml.etree.ElementTree as ET
tree = ET.parse('config/security_ldap.xml')
root = tree.getroot()
properties = root.findall('.//properties')


def create_security_ldap(
    ldap_host,
    ldap_port,
    ldap_type,
    base_dn,
    bind_dn,
    bind_pwd,
    search_timeout,
    reuse_conn,
    ssl_enabled,
    auto_gen_srv_id,
    prim_admin_id,
    ignore_case,
    verify_reg,
    enable_global_security,
    active_user_registry,
    app_security_enabled,
    ):

    AdminTask.configureAdminLDAPUserRegistry([
        '-ldapHost',
        ldap_host,
        '-ldapPort',
        ldap_port,
        '-ldapServerType',
        ldap_type,
        '-baseDN',
        base_dn,
        '-bindDN',
        bind_dn,
        '-bindPassword',
        bind_pwd,
        '-searchTimeout',
        search_timeout,
        '-reuseConnection',
        reuse_conn,
        '-sslEnabled',
        ssl_enabled,
        '-autoGenerateServerId',
        auto_gen_srv_id,
        '-primaryAdminId',
        prim_admin_id,
        '-ignoreCase',
        ignore_case,
        '-verifyRegistry',
        verify_reg,
        ])
    AdminTask.setAdminActiveSecuritySettings([
        '-enableGlobalSecurity',
        enable_global_security,
        '-activeUserRegistry',
        active_user_registry,
        '-appSecurityEnabled',
        app_security_enabled,
        ])


def map_groups(
    role_name,
    ad_group,
    ldap_host,
    ldap_port,
    ):

    try:
        AdminTask.mapGroupsToAdminRole('[-roleName ' + role_name
                + ' -accessids [group:' + ldap_host + ':' + ldap_port
                + '/' + ad_group + '] -groupids [' + ad_group + '@'
                + ldap_host + ':' + ldap_port + ']]')
    except:
        e = sys.exc_info()
        print e

for prop in properties:
    ldap_host = prop.find('ldapHost').text
    ldap_port = prop.find('ldapPort').text
    ldap_type = prop.find('ldapServerType').text
    base_dn = prop.find('baseDN').text
    bind_dn = prop.find('bindDN').text
    bind_pwd = prop.find('bindPassword').text
    search_timeout = prop.find('searchTimeout').text
    reuse_conn = prop.find('reuseConnection').text
    ssl_enabled = prop.find('sslEnabled').text
    auto_gen_srv_id = prop.find('autoGenerateServerId').text
    prim_admin_id = prop.find('primaryAdminId').text
    ignore_case = prop.find('ignoreCase').text
    verify_reg = prop.find('verifyRegistry').text
    enable_global_security = prop.find('enableGlobalSecurity').text
    active_user_registry = prop.find('activeUserRegistry').text
    app_security_enabled = prop.find('appSecurityEnabled').text
    create_security_ldap(
        ldap_host,
        ldap_port,
        ldap_type,
        base_dn,
        bind_dn,
        bind_pwd,
        search_timeout,
        reuse_conn,
        ssl_enabled,
        auto_gen_srv_id,
        prim_admin_id,
        ignore_case,
        verify_reg,
        enable_global_security,
        active_user_registry,
        app_security_enabled,
        )
    group_role = prop.findall('.//groupRoles')
    for group in group_role:
        ad_group = group.find('adGroup').text
        role_names = prop.findall('.//roleName')
        for role in role_names:
            role_name = role.text
            map_groups(role_name, ad_group, ldap_host, ldap_port)

AdminConfig.save()
