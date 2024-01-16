import os
import sys
import requests
import json
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + os.sep + "shlib")

from shlib.prancer_site import get_site
from shlib.prancer_result import get_result
from shlib.prancer_spider import get_spider
from shlib.prancer_output import get_output

def check_debug(url, path=None):
  if not url:
    return False

  data = None

  # Append "/_debug" to the URL
  if path:
    murl = '%s/%s/_debug' % (url, path)
  else:
    murl = '%s/_debug' % (url)
  
  vals = murl.split("://", 1)
  if len(vals) > 1:
    murl = vals[0] + "://" + vals[1].replace('//', '/')
  else:
    murl = murl.replace('//', '/')
  # print(murl)
   
  try:
    resp = requests.get(murl)
    # print('Response Code:', resp.status_code)
    # print('Response:', resp)
    # print('Response text:', resp.text)

    # Check if the response code is 200
    if resp.status_code == 200:
      # title="Requested site %s has a debug URL: '%s' . Status code %d" % (url, murl, resp.status_code)
      title="debug endpoint found"
      data = pr_alert(url, murl, title, resp.text)
  except Exception as ex:
    print("Excepion for URL: %s as exception: %s" % (murl, ex))
  return data


def pr_alert(url, murl=None, title=None, resp=None):

  # Message 1 Content:
  msg_data = {
      "uri": url,
      "method": "GET",
      "param": "",
      "attack": murl,
      "evidence": resp
  } 
 
  if title is None:
      title="debug endpoint found"

  # Alert Content:
  alert_data = {
      "alertid": "213",
      "name": title,
      "severity": "High",
      "desc": "Debug mode in APIs can potentially expose sensitive information, such as system configuration, sensitive data, and stack traces. This can greatly increase the risk of unauthorized access, data breaches, and other security incidents. Debug mode should be disabled in production environments to ensure the confidentiality and integrity of the data.",
      "count": "1",
      "solution": "To mitigate this vulnerability, ensure that debug mode is disabled in the API. If it is necessary for debugging purposes, implement proper access controls to limit who can access the debug information.",
      "reference":"https://www.owasp.org/index.php/Top_10_2017-A7-Insufficient_Logging_and_Monitoring",
      "cweid": "532",
      "wascid": "34",
      "sourceid": "36977",
      "instances": []
  }

  # Add Messages to alertItem
  alert_data["instances"].append(msg_data)
  alert_data["count"] = "%d" % len(alert_data["instances"])
  site_data = get_site(None, url)
  site_data['alerts'].append(alert_data)
  result_data = get_result(None)
  result_data["site"].append(site_data)

  spider_data = get_spider(None, 'spider', url)
  output = get_output(None)
  output["Result"] = result_data
  output["Spider"] = spider_data
  return output


if __name__ == '__main__':
  # Check if a URL is provided
  if len(sys.argv) > 1 : 
    if len(sys.argv) > 2 : 
      data =  check_debug(sys.argv[1], sys.argv[2])
    else:
      data =  check_debug(sys.argv[1], "users/v1")
    if data:   
      print(json.dumps(data, indent=2))
      exit(0)
    else:
      print("The site %s does not have debug URI." % sys.argv[1])
      exit(1)
  print("Usage: python vampi.py <targetURL> [debugpath]")
  exit(1)

