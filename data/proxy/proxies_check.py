# -*- coding: utf-8 -*-


import json

    
#The following statements can be used to filter out usable proxies according to # of total & success
#Usable -> ips.txt  unusable -> ips_wait.txt 

with open('ip_info.json') as f:
    info = json.load(f)
    print(info)
    
with open('ips.txt','w') as ips, open('ips_wait.txt','w') as ipsw:
    proxies_info_checked = {}
    for pair in info:
        if info.get(pair)[1] > 0:
#        if info.get(pair)[1] == info.get(pair)[0]:
#        if info.get(pair)[1] > info.get(pair)[0] - 10:    
            proxies_info_checked.update({pair:info.get(pair)})
            ips.write(pair+'\n')
        else:
            ipsw.write(pair+'\n')
        
with open('ip_info.json', 'w') as wf:
    json.dump(proxies_info_checked, wf, indent=4)
    
print("\n")
print(proxies_info_checked)
print(len(proxies_info_checked))
print(60/len(proxies_info_checked))