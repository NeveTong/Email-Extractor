#####################################################
# Parse the result page and extract email addresses
#####################################################

import bs4
import util


@util.cache('json')
def parse(gpage):

    def parse_snippet(snippet):
        try:
            title = ' '.join(snippet.h3.a.strings)
            content = ''.join(snippet.find('span', class_='st').strings).replace('\n','')
            
            return {
                'title': title,
                'content': content
            }
        except Exception:
            return None
            
    if not gpage:
        raise Exception
    soup = bs4.BeautifulSoup(gpage, 'html.parser')  
    snippets = soup.find_all('div', class_='g')
    snippets = [parse_snippet(s) for s in snippets]
    snippets = [s for s in snippets if s]
    nsnippets = len(snippets)
    for i in range(nsnippets):
        snippets[i]['pos'] = i + 1
    return snippets


def filt_email(snippets):

    def efilter(snippet):
        import re
        emails = []
        rough_pattern = re.compile('[A-Za-z0-9-\._]+(@| at | \[at\] |\[at\]| \(at\) |\(at\)| @ | \-at\- |<at>)(([a-z0-9\-]+)(\.| dot | \. | \[dot\] |\(dot\)|<dot>))+([a-z]+)')
        rough_match = rough_pattern.finditer(snippet['content'])
        for rm in rough_match:
            pattern = re.compile('(([A-Za-z0-9-_]+)(\.| dot | \. )?)+(@| at | \[at\] |\[at\]| \(at\) |\(at\)| @ | \-at\- |<at>)(([a-z0-9\-]+)(\.| dot | \. | \[dot\] |\(dot\)|<dot>))+([a-z]+)')
            match = pattern.finditer(rm.group())
            for m in match:
                emails.append(m.group().lower().replace(' dot ', '.').replace('(dot)', '.').replace(' at ', '@').replace('[at]', '@').replace('(at)', '@').replace('(@)', '@').replace(' [dot] ', '.').replace('<dot>', '.').replace('<at>', '@').replace('--@--', '@').replace('-at-', '@').replace(' ', ''))
        snippet['emails'] = emails
        return snippet

    snippets = [efilter(s) for s in snippets]
    snippets = [s for s in snippets if s['emails']]
    return snippets


if __name__ == '__main__':
    with open('5486beb0dabfaed7b5fa2bce.html', encoding='utf-8') as f:
        gpage = f.read()
    items = parse(gpage)
    print(items)
    print(filt_email(items))
