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

for v in $(seq 50 90); do
  test_install "@1.$v.0"
done

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
python_libs="+python+numpy"
test_install "${python_libs} ^py-numpy@1"
test_install "${python_libs} ^py-numpy@2"
test_install "+parameter_python+python"

# signals was removed in 1.68.0
test_install "@1.67.0 +signals"

# All mpi/parallel stuff
parallel="+mpi+graph_parallel+property_map_parallel"
test_install ${parallel}

# All C++14 non-parallel, non-windows, non-default libraries
cxx14_libs="+locale"
test_install "${cxx14_libs}  cxxstd=14"

# All C++17 non-parallel, non-windows, non-default libraries
cxx17_libs="+mqtt5+redis+parser+openmethod"
test_install "${cxx17_libs} cxxstd=17"

# All C++20 non-parallel, non-windows, non-default libraries
cxx20_libs="+cobalt"
test_install "${cxx20_libs} cxxstd=20"


# Big build with all non-default options
all_libs="${python_libs}+parameter_python"
all_libs+="+nowide"
all_libs+="${parallel}"
all_libs+="${cxx14_libs}"
all_libs+="${cxx17_libs}"
all_libs+="${cxx20_libs}"
test_install "${all_libs} cxxstd=20"

exit $failed
