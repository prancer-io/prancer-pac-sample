import sys
from prancer_template import gen_config_file

if __name__ == '__main__':
    if len(sys.argv) > 3 : 
       infile = sys.argv[1]
       ofile = sys.argv[2]
       template = '%s.json' % sys.argv[3]
       data = {}
       with open(infile) as f:
         for line in f:
            vals=line.strip().split('=', 1)
            data[vals[0]] = vals[1]
       status = gen_config_file(ofile, template, data)
       exit(0 if status else 1)
    exit(1)
