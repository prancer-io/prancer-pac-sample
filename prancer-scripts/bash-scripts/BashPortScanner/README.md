# Bash Port Scanner

Simple bash script that uses Netcat to actively scan a target host for a given port range.

## Overview

- The `check_port()` function will use Netcat to check for open ports in the specified range and add found ports to an Array.
- If open ports are found, the scan will add the array of ports to the JSON template and output the results in a format that can be read by the Prancer platform.
- If no open ports are found, the output will state this without generating a JSON report.

### Usage

- To use this script simply call the script file followed by the target URL/IP and the desired port range.
- The amount of ports in a given range will determine how long the scan takes to run.
- All found Open Ports on the target will be listed in the `Title` field of the JSON output.

IP Address: `./BashPortScanner.sh 192.168.x.x`
             Default Port Range chosen as 22-443
            `./BashPortScanner.sh 192.168.x.x 22-1024`
             Port Range chosen as given by input parameter 22-1024

URL: `./BashPortScanner.sh target.url`
      Default Port Range chosen as 22-443
     `./BashPortScanner.sh target.url 22-1024`
      Port Range chosen as given by input parameter 22-1024
