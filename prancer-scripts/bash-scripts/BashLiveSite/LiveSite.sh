#!/bin/bash

# Source the prancer-lib shell script to call all pr-* library functions.
source shlib/prancer-lib.sh

# Check if a URL is provided
if [ "$#" -ne 1 ]; then
  echo "Usage: $0 <target_url>"
  exit 1
fi

# The target URL
URL=$1

# Using curl to get the HTTP response code
RESPONSE=$(curl -o /dev/null -s -w "%{http_code}\n" "$URL")

# Check if the response code is 200
if [ "$RESPONSE" -ge 200 ] && [ "$RESPONSE" -le 299 ]; then
 title="Requested site $URL is live. Status code $RESPONSE"
 severity="Low"
 desc="The returned status code is between 200 and 226 implying the site is live and healthy."
 alertid="200"
 solution="No action needed unless the target URL is not supposed to be live, in which case it's advisable to take the website down until it's ready to go live."
 cweid="199"
 wascid=
 reference="https://developer.mozilla.org/en-US/docs/Web/HTTP/Status"

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
 echo "The site $URL may not be live. Status code $RESPONSE"
 exit 1
fi

exit 0


