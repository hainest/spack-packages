import spack.package as sp


class variant_set:
    def __init__(self):
        self.libraries = dict()

    def add(
        self,
        name,
        default=None,
        buildable=None,
        is_named=False,
        conflicts=[],
        requires=[],
        **kwargs,
    ):
        """
        Create a spack.Variant with extra logic to handle the cases a library
        should be compiled (i.e., passed to b2 via --with-libraries)

        Args:
         name (str): name of the variant

         default (str,bool,None):  The default value for the variant

                                    By default, each variant is enabled. A value of
                                    'None' is converted to 'True'. This is done so
                                    that each variants.add can omit a default
                                    value. The inversion is done because
                                    spack.Variant assumes a default value of
                                    'False'.

         buildable (str): The version string indicating which versions
                          for which the library should be compiled or `None`

         conflicts (list): The variant's conflicts

                           Each conflict is a dict with keys 'when' and 'msg'
                           that are identical to the values for the spack
                           'conflicts' directive.

                           NOTE: single- and multi-valued variants should use
                                 'requires' instead of 'conflicts'.

         requires (list): The variant's requires

                           Each requirement is a dict with keys 'spec', 'when', and
                           'msg' that are identical to the values for the spack
                           'requires' directive.

         kwargs (dict): The rest of the arguments forwarded on to the
                        spack.Variant constructor

                        This should include 'when' which indicates the version
                        range for which the variant is valid. This is distinct
                        from 'buildable' as the latter only indicates when the
                        library should be compiled.

                        For example, signal2 library was introduced in 1.39.0, but
                        wasn't buildable until 1.88.0. In this case, when="@1.39.0:" and
                        buildable="@1.88.0:".
        """

        if default is None:
            default = True

        if "sticky" not in kwargs:
            kwargs["sticky"] = True

        sp.variant(name, default=default, **kwargs)

        for c in conflicts:
            when = f"+{name}" if not is_named else ""
            if "when" in c:
                when = f"{c['when']} {when}"

            sp.conflicts(c["spec"], when=f"{when}", msg=c["msg"])

        for r in requires:
            when = f"+{name}" if not is_named else ""
            if "when" in r:
                when = f"{r['when']} {when}"

            sp.requires(r["spec"], when=f"{when}", msg=r["msg"])

        if buildable is not None:
            self.libraries[name] = buildable

    def libraries_to_build(self, spec):
        """
        The set of libraries that need to be passed to b2 via --with-libraries to be compiled
        """
        libs = list()

        for name, version in self.libraries.items():
            if spec.satisfies("+{0:s} {1:s}".format(name, version)):
                libs.append(name)

        return sorted(libs)


# fmt: off

def load():

    variants = variant_set()

    # ----------------------------------------------------------------------
    #  Boost-level configurations
    #
    #    These variants affect every library.
    # ----------------------------------------------------------------------
    variants.add(
        "clanglibcpp",
        default=False,
        when="@1.73.0:",
        conflicts=[
            # Boost 1.85.0 stacktrace added a hard compilation error that has to
            # explicitly be suppressed on some platforms:
            # https://github.com/boostorg/stacktrace/issues/163
            {"spec": "@1.85: +stacktrace", "msg": "Stacktrace cannot be used with libc++"},
            # gcc doesn't support libc++
            {"spec": "%gcc", "msg": "gcc doesn't support libc++"},
        ],
        description="Compile with clang's libc++ instead of libstdc++",
    )
    variants.add(
        "cxxstd",
        default="14",
        values=(
            # Boost supports pre-releases like 2a, but spack.CompilerAdaptor doesn't
            "98",
            "03",
            "11",
            "14",
            sp.conditional("17", when="@1.63.0:"),
            sp.conditional("20", when="@1.77.0:"),
            sp.conditional("23", when="@1.79.0:"),
            sp.conditional("26", when="@1.79.0:"),
        ),
        multi=False,
        is_named=True,
        conflicts=[
            # Boost.core requires cxxstd >= 03 since 1.76.0
            {"spec": "cxxstd=98", "when":"@1.76.0:1.83.0", "msg": "This version of Boost requires cxxstd >= 03"},
            # C++98/03 support was removed in 1.84.0
            {"spec": "cxxstd=98", "when":"@1.84.0:", "msg": "This version of Boost requires cxxstd >= 11"},
            {"spec": "cxxstd=03", "when":"@1.84.0:", "msg": "This version of Boost requires cxxstd >= 11"},
        ],
        description="C++ standard",
    )
    variants.add(
        "debug",
        default=False,
        description="Build in debug mode",
    )
    variants.add(
        "icu",
        conflicts=[
            {"spec": "cxxstd=98", "msg": "ICU requires cxxstd >= 11"},
            {"spec": "cxxstd=03", "msg": "ICU requires cxxstd >= 11"},
        ],
        description="Enable Unicode support via ICU",
    )
    variants.add(
        "multithreaded",
        description="Enable use of multiple threads",
    )
    variants.add(
        "pic",
        description="Generate binaries with position-independent code",
    )
    variants.add(
        "shared",
        conflicts=[
            {"spec": "~pic", "msg": "Cannot build non-PIC shared libraries"},
        ],
        description="Generate shared libraries (DSO, DLL, etc.)",
    )
    variants.add(
        "singlethreaded",
        default=False,
        description="Disable use of multiple threads",
    )
    variants.add(
        "taggedlayout",
        default=False,
        when="@1.40.0:",
        conflicts=[
            {"spec": "+versionedlayout", "msg": "Layouts cannot be both tagged and versioned"}
        ],
        description="Augment library names with build options",
    )
    variants.add(
        "versionedlayout",
        default=False,
        conflicts=[
            {"spec": "+taggedlayout", "msg": "Layouts cannot be both tagged and versioned"}
        ],
        description="Augment library layout with versioned subdirs",
    )
    # https://boostorg.github.io/build/manual/develop/index.html#bbv2.builtin.features.visibility
    variants.add(
        "visibility",
        values=("global", "protected", "hidden"),
        default="hidden",
        multi=False,
        when="@1.69.0:",
        description="Default symbol visibility in compiled libraries",
    )

    # ----------------------------------------------------------------------
    #  Library-level configurations
    #
    #  These variants are specific to a particular library.
    #
    #  mpi and python are not enabled by default because they pull in many
    #  dependencies and/or because there is a great deal of customization
    #  possible (and it would be difficult to choose sensible defaults).
    # ----------------------------------------------------------------------
    variants.add(
        "timer",
        when="@1.16.1:",
        buildable="@1.48.0:",
        description="Timers for measuring wallclock and CPU times",
    )
    variants.add(
        "random",
        when="@1.15.0:",
        buildable="@1.43.0:",
        requires=[
            {"spec": "+system", "msg": "Boost.random requires Boost.system"},
        ],
        description="A complete system for random number generation",
    )
    variants.add(
        "graph",
        when="@1.18.0:",
        buildable="@1.18.0:",
        requires=[
            {"spec": "+lexical_cast", "msg": "Boost.graph requires Boost.lexical_cast"},
            {"spec": "+math", "msg": "Boost.graph requires Boost.math"},
            {"spec": "+random", "msg": "Boost.graph requires Boost.random"},
            {"spec": "+serialization", "msg": "Boost.graph requires Boost.serialization"},
        ],
        description=(
            "Generic components for mathematical graphs (collections of nodes and edges)."
        ),
    )
    variants.add(
        "regex",
        when="@1.18.0:",
        buildable="@1.18.0:",
        conflicts=[
            # This was found from experimentation
            {"spec": "cxxstd=98", "when": "@1.43.0:", "msg": "Boost.regex requires cxxstd >= 11"},
            {"spec": "cxxstd=03", "when": "@1.43.0:", "msg": "Boost.regex requires cxxstd >= 11"},
        ],
        requires=[
            # This was found from experimentation
            {"spec": "+icu", "when": "@1.43.0:", "msg": "Boost.regex requires ICU support"},
        ],
        description="Perl and POSIX regular expressions",
    )
    variants.add(
        "python",
        default=False,
        sticky=False,
        when="@1.19.0:",
        buildable="@1.19.0:",
        conflicts=[
            # https://github.com/boostorg/python/issues/400
            {"spec": "@:1.80.0 ^python@3.11:", "msg": "Boost.python.enum has a known bug for boost@:1.80.0 and python@3.11:"},
        ],
        requires=[
            {"spec": "+graph", "msg": "Boost.python requires Boost.graph"},
        ],
        description="C++ wrapper for interacting with Python",
    )
    variants.add(
        "lexical_cast",
        when="@1.20.0:",
        requires=[
            {"spec": "+container", "when": "@1.48.0:", "msg": "Boost.lexical_cast requires Boost.container"},
        ],
        description="General literal text conversions, such as an int represented a string, or vice-versa"
    )
    variants.add(
        "test",
        when="@1.21.0:",
        buildable="@1.21.0:",
        requires=[
            {"spec": "+exception", "msg": "Boost.test requires Boost.exception"},
        ],
        description=(
            "Simple program testing, full unit testing, and program execution monitoring"
        ),
    )
    variants.add(
        "math",
        when="@1.23.0:",
        buildable="@1.23.0:",
        requires=[
            {"spec": "+lexical_cast", "msg": "Boost.math requires Boost.lexical_cast"},
            {"spec": "+random", "msg": "Boost.math requires Boost.random"},
        ],
        description=(
            "Extensive collection of integer, real, and complex mathematical operations"
        ),
    )
    variants.add(
        "thread",
        when="@1.25.0:",
        buildable="@1.25.0:",
        requires=[
            {"spec": "+atomic", "when": "@1.53.0:", "msg": "Boost.thread requires Boost.atomic"},
            {"spec": "+chrono", "when": "@1.47.0:", "msg": "Boost.thread requires Boost.chrono"},
            {"spec": "+container", "when": "@1.48.0:", "msg": "Boost.thread requires Boost.container"},
            {"spec": "+date_time", "msg": "Boost.thread requires Boost.date_time"},
            {"spec": "+exception", "msg": "Boost.thread requires Boost.exception"},
            {"spec": "+system", "msg": "Boost.thread requires Boost.system"},
        ],
        description="Portable C++ multi-threading",
    )
    variants.add(
        "date_time",
        when="@1.29.0:",
        buildable="@1.29.0:",
        requires=[
            {"spec": "+lexical_cast", "msg": "Boost.date_time requires Boost.lexical_cast"}
        ],
        description="Calculate, format, and convert dates and times",
    )
    variants.add(
        "filesystem",
        when="@1.30.0:",
        buildable="@1.30.0:",
        requires=[
            {"spec": "+atomic", "when": "@1.53.0:", "msg": "Boost.filesystem requires Boost.atomic"},
            {"spec": "+system", "msg": "Boost.filesystem requires Boost.system"},
        ],
        description=(
            "Portable facilities to query and manipulate paths, files, and directories"
        ),
    )
    variants.add(
        "program_options",
        when="@1.32.0:",
        buildable="@1.32.0:",
        requires=[
            {"spec": "+lexical_cast", "msg": "Boost.program_options requires Boost.lexical_cast"},
        ],
        description=(
            "Parse command-line options similar to POSIX getops or from config files"
        ),
    )
    variants.add(
        "serialization",
        when="@1.32.0:",
        buildable="@1.32.0:",
        requires=[
            {"spec": "+variant2", "when": "@1.71.0:", "msg": "Boost.serialization requires Boost.variant2"},
        ],
        description="Serialization for persistence and marshalling",
    )
    variants.add(
        "iostreams",
        when="@1.33.0:",
        buildable="@1.33.0:",
        requires=[
            {"spec": "+random", "msg": "Boost.iostreams requires Boost.random"},
            {"spec": "+regex", "msg": "Boost.iostreams requires Boost.regex"},
        ],
        description="Streams, stream buffers, and i/o filters",
    )
    variants.add(
        "wave",
        when="@1.33.0:",
        buildable="@1.33.0:",
        requires=[
            {"spec": "+filesystem", "msg": "Boost.wave requires Boost.filesystem"},
            {"spec": "+lexical_cast", "msg": "Boost.wave requires Boost.lexical_cast"},
            {"spec": "+serialization", "msg": "Boost.wave requires Boost.serialization"},
        ],
        description="Highly configurable implementation of the mandatory C99/C++ preprocessor",
    )
    variants.add(
        "asio",
        when="@1.35.0:",
        requires=[
            {"spec": "+context", "when":"@1.51.0:", "msg": "Boost.asio requires Boost.context"},
            {"spec": "+date_time", "msg": "Boost.asio requires Boost.date_time"},
            {"spec": "+system", "msg": "Boost.asio requires Boost.system"},
        ],
        description="Portable networking and other low-level I/O",
    )
    variants.add(
        "mpi",
        default=False,
        sticky=False,
        when="@1.35.0:",
        buildable="@1.35.0:",
        conflicts=[
            # 1.64 uses out-dated APIs (https://github.com/spack/spack/issues/3963)
            {"spec": "@1.64.0 +python", "msg": "Boost.MPI@1.64.0 does not support python"},
            # Boost.python in 1.72.0 broken with cxxstd=98
            {"spec": "@1.72.0 +python cxxstd=98", "msg": "Boost.MPI@1.72.0 + Boost.Python is broken in C++98 mode"},
        ],
        requires=[
            {"spec": "+graph", "msg": "Boost.mpi requires Boost.graph"},
            {"spec": "+lexical_cast", "msg": "Boost.mpi requires Boost.lexical_cast"},
            {"spec": "+python", "when": "@1.87.0:", "msg": "Boost.mpi requires Boost.python"},
            {"spec": "+serialization", "msg": "Boost.mpi requires Boost.serialization"},
        ],
        description=(
            "C++ wrapper to the Message Passing Interface for distributed-memory parallelism"
        ),
    )
    variants.add(
        "system",
        when="@1.35.0:",
        buildable="@1.35.0:",
        conflicts=[
            # gcc on Darwin incorrectly detects 'mutex'
            # https://github.com/STEllAR-GROUP/hpx/issues/5442#issuecomment-878889166
            {"spec": "platform=darwin %gcc @:1.76", "msg": "Boost.System bug"}
        ],
        requires=[
            {"spec": "+variant2", "when": "@1.71.0:", "msg": "Boost.system requires Boost.variant2"},
        ],
        description="Extensible error reporting",
    )
    variants.add(
        "exception",
        when="@1.36.0:",
        buildable="@1.47.0:",
        description=(
            "Transport arbitrary data in exceptions, and exceptions between threads"
        ),
    )
    variants.add(
        "signals",
        default=False,
        when="@1.29.0:1.68.0",
        buildable="@1.29.0:1.68.0",
        conflicts=[
            {"spec": "@1.69.0:", "msg": "Boost.signals was removed in 1.68.0"}
        ],
        requires=[
            {
                "spec": "+signals",
                "when": "platform=windows @1.29.0:1.68.0",
                "msg": "Boost.Signals is requires on Windows"
            }
        ],
        description="Managed signals & slots callback implementation",
    )
    variants.add(
        "signals2",
        when="@1.39.0:",
        buildable="@1.87.0:",
        conflicts=[
            {"spec": "cxxstd=98", "msg": "Boost.Signals2 requires cxxstd >= 03"}
        ],
        requires=[
            {
                "spec": "+signals2",
                "when": "platform=windows @1.68.0:",
                "msg": "Boost.Signals2 is required on Windows"
            }
        ],
        description="Thread-safe managed signals & slots callback implementation",
    )
    variants.add(
        "graph_parallel",
        default=False,
        when="@1.40.0:",
        buildable="@1.40.0:",
        requires=[
            {"spec": "+filesystem", "msg": "Boost.graph_parallel requires Boost.filesystem"},
            {"spec": "+graph", "msg": "Boost.graph_parallel requires Boost.graph"},
            {"spec": "+lexical_cast", "msg": "Boost.graph_parallel requires Boost.lexical_cast"},
            {"spec": "+mpi", "msg": "Boost.graph_parallel requires Boost.mpi"},
            {"spec": "+random", "msg": "Boost.graph_parallel requires Boost.random"},
            {"spec": "+serialization", "msg": "Boost.graph_parallel requires Boost.serialization"},
        ],
        description="Scalable parallel version of Boost.Graph using MPI multiprocessing",
    )
    variants.add(
        "chrono",
        when="@1.47.0:",
        buildable="@1.47.0:",
        requires=[
            {"spec": "+system", "msg": "Boost.chrono requires Boost.system"},
        ],
        description="Extended version of C++11 time utilities",
    )
    variants.add(
        "geometry",
        when="@1.47.0:",
        requires=[
            {"spec": "+container", "when": "@1.48.0:", "msg": "Boost.geometry requires Boost.container"},
            {"spec": "+graph", "msg": "Boost.geometry requires Boost.graph"},
            {"spec": "+lexical_cast", "msg": "Boost.geometry requires Boost.lexical_cast"},
            {"spec": "+math", "msg": "Boost.geometry requires Boost.math"},
            {"spec": "+serialization", "msg": "Boost.geometry requires Boost.serialization"},
            {"spec": "+thread", "msg": "Boost.geometry requires Boost.thread"},
            {"spec": "+variant2", "when": "@1.71.0:", "msg": "Boost.geometry requires Boost.variant2"},
        ],
        description="The Boost.Geometry library provides geometric algorithms, primitives and spatial index"
    )
    variants.add(
        "container",
        when="@1.48.0:",
        buildable="@1.56.0:",  # Extended Allocators need to be compiled
        description="Standard library containers and extensions",
    )
    variants.add(
        "locale",
        default=False,
        when="@1.48.0:",
        buildable="@1.48.0:",
        requires=[
            {"spec": "+icu", "msg": "Boost.Locale requires Unicode support"},
            {"spec": "+thread", "msg": "Boost.locale requires Boost.thread"},
        ],
        description="Localization and Unicode facilities",
    )
    variants.add(
        "context",
        when="@1.51.0:",
        buildable="@1.51.0:",
        conflicts=[
            {"spec": "cxxstd=98", "when": "@1.61.0:", "msg": "Boost.context requires cxxstd >= 11"},
            {"spec": "cxxstd=03", "when": "@1.61.0:", "msg": "Boost.context requires cxxstd >= 11"},
        ],
        description="Cooperative multitasking on a single thread",
    )
    variants.add(
        "atomic",
        when="@1.53.0:",
        buildable="@1.53.0:",
        description="C++11-style atomic types",
    )
    variants.add(
        "coroutine",
        when="@1.53.0:",
        buildable="@1.54.0:",
        requires=[
            {"spec": "+context", "msg": "Boost.coroutine requires Boost.context"},
            {"spec": "+exception", "msg": "Boost.coroutine requires Boost.exception"},
            {"spec": "+system", "msg": "Boost.coroutine requires Boost.system"},
        ],
        description="DEPRECATED use coroutine2",
    )
    variants.add(
        "log",
        when="@1.54.0:",
        buildable="@1.54.0:",
        requires=[
            {"spec": "+asio", "msg": "Boost.log requires Boost.asio"},
            {"spec": "+atomic", "msg": "Boost.log requires Boost.atomic"},
            {"spec": "+date_time", "msg": "Boost.log requires Boost.date_time"},
            {"spec": "+exception", "msg": "Boost.log requires Boost.exception"},
            {"spec": "+filesystem", "msg": "Boost.log requires Boost.filesystem"},
            {"spec": "+regex", "msg": "Boost.log requires Boost.regex"},
            {"spec": "+system", "msg": "Boost.log requires Boost.system"},
            {"spec": "+thread", "msg": "Boost.log requires Boost.thread"},
        ],
        description="Simple, extensible, and fast logging",
    )
    variants.add(
        "type_erasure",
        when="@1.54.0:",
        buildable="@1.60.0:",
        requires=[
            {"spec": "+thread", "msg": "Boost.type_erasure requires Boost.thread"},
        ],
        description="Runtime polymorphism based on concepts",
    )
    variants.add(
        "hana",
        when="@1.61.0:",
        description="Modern metaprogramming suited for computations on both types and values",
    )
    variants.add(
        "fiber",
        when="@1.62.0:",
        buildable="@1.62.0:",
        conflicts=[
            {"spec": "cxxstd=98", "msg": "Boost.fiber requires cxxstd >= 11"},
            {"spec": "cxxstd=03", "msg": "Boost.fiber requires cxxstd >= 11"},
        ],
        requires=[
            {"spec": "+context", "msg": "Boost.fiber requires Boost.context"},
            {"spec": "+filesystem", "msg": "Boost.fiber requires Boost.filesystem"},
        ],
        description="Lightweight userland threads",
    )
    variants.add(
        "numpy",
        when="@1.63.0:",
        default=False,
        requires=[
            {"spec": "+python", "msg": "Numpy support requires Boost.python"}
        ],
        description="Enable numpy support in Boost.Python",
    )
    variants.add(
        "process",
        when="@1.64.0:",
        buildable="@1.86.0:",
        requires=[
            {"spec": "+asio", "msg": "Boost.process requires Boost.asio"},
            {"spec": "+filesystem", "msg": "Boost.process requires Boost.filesystem"},
            {"spec": "+system", "msg": "Boost.process requires Boost.system"},
        ],
        description="Portable process creation and management",
    )
    variants.add(
        "context-impl",
        when="@1.65.0:",
        is_named=True,
        requires=[
            {"spec": "+context", "when":"context-impl=fcontext", "msg": "context-impl requires Boost.Context"},
            {"spec": "+context", "when":"context-impl=ucontext", "msg": "context-impl requires Boost.Context"},
            {"spec": "+context", "when":"context-impl=winfib", "msg": "context-impl requires Boost.Context"},
        ],
        default="fcontext",
        values=("fcontext", "ucontext", "winfib"),
        multi=False,
        description="The backend for Boost.Context",
    )
    variants.add(
        "stacktrace",
        when="@1.65.0:",
        buildable="@1.65.0:",
        description="Gather, store, copy, and print backtraces",
    )
    variants.add(
        "beast",
        when="@1.66.0:",
        buildable="@1.87.0:",
        requires=[
            {"spec": "+asio", "msg": "Boost.beast requires Boost.asio"},
            {"spec": "+container", "msg": "Boost.beast requires Boost.container"},
            {"spec": "+static_string", "when": "@1.73.0:", "msg": "Boost.beast requires Boost.static_string"},
            {"spec": "+system", "msg": "Boost.beast requires Boost.system"},
        ],
        description="Portable HTTP, WebSocket, and network operations using Boost.Asio",
    )
    variants.add(
        "contract",
        when="@1.67.0:",
        buildable="@1.67.0:",
        requires=[
            {"spec": "+exception", "msg": "Boost.contract requires Boost.exception"},
            {"spec": "+thread", "msg": "Boost.contract requires Boost.thread"},
        ],
        description=(
            "Contract programming with subcontracting, class invariants, and pre/postconditions."
        ),
    )
    variants.add(
        "parameter_python",
        default=False,
        when="@1.69.0:",
        conflicts=[
            {"spec": "cxxstd=98", "msg": "Boost.parameter_python requires cxxstd >= 03"},
        ],
        requires=[
            {"spec": "+python", "msg": "Boost.parameter_python requires Boost.python"},
        ],
        description="python bindings for Boost.Parameter"
    )
    variants.add(
        "outcome",
        when="@1.70.0:",
        requires=[
            {"spec": "+exception", "msg": "Boost.outcome requires Boost.exception"},
            {"spec": "+system", "msg": "Boost.outcome requires Boost.system"},
        ],
        description=(
            "Deterministic failure handling, partially simulating lightweight exceptions"
        ),
    )
    variants.add(
        "variant2",
        when="@1.71.0:",
        description="A never-valueless, strong-guarantee tagged union",
    )
    variants.add(
        "nowide",
        default=False,
        when="@1.73.0:",
        buildable="@1.73.0:",
        requires=[
            {"spec": "+filesystem", "msg": "Boost.nowide requires Boost.filesystem"},
        ],
        description="Standard library functions with UTF-8 API on Windows",
    )
    variants.add(
        "static_string",
        when="@1.73.0:",
        description="A fixed capacity dynamically sized string"
    )
    variants.add(
        "json",
        when="@1.75.0:",
        buildable="@1.75.0:",
        conflicts=[
            {"spec": "cxxstd=98", "msg": "Boost.JSON requires cxxstd >= 11"},
            {"spec": "cxxstd=03", "msg": "Boost.JSON requires cxxstd >= 11"},
        ],
        requires=[
            {"spec": "+container", "msg": "Boost.json requires Boost.container"},
            {"spec": "+system", "msg": "Boost.json requires Boost.system"},
        ],
        description="JSON parsing, serialization, and DOM in C++11",
    )
    variants.add(
        "leaf",
        when="@1.75.0:",
        description="Lightweight error-handling",
    )
    variants.add(
        "property_map_parallel",
        default=False,
        when="@1.77.0:",
        requires=[
            {"spec": "+mpi", "msg": "Boost.property_map_parallel requires Boost.mpi"},
            {"spec": "+serialization", "msg": "Boost.property_map_parallel requires Boost.serialization"},
        ],
        description="Parallel extensions to Property Map for use with Parallel Graph"
    )

    return variants
