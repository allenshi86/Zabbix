#!/usr/bin/env python
#-*- coding:utf-8 -*-
#------ push_wireless_ssid ----------2020-07-30

import os
import json

ssid = ['A-Office',
        'A-Guest',
        'A-Stage',
        'A-Test']
        
ssid_json = {"data": []}

for i in ssid:
    ssid_json["data"].append({"{#SSID}": i})

#tmp = json.dumps(ssid_data, indent=4)
temp = json.dumps(ssid_json) 

os.system("/usr/bin/zabbix_sender -vv -z ZABBIX_SERVER -p 10051 -s HOSTNAME  -k ssid.discovery -o '%s'" %temp)
