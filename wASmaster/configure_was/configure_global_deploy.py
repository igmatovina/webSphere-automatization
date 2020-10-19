#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import xml.etree.ElementTree as ET
import myfunctions as fl

tree = ET.parse('config/global_deploy.xml')
root = tree.getroot()

properti = root.findall('.//properties')


def globdep(mondirdep_enable, mondirdep_interval, mondirdep_path):
    cell_id = fl.getCellId()
    attribute = AdminConfig.showAttribute(cell_id,
                                    'monitoredDirectoryDeployment')
    AdminConfig.modify(attribute, [['enabled', mondirdep_enable],
                       ['pollingInterval', mondirdep_interval],
                       ['monitoredDirectory', mondirdep_path]])
    print ''
    print 'Global deployment settings' + attribute
    print 'MonitoredDirectoryDeployment ' + mondirdep_enable
    print 'PollingInterval ' + mondirdep_interval
    print 'MonitoredDirectory ' + mondirdep_path
    print ''


for prop in properti:
    mondirdep_enable = prop.find('monitoredDirectoryDeployment').text
    mondirdep_interval = prop.find('pollingInterval').text
    mondirdep_path = prop.find('monitoredDirectory').text
    globdep(mondirdep_enable, mondirdep_interval, mondirdep_path)

AdminConfig.save()
