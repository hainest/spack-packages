#!/bin/bash

declare failed=0
declare test_num=0

function test_patch () {
  declare log_file="patch_test_${test_num}.log"
  echo -n "Patch test ${test_num}: '$1'..." | tee ${log_file}
  ((test_num++))

  if timeout 2m spack patch --deprecated boost "$1" >>${log_file} 2>&1; then
    echo "PASSED"
    rm ${log_file}
  else
    RED='\033[0;31m'
    NC='\033[0m' # No Color
    echo -e "${RED}FAILED${NC}"
    failed=1
  fi
}

# Patches requiring a specific version of a compiler or OS are not included

test_patch "@1.50.0"                          # unordered_v1500
test_patch "@1.51.0 +context"                 # context_uintptr_t
test_patch "@1.54.0 +python ^python@3"        # python_jam_pre156, glibc_gentoo_v1.53.0.patch, call_once_variadic
test_patch "@1.54.0 +coroutine"               # coroutine_v1540
test_patch "@1.54.0 +date_time"               # date_time_v1540
test_patch "@1.54.0 +log"                     # log_v1540
test_patch "@1.54.0 +thread"                  # thread_v1540
test_patch "@1.55.0 +log"                     # log_v1550
test_patch "@1.55.0 %clang"                   # clang-linux_add_option2
test_patch "@1.56.0 %clang"                   # clang-linux_add_option, build_PR154
test_patch "@1.58.0 +python"                  # python_v1580, fusion_v1580
test_patch "@1.59.0 +log"                     # log_v1590
test_patch "@1.63.0 +python +numpy"           # python_PR218, python_PR432
test_patch "@1.65.0 +fiber+thread"            # fiber_v1650, thread_v1650
test_patch "@1.67.0 +python+wave+fiber"       # python_v1670, wave_v1670, fiber_v1670
test_patch "@1.68.0 +container"               # container_PR101
test_patch "@1.69.0 +system"                  # system-non-virtual-dtor-{include,test}, pthread-stack-min-fix
test_patch "@1.70.0 +beast"                   # beast_PR1599
test_patch "@1.72.0 +process+coroutine"       # process_PR116, coroutine_PR44
test_patch "@1.73.0 +beast+outcome"           # beast_PR1927, outcome_PR223
test_patch "@1.75"                            # bootstrap-toolset
test_patch "@1.76.0 +math"                    # math_v1760
test_patch "@1.76.0 +python ^python@3"        # python_jam, bootstrap-compiler
test_patch "@1.77.0 +python ^python@3"        # python_jam-1_77, b2_PR79
test_patch "@1.78.0 +atomic"                  # atomic_PR54, build_PR113
test_patch "@1.82.0"                          # phoenix_PR111
test_patch "@1.87.0 +context"                 # context_PR280

exit $failed
