# -*- coding: utf-8 -*-


import json

proxies = []

with open('ips.txt', 'r') as rf:
#with open('ips_wait.txt', 'r') as rf:
#with open('ips_test.txt', 'r') as rf:    
    lines = rf.readlines()
    for line in lines:
        proxies.append(line.strip('\n'))  

print(len(proxies))
print(60/len(proxies))

proxies_info = {}
i = 0   

for proxy in proxies:
#    i += 1
    proxies_info[proxy] = [i,0] # total, success

with open('ip_info.json', 'w') as wf:
    json.dump(proxies_info, wf, indent=4)
    
with open('ip_info.json') as f:
    info = json.load(f)
    print(info)
    