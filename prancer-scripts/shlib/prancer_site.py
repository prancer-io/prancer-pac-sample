import sys
import urllib.parse
from prancer_template import gen_config_file

def prepare_data(tgt):
    result = urllib.parse.urlparse(tgt)
    ssl = True if result.scheme == 'https' else False
    if ':' in result.netloc:
        parts = result.netloc.split(':')
        host = parts[0]
        port = parts[1]
    else:
        host = result.netloc
        port = 443 if result.scheme == 'https' else 80
    data = {
        'target': tgt,
        'host': host,
        'port': port,
        'ssl': ssl
    }
    return data

def get_site(fname, url, name='site'):
    data = prepare_data(url)
    template = '%s.json' % name
    sitedata = gen_config_file(fname, template, data)
    return sitedata

if __name__ == '__main__':
    if len(sys.argv) > 3 : 
       exit(0 if get_site(sys.argv[1], sys.argv[2], sys.argv[3]) else 1)
    exit(1)
