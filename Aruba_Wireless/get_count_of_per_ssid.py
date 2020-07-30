#!/usr/bin/env python
#-*- coding:utf-8 -*-
#----get the number of users per ssid----2020-07-30 

import os

num_oid_aruba = '.1.3.6.1.4.1.14823.2.2.1.5.2.1.8.1.2'
#先用ireasoning找到每个ssid的index，即ssid_aruba中的值。
ssid_aruba = {'A-Office': '.7.77.111.106.105.45.81.65',
              'A-Guest': '.8.73.110.45.71.117.101.115.116',
              'A-TEST': '.9.77.79.77.79.45.84.69.83.84',
              'A-Test': '.9.77.111.106.105.45.84.101.115.116'}



def snmpdata():
    for i in ssid_aruba.keys():
        numlist = os.popen("snmpwalk -v 2c -c readcommunity WLC_IP %s%s | awk -F ':' '{print $4}'" %(num_oid_aruba,ssid_aruba[i]))
        number = numlist.read().splitlines()
        os.system("/usr/bin/zabbix_sender -vv -z ZABBIX_SERVER -p 10051 -s HOSTNAME -k count.[%s] -o %s" %(i,int(number[0])))

if __name__ == '__main__':    
    snmpdata()
