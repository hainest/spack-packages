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
should_fail "+beast ~asio"                                            # beast requires asio
should_fail "+beast ~container"                                       # beast requires container
should_fail "+beast ~system"                                          # beast requires system
should_fail "+chrono ~system"                                         # chrono requires system
should_fail "+clanglibcpp %gcc"                                       # gcc doesn't support libc++
should_fail "+icu cxxstd=03"                                          # icu requires cxxstd >= 11
should_fail "~context context-impl=fcontext"                          # context-impl requires context
should_fail "+contract ~exception"                                    # contract requires exception
should_fail "+contract ~thread"                                       # contract requires thread
should_fail "+coroutine~context"                                      # coroutine requires context
should_fail "+coroutine ~exception"                                   # coroutine requires exception
should_fail "+coroutine ~system"                                      # coroutine requires system
should_fail "+date_time ~lexical_cast"                                # date_time requires lexical_cast
should_fail "+filesystem ~system"                                     # filesystem requires system
should_fail "+fiber cxxstd=98"                                        # fiber requires cxxstd >= 11
should_fail "+fiber cxxstd=03"                                        # fiber requires cxxstd >= 11
should_fail "+fiber ~context"                                         # fiber requires context
should_fail "+fiber ~filesystem"                                      # fiber requires filesystem
should_fail "+geometry ~graph"                                        # geometry requires graph
should_fail "+geometry ~lexical_cast"                                 # geometry requires lexical_cast
should_fail "+geometry ~math"                                         # geometry requires math
should_fail "+geometry ~serialization"                                # geometry requires serialization
should_fail "+geometry ~thread"                                       # geometry requires thread
should_fail "+graph ~random"                                          # graph requires random
should_fail "+graph ~lexical_cast"                                    # graph requires lexical_cast
should_fail "+graph ~serialization"                                   # graph requires serialization
should_fail "+graph_parallel ~filesystem"                             # graph_parallel requires filesystem
should_fail "+graph_parallel ~graph"                                  # graph_parallel requires graph
should_fail "+graph_parallel ~lexical_cast"                           # graph_parallel requires lexical_cast
should_fail "+graph_parallel ~mpi"                                    # graph_parallel requires mpi
should_fail "+graph_parallel ~random"                                 # graph_parallel requires random
should_fail "+graph_parallel ~serialization"                          # graph_parallel requires serialization
should_fail "+iostreams ~random"                                      # iostreams requires random
should_fail "+iostreams ~regex"                                       # iostreams requires regex
should_fail "+python ~graph"                                          # python requires graph
should_fail "+test ~exception"                                        # test requires exception
should_fail "+locale ~icu"                                            # locale requires icu
should_fail "+locale ~thread"                                         # locale requires thread
should_fail "+log ~asio"                                              # log requires asio
should_fail "+log ~atomic"                                            # log requires atomic
should_fail "+log ~date_time"                                         # log requires date_time
should_fail "+log ~exception"                                         # log requires exception
should_fail "+log ~filesystem"                                        # log requires filesystem
should_fail "+log ~regex"                                             # log requires regex
should_fail "+log ~system"                                            # log requires system
should_fail "+log ~thread"                                            # log requires thread
should_fail "+math ~lexical_cast"                                     # math requires lexical_cast
should_fail "+math ~random"                                           # math requires random
should_fail "+mpi ~graph"                                             # mpi requires graph
should_fail "+mpi ~lexical_cast"                                      # mpi requires lexical_cast
should_fail "+mpi ~serialization"                                     # mpi requires serialization
should_fail "+program_options ~lexical_cast"                          # program_options requires lexical_cast
should_fail "+numpy ~python"                                          # numpy requires python
should_fail "+process ~asio"                                          # process requires asio
should_fail "+process ~filesystem"                                    # process requires filesystem
should_fail "+process ~system"                                        # process requires system
should_fail "+random ~system"                                         # random requires system
should_fail "+signals2 cxxstd=98"                                     # signals2 requires cxxstd >= 03
should_fail "+system ~variant2"                                       # system requires variant2
should_fail "+test ~exception"                                        # test requires exception
should_fail "+thread ~atomic"                                         # thread requires atomic
should_fail "+thread ~chrono"                                         # thread requires chrono
should_fail "+thread ~container"                                      # thread requires container
should_fail "+thread ~date_time"                                      # thread requires date_time
should_fail "+thread ~exception"                                      # thread requires exception
should_fail "+thread ~system"                                         # thread requires system
should_fail "+type_erasure ~thread"                                   # type_erasure requires thread
should_fail "+wave ~filesystem"                                       # wave requires filesystem
should_fail "+wave ~lexical_cast"                                     # wave requires lexical_cast
should_fail "+wave ~serialization"                                    # wave requires serialization
should_fail "@1.20.0 +python ~lexical_cast"                           # python requires lexical_cast since 1.20.0
should_fail "@1.47.0 +thread ~chrono"                                 # thread requires chrono since 1.47.0
should_fail "@1.48.0 +geometry ~container"                            # geometry requires container since 1.48.0
should_fail "@1.48.0 +lexical_cast ~container"                        # lexical_cast requires container since 1.48.0
should_fail "@1.48.0 +thread ~container"                              # thread requires container  since 1.48.0
should_fail "@1.51.0 +asio ~context"                                  # asio requires context since 1.51.0
should_fail "@1.61.0 +context cxxstd=98"                              # context requires cxxstd >= 11 after 1.61.0
should_fail "@1.61.0 +context cxxstd=03"                              # context requires cxxstd >= 11 after 1.61.0
should_fail "@1.53.0 +filesystem ~atomic"                             # filesystem requires atomic 1.53.0
should_fail "@1.53.0 +thread ~atomic"                                 # thread requires atomic since 1.53.0
should_fail "@1.60.0 +hana"                                           # hana was added in 1.61.0
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
should_fail "@1.85.0 +clanglibcpp+stacktrace"                         # 1.85.0 stacktrace added a hard compilation error
should_fail "@1.87.0 +mpi ~python"                                    # Boost.MPI requires Boost.Python

exit $failed
