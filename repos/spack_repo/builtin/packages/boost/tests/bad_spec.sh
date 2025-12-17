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
should_fail "+cobalt cxxstd=17"                                       # cobalt requires cxxstd >= 20
should_fail "+cobalt ~asio"                                           # cobalt requires asio
should_fail "+cobalt ~container"                                      # cobalt requires container
should_fail "+cobalt ~context"                                        # cobalt requires context
should_fail "+cobalt ~static_string"                                  # cobalt requires static_string
should_fail "+cobalt ~system"                                         # cobalt requires system
should_fail "+cobalt ~variant2"                                       # cobalt requires variant2
should_fail "~context context-impl=fcontext"                          # context-impl requires context
should_fail "+contract ~exception"                                    # contract requires exception
should_fail "+contract ~thread"                                       # contract requires thread
should_fail "+coroutine~context"                                      # coroutine requires context
should_fail "+coroutine ~exception"                                   # coroutine requires exception
should_fail "+coroutine ~system"                                      # coroutine requires system
should_fail "+date_time ~lexical_cast"                                # date_time requires lexical_cast
should_fail "+filesystem ~system"                                     # filesystem requires system
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
should_fail "+histogram cxxstd=11"                                    # histogram requires cxxstd >= 14
should_fail "+histogram ~math"                                        # histogram requires math
should_fail "+histogram ~serialization"                               # histogram requires serialization
should_fail "+histogram ~variant2"                                    # histogram requires variant2
should_fail "+iostreams ~random"                                      # iostreams requires random
should_fail "+iostreams ~regex"                                       # iostreams requires regex
should_fail "+json ~container"                                        # json requires container
should_fail "+json ~system"                                           # json requires system
should_fail "+lambda2 cxxstd=11"                                      # lambda2 requires cxxstd >= 14
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
should_fail "+mqtt5 cxxstd=11"                                        # mqtt5 requires cxxstd >= 17
should_fail "+mqtt5 cxxstd=14"                                        # mqtt5 requires cxxstd >= 17
should_fail "+mqtt5 ~asio"                                            # mqtt5 requires asio
should_fail "+mqtt5 ~beast"                                           # mqtt5 requires beast
should_fail "+mqtt5 ~container"                                       # mqtt5 requires container
should_fail "+mqtt5 ~random"                                          # mqtt5 requires random
should_fail "+mqtt5 ~system"                                          # mqtt5 requires system
should_fail "+multiprecision ~lexical_cast"                           # multiprecision requires lexical_cast
should_fail "+multiprecision ~math"                                   # multiprecision requires math
should_fail "+multiprecision ~random"                                 # multiprecision requires random
should_fail "+mysql ~asio"                                            # mysql requires asio
should_fail "+mysql ~charconv"                                        # mysql requires charconv
should_fail "+mysql ~container"                                       # mysql requires container
should_fail "+mysql ~pfr"                                             # mysql requires pfr
should_fail "+mysql ~system"                                          # mysql requires system
should_fail "+mysql ~variant2"                                        # mysql requires variant2
should_fail "+nowide ~filesystem"                                     # nowide requires filesystem
should_fail "+program_options ~lexical_cast"                          # program_options requires lexical_cast
should_fail "+numpy ~python"                                          # numpy requires python
should_fail "+parameter_python ~python"                               # parameter_python requires python
should_fail "+parser ~charconv"                                       # parser requires charconv
should_fail "+parser ~hana"                                           # parser requires hana
should_fail "+pfr cxxstd=11"                                          # pfr requires cxxstd >= 14
should_fail "+process ~asio"                                          # process requires asio
should_fail "+process ~filesystem"                                    # process requires filesystem
should_fail "+process ~system"                                        # process requires system
should_fail "+outcome ~exception"                                     # outcome requires exception
should_fail "+outcome ~system"                                        # outcome requires system
should_fail "+property_map_parallel ~mpi"                             # property_map_parallel requires mpi
should_fail "+property_map_parallel ~serialization"                   # property_map_parallel requires serialization
should_fail "+random ~system"                                         # random requires system
should_fail "+redis cxxstd=11"                                        # redis requires cxxstd >= 17
should_fail "+redis cxxstd=14"                                        # redis requires cxxstd >= 17
should_fail "+redis ~asio"                                            # redis requires asio
should_fail "+redis ~system"                                          # redis requires system
should_fail "+safe_numerics cxxstd=11"                                # safe_numerics requires cxxstd >= 14
should_fail "+stl_interfaces cxxstd=11"                               # stl_interfaces requires cxxstd >= 14
should_fail "+system ~variant2"                                       # system requires variant2
should_fail "+test ~exception"                                        # test requires exception
should_fail "+thread ~atomic"                                         # thread requires atomic
should_fail "+thread ~chrono"                                         # thread requires chrono
should_fail "+thread ~container"                                      # thread requires container
should_fail "+thread ~date_time"                                      # thread requires date_time
should_fail "+thread ~exception"                                      # thread requires exception
should_fail "+thread ~system"                                         # thread requires system
should_fail "+type_erasure ~thread"                                   # type_erasure requires thread
should_fail "+url ~system"                                            # url requires system
should_fail "+url ~variant2"                                          # url requires variant2
should_fail "+wave ~filesystem"                                       # wave requires filesystem
should_fail "+wave ~lexical_cast"                                     # wave requires lexical_cast
should_fail "+wave ~serialization"                                    # wave requires serialization
should_fail "+yap cxxstd=11"                                          # yap requires cxxstd >= 14
should_fail "+yap ~hana"                                              # yap requires hana
should_fail "@1.20.0 +python ~lexical_cast"                           # python requires lexical_cast since 1.20.0
should_fail "@1.47.0 +thread ~chrono"                                 # thread requires chrono since 1.47.0
should_fail "@1.48.0 +geometry ~container"                            # geometry requires container since 1.48.0
should_fail "@1.48.0 +lexical_cast ~container"                        # lexical_cast requires container since 1.48.0
should_fail "@1.48.0 +thread ~container"                              # thread requires container  since 1.48.0
should_fail "@1.51.0 +asio ~context"                                  # asio requires context since 1.51.0
should_fail "@1.53.0 +filesystem ~atomic"                             # filesystem requires atomic 1.53.0
should_fail "@1.53.0 +thread ~atomic"                                 # thread requires atomic since 1.53.0
should_fail "@1.60.0 +hana"                                           # hana was added in 1.61.0
should_fail "@1.62.0 cxxstd=17"                                       # 1.63.0 added C++17 support
should_fail "@1.64.0 +python +mpi"                                    # 1.64 uses out-dated APIs
should_fail "@1.68.0 +safe_numerics"                                  # safe_numerics was added in 1.69.0
should_fail "@1.69.0 +signals"                                        # signals was removed in 1.68.0
should_fail "@1.71.0 +geometry ~variant2"                             # geometry requires variant2 since 1.71.0
should_fail "@1.71.0 +serialization ~variant2"                        # serialization requires variant2 since 1.71.0
should_fail "@1.71.0 +system ~variant2"                               # system requires variant2 since 1.71.0
should_fail "@1.72.0 +clanglibcpp"                                    # clanglibcpp was introduced in 1.73.0
should_fail "@1.73.0 +beast ~static_string"                           # beast requires static_string since 1.73.0
should_fail "@1.75.0 +geometry cxxstd=11"                             # geometry requires cxxstd >= 14 after 1.75.0
should_fail "@1.76.0 cxxstd=20"                                       # 1.77.0 added C++20 support
should_fail "@1.78.0 cxxstd=23"                                       # 1.79.0 added C++23 support
should_fail "@1.78.0 cxxstd=26"                                       # 1.79.0 added C++26 support
should_fail "@1.80.0 +gil cxxstd=11"                                  # gil requires cxxstd >= 14 as of 1.80.0
should_fail "@1.82.0 +math cxxstd=11"                                 # math requires cxxstd >= 14 after 1.82.0
should_fail "@1.82.0: +multiprecision cxxstd=11"                      # multiprecision requires cxxstd >= 14
should_fail "@1.85.0 +clanglibcpp+stacktrace"                         # 1.85.0 stacktrace added a hard compilation error
should_fail "@1.85.0 +locale ~charconv"                               # locale requires charconv since 1.85.0
should_fail "@1.86.0 +graph ~regex"                                   # graph requires regex until 1.86.0
should_fail "@1.86.0 +graph cxxstd=11"                                # graph requires cxxstd >= 14 since 1.86.0
should_fail "@1.87.0 +mpi ~python"                                    # Boost.MPI requires Boost.Python
should_fail "@1.88.0 +heap cxxstd=11"                                 # heap requires cxxstd >= 14 after 1.88.0
should_fail "@1.88.0 +lockfree cxxstd=11"                             # lockfree requires cxxstd >= 14 after 1.87.0
should_fail "@1.89.0 +parser cxxstd=14"                               # parser requires cxxstd >= 17 since 1.89.0
should_fail "@1.90.0 +openmethod cxxstd=14"                           # openmethod requires cxxstd >= 17

exit $failed
