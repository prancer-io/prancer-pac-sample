#!/bin/bash

# Source the prancer-lib shell script to call all pr-* library functions.
source shlib/prancer-lib.sh

# Checks for correct usage/syntax
if [ "$#" -lt 1 ]; then
  echo "Usage: $0 <Target URL/IP> [Port Range]"
  echo "Default Port Range: 22-443"
  exit 1
fi

# Assigned command line arguments
fqdn=`python3 shlib/prancer_fqdn.py $1`
# echo $fqdn
TARGET="$fqdn"

PORT_RANGE="22-443"
if [ "$#" -gt 1 ]; then
  PORT_RANGE="$2"
fi

# Setting the array name
OPEN_PORTS=()

#Function for netcat scan
check_port() {
  if nc -z -w 1 $1 $2; then
     # Add the open port to the array
     OPEN_PORTS+=($2)
  fi
}

# Splitting the port range into 'start' and 'end'
IFS="-" read START_PORT END_PORT <<< "$PORT_RANGE"

# Scanning each port in the range
for ((port=START_PORT; port<=END_PORT; port++)); do
  check_port $TARGET $port
done

# Check if any open ports were found
if [ ${#OPEN_PORTS[@]} -ne 0 ]; then
# echo "Open ports on $TARGET found: ${OPEN_PORTS[*]}"
  OPEN_PORTS_FOUND=true
     title="Open ports found on $TARGET found: ${OPEN_PORTS[*]}"
     severity="High"
     desc="Open or exposed ports increase the potential attack surface and could leave you vulnerable to compromise."
     alertid="202"
     solution=""
     cweid=1125
     wascid=15
     reference="https://cwe.mitre.org/data/definitions/1125.html"

     msg_out1_file=`pr_get_message_json "$TARGET" "" "" "$modified_url" "$r"`
    # cat msg_out1_file
     al_out_file=`pr_get_alert_json "$alertid" "$title" "$severity" "$desc" "1" "$solution" "$reference" "$cweid" "$wascid" ""`
 
    pr_update_json "$al_out_file" "$msg_out1_file" "instances"

  # Get an temporary site json file
    site_out_file=`pr_site_file $1`
    pr_update_json "$site_out_file" "$al_out_file" "alerts"
  # echo "SITE: $site_out_file"
  # Get an temporary result json file
    result_out_file=`pr_result_file $1`
    pr_update_json "$result_out_file" "$site_out_file" "site"
  # echo "result: $result_out_file"
  # Get an temporary spider json file
  # spider_out_file=`pr_spider_file $1`
  # echo "spider: $spider_out_file"
  # Build the alert output json file
    out_file=`pr_output_file`
  # echo "OUTPUT: $out_file"
    pr_update_json "$out_file" "$result_out_file" "Result"
  # pr_update_json "$out_file" "$spider_out_file" "Spider"
# print_and_write "$out_file" "$site_out_file" "site"

# Check the output
  if [ $? -ne 0 ]; then
  echo "Failed to generate alert!...."
  else
  cat $out_file
  fi
  # Handle the case when no ports are found
  else
  echo "No open ports found on $TARGET"
exit 1
fi

exit 0
