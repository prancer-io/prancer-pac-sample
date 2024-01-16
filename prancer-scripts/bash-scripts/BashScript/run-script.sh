#!/bin/bash

# Source the prancer-lib shell script to call all pr-* library functions.
source shlib/prancer-lib.sh

# Message 1 Content:
uri="${1}/bodgeit/search.jsp?q=%3C%2Ffont%3E%3CscrIpt%3Ealert%281%29%3B%3C%2FscRipt%3E%3Cfont%3E"
method="GET"
param="q"
attack="</font><scrIpt>alert(1);</scRipt><font>"
evidence="</font><scrIpt>alert(1);</scRipt><font>"

# Generate a json using the message parameters for Message 1
msg_out1_file=`pr_get_message_json "$uri" "$method" "$param" "$attack" "$evidence"` 
# echo "MSG1: $msg_out1_file"

# Message 2 Content:
uri="${1}/bodgeit/contact.jsp"
method="POST"
param="comments"
attack="</td><scrIpt>alert(1);</scRipt><td>"
evidence="</td><scrIpt>alert(1);</scRipt><td>"

# Generate a json using the message parameters for Message 2
msg_out2_file=`pr_get_message_json "$uri" "$method" "$param" "$attack" "$evidence"` 
# echo "MSG2: $msg_out2_file"

# Alert Content:
alertid="40012"
title="Cross Site Scripting (Reflected)"
severity="Medium"
desc="<p>Cross-site Scripting (XSS) is an attack technique that involves ...</p>"
count="2"
solution="<p>Phase: Architecture and Design</p><p>Use a vetted library or framework that does not ...</p>"
reference="<p>http://projects.webappsec.org/Cross-Site-Scripting</p><p>http://cwe.mitre.org/data/definitions/79.html</p>"
cweid="79"
wascid="8"
sourceid="36977"

al_out_file=`pr_get_alert_json "$alertid" "$title" "$severity" "$desc" "$count" "$solution" "$reference" "$cweid" "$wascid" "$sourceid"`

# Add Messages to alertItem
pr_update_json "$al_out_file" "$msg_out1_file" "instances"
pr_update_json "$al_out_file" "$msg_out2_file" "instances"

# Get an temporary site json file
site_out_file=`pr_site_file $1`
pr_update_json "$site_out_file" "$al_out_file" "alerts"
# echo "SITE: $site_out_file"

# Get an temporary result json file
result_out_file=`pr_result_file $1` 
pr_update_json "$result_out_file" "$site_out_file" "site"
# echo "result: $result_out_file"

# Get an temporary spider json file
spider_out_file=`pr_spider_file $1`
# echo "spider: $spider_out_file"

# Build the alert output json file
out_file=`pr_output_file`
# echo "OUTPUT: $out_file"
pr_update_json "$out_file" "$result_out_file" "Result"
pr_update_json "$out_file" "$spider_out_file" "Spider"
if [ $? -ne 0 ];  then
  echo "Failed to generate alert!...."
else
  # echo "$out_file"
  cat $out_file
fi

exit 0
