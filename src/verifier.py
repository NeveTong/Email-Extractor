###############################################
# Verify the email address over SMTP
###############################################


import csv
import constant
import json
from smtplib import SMTP
from os.path import join
            
def server(people,id2ep_group,id2e_group,verbose=True, maxtry=1):
    def retry():
        if verbose:
            print('[FAIL-{}] {}'.format(maxtry, proxy_ip))
        return server(people, id2ep_group, id2e_group, verbose, maxtry - 1)
        
    if maxtry <= 0:
        return None
        
    try:
        proxy_ip = 'localhost'
        
        for id2eps in id2ep_group:
            smtp=smtplib.SMTP()
            print(smtp.connect('smtp.163.com','25'))
            smtp.login('yiyeqqa@163.com','1996wyyx17')
            smtp.mail('yiyeqqa@163.com')
            for id2ep in id2eps:
                try:            
                    re = smtp.rcpt(id2ep[1][0])
                except Exception as e:
                    print(e)
                    print(id2ep[1][0])
                if re[0] != 250:
                    people[id2ep[0]]['email_list_crawl'].remove(id2ep[1])
                    print(re)
            smtp.quit() 
            
        for id2es in id2e_group:
            smtp=smtplib.SMTP()
            print(smtp.connect('smtp.163.com','25'))
            smtp.login('yiyeqqa@163.com','1996wyyx17')
            smtp.mail('yiyeqqa@163.com')
            for id2e in id2es:
                try:            
                    re = smtp.rcpt(id2e[1])
                except Exception as e:
                    print(e)
                    print(id2e[1])
                if re[0] != 250:
                    people[id2e[0]]['email_list'].remove(id2e[1])
                    print(re)
            smtp.quit()
                
        if verbose:
            print('[OK] {}'.format(proxy_ip))
        
        return people

    except Exception as e:
        print('Exception:')
        print(e)
        return retry()


def split_list(lst):
    return [lst[i:i+90] for i in range(0,len(lst),90)]
    
def verify(fname,people,turnon):
    id2ep_all = []
    id2email_list = []
    for person in people.values():
        for ep in person['email_list_crawl']:
            id2ep_all.append((person['id'],ep))
        for e in person['email_list']:
            id2email_list.append((person['id'],e))
    id2ep_group = split_list(id2ep_all)
    id2e_group = split_list(id2email_list)
#    if turnon == True:
#        people_verified = server(people,id2ep_group,id2e_group)
#    else:
    people_verified = people
    with open(join(constant.RESULT_DIR,'{}.csv'.format(fname[:-4])),'w',newline='\n',encoding='utf-8') as cf:
        infowriter = csv.writer(cf)
        infowriter.writerow(constant.FIELD)
        for person in people_verified.values():
            if len(person['email_list_crawl'])==0:
                best_email = ''
                best_email_score = ''
            else:
                best_email = person['email_list_crawl'][0][0]
                best_email_score = person['email_list_crawl'][0][1]
            infowriter.writerow([person['id'],person['name'],person['affiliation'],';'.join(person['email_list']),best_email,best_email_score,person['h_index'],person['keyword'],person['language'],person['relevance'],person['cag']])
    with open(join(constant.PEOPLE_INFO_DIR,'people_info_verified_{}.json'.format(fname)), 'w') as wf:
        json.dump(people_verified, wf, indent=4)


if __name__ == '__main__':
    print()