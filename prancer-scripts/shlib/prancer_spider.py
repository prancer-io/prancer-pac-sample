import sys
import json
from prancer_template import gen_config_file

def get_spider(fname, name='spider', spiderUrl=None):
    template = '%s.json' % name
    data = {}
    spider_data = gen_config_file(fname, template, data)
    if spiderUrl:
        if spider_data and 'allUrls' in spider_data :
            spider_data['allUrls'].append(spiderUrl)
    return spider_data

if __name__ == '__main__':
    if len(sys.argv) > 2 : 
       if len(sys.argv) > 3 : 
           data = get_spider(sys.argv[1], sys.argv[2], sys.argv[3])
           with open(sys.argv[1], 'w') as f:
               f.write(json.dumps(data, indent=2))
       else:
           data = get_spider(sys.argv[1], sys.argv[2])
       exit(0 if data else 1)
    exit(1)
