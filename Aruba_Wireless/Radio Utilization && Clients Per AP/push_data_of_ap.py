#!/usr/bin/env python
#-*- coding:utf-8 -*-
#------ push ap radio utilization and number of clients to zabbix.------


import os

prefix_ap_oid = '1.3.6.1.4.1.14823.2.2.1.5.2.1.4.1.3'
prefix_radio_clients_oid = '1.3.6.1.4.1.14823.2.2.1.5.2.1.5.1.7'
prefix_channel_oid = '1.3.6.1.4.1.14823.2.2.1.5.2.1.5.1.6'
prefix_double5G_oid = '1.3.6.1.4.1.14823.2.2.1.5.2.1.4.1.48'
ap_names_dict = {}   # key存储AP名字，值存储AP索引
double_5G = []       #开启双5G的AP列表.开启双5G的AP,radio0客户端数量准确，radio1的客户端数量需要除以2.
snmpwalk_ap_datas = os.popen("snmpwalk -v 2c -c momo 172.16.202.10 %s" %prefix_ap_oid)
ap_disabled_list = ['AP-01', 'T2-F19-AP04', 'T1-F16-AP30']

def  get_ap_dic_fun(dict):
    for ap_names in snmpwalk_ap_datas.readlines():
        ap_name = ap_names.split('"')[1]
        ap_index = (ap_names.split('=')[0]).split('1.4.1.3')[1].rstrip()
        dict[ap_name] = ap_index
    return dict

def remove_disabled_ap():
    for ap_name in ap_disabled_list:
        ap_names_dict.pop(ap_name)

def tapper_channel_util(dict_ap):
    for ap_name in dict_ap.keys():
        try:
            snmpwalk_ap_radio0 = os.popen("snmpwalk  -v 2c -c hello 172.16.202.10 %s%s.2" % (prefix_channel_oid, dict_ap[ap_name]))
            snmpwalk_ap_radio1 = os.popen("snmpwalk  -v 2c -c hello 172.16.202.10 %s%s.1" % (prefix_channel_oid, dict_ap[ap_name]))
            channel0_data_source = snmpwalk_ap_radio0.read()
            channel1_data_source = snmpwalk_ap_radio1.read()
            if ap_name != 'AP-01' and ap_name != 'T2-F19-AP04' and ap_name != 'T1-F16-AP30':
                radio0_util_percent = int(channel0_data_source.split(':')[-1])
                radio1_util_percent = int(channel1_data_source.split(':')[-1])
                os.system("/bin/zabbix_sender -z 172.16.7.20 -vv -s aruba-bj-ac-10 -k uti_radio0.[%s] -o %s" %(ap_name, radio0_util_percent))
                os.system("/bin/zabbix_sender -z 172.16.7.20 -vv -s aruba-bj-ac-10 -k uti_radio1.[%s] -o %s" %(ap_name, radio1_util_percent))
        except Exception as e:
            print e

def check_double_5G(dict_ap):
    for ap_name in dict_ap.keys():
        datas = os.popen("snmpwalk -v 2c -c hello 172.16.202.10 %s%s" % (prefix_double5G_oid, dict_ap[ap_name])).read()
        value = int(datas.split(':')[-1])
        if value == 1:       #值为1，已启用双5G.值为0，未启用.
            double_5G.append(ap_name)

def tapper_clients_ap(dict_ap):
    for ap_name in dict_ap.keys():
        radio0_datas = os.popen("snmpwalk -v 2c -c hello 172.16.202.10 %s%s.2" % (prefix_radio_clients_oid, dict_ap[ap_name])).read()
        radio1_datas = os.popen("snmpwalk -v 2c -c hello 172.16.202.10 %s%s.1" % (prefix_radio_clients_oid, dict_ap[ap_name])).read()
        clients_radio1 = int(radio1_datas.split(':')[-1])
        if ap_name in double_5G:
            clients_radio0 = int(radio0_datas.split(':')[-1]) / 2
        else:
            clients_radio0 = int(radio0_datas.split(':')[-1])
     
        clients_sum = clients_radio0 + clients_radio1
        os.system("/bin/zabbix_sender -z 172.16.7.20 -vv -s office-aruba-bj-t2-11-ac-10 -k clients.radio0.[%s] -o %s" % (ap_name, clients_radio0))
        os.system("/bin/zabbix_sender -z 172.16.7.20 -vv -s office-aruba-bj-t2-11-ac-10 -k clients.radio1.[%s] -o %s" % (ap_name, clients_radio1))
        os.system("/bin/zabbix_sender -z 172.16.7.20 -vv -s aruba-bj-ac-10 -k clients.[%s] -o %s" %(ap_name,clients_sum))

if __name__ == '__main__':
    get_ap_dic_fun(ap_names_dict)
    snmpwalk_ap_datas.close()
    remove_disabled_ap()
    tapper_channel_util(ap_names_dict)
    check_double_5G(ap_names_dict)
    tapper_clients_ap(ap_names_dict)
    
    
    
