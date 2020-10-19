#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import xml.etree.ElementTree as ET

tree = ET.parse('config/users.xml')
root = tree.getroot()

users = root.findall('.//user')


def createAuthAlias(user, pwd, user_id):
    try:
        security = AdminConfig.getid('/Security:/')
        alias = ['alias', user]
        user_id = ['userId', user_id]
        pw = ['password', pwd]
        jaasAttrs = [alias, user_id, pw]
        print 'creating user ' + user
        AdminConfig.create('JAASAuthData', security, jaasAttrs)
    except:
        e = sys.exc_info()
        print e


for user in users:
    name = user.find('name').text
    pwd = user.find('pwd').text
    user_id = user.find('userId').text
    createAuthAlias(name, pwd,user_id)

AdminConfig.save()
