import os
import sys
import json

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + os.sep + "shlib")

from shlib.prancer_lib import pr_hello_alert

if __name__ == '__main__':
    if len(sys.argv) > 1 : 
        if len(sys.argv) > 2:
            data =  pr_hello_alert(sys.argv[1], sys.argv[2])
        else:
            data =  pr_hello_alert(sys.argv[1])
        if data:
            print(json.dumps(data, indent=2))
            exit(0)
        else:
            print("Failed to generate alert!....")
    exit(1)
