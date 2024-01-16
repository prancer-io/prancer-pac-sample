#!/bin/bash

# Source the prancer-lib shell script to call all pr-* library functions.
source shlib/prancer-lib.sh

# generate a hello alert, pass the target like: "https://brokencrystals.com/"
# output=`pr_hello_world_alert "$1"`
#
# # Capture the URL passed as an argument
url="$1"

# Append "/debug" to the URL
modified_url="${url}/users/v1/_debug"
# Display the modified URL
# echo "Fetching data from $modified_url"

# Use curl to fetch data from the modified URL and store the HTTP response code in a variable
code=$(curl --write-out '%{http_code}' --silent --output /dev/null "$modified_url")
response=$(curl --silent "$modified_url")

# escape double quotes - temp replacing with single quotes
r=`echo $response | sed -e "s/\"/\'/g"`


# Check if the response code is 200
if [ $code -eq 200 ]; then
 title="debug endpoint found"
 severity="High"
 desc="Debug mode in APIs can potentially expose sensitive information, such as system configuration, sensitive data, and stack traces. This can greatly increase the risk of unauthorized access, data breaches, and other security incidents. Debug mode should be disabled in production environments to ensure the confidentiality and integrity of the data."
 alertid="213"
 solution="To mitigate this vulnerability, ensure that debug mode is disabled in the API. If it is necessary for debugging purposes, implement proper access controls to limit who can access the debug information."
 cweid=532
 wascid=34
 reference="https://www.owasp.org/index.php/Top_10_2017-A7-Insufficient_Logging_and_Monitoring"

 msg_out1_file=`pr_get_message_json "$url" "" "" "$modified_url" "$r"`
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
else
 echo "Request failed with status code $response"
 exit 1
fi

exit 0


