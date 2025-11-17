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

should_fail "+asio ~date_time"                                        # asio requires date_time
should_fail "+asio ~system"                                           # asio requires system
should_fail "+clanglibcpp %gcc"                                       # gcc doesn't support libc++
should_fail "+icu cxxstd=03"                                          # icu requires cxxstd >= 11
should_fail "+date_time ~lexical_cast"                                # date_time requires lexical_cast
should_fail "+filesystem ~system"                                     # filesystem requires system
should_fail "+graph ~random"                                          # graph requires random
should_fail "+graph ~lexical_cast"                                    # graph requires lexical_cast
should_fail "+graph ~serialization"                                   # graph requires serialization
should_fail "+iostreams ~random"                                      # iostreams requires random
should_fail "+iostreams ~regex"                                       # iostreams requires regex
should_fail "+python ~graph"                                          # python requires graph
should_fail "+test ~exception"                                        # test requires exception
should_fail "+math ~lexical_cast"                                     # math requires lexical_cast
should_fail "+math ~random"                                           # math requires random
should_fail "+mpi ~graph"                                             # mpi requires graph
should_fail "+mpi ~lexical_cast"                                      # mpi requires lexical_cast
should_fail "+mpi ~serialization"                                     # mpi requires serialization
should_fail "+program_options ~lexical_cast"                          # program_options requires lexical_cast
should_fail "+random ~system"                                         # random requires system
should_fail "+system ~variant2"                                       # system requires variant2
should_fail "+test ~exception"                                        # test requires exception
should_fail "+thread ~chrono"                                         # thread requires chrono
should_fail "+thread ~container"                                      # thread requires container
should_fail "+thread ~date_time"                                      # thread requires date_time
should_fail "+thread ~exception"                                      # thread requires exception
should_fail "+thread ~system"                                         # thread requires system
should_fail "+wave ~filesystem"                                       # wave requires filesystem
should_fail "+wave ~lexical_cast"                                     # wave requires lexical_cast
should_fail "+wave ~serialization"                                    # wave requires serialization
should_fail "@1.20.0 +python ~lexical_cast"                           # python requires lexical_cast since 1.20.0
should_fail "@1.62.0 cxxstd=17"                                       # 1.63.0 added C++17 support
should_fail "@1.64.0 +python +mpi"                                    # 1.64 uses out-dated APIs
should_fail "@1.69.0 +signals"                                        # signals was removed in 1.68.0
should_fail "@1.72.0 +clanglibcpp"                                    # clanglibcpp was introduced in 1.73.0
should_fail "@1.72.0 +python +mpi cxxstd=98"                          # @1.72.0 mpi+python does not support C++98
should_fail "@1.76.0 cxxstd=98"                                       # core requires cxxstd >= 03
should_fail "@1.76.0 cxxstd=20"                                       # 1.77.0 added C++20 support
should_fail "@1.78.0 cxxstd=23"                                       # 1.79.0 added C++23 support
should_fail "@1.78.0 cxxstd=26"                                       # 1.79.0 added C++26 support
should_fail "@1.85.0 cxxstd=03"                                       # 1.84.0 removed C++98/03 support
should_fail "@1.87.0 +mpi ~python"                                    # Boost.MPI requires Boost.Python

exit $failed
