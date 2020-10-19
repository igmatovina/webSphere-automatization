#!/usr/bin/python
# -*- coding: utf-8 -*-

from java.lang import System as jvm
import sys
sys.modules['AdminConfig'] = AdminConfig
sys.modules['AdminControl'] = AdminControl
sys.modules['AdminApp'] = AdminApp
sys.modules['AdminTask'] = AdminTask
sys.modules['Help'] = Help
import myfunctions as fl


items = fl._splitlines(AdminConfig.list('SharedLibrary'))
for item in items:
    propname = AdminConfig.showAttribute(item, 'name')
    print propname

  

        

