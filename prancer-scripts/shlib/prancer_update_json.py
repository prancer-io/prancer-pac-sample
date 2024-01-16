import sys
import json

if __name__ == '__main__':
    if len(sys.argv) > 3 : 
       infile = sys.argv[1]
       ofile = sys.argv[2]
       field = sys.argv[3]
       f = open(infile)
       indata = json.loads(f.read())
       f.close()
       f = open(ofile)
       odata = json.loads(f.read())
       f.close()
       if field in indata:
           if isinstance(indata[field], list):
               indata[field].append(odata)
           else:
               indata[field] = odata
       else:
           indata[field] = odata
       
       f = open(infile, 'w')
       f.write(json.dumps(indata, indent=2))
       f.close()
       exit(0)
    exit(1)
