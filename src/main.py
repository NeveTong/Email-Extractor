import os
import constant
import prep
import verifier
import emails


if __name__ == '__main__':
    
    fnames = os.listdir(constant.RAW_DIR)
    for fname in fnames:    
        people = prep.rearrange_info(fname)
        for person in people.values():
            print(person)
            email_prob_list = emails.get_emails(person)
            people[person['id']]['email_list_crawl'] = email_prob_list
            
        print('start verify')
        verifier.verify(fname,people,False)
        print('end verify')