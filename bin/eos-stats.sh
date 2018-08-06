#!/bin/bash

get_EOS_metrics(){
python3 /etc/zabbix/zabbix-eos.py
}

# Send the results to zabbix server by using zabbix sender
result=$(get_EOS_metrics | /usr/bin/zabbix_sender -c /etc/zabbix/zabbix_agentd.conf -i - 2>&1)
response=$(echo "$result" | awk -F ';' '$1 ~ /^info/ && match($1,/[0-9].*$/) {sum+=substr($1,RSTART,RLENGTH)} END {print sum}')
if [ -n "$response" ]; then
        echo "$response"
else
        echo "$result"
fi
