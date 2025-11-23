#!/bin/bash

declare build_jobs=16

declare failed=0
declare test_num=0

function test_install () {
  declare log_file="install_test_${test_num}.log"
  echo -n "Install test ${test_num}: '$1'... " | tee ${log_file}
  ((test_num++))
  
  if timeout 20m spack install --deprecated -v -j ${build_jobs} boost "$1" >>${log_file} 2>&1; then
    echo "PASSED"
    spack uninstall -y boost "$1" >/dev/null 2>&1
    rm -f ${log_file}
  else
    RED='\033[0;31m'
	NC='\033[0m' # No Color
    echo -e "${RED}FAILED${NC}"
    failed=1
  fi
}

test_install ""
test_install "%gcc"
test_install "@develop %gcc"
test_install "@develop %clang"
test_install "+clanglibcpp~stacktrace %clang"

# Layouts (can only be one type)
for l in "versionedlayout" "taggedlayout"; do
  # non-default build options
  test_install "+debug+icu+singlethreaded+$l"
done

# All python stuff
python_libs="+python"
test_install "${python_libs}"
test_install "${python_libs}"

# signals was removed in 1.68.0
test_install "@1.67.0 +signals"

# All mpi/parallel stuff
parallel="+mpi+graph_parallel"
test_install ${parallel}

# All C++14 non-parallel, non-windows, non-default libraries
cxx14_libs="+locale"
test_install "${cxx14_libs}  cxxstd=14"

exit $failed
