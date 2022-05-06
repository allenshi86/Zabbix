#!/usr/bin/env python
#-*- coding:UTF-8 -*-
#--------AP DISCOVYER 2020-08-07--------

import os
import  json

ap_json = {"data": []}

ap_sets = os.popen("snmpwalk  -v 2c -c hello 172.16.202.x .1.3.6.1.4.1.14823.2.2.1.5.2.1.4 | grep -i ap | awk -F ':' '{print $4}'|awk -F '\"' '{print $2}'")
ap_list = ap_sets.read().splitlines()
ap_sets.close()

for ap in ap_list:
    ap_json["data"].append({"{#AP_NAME}": ap})

push_data = json.dumps(ap_json)

os.system("/bin/zabbix_sender -z ZABBIX_SERVER -p 10051 -s aruba-bj-ac-10 -k ap.discovery -o '%s'"  %push_data)


