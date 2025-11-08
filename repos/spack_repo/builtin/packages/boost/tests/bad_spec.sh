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

should_fail "@1.62.0 cxxstd=17"                                       # 1.63.0 added C++17 support
should_fail "@1.76.0 cxxstd=98"                                       # core requires cxxstd >= 03
should_fail "@1.76.0 cxxstd=20"                                       # 1.77.0 added C++20 support
should_fail "@1.78.0 cxxstd=23"                                       # 1.79.0 added C++23 support
should_fail "@1.78.0 cxxstd=26"                                       # 1.79.0 added C++26 support

exit $failed
