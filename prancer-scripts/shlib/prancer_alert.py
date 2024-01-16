import sys
import urllib.parse
import datetime
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
    dt = datetime.datetime.now().strftime('%a, %d %b %Y %H:%M:%S')
    data = {
        'dt': dt,
        'target': tgt,
        'host': host,
        'port': port,
    }
    return data

if __name__ == '__main__':
    if len(sys.argv) > 3 : 
       fname = sys.argv[1]
       data = prepare_data(sys.argv[2])
       template = '%s.json' % sys.argv[3]
       status = gen_config_file(fname, template, data)
       exit(0 if status else 1)
    exit(1)
