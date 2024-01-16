# apppend key=value to a file
# If file exists will append, else will create a new file. 
pr_append_file() {
  fname=$1
  ky=$2
  v=`echo $3 | sed -e 's/\n//g'`
  if [ -f $fname ]; then
    echo "${ky}=${v}" >> $fname
  else
    echo "${ky}=${v}" > $fname
  fi
}

# Generate a tmp file with default extension as .json
# pass the extension like txt, xml for the type of the file.
pr_get_file() {
  ext='json'
  if [ "$#" -gt 0 ]; then
    ext=$1
  fi
  fname=$(mktemp)
  echo "${fname}.${ext}"
}

# Create the result to be raised.
pr_result_file() {
  result_file=`pr_get_file json`
  python3 shlib/prancer_result.py $result_file result
  echo $result_file
}

# Create the spider to be raised.
pr_spider_file() {
  spider_file=`pr_get_file json`
  python3 shlib/prancer_spider.py $spider_file spider "$1"
  echo $spider_file
}

# Create the alert to be raised.
pr_output_file() {
  out_file=`pr_get_file json`
  python3 shlib/prancer_output.py $out_file output
  echo $out_file
}

# Alert is for a site, so the alert could be for multiple sites, so for each site multiple instances to be created. 
pr_site_file() {
  tgt=$1
  site_out_file=`pr_get_file json`
  python3 shlib/prancer_site.py $site_out_file $tgt site
  echo $site_out_file
}

# Generate a message json with parameters
pr_get_message_json() {
  # Get an temporary input text file
  msg_inp1_file=`pr_get_file txt`

  # Append name=value to this input text file
  pr_append_file "$msg_inp1_file" "uri" "$1"
  pr_append_file "$msg_inp1_file" "method" "$2"
  pr_append_file "$msg_inp1_file" "param" "$3"
  pr_append_file "$msg_inp1_file" "attack" "$4"
  pr_append_file "$msg_inp1_file" "evidence" "$5"

  # Get an temporary output json file
  msg_out1_file=`pr_get_file json`
  # echo "MSG1: $msg_out1_file"

  # Generate a json using the message 
  python3 shlib/prancer_gen_json.py "$msg_inp1_file" "$msg_out1_file" message
  
  echo "$msg_out1_file"
}

# Generate a alert json with parameters
pr_get_alert_json() {
  # Get an temporary input text file
  al_inp_file=`pr_get_file txt`

  # Append name=value to this input text file
  pr_append_file "$al_inp_file" "alertid" "${1}"
  pr_append_file "$al_inp_file" "name" "${2}"
  pr_append_file "$al_inp_file" "severity" "${3}"
  pr_append_file "$al_inp_file" "desc" "${4}"
  pr_append_file "$al_inp_file" "count" "${5}"
  pr_append_file "$al_inp_file" "solution" "${6}"
  pr_append_file "$al_inp_file" "reference" "${7}"
  pr_append_file "$al_inp_file" "cweid" "${8}"
  pr_append_file "$al_inp_file" "wascid" "${9}"
  pr_append_file "$al_inp_file" "sourceid" "${10}"

  # Get an temporary output json file
  al_out_file=`pr_get_file json`
  # echo "ALERT: $al_out_file"

  # Generate a json using the message 
  python3 shlib/prancer_gen_json.py "$al_inp_file" "$al_out_file" alert

  echo "$al_out_file"
}


# Update json file.
pr_update_json() {
  # Add Messages to alertItem
  python3 shlib/prancer_update_json.py "$1" "$2" "$3"
}

pr_hello_world_alert(){
  # Message 1 Content:
  uri="${1}/search?q=%3C%2Ffont%3E%3CscrIpt%3Ealert%281%29%3B%3C%2FscRipt%3E%3Cfont%3E"
  method="GET"
  param="q"
  attack="</font><scrIpt>alert(1);</scRipt><font>"
  evidence="</font><scrIpt>alert(1);</scRipt><font>"

  # Generate a json using the message parameters for Message 1
  msg_out1_file=`pr_get_message_json "$uri" "$method" "$param" "$attack" "$evidence"`

  # Alert Content:
  alertid="40012"
  title="Prancer Bash Hello Alert"
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
  cat $out_file

}
