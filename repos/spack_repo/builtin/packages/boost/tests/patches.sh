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

test_patch "@1.54.0 +python ^python@3"        # python_jam_pre156, glibc_gentoo_v1.53.0.patch, call_once_variadic
test_patch "@1.55.0 %clang"                   # clang-linux_add_option2
test_patch "@1.56.0 %clang"                   # clang-linux_add_option, build_PR154
test_patch "@1.63.0 +python"                  # python_PR218
test_patch "@1.69.0 +system"                  # system-non-virtual-dtor-{include,test}, pthread-stack-min-fix
test_patch "@1.75"                            # bootstrap-toolset
test_patch "@1.76.0 +python ^python@3"        # python_jam, bootstrap-compiler
test_patch "@1.77.0 +python ^python@3"        # python_jam-1_77, b2_PR79
test_patch "@1.87.0 +context"                 # context_PR280

exit $failed
