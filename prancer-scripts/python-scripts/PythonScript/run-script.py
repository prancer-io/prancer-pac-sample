import os
import sys
import json

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + os.sep + "shlib")

from shlib.prancer_site import get_site
from shlib.prancer_result import get_result
from shlib.prancer_spider import get_spider
from shlib.prancer_output import get_output

def pr_alert(url, title=None):

  # Message 1 Content:
  msg_data1 = {
      "uri": url + "/bodgeit/search.jsp?q=%3C%2Ffont%3E%3CscrIpt%3Ealert%281%29%3B%3C%2FscRipt%3E%3Cfont%3E",
      "method": "GET",
      "param": "q",
      "attack": "</font><scrIpt>alert(1);</scRipt><font>",
      "evidence": "</font><scrIpt>alert(1);</scRipt><font>"
  } 
 
  # Message 2 Content:
  msg_data2 = {
      "uri": url + "/bodgeit/contact.jsp",
      "method": "GET",
      "param": "q",
      "attack": "</font><scrIpt>alert(2);</scRipt><font>",
      "evidence": "</font><scrIpt>alert(2);</scRipt><font>"
  } 

  if title is None:
      title = "Prancer Python Script Alert"

  # Alert Content:
  alert_data = {
      "alertid": "40012",
      "name": title,
      "severity": "Medium",
      "desc": "<p>Cross-site Scripting (XSS) is an attack technique that involves ...</p>",
      "count": "",
      "solution": "<p>Phase: Architecture and Design</p><p>Use a vetted library or framework that does not ...</p>",
      "reference":"<p>http://projects.webappsec.org/Cross-Site-Scripting</p><p>http://cwe.mitre.org/data/definitions/79.html</p>",
      "cweid": "532",
      "wascid": "34",
      "sourceid": "36977",
      "instances": []
  }

  # Add Messages to alertItem
  alert_data["instances"].append(msg_data1)
  alert_data["instances"].append(msg_data2)
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
    if len(sys.argv) > 1 : 
        if len(sys.argv) > 2:
            data =  pr_alert(sys.argv[1], sys.argv[2])
        else:
            data =  pr_alert(sys.argv[1])
        print(json.dumps(data, indent=2))
        exit(0)
    exit(1)

