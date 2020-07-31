#!/usr/bin/env python
#-*- coding:utf-8 -*-
#----get the number of users per ssid----2020-07-30 

import os

num_oid_aruba = '.1.3.6.1.4.1.14823.2.2.1.5.2.1.8.1.2'
#先用ireasoning找到每个ssid的index，即ssid_aruba中的值。
ssid_aruba = {'A-Office': '.7.77.111.106.105.45.81.65',
              'A-Guest': '.8.73.110.45.71.117.101.115.116',
              'A-Stage': '.9.77.79.77.79.45.84.69.83.84',
              'A-QA': '.7.77.111.106.105.45.81.65',
              'M-TEST': '.9.77.79.77.79.45.84.69.83.84',
              'A-Test': '.9.77.111.106.105.45.84.101.115.116'}



ssid_cisco = {'A-Office': '.1.3.6.1.4.1.14179.2.1.1.1.38.2',
              'A-Guest': '.1.3.6.1.4.1.14179.2.1.1.1.38.3',
              'A-Coldbackup-Prod': '.1.3.6.1.4.1.14179.2.1.1.1.38.16',
              'A-Test': '.1.3.6.1.4.1.14179.2.1.1.1.38.17',
              'A-Stage': '.1.3.6.1.4.1.14179.2.1.1.1.38.20',


others_cisco = {'Audit': '.1.3.6.1.4.1.14179.2.1.1.1.38.7',
                'A-Office-2.4G': '.1.3.6.1.4.1.14179.2.1.1.1.38.10',
                'A-TC': '.1.3.6.1.4.1.14179.2.1.1.1.38.12',  
                'A-Stage-2.4G': '.1.3.6.1.4.1.14179.2.1.1.1.38.23',
                'A-test-javaApi': '.1.3.6.1.4.1.14179.2.1.1.1.38.30',
                'A-Ipv6-Test-V2': '.1.3.6.1.4.1.14179.2.1.1.1.38.28',
                'momo_wifi5': '.1.3.6.1.4.1.14179.2.1.1.1.38.18'}

              
def snmpdata():
    for i in ssid_aruba.keys():
        f1 = os.popen("snmpwalk -v 2c -c momo ARUBA_IP %s%s | awk -F ':' '{print $4}'" %(num_oid_aruba,ssid_aruba[i]))
        num_a = f1.read().splitlines()
        num1 = int(num_a[0])
        f1.close()
        if i in ssid_cisco.keys():
            f2 = os.popen("snmpwalk -v 2c -c momo CISCO_IP %s | awk -F ':' '{print $4}'" %ssid_cisco[i])
            num_c = f2.read().splitlines()
            num2 = int(num_c[0])
            num_all = num1 + num2
            f2.close()
            os.system("/usr/bin/zabbix_sender -vv -z ZABBIX_SERVER -p 10051 -s wlc-ssid-monitor -k count.[%s] -o %s" %(i,num_all))
        else:
            os.system("/usr/bin/zabbix_sender -vv -z ZABBIX_SERVER -p 10051 -s wlc-ssid-monitor -k count.[%s] -o %s" %(i,num1))

def snmpdata1():    
    for i in others_cisco.keys():
        f = os.popen("snmpwalk -v 2c -c momo CISCO_IP %s | awk -F ':' '{print $4}'" %others_cisco[i])
        num_list = f.read().splitlines()
        num = int(num_list[0])
        f.close()
        os.system("/usr/bin/zabbix_sender -vv -z ZABBIX_SERVER -p 10051 -s wlc-ssid-monitor -k count.[%s] -o %s" %(i,num))
        


if __name__ == '__main__':    
    snmpdata()
    snmpdata1()
