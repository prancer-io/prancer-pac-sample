import sys
from urllib.parse import urlparse

def gen_fqdn(urlname):
    fqdn = urlname
    if urlname:
        val = urlparse(urlname)
        # print(val)
        if val and val.scheme and val.netloc:
            if ':' in val.netloc:
                fqdn = val.netloc.split(':', 1)[0]
            else:
                fqdn = val.netloc
        else:
            if ':' in urlname:
                fqdn = urlname.split(':', 1)[0]
            else:
                fqdn = urlname
    return fqdn
       

if __name__ == '__main__':
    if len(sys.argv) > 1 : 
       urlname = sys.argv[1]
       fqdn = gen_fqdn(urlname)
       print(fqdn)
       exit(0)
    exit(1)
