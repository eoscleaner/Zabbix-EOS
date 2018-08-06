============
# Zabbix-EOS

**Installation**

1. Import the eos template to zabbix and link it to the eos node host.
2. Copy the scripts to a path. like /etc/zabbix.
3. Copy eos zabbix agent configuration to /etc/zabbix-agent/zabbix_agentd.d and restart zabbix agent.

Note:
- Zabbix sender uses zabbix agent configuration to send the metrics, please check the hostname is set in the zabbix agent config /etc/zabbix/zabbix_agentd.conf, by default the hostname may be commented out.

The following metrics are collected, and then sent by zabbix sender.

**INFO Stats**
- info.head_block_time
- info.last_irreversible_block_num 
- info.head_block_num 

**DBSIZE Stats**
- db_size.size 
- db_size.used_bytes 
- db_size.free_bytes 
