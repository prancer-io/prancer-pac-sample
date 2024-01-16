#!/bin/bash

# Source the prancer-lib shell script to call all pr-* library functions.
source shlib/prancer-lib.sh

# generate a hello alert, pass the target like: "https://brokencrystals.com/"
output=`pr_hello_world_alert "$1"`

# Check the output
if [ $? -ne 0 ];  then
  echo "Failed to generate alert!...."
else
  echo "$output"
fi

exit 0

