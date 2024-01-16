import os
import sys
import json
#  Chatgpt suggested imports.
import socket
import threading

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + os.sep + "shlib")

from shlib.prancer_lib import pr_hello_alert
from shlib.prancer_fqdn import gen_fqdn

from shlib.prancer_site import get_site
from shlib.prancer_result import get_result
from shlib.prancer_spider import get_spider
from shlib.prancer_output import get_output

def pr_alert(url, title=None, portscanned="21-80"):

  # Message 1 Content:
  msg_data1 = {
      "uri": url,
      "method": "GET",
      "param": "q",
      "attack": "ports scanned: %s" % portscanned,
      "evidence": title
  } 
 
  if title is None:
      title = "Prancer Python Script Alert: Open ports found."

  # Alert Content:
  alert_data = {
      "alertid": "202",
      "name": title,
      "severity": "Medium",
      "desc": "Open or exposed ports increase the potential attack surface and could leave you vulnerable to compromise.",
      "count": "",
      "solution": "",
      "reference":"https://cwe.mitre.org/data/definitions/1125.html",
      "cweid": "1125",
      "wascid": "15",
      "sourceid": "36977",
      "instances": []
  }

  # Add Messages to alertItem
  alert_data["instances"].append(msg_data1)
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

def scan_port(target_host, port, ports):
    sock = None
    try:
        # Create a socket object
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Set a timeout for the connection attempt
        sock.settimeout(1)
        
        # Attempt to connect to the target host and port
        sock.connect((target_host, port))
        
        # print(f"Port {port} is open")
        ports.append(str(port))
        
    except socket.error:
        pass
    finally:
        # Close the socket
        if sock:
            sock.close()

def port_scan(target_host, start_port, end_port):
    ports = []
    # print(f"Scanning target {target_host} for open ports...\n")
    
    # Create threads for concurrent scanning
    threads = []
    
    for port in range(start_port, end_port + 1):
        thread = threading.Thread(target=scan_port, args=(target_host, port, ports))
        threads.append(thread)
        thread.start()

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

    return ports

if __name__ == '__main__':
    # Set your target host and port range
    # target_host = "example.com"
    target_host = ""
    start_port = 21
    end_port = 80  # You can adjust the port range as needed
    if len(sys.argv) > 1 : 
        target_host = gen_fqdn(sys.argv[1])
        if len(sys.argv) > 2:
            vals = sys.argv[2].split('-')
            start_port = int(vals[0])
            end_port = int(vals[1])
        ports =  port_scan(target_host, start_port, end_port)
        # print(ports)
        # print(type(ports))
        if ports:
            data = pr_alert(sys.argv[1], "Open ports found: %s" % ','.join(ports), '%d-%d' % (start_port, end_port))
            print(json.dumps(data, indent=2))
            exit(0)
        else:
            print("Failed to generate alert!....")
    exit(1)
