import os
import sys
import requests
import json

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + os.sep + "shlib")

from shlib.prancer_site import get_site
from shlib.prancer_result import get_result
from shlib.prancer_spider import get_spider
from shlib.prancer_output import get_output


def check_livesite(url):
  if not url:
    return False
  data = None
  try:
    resp = requests.get(url)
    # print('Response Code:', resp.status_code)

    # Check if the response code is 200
    if resp.status_code >= 200 and resp.status_code <= 299:
      title="Requested site %s is live. Status code %d" % (url, resp.status_code)
      data = pr_alert(url, title)
  except Exception as ex:
    print("Excepion for URL: %s as exception: %s" % (url, ex))
  return data


def pr_alert(url, title=None):
  # Message 1 Content:
  msg_data = {
      "uri": url,
      "method": "GET",
      "param": "",
      "attack": "</font><scrIpt>alert(1);</scRipt><font>",
      "evidence": "</font><scrIpt>alert(1);</scRipt><font>"
  } 
 
  if title is None:
      title = "Prancer Python Script Alert"

  # Alert Content:
  alert_data = {
      "alertid": "200",
      "name": title,
      "severity": "Low",
      "desc": "The returned status code is between 200 and 226 implying the site is live and healthy.",
      "count": "1",
      "solution": "No action needed unless the target URL is not supposed to be live, in which case it's advisable to take the website down until it's ready to go live.",
      "reference":"https://developer.mozilla.org/en-US/docs/Web/HTTP/Status",
      "cweid": "199",
      "wascid": "",
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
    data =  check_livesite(sys.argv[1])
    if data:   
      print(json.dumps(data, indent=2))
      exit(0)
    else:
      print("The site %s may not be live." % sys.argv[1])
      exit(1)
  print("Usage: python livesite.py <targetURL>")
  exit(1)

