#!/usr/bin/env python

import datetime
from sys import exit

import requests
f = open("/etc/zabbix/zabbix-eos.log", "a")

class EOS(object):
    """main script class"""
    def __init__(self, host="127.0.0.1", port=8888):
        self.eos_host = host
        self.eos_port = port
        self.__conn = None
        self.__metrics = []


    def add_metrics(self, k, v):
        """add each metric to the metrics list"""
        dict_metrics = {}
        dict_metrics['key'] = k
        dict_metrics['value'] = v
        self.__metrics.append(dict_metrics)

    def get_data(self, d, f):
        """use filter to get data"""
        data={}
        for k in f:
            karray= k.split('.')
            v = d
            for i in karray:
                if i.isdecimal():
                    i = int(i)
                v = v[i]
            data[k] = v
        return data


    def print_metrics(self):
        """print out all metrics"""
        metrics = self.__metrics
        for metric in metrics:
            zabbix_item_key = str(metric['key'])
            zabbix_item_value = str(metric['value'])
            print('- ' + zabbix_item_key + ' ' + zabbix_item_value)

    def get_info(self):
        info_filter = ["head_block_num", "last_irreversible_block_num", "head_block_time"]
        info_path = 'http://'+self.eos_host+ ":" + str(self.eos_port) + '/v1/chain/get_info'
        now_timestamp = datetime.datetime.now().timestamp()
        try:
            info = requests.get(info_path, timeout=3)
        except Exception as e:
            f.write(e)
            return
        if info.status_code == 200:
            data = self.get_data(info.json(), info_filter)
            data["head_block_time"] = datetime.datetime.strptime(data["head_block_time"],"%Y-%m-%dT%H:%M:%S.%f").timestamp()
            data["delay_time"] = abs(now_timestamp - data["head_block_time"]) * 1000
            for k, v in data.items():
                self.add_metrics("info."+k,v)
        else:
            f.write(dbsize.status_code + " " + dbsize.text)

    def get_db_size(self):
        dbsize_filter = ["free_bytes", "used_bytes", "size"]
        dbsize_path = 'http://'+self.eos_host+ ":" + str(self.eos_port) + '/v1/db_size/get'

        try:
            dbsize = requests.get(dbsize_path, timeout=3)
        except Exception as e:
            f.write(e)
            return
        if dbsize.status_code == 200:
            data = self.get_data(dbsize.json(), dbsize_filter)
            for k, v in data.items():
                self.add_metrics("db_size."+k,v)
        else:
            f.write(dbsize.status_code + " " + dbsize.text)

    def close(self):
        """close connection to eos"""
        if self.__conn is not None:
            self.__conn.close()

if __name__ == '__main__':
    #eos = EOS("api.eoscleaner.com", 80)
    eos = EOS()
    eos.get_info()
    eos.get_db_size()
    eos.print_metrics()
