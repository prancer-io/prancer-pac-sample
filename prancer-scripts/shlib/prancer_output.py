import sys
from prancer_template import gen_config_file

def get_output(fname, name='output'):
    template = '%s.json' % name
    output = gen_config_file(fname, template, {})
    return output

if __name__ == '__main__':
    if len(sys.argv) > 2 : 
       exit(0 if get_output(sys.argv[1], sys.argv[2]) else 1)
    exit(1)
