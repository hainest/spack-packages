#!/bin/bash

declare failed=0
declare test_num=0

function should_fail () {
  declare log_file="bad_spec_test_${test_num}.log"
  echo -n "Bad spec test ${test_num}: '$1'... " | tee ${log_file}  
  ((test_num++))
  
  if ! timeout 2m spack spec --deprecated boost "$1" 2>&1 | tee -a ${log_file} | grep -iq "failed to concretize"; then
    RED='\033[0;31m'
    NC='\033[0m' # No Color
    echo -e "${RED}FAILED${NC}"
    failed=1
  else
    echo "PASSED"
    rm ${log_file}
  fi
}

exit $failed
