import sys
import datetime
import time
import uuid
from prancer_template import gen_config_file

def get_result(fname, name='result'):
    dt = datetime.datetime.now().strftime('%a, %d %b %Y %H:%M:%S')
    ep = int(time.time())
    uid = str(uuid.uuid4()).replace('-', '')
    data = {
        'dt': dt,
        'epoch': ep,
        'id': uid,
    }
    template = '%s.json' % name
    result_data = gen_config_file(fname, template, data)
    return result_data


if __name__ == '__main__':
    if len(sys.argv) > 2 :
       exit(0 if get_result(sys.argv[1], sys.argv[2]) else 1)
    exit(1)
