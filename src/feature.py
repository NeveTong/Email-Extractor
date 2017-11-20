########################################
# Construct features for email address
########################################

def get_name_dict(name):
    name = name.lower().replace('.', '').replace('-', '')
    parts = name.split(' ')
    parts = [p for p in parts if p]
    return {
        'first': parts[0],
        'last': parts[-1],
        'other': parts[1:-1],
        'parts': parts
    }


def get_context_features(namedict, snippet):
    n_last = namedict['last']
    n_first = namedict['first']

    s_title = snippet['title'].lower()
    s_content = snippet['content'].lower()

    valid_length = 2
    f_ln_in_title = int(n_last in s_title)
    f_fn_in_title = int(len(n_first) > valid_length and n_first in s_title)
    f_ln_in_content = int(n_last in s_content)
    f_fn_in_content = int(len(n_first) > valid_length and n_first in s_content)

    return [
        snippet['pos'],
        f_ln_in_title,
        f_fn_in_title,
        f_ln_in_content,
        f_fn_in_content,
    ]


def get_email_features(namedict, email):

    n_last = namedict['last']
    n_first = namedict['first']
    n_parts = namedict['parts']
    try:    
        e_prefix, e_domain = email.split('@')
    except:
        _, e_prefix, e_domain = email.split('@')
    len_e_prefix = float(len(e_prefix))

    f_contain_n_last = float(n_last in e_prefix) * float(len(n_last)) / (len_e_prefix + 0.1)
    if n_last in e_prefix:
        e_prefix.replace(n_last,'')
        
    f_contain_n_first = float(n_first in e_prefix) * float(len(n_first)) / (len_e_prefix + 0.1)
    if n_first in e_prefix:
        e_prefix.replace(n_first,'')

    f_contain_n_initials = 0
    pos = 0
    for part in n_parts:
        initial = part[0]
        pos = e_prefix.find(initial, pos)
        f_contain_n_initials += int(pos > -1)
    f_contain_n_initials /= (len_e_prefix + 0.1)

    return [
        f_contain_n_last,
        f_contain_n_first,
        f_contain_n_initials,
    ]


def get_snippet_X(person, snippet):
    X = []
    namedict = get_name_dict(person['name'])
    cfeature = get_context_features(namedict, snippet)
    emails = snippet['emails']
    for email in emails:
        efeature = get_email_features(namedict, email)
        X.append(cfeature + efeature)
    return X
