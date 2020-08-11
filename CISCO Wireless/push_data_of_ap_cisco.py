#!/usr/bin/env python
#-*- coding:utf-8 -*-
#------Push CISCO AP Info To Zabbix.2020-08-11------

import os

prefix_ap_oid = '1.3.6.1.4.1.14179.2.2.1.1.3'
prefix_radio_clients_oid = '1.3.6.1.4.1.14179.2.2.2.1.15'
prefix_channel_oid = '1.3.6.1.4.1.14179.2.2.13.1.3'
ap_names_dict = {}   # key存储AP名字，值存储AP索引
snmpwalk_ap_datas = os.popen("snmpwalk -v 2c -c momo 172.16.201.3 %s" % prefix_ap_oid)


def get_ap_dic_fun(dict):
    for ap_names in snmpwalk_ap_datas.readlines():
        ap_name = ap_names.split('"')[1]
        ap_index = (ap_names.split('=')[0]).split('2.1.1.3')[1].rstrip()
        dict[ap_name] = ap_index

    return dict

def tapper_channel_util(dict_ap):
    for ap_name in dict_ap.keys():
        try:
            snmpwalk_ap_radio0 = os.popen("snmpwalk  -v 2c -c momo 172.16.201.3 %s%s.0" % (prefix_channel_oid, dict_ap[ap_name]))
            snmpwalk_ap_radio1 = os.popen("snmpwalk  -v 2c -c momo 172.16.201.3 %s%s.1" % (prefix_channel_oid, dict_ap[ap_name]))
            channel0_data_source = snmpwalk_ap_radio0.read()
            channel1_data_source = snmpwalk_ap_radio1.read()
            radio0_util_percent = int(channel0_data_source.split(':')[-1])
            radio1_util_percent = int(channel1_data_source.split(':')[-1])
#           print radio0_util_percent
#           print type(radio0_util_percent)
            os.system("/bin/zabbix_sender -z 172.16.7.20 -vv -s office-wlc-bj-t2-11-ac-3 -k uti_radio0.[%s] -o %s" % (ap_name, radio0_util_percent))
            os.system("/bin/zabbix_sender -z 172.16.7.20 -vv -s office-wlc-bj-t2-11-ac-3 -k uti_radio1.[%s] -o %s" % (ap_name, radio1_util_percent))
        except Exception as e:
            print e

def tapper_clients_ap(dict_ap):
    for ap_name in dict_ap.keys():
        radio0_datas = os.popen("snmpwalk -v 2c -c momo 172.16.201.3 %s%s.2" % (prefix_radio_clients_oid, dict_ap[ap_name])).read()
        radio1_datas = os.popen("snmpwalk -v 2c -c momo 172.16.201.3 %s%s.1" % (prefix_radio_clients_oid, dict_ap[ap_name])).read()
        clients_radio0 = int(radio0_datas.split(':')[-1])
        clients_radio1 = int(radio1_datas.split(':')[-1])
        clients_sum = clients_radio0 + clients_radio1
        os.system("/bin/zabbix_sender -z 172.16.7.20 -vv -s office-wlc-bj-t2-11-ac-3 -k clients.radio0.[%s] -o %s" % (ap_name, clients_radio0))
        os.system("/bin/zabbix_sender -z 172.16.7.20 -vv -s office-wlc-bj-t2-11-ac-3 -k clients.radio1.[%s] -o %s" % (ap_name, clients_radio1))
        os.system("/bin/zabbix_sender -z 172.16.7.20 -vv -s office-wlc-bj-t2-11-ac-3 -k clients.[%s] -o %s" %(ap_name,clients_sum))

if __name__ == '__main__':
    get_ap_dic_fun(ap_names_dict)
    snmpwalk_ap_datas.close()
    tapper_channel_util(ap_names_dict)
    tapper_clients_ap(ap_names_dict)
